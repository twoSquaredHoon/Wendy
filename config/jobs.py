import curses
import os
import re
import subprocess
from pathlib import Path
from config.palette import make_palette
from config.settings_store import load_settings, save_settings, REPO_ROOT

os.environ.setdefault("ESCDELAY", "0")

WENDY_DIR = Path.home() / ".wendy"
JOBS_DIR = WENDY_DIR / "jobs"
LOGS_DIR = WENDY_DIR / "logs"

CRON_START = "# >>> wendy jobs >>>"
CRON_END = "# <<< wendy jobs <<<"


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "job"


def write_script(name: str, command: str) -> Path:
    # each job is a small bash script that logs when it ran and how it ended
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    script = JOBS_DIR / f"{slug(name)}.sh"
    log = LOGS_DIR / f"{slug(name)}.log"
    script.write_text(
        "#!/bin/bash -l\n"
        f'echo "=== $(date \'+%Y-%m-%d %H:%M:%S\') ==="\n'
        f'cd "{REPO_ROOT}"\n'
        f"{command}\n"
        'echo "exit $?"\n'
    )
    script.chmod(0o755)
    return script


def log_path(name: str) -> Path:
    return LOGS_DIR / f"{slug(name)}.log"


def last_status(name: str) -> str:
    log = log_path(name)
    if not log.exists():
        return "never run"
    lines = log.read_text(errors="ignore").splitlines()
    when, code = "", ""
    for line in lines:
        if line.startswith("=== "):
            when = line.strip("= ")
        elif line.startswith("exit "):
            code = line[5:]
    if not when:
        return "never run"
    if code == "0":
        return f"ok  {when}"
    if code:
        return f"FAILED ({code})  {when}"
    return f"running?  {when}"


def sync_cron(jobs: dict) -> str:
    # rewrite only Wendy's block in crontab, leave everything else alone
    for name, job in jobs.items():
        write_script(name, job["command"])

    current = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    kept = []
    inside = False
    for line in current.splitlines():
        if line == CRON_START:
            inside = True
        elif line == CRON_END:
            inside = False
        elif not inside:
            kept.append(line)

    block = [CRON_START]
    for name, job in jobs.items():
        t = job.get("time", "")
        if t:
            hh, mm = t.split(":")
            script = JOBS_DIR / f"{slug(name)}.sh"
            block.append(f'{int(mm)} {int(hh)} * * * "{script}" >> "{log_path(name)}" 2>&1')
    block.append(CRON_END)

    new_tab = "\n".join(kept + block) + "\n"
    r = subprocess.run(["crontab", "-"], input=new_tab, capture_output=True, text=True)
    if r.returncode != 0:
        return "crontab failed: " + r.stderr.strip()
    return "schedule saved."


def valid_time(t: str) -> bool:
    if t == "":
        return True
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", t)
    return bool(m) and int(m.group(1)) < 24 and int(m.group(2)) < 60


def run_now(stdscr, name: str) -> None:
    script = write_script(name, load_settings()["jobs"][name]["command"])
    curses.endwin()
    print(f"\n  ✦ Wendy → {name}\n")
    # show output on screen and also append it to the job's log
    subprocess.run(f'"{script}" 2>&1 | tee -a "{log_path(name)}"', shell=True)
    input("\n  press enter to go back to Wendy...")
    stdscr.refresh()


def view_log(stdscr, name: str) -> None:
    log = log_path(name)
    curses.endwin()
    if log.exists():
        subprocess.run(["less", "+G", str(log)])
    else:
        input("\n  no log yet. press enter...")
    stdscr.refresh()


def run_jobs(stdscr) -> str:
    curses.curs_set(0)
    p = make_palette()

    def safe(y, x, text, attr=None):
        if attr is None:
            attr = p["NORM"]
        h, w = stdscr.getmaxyx()
        text = str(text)
        if y < 0 or y >= h or x < 0 or x >= w:
            return
        try:
            stdscr.attron(attr)
            stdscr.addstr(y, x, text[:w - x - 1])
            stdscr.attroff(attr)
        except:
            pass

    settings = load_settings()
    cursor = 0
    message = ""
    # adding a job asks 3 things in a row
    asking = None          # None, "name", "command", "time"
    input_buf = ""
    new_job = {}

    while True:
        jobs = settings["jobs"]
        names = list(jobs.keys())
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        controls = "enter run   n new   t time   l log   d delete   esc back"
        safe(0, 0, " @ WENDY ", p["RED"])
        safe(0, 9, "jobs", p["DIM"])
        safe(0, w - len(controls) - 1, controls, p["PINK"])
        try:
            stdscr.attron(p["RED"])
            stdscr.hline(1, 0, curses.ACS_HLINE, w - 1)
            stdscr.attroff(p["RED"])
        except:
            pass

        if not names:
            safe(3, 4, "No jobs yet. Press n to add one.", p["DIM"])

        for i, name in enumerate(names):
            row = 3 + i * 3
            job = jobs[name]
            when = f"daily {job['time']}" if job.get("time") else "manual"
            status = last_status(name)
            if cursor == i:
                safe(row, 2, ">", p["RED"])
                safe(row, 4, name, p["RED"])
            else:
                safe(row, 4, name, p["NORM"])
            safe(row, 4 + len(name), f"  [{when}]", p["PINK"])
            status_attr = p["RED"] if status.startswith("FAILED") else p["DIM"]
            safe(row, 6 + len(name) + len(when) + 4, status, status_attr)
            safe(row + 1, 6, job["command"], p["DIM"])

        try:
            stdscr.attron(p["RED"])
            stdscr.hline(h - 2, 0, curses.ACS_HLINE, w - 1)
            stdscr.attroff(p["RED"])
        except:
            pass

        if asking:
            prompts = {
                "name": "job name: ",
                "command": "bash command: ",
                "time": "daily time HH:MM (empty = manual): ",
            }
            safe(h - 1, 0, prompts[asking] + input_buf + "█", p["PINK"])
        elif message:
            safe(h - 1, 0, f" {message} ", p["NORM"])

        stdscr.refresh()
        key = stdscr.getch()

        if asking:
            if key in (curses.KEY_ENTER, 10, 13):
                value = input_buf.strip()
                input_buf = ""
                if asking == "name":
                    if not value:
                        asking = None
                    else:
                        new_job = {"name": value}
                        asking = "command"
                elif asking == "command":
                    if not value:
                        asking = None
                    else:
                        new_job["command"] = value
                        asking = "time"
                elif asking == "time":
                    if not valid_time(value):
                        message = "time must look like 09:00"
                        asking = None
                    elif new_job.get("name") == "__edit_time__":
                        jobs[new_job["target"]]["time"] = value
                        save_settings(settings)
                        message = sync_cron(jobs)
                        asking = None
                    else:
                        jobs[new_job["name"]] = {"command": new_job["command"], "time": value}
                        save_settings(settings)
                        message = sync_cron(jobs)
                        cursor = list(jobs.keys()).index(new_job["name"])
                        asking = None
            elif key == 27:
                asking = None
                input_buf = ""
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                input_buf = input_buf[:-1]
            elif 32 <= key <= 126:
                input_buf += chr(key)
            continue

        message = ""
        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(max(0, len(names) - 1), cursor + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            if names:
                run_now(stdscr, names[cursor])
        elif key == ord("n"):
            asking = "name"
            input_buf = ""
        elif key == ord("t"):
            if names:
                new_job = {"name": "__edit_time__", "target": names[cursor]}
                input_buf = jobs[names[cursor]].get("time", "")
                asking = "time"
        elif key == ord("l"):
            if names:
                view_log(stdscr, names[cursor])
        elif key == ord("d"):
            if names:
                jobs.pop(names[cursor], None)
                save_settings(settings)
                message = sync_cron(jobs)
                cursor = min(cursor, max(0, len(jobs) - 1))
        elif key in (ord("q"), 27):
            break

    return ""

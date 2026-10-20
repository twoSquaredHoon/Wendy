import curses
import os
import subprocess
from config.palette import make_palette
from config.settings_store import load_settings, REPO_ROOT

os.environ.setdefault("ESCDELAY", "0")


def run_mode(stdscr, command: str) -> None:
    # leave the TUI, run the command in this terminal, then come back
    curses.endwin()
    print(f"\n  ✦ Wendy → {command}\n")
    # run from the Wendy folder so "scripts/..." paths work
    subprocess.run(command, shell=True, cwd=REPO_ROOT)
    input("\n  ✓ done. press enter to go back to Wendy...")
    stdscr.refresh()


def run_modes(stdscr) -> str:
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

    modes = load_settings()["modes"]
    names = list(modes.keys())
    cursor = 0
    last_run = ""

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        controls = "↑↓ navigate   enter run   esc back"
        safe(0, 0, " @ WENDY ", p["RED"])
        safe(0, 9, "modes", p["DIM"])
        safe(0, w - len(controls) - 1, controls, p["PINK"])
        try:
            stdscr.attron(p["RED"])
            stdscr.hline(1, 0, curses.ACS_HLINE, w - 1)
            stdscr.attroff(p["RED"])
        except:
            pass

        if not names:
            safe(3, 4, "No modes yet. Add some under \"modes\" in settings.json.", p["DIM"])

        for i, name in enumerate(names):
            row = 3 + i * 2
            if cursor == i:
                safe(row, 2, ">", p["RED"])
                safe(row, 4, name, p["RED"])
            else:
                safe(row, 4, name, p["NORM"])
            safe(row, 4 + len(name), f"  {modes[name]}", p["DIM"])

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(len(names) - 1, cursor + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            if names:
                name = names[cursor]
                run_mode(stdscr, modes[name])
                last_run = name
        elif key in (ord("q"), 27):
            break

    return last_run

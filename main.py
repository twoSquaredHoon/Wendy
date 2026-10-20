import curses
import random
import os
from config.palette import make_palette
from config.welcome import show_welcome

os.environ.setdefault("ESCDELAY", "0")

MENU_ITEMS = [
    "Modes",
    "Jobs",
    "Script Toggles",
    "Dashboard",
    "Projects",
    "Remote",
    "Notes",
]

# not built yet — shown with "(soon)"
SOON_ITEMS = {"Dashboard", "Projects", "Remote", "Notes"}

JOKES = [
    "I once sorted a list alphabetically. Still my greatest achievement.",
    "A terminal is just a GUI for people with taste.",
    "I'd tell you a UDP joke but you might not get it.",
    "It's not a bug, it's an undocumented feature. Donna would agree.",
    "There are 10 types of people. Those who get binary, and those who don't.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I'm not lazy, I'm in power-saving mode.",
    "sudo make me a sandwich. Please.",
    "Tabs or spaces? I don't want to talk about it.",
    "The best code is the code you didn't have to write.",
    "I've seen things you people wouldn't believe. Mostly stack traces.",
    "Life is short. Use aliases.",
]

def run(stdscr):
    show_welcome(stdscr)

    curses.curs_set(0)
    p = make_palette()

    cursor = 0
    message = random.choice(JOKES)
    is_update = False

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

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()

        # header
        controls = "↑↓ navigate   enter open   esc quit"
        safe(0, 0, " @ WENDY ", p["RED"])
        safe(0, 9, "config", p["DIM"])
        safe(0, w - len(controls) - 1, controls, p["PINK"])

        try:
            stdscr.attron(p["RED"])
            stdscr.hline(1, 0, curses.ACS_HLINE, w - 1)
            stdscr.attroff(p["RED"])
        except:
            pass

        # menu
        for i, item in enumerate(MENU_ITEMS):
            row = 3 + i * 2
            if cursor == i:
                safe(row, 2, ">", p["RED"])
                safe(row, 4, item, p["RED"])
            else:
                safe(row, 4, item, p["NORM"])
            if item in SOON_ITEMS:
                safe(row, 4 + len(item), "  (soon)", p["DIM"])

        # footer
        try:
            stdscr.attron(p["RED"])
            stdscr.hline(h - 2, 0, curses.ACS_HLINE, w - 1)
            stdscr.attroff(p["RED"])
        except:
            pass
        msg_attr = p["NORM"] if is_update else p["PINK"]
        msg_text = f" {message} " if is_update else f' "{message}" '
        safe(h - 1, 0, msg_text, msg_attr)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
            message = random.choice(JOKES)
            is_update = False
        elif key == curses.KEY_DOWN:
            cursor = min(len(MENU_ITEMS) - 1, cursor + 1)
            message = random.choice(JOKES)
            is_update = False
        elif key in (curses.KEY_ENTER, 10, 13):
            selected = MENU_ITEMS[cursor]
            if selected == "Modes":
                from config.modes import run_modes
                last_run = run_modes(stdscr)
                if last_run:
                    message = f"Back from {last_run}."
                    is_update = True
                else:
                    message = random.choice(JOKES)
                    is_update = False
            elif selected == "Jobs":
                from config.jobs import run_jobs
                run_jobs(stdscr)
                message = random.choice(JOKES)
                is_update = False
            elif selected == "Script Toggles":
                from config.config_menu import run_config
                run_config(stdscr)
                message = random.choice(JOKES)
                is_update = False
            elif selected == "Dashboard":
                from config.dashboard import run_dashboard
                run_dashboard(stdscr)
                message = random.choice(JOKES)
                is_update = False
            elif selected == "Projects":
                from config.projects import run_projects
                run_projects(stdscr)
                message = random.choice(JOKES)
                is_update = False
            elif selected == "Remote":
                from config.remote import run_remote
                run_remote(stdscr)
                message = random.choice(JOKES)
                is_update = False
            elif selected == "Notes":
                from config.notes import run_notes
                run_notes(stdscr)
                message = random.choice(JOKES)
                is_update = False
        elif key in (ord("q"), 27):
            break

if __name__ == "__main__":
    curses.wrapper(run)

import curses
import os
import random
from config.palette import make_palette

os.environ.setdefault("ESCDELAY", "0")

LOGO = [
    " _    _ _____ _   _________   __",
    "| |  | |  ___| \\ | |  _  \\ \\ / /",
    "| |  | | |__ |  \\| | | | |\\ V / ",
    "| |/\\| |  __|| . ` | | | | \\ /  ",
    "\\  /\\  / |___| |\\  | |/ /  | |  ",
    " \\/  \\/\\____/\\_| \\_/___/   \\_/  ",
]

GREETINGS = [
    "\"Welcome back. Let's get to work.\"",
    "\"Aesthetics matter. Donna taught me that.\"",
    "\"Ready when you are.\"",
]


def show_welcome(stdscr) -> None:
    # welcome screen: logo + greeting, any key continues to the menu
    curses.curs_set(0)
    p = make_palette()
    greeting = random.choice(GREETINGS)   # picked once per launch
    hint = "press any key"

    def safe(y, x, text, attr):
        h, w = stdscr.getmaxyx()
        if y < 0 or y >= h or x < 0 or x >= w:
            return
        try:
            stdscr.attron(attr)
            stdscr.addstr(y, x, str(text)[:w - x - 1])
            stdscr.attroff(attr)
        except:
            pass

    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        top = max(1, h // 2 - 5)

        for i, line in enumerate(LOGO):
            safe(top + i, max(0, (w - len(line)) // 2), line, p["RED"])

        safe(top + 7, max(0, (w - len(greeting)) // 2), greeting, p["NORM"] | curses.A_ITALIC)
        safe(top + 10, max(0, (w - len(hint)) // 2), hint, p["DIM"])

        stdscr.refresh()
        key = stdscr.getch()
        if key != curses.KEY_RESIZE:   # redraw on window resize, anything else continues
            return

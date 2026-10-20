"""Placeholder screens — features that aren't built yet, so you can feel the flow first."""

import curses
import time
from config.palette import make_palette
from config.menu_list import list_screen

SOON = "(soon)"


def _safe(stdscr, p):
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
    return safe


def header(stdscr, p, title, controls):
    safe = _safe(stdscr, p)
    h, w = stdscr.getmaxyx()
    safe(0, 0, " @ WENDY ", p["RED"])
    safe(0, 9, title, p["DIM"])
    safe(0, w - len(controls) - 1, controls, p["PINK"])
    try:
        stdscr.attron(p["RED"])
        stdscr.hline(1, 0, curses.ACS_HLINE, w - 1)
        stdscr.attroff(p["RED"])
    except:
        pass
    return safe


def show_placeholder(stdscr, title: str, would: list) -> None:
    """'Not built yet' screen: shows what this would do."""
    p = make_palette()
    while True:
        stdscr.erase()
        safe = header(stdscr, p, title, "any key back")
        safe(3, 4, "not built yet " + SOON, p["PINK"])
        safe(5, 4, "this would:", p["DIM"])
        for i, line in enumerate(would):
            safe(6 + i, 6, "· " + line, p["NORM"])
        stdscr.refresh()
        if stdscr.getch() != curses.KEY_RESIZE:
            return


def soon(title: str, would: list):
    """Action for list_screen that opens a placeholder screen."""
    return lambda s: show_placeholder(s, title, would)


def toggle_placeholder(stdscr, title: str, what: str) -> None:
    """Fake on/off/status screen for a toggle that isn't built yet."""
    items = [
        ("Turn on",  SOON, soon(f"{title} / on",     [f"turn {what} on"])),
        ("Turn off", SOON, soon(f"{title} / off",    [f"turn {what} off"])),
        ("Status",   SOON, soon(f"{title} / status", [f"show whether {what} is on"])),
    ]
    list_screen(stdscr, title, items, "↑↓ navigate   enter run   esc back")


def fake_progress(stdscr, title: str, steps: list) -> None:
    """Animated fake progress bar so long-running features can be felt."""
    p = make_palette()
    total = 40
    for n in range(total + 1):
        stdscr.erase()
        safe = header(stdscr, p, title, "fake run " + SOON)
        step = steps[min(len(steps) - 1, n * len(steps) // (total + 1))]
        safe(3, 4, step, p["NORM"])
        bar = "█" * n + "░" * (total - n)
        safe(5, 4, bar, p["RED"])
        safe(5, 6 + total, f"{n * 100 // total}%", p["PINK"])
        stdscr.refresh()
        time.sleep(0.06)
    safe(7, 4, "done (fake). press any key", p["DIM"])
    stdscr.refresh()
    stdscr.getch()

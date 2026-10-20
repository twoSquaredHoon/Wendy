import curses
from config.palette import make_palette


def list_screen(stdscr, title: str, items: list, controls: str = "↑↓ navigate   enter open   esc back"):
    """Generic list screen. items = [(label, detail, action)], action(stdscr) runs on enter."""
    curses.curs_set(0)
    p = make_palette()
    cursor = 0

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

        safe(0, 0, " @ WENDY ", p["RED"])
        safe(0, 9, title, p["DIM"])
        safe(0, w - len(controls) - 1, controls, p["PINK"])
        try:
            stdscr.attron(p["RED"])
            stdscr.hline(1, 0, curses.ACS_HLINE, w - 1)
            stdscr.attroff(p["RED"])
        except:
            pass

        for i, (label, detail, _) in enumerate(items):
            row = 3 + i * 2
            if cursor == i:
                safe(row, 2, ">", p["RED"])
                safe(row, 4, label, p["RED"])
            else:
                safe(row, 4, label, p["NORM"])
            if detail:
                safe(row, 4 + len(label), f"  {detail}", p["DIM"])

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP:
            cursor = max(0, cursor - 1)
        elif key == curses.KEY_DOWN:
            cursor = min(len(items) - 1, cursor + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            items[cursor][2](stdscr)
        elif key in (ord("q"), 27):
            break

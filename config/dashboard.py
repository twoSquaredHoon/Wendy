import curses
from config.palette import make_palette
from config.placeholder import header, SOON
from config.menu_list import list_screen

# all fake data — placeholder
OVERVIEW = [
    ("Toggles", [
        ("Firefox theme",     "nether"),
        ("GitHub daily push", "ON"),
        ("Tailscale",         "ON"),
        ("Life-log server",   "OFF"),
    ]),
    ("Today", [
        ("GitHub commit",     "✓ pushed 12:13"),
        ("Next job",          "none scheduled"),
    ]),
    ("This Mac", [
        ("Battery",           "84%  charging"),
        ("Disk",              "312 GB free"),
    ]),
]

AI_STATION = [
    ("Machines", [
        ("M4 MacBook Pro",    "● online   CPU 12%   disk 61%"),
        ("ThinkPad T480",     "● online   CPU  4%   disk 38%"),
        ("Storage PC (3TB)",  "● online   CPU  1%   disk 72%"),
        ("Ubuntu server",     "○ offline"),
    ]),
    ("Services", [
        ("Schedule (life-log)", "running on T480"),
        ("SharedComputing",     "idle"),
        ("demo3 multiplayer",   "stopped"),
    ]),
]


def show_board(stdscr, title, sections):
    p = make_palette()
    while True:
        stdscr.erase()
        safe = header(stdscr, p, title, "any key back")
        safe(3, 4, "fake data " + SOON, p["PINK"])
        row = 5
        for name, rows in sections:
            safe(row, 4, name, p["RED"])
            row += 1
            for label, value in rows:
                safe(row, 6, f"{label:<22}", p["DIM"])
                attr = p["NORM"]
                if value.startswith("○") or value == "OFF":
                    attr = p["DIM"]
                safe(row, 28, value, attr)
                row += 1
            row += 1
        stdscr.refresh()
        if stdscr.getch() != curses.KEY_RESIZE:
            return


def run_dashboard(stdscr) -> None:
    items = [
        ("Overview",   SOON, lambda s: show_board(s, "dashboard  /  overview", OVERVIEW)),
        ("AI station", SOON, lambda s: show_board(s, "dashboard  /  ai station", AI_STATION)),
    ]
    list_screen(stdscr, "dashboard", items)

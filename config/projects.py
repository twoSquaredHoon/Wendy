from config.menu_list import list_screen
from config.placeholder import soon, SOON

# fake list — placeholder
PROJECTS = [
    ("Wendy",            "~/Documents/2.Area/Wendy"),
    ("demo-3",           "Godot farming sim"),
    ("Viewer",           "iPad manga reader"),
    ("twoSquaredTyping", "desktop GIF app"),
    ("SharedComputing",  "distributed training"),
    ("Schedule",         "life-log app"),
]


def run_project(stdscr, name, where) -> None:
    items = [
        ("Open with Claude", SOON, soon(f"projects / {name}", [f"cd into {where}", "start claude there", "come back to Wendy when you exit"])),
        ("Open shell",       SOON, soon(f"projects / {name}", [f"open a shell in {where}"])),
        ("Git status",       SOON, soon(f"projects / {name}", ["show branch, changes, last commit"])),
        ("Open in editor",   SOON, soon(f"projects / {name}", ["open the folder in Cursor"])),
    ]
    list_screen(stdscr, f"projects  /  {name.lower()}", items, "↑↓ navigate   enter run   esc back")


def run_projects(stdscr) -> None:
    items = [
        (name, where, lambda s, n=name, w=where: run_project(s, n, w))
        for name, where in PROJECTS
    ]
    list_screen(stdscr, "projects  " + SOON, items)

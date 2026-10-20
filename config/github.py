from config.menu_list import list_screen
from config.modes import run_mode

PUSH = "scripts/daily-push.sh"

# label, what it does, command
GITHUB_ITEMS = [
    ("Turn on",   "daily commit at login + every hour", f"{PUSH} on"),
    ("Turn off",  "stop the daily commit",              f"{PUSH} off"),
    ("Status",    "on/off, last entries, last run",     f"{PUSH} status"),
    ("Push now",  "run the daily commit right now",     f"{PUSH} now"),
    ("View log",  "full run log",                       f"{PUSH} log"),
]


def run_github(stdscr) -> None:
    items = [
        (label, detail, lambda s, cmd=cmd: run_mode(s, cmd))
        for label, detail, cmd in GITHUB_ITEMS
    ]
    list_screen(stdscr, "script toggles  /  github daily push", items, "↑↓ navigate   enter run   esc back")

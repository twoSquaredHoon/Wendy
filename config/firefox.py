from config.menu_list import list_screen
from config.modes import run_mode

THEME = "scripts/firefox-theme.sh"

# label, what it does, command
FIREFOX_ITEMS = [
    ("Random theme",    "pick nether or overworld, open Firefox", f"{THEME} random && open -a Firefox"),
    ("Nether theme",    "turn on nether",                         f"{THEME} nether"),
    ("Overworld theme", "turn on overworld",                      f"{THEME} overworld"),
    ("Theme off",       "back to normal Firefox",                 f"{THEME} off"),
    ("Status",          "which theme is on",                      f"{THEME} status"),
]


def run_firefox(stdscr) -> None:
    items = [
        (label, detail, lambda s, cmd=cmd: run_mode(s, cmd))
        for label, detail, cmd in FIREFOX_ITEMS
    ]
    list_screen(stdscr, "script toggles  /  firefox", items, "↑↓ navigate   enter run   esc back")

from config.menu_list import list_screen
from config.firefox import run_firefox
from config.github import run_github
from config.placeholder import toggle_placeholder, SOON


def run_config(stdscr) -> None:
    items = [
        ("Firefox", "themes", run_firefox),
        ("GitHub daily push", "toggle the daily commit", run_github),
        # placeholders
        ("Tailscale",         SOON, lambda s: toggle_placeholder(s, "script toggles  /  tailscale", "Tailscale")),
        ("Life-log server",   SOON, lambda s: toggle_placeholder(s, "script toggles  /  life-log server", "the Schedule server")),
        ("demo3 server",      SOON, lambda s: toggle_placeholder(s, "script toggles  /  demo3 server", "the demo3 multiplayer server")),
        ("twoSquaredTyping",  SOON, lambda s: toggle_placeholder(s, "script toggles  /  twosquaredtyping", "the desktop GIF app")),
        ("Dark mode",         SOON, lambda s: toggle_placeholder(s, "script toggles  /  dark mode", "macOS dark mode")),
        ("Do Not Disturb",    SOON, lambda s: toggle_placeholder(s, "script toggles  /  do not disturb", "Do Not Disturb")),
        ("Keep awake",        SOON, lambda s: toggle_placeholder(s, "script toggles  /  keep awake", "keep-the-Mac-awake")),
    ]
    list_screen(stdscr, "script toggles", items)

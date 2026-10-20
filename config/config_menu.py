from config.menu_list import list_screen
from config.firefox import run_firefox


def run_config(stdscr) -> None:
    items = [
        ("Firefox", "themes", run_firefox),
    ]
    list_screen(stdscr, "config", items)

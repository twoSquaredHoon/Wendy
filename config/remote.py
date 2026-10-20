from config.menu_list import list_screen
from config.placeholder import soon, fake_progress, SOON


def run_league(stdscr) -> None:
    items = [
        ("Pick mp4",       SOON, soon("league / pick", ["list gameplay mp4s on this laptop", "let you pick one"])),
        ("Upload + run",   SOON, lambda s: fake_progress(s, "league / ward detection", [
            "uploading game_0412.mp4 to server...",
            "running minimap ward detection...",
            "downloading results...",
        ])),
        ("View results",   SOON, soon("league / results", ["show wards found per minute", "open the result video"])),
    ]
    list_screen(stdscr, "remote  /  league server", items, "↑↓ navigate   enter run   esc back")


def run_shared_computing(stdscr) -> None:
    items = [
        ("Start training run", SOON, lambda s: fake_progress(s, "sharedcomputing / training", [
            "copying dataset to 3 machines...",
            "training epoch 1/5 across M4, T480, storage PC...",
            "training epoch 3/5...",
            "training epoch 5/5...",
            "saving model + time/power report...",
        ])),
        ("Watch progress",     SOON, soon("sharedcomputing / progress", ["live epoch + loss per machine"])),
        ("Past runs",          SOON, soon("sharedcomputing / runs", ["list runs with time and power saved"])),
    ]
    list_screen(stdscr, "remote  /  sharedcomputing", items, "↑↓ navigate   enter run   esc back")


def run_remote(stdscr) -> None:
    items = [
        ("SSH: ThinkPad T480",  SOON, soon("remote / ssh t480",   ["open a shell on the T480 (over Tailscale)", "come back to Wendy when you exit"])),
        ("SSH: Ubuntu server",  SOON, soon("remote / ssh server", ["open a shell on the Ubuntu server", "come back to Wendy when you exit"])),
        ("SSH: Storage PC",     SOON, soon("remote / ssh storage", ["open a shell on the 3TB storage PC"])),
        ("League server",       SOON, run_league),
        ("SharedComputing",     SOON, run_shared_computing),
    ]
    list_screen(stdscr, "remote", items)

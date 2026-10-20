import curses


def make_palette() -> dict:
    curses.start_color()
    curses.use_default_colors()

    if curses.can_change_color():
        curses.init_color(16, 514, 180, 192)   # #832e31
        curses.init_color(17, 875, 576, 588)   # #df9396
        custom_red  = 16
        custom_pink = 17
    else:
        custom_red  = curses.COLOR_RED
        custom_pink = curses.COLOR_MAGENTA

    curses.init_pair(1, custom_red,  -1)  # RED
    curses.init_pair(2, custom_pink, -1)  # PINK
    curses.init_pair(3, curses.COLOR_WHITE, -1)  # NORM

    return {
        "RED":  curses.color_pair(1) | curses.A_BOLD,
        "PINK": curses.color_pair(2) | curses.A_BOLD,
        "NORM": curses.color_pair(3),
        "DIM":  curses.color_pair(3) | curses.A_DIM,
    }

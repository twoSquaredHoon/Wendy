import curses
from config.palette import make_palette
from config.placeholder import header, SOON


def run_notes(stdscr) -> None:
    # placeholder: notes only live until you leave this screen (would save to Obsidian)
    p = make_palette()
    notes = ["buy C10 brake lines", "CS 577 hw due fri"]   # fake starting notes
    typing = False
    buf = ""
    while True:
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        safe = header(stdscr, p, "notes", "n new   d delete last   esc back")
        safe(3, 4, "not saved anywhere yet " + SOON + " — would save to your Obsidian vault", p["PINK"])
        for i, note in enumerate(notes):
            safe(5 + i, 4, "· " + note, p["NORM"])
        if typing:
            safe(h - 1, 0, "note: " + buf + "█", p["PINK"])
        stdscr.refresh()
        key = stdscr.getch()

        if typing:
            if key in (curses.KEY_ENTER, 10, 13):
                if buf.strip():
                    notes.append(buf.strip())
                typing, buf = False, ""
            elif key == 27:
                typing, buf = False, ""
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                buf = buf[:-1]
            elif 32 <= key <= 126:
                buf += chr(key)
        elif key == ord("n"):
            typing = True
        elif key == ord("d") and notes:
            notes.pop()
        elif key in (ord("q"), 27):
            return

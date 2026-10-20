# 🤖 Wendy

A terminal TUI for launching your stuff.

## Run

```
python3 main.py
```

No installs needed — `curses` is built into Python on macOS.

## Menu

- **Modes** — pick one and Wendy runs it in this terminal (e.g. `claude`). When it exits, press enter to go back to Wendy.
- **Jobs** — saved bash commands, run now or daily.
- **Config** — settings for other apps. **Config → Firefox** has the theme switcher.

## Modes

Modes live in `settings.json` as `"name": "shell command"`:

```json
"modes": {
  "Claude": "claude",
  "Claude (resume last)": "claude --continue",
  "Shell": "$SHELL"
}
```

Add your own, e.g. `"Server": "cd ~/SharedComputing && ./run.sh"`.

## Jobs

Saved bash commands (e.g. a daily git push). In the Jobs screen:

| key   | does                                         |
| ----- | -------------------------------------------- |
| enter | run the job now                              |
| n     | new job — name, command, daily time (HH:MM)  |
| t     | change a job's time (empty = manual only)    |
| l     | view the job's log                           |
| d     | delete                                       |

Jobs with a time are scheduled in your `crontab` (Wendy only touches its own
`# >>> wendy jobs >>>` block). Each run is logged to `~/.wendy/logs/<job>.log`,
and the Jobs screen shows the last run and whether it failed.

Note: cron only runs while the Mac is awake.

## Firefox themes

`scripts/firefox-theme.sh` switches your Minecraft Firefox themes. Wendy runs it from **Config → Firefox**:

| item            | does                                          |
| --------------- | --------------------------------------------- |
| Random theme    | picks nether or overworld, then opens Firefox |
| Nether theme    | nether theme on                               |
| Overworld theme | overworld theme on                            |
| Theme off       | back to normal Firefox                        |
| Status          | shows which theme is on                       |

Firefox only loads the theme when it starts, so restart Firefox (⌘Q) after switching.
Theme files are read from `~/Documents/firefox-chrome-backup/chrome`
(change with `WENDY_FIREFOX_THEMES=/other/path`).

## Structure

```
main.py                 # entry point — the TUI
settings.json           # modes, jobs
config/
├── welcome.py          # welcome screen (logo + greeting) on launch
├── modes.py            # Modes screen — runs commands
├── jobs.py             # Jobs screen — saved/scheduled bash commands
├── config_menu.py      # Config screen (Firefox, ...)
├── firefox.py          # Config → Firefox: theme switcher items
├── menu_list.py        # shared list screen used by Config
├── palette.py          # colors
└── settings_store.py   # load / save settings.json
scripts/
└── firefox-theme.sh    # nether | overworld | random | off | status
documentation/          # per-file notes
```

## License

MIT

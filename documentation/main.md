# main.py

**Shared UI/code conventions:** `documentation/config-style.md` (hub layout, footer rules, `safe`, keys, palette).

## Role

Entry point. Shows the welcome screen (`config/welcome.py`, any key continues), then the hub menu and **routes** to each screen. Does not read or write `settings.json` itself — screens use `config/settings_store.py`.

## Flow

```text
main.py  →  config/modes.py   (name of last mode run, or "")
         →  config/jobs.py
```

## Screens

| Module | Purpose |
|--------|---------|
| `config/modes.py` | Run a saved command (e.g. `claude`) in this terminal, then return to Wendy |
| `config/jobs.py` | Saved bash commands — run now, schedule daily via `crontab`, view logs |

## Menu

Order is `MENU_ITEMS`: **Modes**, **Jobs**. `esc` or `q` quits.

## settings.json

- `modes` — name → shell command
- `jobs` — name → `{ "command": "...", "time": "HH:MM" or "" }`

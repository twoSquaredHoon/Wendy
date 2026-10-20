# settings_store.py

Single module for **`settings.json`** path, **normalization**, and **read/write**, used by every screen.

## Canonical shape

| Key | Type | Notes |
|-----|------|-------|
| `modes` | object | Mode name → shell command. Defaults to `DEFAULT_MODES` (Claude, Claude resume, Shell) |
| `jobs` | object | Job name → `{ "command": string, "time": "HH:MM" or "" }`. Defaults to `{}` |

## normalize_settings

Fills in any missing key with its default. Unknown keys are dropped on save.

## load_settings / save_settings

- `load_settings()` — returns defaults if the file is missing or not valid JSON.
- `save_settings(settings)` — writes the normalized shape, `indent=2`, trailing newline.

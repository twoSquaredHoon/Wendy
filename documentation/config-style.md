# Style & UI conventions — `config/` + hub (`main.py`)

Single reference for **formatting, code layout, shared curses patterns, palette, and hub chrome**. Feature-specific behavior (what data means, business rules) stays in the per-topic docs listed under [Documentation map](#documentation-map).

---

## Documentation map

| Doc | Contents |
|-----|----------|
| `documentation/main.md` | `main.py` hub: flow, menu, `settings.json` overview, footer **messages** |
| `config/modes.py` | Modes screen: runs a saved command in the terminal, then returns |
| `config/jobs.py` | Jobs screen: saved bash commands, daily cron schedule, logs in `~/.wendy/logs` |
| `documentation/settings_store.md` | `settings.json` path, canonical keys, `normalize_settings` |
| `documentation/palette.md` | Pointer — palette API lives **below** in this file |

---

## Global — `main.py` hub

Applies to the **menu loop** in `main.py` (not the `config/` package, but the same visual language).

### Layout

| Row | Content |
|-----|---------|
| 0 | `@ WENDY` (`RED`), title `config` (`DIM`, col 9), controls (`PINK`, right-aligned): `↑↓ navigate   enter open   esc quit` |
| 1 | Full-width `ACS_HLINE` in `RED` via `stdscr.hline` — **never** `safe()` (string clipping breaks line drawing) |
| 2 | Empty |
| 3+ | Menu: first item row **3**, step **2** between rows (`3 + i * 2`) |
| `h-2` | Full-width red `hline` |
| `h-1` | Footer message |

### Menu rows

- **Selected:** `>` at column **2** (`RED`), label column **4** (`RED`).
- **Unselected:** label column **4** (`NORM`).

### Footer message styling

| Mode | Template | Attribute |
|------|------------|-------------|
| Joke (navigating) | ` '"…"' ` (quotes part of display) | `PINK` |
| Update | ` … ` (spaces, no decorative quotes) | `NORM` |

After **Modes**, update style only if something was run.

### Hub update messages

| Source | Message |
|--------|---------|
| Modes — ran something | `Back from {mode}.` |
| Modes — ran nothing | new random joke |
| Jobs | new random joke |

### `safe()` (hub)

Same rules as in [Nested helpers](#nested-helpers-safe--draw_header): clip to bounds, swallow curses errors; **not** for full-width `hline`.

### Hub keys

| Key | Action |
|-----|--------|
| `↑` / `↓` | Move cursor; new joke on each move |
| `enter` | Open selected section |
| `q` / `esc` | Quit |

---

## Imports

1. **Standard library** — `curses`, `json`, `os`, `pathlib`, `random`, `typing` as needed.
2. **Blank line.**
3. **Package imports** — `from config.…` (absolute from project root when running `main.py`).

`settings_store.py` may use `from __future__ import annotations` and `typing`; curses modules typically leave `stdscr` untyped.

---

## Environment

Every **curses** module that handles keys:

```python
os.environ.setdefault("ESCDELAY", "0")
```

Immediately after imports. Omit in `palette.py` and `settings_store.py`.

---

## Persistence

- Read/write **`settings.json`** only through **`config/settings_store.py`** (`load_settings`, `save_settings`).
- Do not use `Path("settings.json")` ad hoc in screen modules.
- After edits, `save_settings(settings)` with the dict you loaded and mutated.

Details: `documentation/settings_store.md`.

---

## Palette (`config/palette.py`)

### API

```text
make_palette() -> dict[str, ...]
```

| Key | Role |
|-----|------|
| `RED` | Brand — wordmark, dividers, selection (`A_BOLD` + pair 1) |
| `PINK` | Controls, accents (`A_BOLD` + pair 2) |
| `NORM` | Default text (pair 3: white on the terminal background) |
| `DIM` | `NORM` + `A_DIM` |

### Implementation

- Calls `curses.start_color()` / `use_default_colors()`.
- If `curses.can_change_color()`: custom indices **16** (`#832e31`) and **17** (`#df9396`). Else pair 1 → `COLOR_RED`, pair 2 → `COLOR_MAGENTA`.
- Dark theme only — there is no light mode.

### Consumers

`main.py`, `config/modes.py`, `config/jobs.py`.

---

## Screen modules (`modes`, `jobs`)

### Public entrypoint

```text
def run_<name>(stdscr) -> str:
```

- Return value drives the hub footer (e.g. `modes` returns the name of the last mode run, or `""`).
- First lines:

```python
curses.curs_set(0)
p = make_palette()
```

### Nested helpers (`safe` / `draw_header`)

**`safe(y, x, text, attr=None)`** — coerce `text` to `str`, default `attr` to `p["NORM"]`, clip to terminal, `attron` / `addstr` / `attroff`, bare `except:` for curses errors. **Do not** use for horizontal rules.

**`draw_header(title, controls=...)`** — default controls vary by screen; see below.

| Column | Content |
|--------|---------|
| 0 | ` @ WENDY ` — `RED` |
| 9 | `title` — `DIM` |
| Right | `controls` — `PINK` |
| Row 1 | `hline` + `RED` (not `safe`) |

Default control strings:

- `↑↓ navigate   enter run   esc back` — `modes`
- `enter run   n new   t time   l log   d delete   esc back` — `jobs`

### List layout (shared)

- First content row **3**, row step **2** (`3 + i * 2`).
- Selected: `>` col **2**, label col **4**, `RED`.
- Scrollable lists: `list_rows = (h - 4) // 2`, keep cursor in view with a `scroll` index.

### Input (shared)

| Meaning | Code |
|---------|------|
| Enter | `key in (curses.KEY_ENTER, 10, 13)` |
| Quit / back | `key in (ord("q"), 27)` |
| Up / down | `curses.KEY_UP` / `curses.KEY_DOWN` |

### Section banners

```python
# ── Section name ──────────────────────────────────────────────────
```

---

## `settings_store.py` (code conventions)

- **`REPO_ROOT`** = `Path(__file__).resolve().parent.parent`.
- Constants: **`UPPER_SNAKE`** (`SETTINGS_PATH`, `DEFAULT_MODES`).
- Private helpers: **`_` prefix**.
- **`save_settings`**: JSON `indent=2` and **trailing newline** on the file.
- Canonical payload and normalization: `documentation/settings_store.md`.

---

## Naming

- **`snake_case`** — functions, locals, controlled JSON keys.
- **`UPPER_SNAKE`** — module constants.
- Screen runners: **`run_modes`**, **`run_jobs`**.

---

## Formatting (Python)

- **Two blank lines** between top-level definitions (PEP 8).
- Avoid heavy docstrings on tiny helpers; module docstring on `settings_store` is enough unless logic is opaque.

---

## Design rules

1. One settings pipeline — **`settings_store`**.
2. One shared palette for hub UIs — **`make_palette`**.
3. Honest return values to the hub.
4. Full-width dividers — **`hline`** + `RED`, never **`safe`**.

---

## Checklist — new `config` screen

- [ ] `ESCDELAY` if handling keys
- [ ] `run_*(stdscr)`
- [ ] `curs_set(0)` + `make_palette` where applicable
- [ ] `safe` / `draw_header` per tables above
- [ ] Settings via `load_settings` / `save_settings` only
- [ ] Shared input idioms
- [ ] Lists from row 3, step 2

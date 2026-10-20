"""Single source of truth for settings.json path, shape, and persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = REPO_ROOT / "settings.json"

# Default terminal modes: name -> shell command run from the Modes screen.
DEFAULT_MODES = {
    "Claude": "claude",
    "Claude (resume last)": "claude --continue",
    "Shell": "$SHELL"
}


def normalize_settings(raw: dict[str, Any]) -> dict[str, Any]:
    """Fill in defaults so every key exists."""
    return {
        "modes": dict(raw.get("modes") or DEFAULT_MODES),
        "jobs": dict(raw.get("jobs") or {}),
    }


def load_settings() -> dict[str, Any]:
    if not SETTINGS_PATH.exists():
        return normalize_settings({})
    try:
        raw = json.loads(SETTINGS_PATH.read_text())
    except Exception:
        return normalize_settings({})
    if not isinstance(raw, dict):
        return normalize_settings({})
    return normalize_settings(raw)


def save_settings(settings: dict[str, Any]) -> None:
    """Write modes and jobs (canonical settings.json)."""
    SETTINGS_PATH.write_text(json.dumps(normalize_settings(settings), indent=2) + "\n")

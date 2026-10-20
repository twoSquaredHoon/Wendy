#!/bin/bash
# Wendy — toggle the daily GitHub commit (workflows repo's LaunchAgent)
# usage: daily-push.sh on | off | status | now | log

WORKFLOWS_DIR="${WENDY_WORKFLOWS_DIR:-$HOME/workflows}"
LABEL="com.twosquaredhoon.workflows.dailypush"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
SRC_PLIST="$WORKFLOWS_DIR/launchd/$LABEL.plist"
OUT_LOG="$WORKFLOWS_DIR/log/launchd.out.log"

is_on() {
  launchctl list 2>/dev/null | grep -q "$LABEL"
}

case "$1" in
  on)
    if [ ! -f "$PLIST" ]; then
      if [ ! -f "$SRC_PLIST" ]; then
        echo "  ✗ can't find $SRC_PLIST"
        exit 1
      fi
      mkdir -p "$HOME/Library/LaunchAgents"
      cp "$SRC_PLIST" "$PLIST"
    fi
    launchctl unload "$PLIST" 2>/dev/null
    launchctl load -w "$PLIST"
    if is_on; then echo "  ✓ daily push is ON (runs at login + every hour)"; else echo "  ✗ couldn't turn it on"; exit 1; fi
    ;;
  off)
    launchctl unload -w "$PLIST" 2>/dev/null
    if is_on; then echo "  ✗ still running"; exit 1; else echo "  ✓ daily push is OFF"; fi
    ;;
  status)
    if is_on; then echo "  daily push: ON"; else echo "  daily push: OFF"; fi
    echo "  repo: $WORKFLOWS_DIR"
    echo ""
    echo "  last entries in log/daily.md:"
    tail -3 "$WORKFLOWS_DIR/log/daily.md" 2>/dev/null | sed 's/^/    /'
    echo ""
    echo "  last run:"
    tail -4 "$OUT_LOG" 2>/dev/null | sed 's/^/    /'
    ;;
  now)
    bash "$WORKFLOWS_DIR/scripts/daily_push.sh"
    ;;
  log)
    less +G "$OUT_LOG"
    ;;
  *)
    echo "usage: $0 on | off | status | now | log"
    exit 1
    ;;
esac

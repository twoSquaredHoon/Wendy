#!/bin/bash
# Wendy — Firefox theme switcher
# usage: firefox-theme.sh nether | overworld | random | off | status
# Firefox only reads the theme when it starts, so restart Firefox after switching.

THEME_DIR="${WENDY_FIREFOX_THEMES:-$HOME/Documents/firefox-chrome-backup/chrome}"
FF_DIR="$HOME/Library/Application Support/Firefox"

# ── find the profile Firefox actually uses (from profiles.ini) ──
PROFILE_REL=$(awk '/^\[Install/{f=1;next} /^\[/{f=0} f && /^Default=/{sub(/^Default=/,"");print;exit}' "$FF_DIR/profiles.ini" 2>/dev/null)
if [ -n "$PROFILE_REL" ]; then
  PROFILE="$FF_DIR/$PROFILE_REL"
else
  PROFILE=$(ls -dt "$FF_DIR"/Profiles/*.default-release* 2>/dev/null | head -1)
fi
if [ ! -d "$PROFILE" ]; then
  echo "  ✗ couldn't find your Firefox profile. Open Firefox once, then try again."
  exit 1
fi
CHROME="$PROFILE/chrome"

turn_on() {
  NAME="$1"
  if [ ! -f "$THEME_DIR/userContent-$NAME.css" ]; then
    echo "  ✗ no theme '$NAME' in $THEME_DIR"
    exit 1
  fi
  mkdir -p "$CHROME" || exit 1
  # images the themes use
  cp -R "$THEME_DIR/Backgrounds" "$THEME_DIR/Banner" "$THEME_DIR/Searchbar" "$CHROME/" 2>/dev/null
  cp "$THEME_DIR/userContent-$NAME.css" "$CHROME/userContent.css" || exit 1
  # square Firefox UI (tabs, address bar, menus) — same for every theme
  [ -f "$THEME_DIR/userChrome.css" ] && cp "$THEME_DIR/userChrome.css" "$CHROME/userChrome.css"
  # let Firefox load custom CSS (off by default)
  PREF='user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);'
  grep -qF "$PREF" "$PROFILE/user.js" 2>/dev/null || echo "$PREF" >> "$PROFILE/user.js"
  echo "$NAME" > "$CHROME/.wendy-theme"
  echo "  ✓ $NAME theme on. Restart Firefox to see it."
}

case "$1" in
  nether|overworld)
    turn_on "$1"
    ;;
  random)
    if [ $(( RANDOM % 2 )) -eq 0 ]; then turn_on nether; else turn_on overworld; fi
    ;;
  off)
    rm -f "$CHROME/userContent.css" "$CHROME/userChrome.css" "$CHROME/.wendy-theme"
    echo "  ✓ theme off. Restart Firefox to see it."
    ;;
  status)
    if [ -f "$CHROME/userContent.css" ]; then
      echo "  current theme: $(cat "$CHROME/.wendy-theme" 2>/dev/null || echo unknown)"
    else
      echo "  theme is off"
    fi
    echo "  profile: $PROFILE"
    ;;
  *)
    echo "usage: $0 nether | overworld | random | off | status"
    exit 1
    ;;
esac

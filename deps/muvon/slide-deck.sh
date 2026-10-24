#!/usr/bin/env bash
# dep: muvon/slide-deck
# type: dep
# description: slide-deck - Marp slide deck CLI (lint, PDF/HTML/PPTX/PNG export, overflow check, octo theme) shipped with this tap
# check: slide-deck
# https://github.com/muvon/octomind-tap

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# The CLI is the slide-decks skill's bundled script; linking it onto PATH makes it
# callable whether or not the skill is active in the session. It runs a pinned
# Marp CLI through npx and renders with a local Chromium-family browser or Firefox.
SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../skills/slide-decks/scripts" && pwd)/deck.py"
BIN_DIR="${HOME}/.local/bin"
LINK="${BIN_DIR}/slide-deck"
BROWSERS_DIR="${HOME}/.cache/puppeteer"

have_browser() {
  [[ -n ${CHROME_PATH:-} && -x ${CHROME_PATH:-} ]] && return 0
  local p
  for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
    "/Applications/Firefox.app/Contents/MacOS/firefox"; do
    [[ -x $p ]] && return 0
  done
  for p in google-chrome google-chrome-stable chromium chromium-browser microsoft-edge firefox; do
    pkg_check "$p" && return 0
  done
  compgen -G "${BROWSERS_DIR}/chrome-headless-shell/*/*/chrome-headless-shell" >/dev/null && return 0
  compgen -G "${HOME}/.cache/ms-playwright/chromium-*/chrome-*/chrome" >/dev/null && return 0
  return 1
}

# Fast path — linked to this tap's script, Node available, a browser present
if pkg_check slide-deck && [[ "$(readlink "$LINK" 2>/dev/null)" == "$SCRIPT" ]] && pkg_check npx && have_browser; then
  exit 0
fi

[[ -f $SCRIPT ]] || die "Slide deck script not found: $SCRIPT"

if ! pkg_check python3; then
  info "python3 not found — installing..."
  case "$OS" in
    macos)
      if pkg_check brew; then
        brew install python
      else
        die "brew not found. Install Homebrew first: https://brew.sh"
      fi
      ;;
    linux)
      pkg_install python3
      ;;
    *)
      die "Install Python 3.9+ manually: https://www.python.org/downloads/"
      ;;
  esac
fi

if ! pkg_check npx; then
  install_dep nodejs/node
fi

if ! have_browser; then
  info "No Chrome, Edge, Chromium, or Firefox found — installing chrome-headless-shell for PDF/PNG export..."
  mkdir -p "$BROWSERS_DIR"
  npx -y @puppeteer/browsers@3.2.6 install chrome-headless-shell@stable --path "$BROWSERS_DIR" >/dev/null ||
    warn "chrome-headless-shell install failed; install Chrome or Chromium, or set CHROME_PATH"
fi

chmod +x "$SCRIPT"
mkdir -p "$BIN_DIR"
ln -sf "$SCRIPT" "$LINK"
export PATH="${BIN_DIR}:$PATH"

if ! pkg_check slide-deck; then
  die "slide-deck linked but not in PATH. Add ~/.local/bin to PATH."
fi

info "slide-deck installed: $LINK -> $SCRIPT"

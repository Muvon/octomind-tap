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
PLAYWRIGHT="playwright@1.64.1"

have_browser() {
  [[ -n ${CHROME_PATH:-} && -x ${CHROME_PATH:-} ]] && return 0
  local p
  for p in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
    "/Applications/Firefox.app/Contents/MacOS/firefox" \
    "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
    "/c/Program Files/Microsoft/Edge/Application/msedge.exe"; do
    [[ -x $p ]] && return 0
  done
  for p in google-chrome google-chrome-stable chromium chromium-browser microsoft-edge firefox; do
    pkg_check "$p" && return 0
  done
  compgen -G "${HOME}/.cache/puppeteer/chrome-headless-shell/*/*/chrome-headless-shell" >/dev/null && return 0
  compgen -G "${HOME}/.cache/ms-playwright/chromium-*/chrome-*/chrome" >/dev/null && return 0
  compgen -G "${HOME}/Library/Caches/ms-playwright/chromium-*/chrome-mac*/*.app/Contents/MacOS/*" >/dev/null && return 0
  compgen -G "${LOCALAPPDATA:-/nonexistent}/ms-playwright/chromium-*/chrome-win*/chrome.exe" >/dev/null && return 0
  return 1
}

# Root or passwordless sudo: Playwright may also install Chromium's system libraries (Linux).
can_install_system_deps() {
  [[ $OS == "linux" ]] || return 1
  [[ "$(id -u)" -eq 0 ]] && return 0
  pkg_check sudo && sudo -n true 2>/dev/null
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
  info "No Chrome, Edge, Chromium, or Firefox found — installing Playwright's Chromium for PDF/PNG export..."
  if can_install_system_deps; then
    npx -y "$PLAYWRIGHT" install --with-deps chromium >/dev/null ||
      warn "Chromium install failed; install Chrome or Chromium, or set CHROME_PATH"
  else
    npx -y "$PLAYWRIGHT" install chromium >/dev/null ||
      warn "Chromium install failed; install Chrome or Chromium, or set CHROME_PATH"
    if [[ $OS == "linux" ]]; then
      warn "If rendering fails on missing libraries, run: sudo npx $PLAYWRIGHT install-deps chromium"
    fi
  fi
fi

# The script ships executable; chmod only if a checkout lost the bit (read-only mounts fail on chmod).
[[ -x $SCRIPT ]] || chmod +x "$SCRIPT"
mkdir -p "$BIN_DIR"
ln -sf "$SCRIPT" "$LINK"
export PATH="${BIN_DIR}:$PATH"

if ! pkg_check slide-deck; then
  die "slide-deck linked but not in PATH. Add ~/.local/bin to PATH."
fi

info "slide-deck installed: $LINK -> $SCRIPT"

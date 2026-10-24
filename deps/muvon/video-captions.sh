#!/usr/bin/env bash
# dep: muvon/video-captions
# type: dep
# description: video-captions - word-timed TikTok-style video caption generator CLI (ASS + SRT, ffmpeg burn) shipped with this tap
# check: video-captions
# https://github.com/muvon/octomind-tap

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# The renderer is the video-captions skill's bundled script; linking it onto
# PATH makes it callable whether or not the skill is active in the session.
SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../skills/video-captions/scripts" && pwd)/captions.py"
BIN_DIR="${HOME}/.local/bin"
LINK="${BIN_DIR}/video-captions"

# Fast path — already linked to this tap's script
if pkg_check video-captions && [[ "$(readlink "$LINK" 2>/dev/null)" == "$SCRIPT" ]]; then
  exit 0
fi

[[ -f $SCRIPT ]] || die "Caption script not found: $SCRIPT"

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

chmod +x "$SCRIPT"
mkdir -p "$BIN_DIR"
ln -sf "$SCRIPT" "$LINK"
export PATH="${BIN_DIR}:$PATH"

if ! pkg_check video-captions; then
  die "video-captions linked but not in PATH. Add ~/.local/bin to PATH."
fi

info "video-captions installed: $LINK -> $SCRIPT"

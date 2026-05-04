#!/usr/bin/env bash
# dep: ffmpeg/ffmpeg
# type: dep
# description: ffmpeg — multimedia framework for stitching, transcoding, and burning captions
# check: ffmpeg
# https://ffmpeg.org/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check ffmpeg; then
  exit 0
fi

info "ffmpeg not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install ffmpeg
    else
      die "brew not found. Install Homebrew first: https://brew.sh"
    fi
    ;;

  linux)
    case "$PKG_MANAGER" in
      apt)
        sudo apt-get update
        sudo apt-get install -y ffmpeg
        ;;
      dnf)
        sudo dnf install -y ffmpeg
        ;;
      pacman)
        sudo pacman -S --noconfirm ffmpeg
        ;;
      zypper)
        sudo zypper install -y ffmpeg
        ;;
      apk)
        sudo apk add ffmpeg
        ;;
      *)
        die "No supported package manager. Install ffmpeg manually: https://ffmpeg.org/download.html"
        ;;
    esac
    ;;

  windows)
    # Download pre-built ffmpeg from gyan.dev (essentials zip — no 7z needed)
    TMP_DIR=$(mktemp -d)
    trap 'rm -rf "$TMP_DIR"' EXIT
    curl -fsSL "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -o "$TMP_DIR/ffmpeg.zip"
    unzip -qo "$TMP_DIR/ffmpeg.zip" -d "$TMP_DIR"
    # Archive contains a single directory like ffmpeg-8.0-essentials_build/
    BIN_DIR=$(dirname "$(find "$TMP_DIR" -name "ffmpeg.exe" | head -1)")
    mkdir -p "${HOME}/.local/bin"
    cp "$BIN_DIR/ffmpeg.exe" "${HOME}/.local/bin/ffmpeg.exe"
    cp "$BIN_DIR/ffprobe.exe" "${HOME}/.local/bin/ffprobe.exe" 2>/dev/null || true
    export PATH="${HOME}/.local/bin:$PATH"
    ;;
esac

if ! pkg_check ffmpeg; then
  die "ffmpeg installed but not in PATH."
fi

info "ffmpeg installed successfully."

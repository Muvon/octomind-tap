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
    # Download pre-built ffmpeg from gybern.dev (official Windows builds)
    VERSION="7.1.1"
    TMP_DIR=$(mktemp -d)
    trap 'rm -rf "$TMP_DIR"' EXIT
    FILENAME="ffmpeg-${VERSION}-full_build.zip"
    curl -fsSL "https://www.gyan.dev/ffmpeg/builds/${FILENAME}" -o "$TMP_DIR/${FILENAME}"
    unzip -qo "$TMP_DIR/${FILENAME}" -d "$TMP_DIR"
    mkdir -p "${HOME}/.local/bin"
    cp "$TMP_DIR/ffmpeg-${VERSION}-full_build/bin/ffmpeg.exe" "${HOME}/.local/bin/ffmpeg.exe"
    cp "$TMP_DIR/ffmpeg-${VERSION}-full_build/bin/ffprobe.exe" "${HOME}/.local/bin/ffprobe.exe"
    export PATH="${HOME}/.local/bin:$PATH"
    ;;
esac

if ! pkg_check ffmpeg; then
  die "ffmpeg installed but not in PATH."
fi

info "ffmpeg installed successfully."

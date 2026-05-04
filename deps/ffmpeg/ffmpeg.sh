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
esac

if ! pkg_check ffmpeg; then
  die "ffmpeg installed but not in PATH."
fi

info "ffmpeg installed successfully."

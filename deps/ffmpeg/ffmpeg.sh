#!/usr/bin/env bash
# dep: ffmpeg/ffmpeg
# type: dep
# description: ffmpeg with libass + freetype - stitching, transcoding, burning styled captions and text overlays
# check: ffmpeg
# https://ffmpeg.org/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Caption burning (`ass` / `subtitles`) and text overlays (`drawtext`) need an
# ffmpeg built with libass + freetype. Homebrew's default `ffmpeg` formula ships
# without both; its keg-only `ffmpeg-full` formula has them.
has_text_filters() {
  "$1" -hide_banner -filters 2>/dev/null |
    awk '$2 == "ass" { a = 1 } $2 == "drawtext" { d = 1 } END { exit !(a && d) }'
}

# Fast path — an ffmpeg with libass + freetype is already on PATH
if pkg_check ffmpeg && has_text_filters ffmpeg; then
  exit 0
fi

FULL=""
case "$OS" in
  macos)
    if ! pkg_check brew; then
      die "brew not found. Install Homebrew first: https://brew.sh"
    fi
    FULL="$(brew --prefix)/opt/ffmpeg-full/bin/ffmpeg"
    if ! { [[ -x $FULL ]] && has_text_filters "$FULL"; }; then
      info "Installing ffmpeg-full (ffmpeg with libass, freetype, harfbuzz)..."
      brew install ffmpeg-full
    fi
    # ffmpeg-full can pull newer shared libraries (x265, ...) than an outdated
    # stock ffmpeg was built against; upgrading relinks it.
    if pkg_check ffmpeg && ! ffmpeg -version &>/dev/null; then
      brew upgrade ffmpeg
    fi
    if ! pkg_check ffmpeg; then
      brew link --force ffmpeg-full
    elif ! has_text_filters ffmpeg; then
      info "Stock ffmpeg stays first on PATH; the libass build is $FULL."
      info "To make it the default: brew unlink ffmpeg && brew link --force ffmpeg-full"
    fi
    ;;

  linux)
    info "Installing ffmpeg..."
    case "$PKG_MANAGER" in
      apt)
        as_root apt-get update
        as_root apt-get install -y ffmpeg
        ;;
      dnf)
        # Fedora main repos ship ffmpeg-free; RPM Fusion ships ffmpeg.
        as_root dnf install -y ffmpeg || as_root dnf install -y ffmpeg-free
        ;;
      pacman)
        as_root pacman -S --noconfirm ffmpeg
        ;;
      zypper)
        as_root zypper install -y ffmpeg
        ;;
      apk)
        as_root apk add ffmpeg
        ;;
      *)
        die "No supported package manager. Install ffmpeg manually: https://ffmpeg.org/download.html"
        ;;
    esac
    ;;

  windows)
    # gyan.dev essentials builds include libass and freetype.
    # Download pre-built ffmpeg from gyan.dev (essentials zip — no 7z needed)
    TMP_DIR=$(mktemp -d)
    trap 'rm -rf "$TMP_DIR"' EXIT
    curl -fsSL --retry 3 "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -o "$TMP_DIR/ffmpeg.zip"
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

if ! has_text_filters ffmpeg && ! { [[ -n $FULL ]] && has_text_filters "$FULL"; }; then
  warn "This ffmpeg lacks libass/freetype: caption burning (ass, subtitles) and drawtext will fail."
fi

info "ffmpeg installed successfully."

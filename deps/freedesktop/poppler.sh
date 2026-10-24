#!/usr/bin/env bash
# dep: freedesktop/poppler
# type: dep
# description: poppler-utils - pdftotext, pdfinfo, and pdffonts for checking a PDF's pages, fonts, and text layer
# check: pdftotext
# https://poppler.freedesktop.org

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Windows: prebuilt poppler from the conda-forge-based poppler-windows release, pinned.
WIN_RELEASE="v26.09.0-0"
WIN_SHA="7a6f256a0ddf7536182246a5733331bf4677cbcc34f4663774947ad34556c8d0"

sha256_of() {
  if pkg_check sha256sum; then
    sha256sum "$1" | cut -d' ' -f1
  else
    shasum -a 256 "$1" | cut -d' ' -f1
  fi
}

install_windows() {
  local tmp bin
  tmp="$(mktemp -d)"
  curl -fsSL --retry 3 -o "$tmp/poppler.zip" \
    "https://github.com/oschwartz10612/poppler-windows/releases/download/${WIN_RELEASE}/Release-${WIN_RELEASE#v}.zip"
  [[ "$(sha256_of "$tmp/poppler.zip")" == "$WIN_SHA" ]] || die "poppler download failed its checksum"
  unzip -qo "$tmp/poppler.zip" -d "$tmp"
  bin="$(dirname "$(find "$tmp" -name pdftotext.exe | head -1)")"
  [[ -d $bin ]] || die "pdftotext.exe not found in the poppler archive"
  # The tools need the DLLs next to them.
  mkdir -p "$HOME/.local/bin"
  cp "$bin"/*.exe "$bin"/*.dll "$HOME/.local/bin/"
  rm -rf "$tmp"
  export PATH="$HOME/.local/bin:$PATH"
}

# Fast path — already installed
if pkg_check pdftotext && pkg_check pdfinfo; then
  exit 0
fi

info "poppler utilities not found — installing..."
case "$PKG_MANAGER" in
  brew) brew install poppler ;;
  apt) apt_install poppler-utils ;;
  dnf) dnf_install poppler-utils ;;
  pacman) as_root pacman -S --noconfirm poppler ;;
  zypper) as_root zypper --non-interactive install poppler-tools ;;
  apk) as_root apk add --no-cache poppler-utils ;;
  *)
    if [[ $OS == "windows" ]]; then
      install_windows
    else
      die "Install poppler-utils (pdftotext, pdfinfo, pdffonts) with your package manager: https://poppler.freedesktop.org"
    fi
    ;;
esac

if ! pkg_check pdftotext; then
  die "poppler installed but pdftotext is not in PATH"
fi

info "poppler utilities installed successfully."

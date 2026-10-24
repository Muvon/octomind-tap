#!/usr/bin/env bash
# dep: freedesktop/poppler
# type: dep
# description: poppler-utils - pdftotext, pdfinfo, and pdffonts for checking a PDF's pages, fonts, and text layer
# check: pdftotext
# https://poppler.freedesktop.org

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

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
    die "Install poppler-utils (pdftotext, pdfinfo, pdffonts) with your package manager: https://poppler.freedesktop.org"
    ;;
esac

if ! pkg_check pdftotext; then
  die "poppler installed but pdftotext is not in PATH"
fi

info "poppler utilities installed successfully."

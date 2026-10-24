#!/usr/bin/env bash
# dep: muvon/office-fonts
# type: dep
# description: office-fonts - Carlito, Caladea, and Liberation fonts, metric-compatible with Calibri, Cambria, Arial, Times New Roman, and Courier New
# check: fc-list
# https://github.com/liberationfonts/liberation-fonts

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# A document set in Calibri or Times New Roman keeps its line breaks and page count when it
# renders with a metric-compatible clone: Typst PDFs and LibreOffice page counts use these.
FONT_DIRS=(/usr/share/fonts /usr/local/share/fonts "$HOME/.local/share/fonts" "$HOME/.fonts"
  "$HOME/Library/Fonts" /Library/Fonts /System/Library/Fonts)

has_font() {
  local dir
  for dir in "${FONT_DIRS[@]}"; do
    [[ -d $dir ]] && [[ -n "$(find "$dir" -iname "$1" -print -quit 2>/dev/null)" ]] && return 0
  done
  return 1
}

fonts_ok() {
  has_font 'Carlito-Regular.ttf' && { has_font 'LiberationSerif-Regular.ttf' || has_font 'Times New Roman.ttf'; }
}

# Windows ships the original fonts.
if [[ $OS == "windows" ]] || fonts_ok; then
  exit 0
fi

info "Installing metric-compatible office fonts..."
case "$PKG_MANAGER" in
  # macOS ships Arial, Times New Roman, and Courier New; Calibri and Cambria come only with Office.
  brew) brew install --cask font-carlito font-caladea ;;
  apt) as_root apt-get install -y fonts-crosextra-carlito fonts-crosextra-caladea fonts-liberation ;;
  dnf) as_root dnf install -y google-carlito-fonts google-crosextra-caladea-fonts liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts ;;
  pacman) as_root pacman -S --noconfirm ttf-carlito ttf-caladea ttf-liberation ;;
  zypper) as_root zypper --non-interactive install google-carlito-fonts google-caladea-fonts liberation-fonts ;;
  apk) as_root apk add --no-cache font-carlito font-liberation ;;
  *) die "Install the Carlito, Caladea, and Liberation fonts with your package manager." ;;
esac

if ! fonts_ok; then
  die "office fonts installed but Carlito or Liberation Serif was not found in the font directories"
fi

info "office fonts installed."

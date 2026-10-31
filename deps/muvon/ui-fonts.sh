#!/usr/bin/env bash
# dep: muvon/ui-fonts
# type: dep
# description: ui-fonts - Inter and JetBrains Mono variable fonts for rendered cards, previews, and UI mockups
# check: test -s "${OCTOMIND_FONTS_DIR:-$HOME/.local/share/octomind/fonts}/Inter.ttf"
# https://github.com/google/fonts

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Renderers that load fonts explicitly (no system fonts) default to this directory, so output is
# identical on every machine.
FONTS_DIR="${OCTOMIND_FONTS_DIR:-$HOME/.local/share/octomind/fonts}"

# Pinned google/fonts commit + SHA-256 per file: a repository change can never alter what users get.
# Entries are "<url-encoded path> <sha256> <installed name>"; curl globs on raw [ ].
COMMIT="e7db6ca603fd4862010383ff17ffd6cc4ffac1c0"
FONTS=(
  "ofl/inter/Inter%5Bopsz,wght%5D.ttf 29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031 Inter.ttf"
  "ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf 48715a42ec242c21e9f02692891e147d022299a52e48d5e413e1a942193ffeda JetBrainsMono.ttf"
)

# Fast path — every font already present
missing=0
for entry in "${FONTS[@]}"; do
  [[ -s "$FONTS_DIR/${entry##* }" ]] || missing=1
done
if [[ $missing -eq 0 ]]; then
  exit 0
fi

sha256_of() {
  if pkg_check sha256sum; then
    sha256sum "$1" | cut -d' ' -f1
  elif pkg_check shasum; then
    shasum -a 256 "$1" | cut -d' ' -f1
  else
    die "Neither sha256sum nor shasum found — cannot verify font downloads."
  fi
}

fetch() {
  if pkg_check curl; then
    curl -fsSL --retry 2 -o "$2" "$1"
  elif pkg_check wget; then
    wget -q -O "$2" "$1"
  else
    die "Neither curl nor wget found. Install one: macOS ships curl; Linux: apt/dnf/pacman install curl"
  fi
}

mkdir -p "$FONTS_DIR"
for entry in "${FONTS[@]}"; do
  read -r path want name <<<"$entry"
  dest="$FONTS_DIR/$name"
  [[ -s $dest ]] && continue
  tmp="$(mktemp)"
  info "Downloading $name..."
  fetch "https://raw.githubusercontent.com/google/fonts/${COMMIT}/${path}" "$tmp"
  got="$(sha256_of "$tmp")"
  if [[ $got != "$want" ]]; then
    rm -f "$tmp"
    die "Checksum mismatch for $name (got $got)"
  fi
  mv "$tmp" "$dest"
  chmod 644 "$dest"
done

if [[ ! -s "$FONTS_DIR/Inter.ttf" ]]; then
  die "Font install incomplete in $FONTS_DIR"
fi

info "UI fonts installed in $FONTS_DIR"

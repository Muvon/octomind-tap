#!/usr/bin/env bash
# dep: muvon/video-fonts
# type: dep
# description: video-fonts - heavy display fonts (Poppins, Anton, Bebas Neue, Archivo Black) for burned-in captions and thumbnails
# check: test -s "${OCTOMIND_FONTS_DIR:-$HOME/.local/share/octomind/fonts}/Poppins-Black.ttf"
# https://github.com/google/fonts

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# The caption and thumbnail renderers default to this directory (libass `fontsdir`), so the
# styles render with the intended typeface instead of a silent fallback.
FONTS_DIR="${OCTOMIND_FONTS_DIR:-$HOME/.local/share/octomind/fonts}"

# Pinned google/fonts commit + SHA-256 per file: a repository change can never alter what users get.
COMMIT="e7db6ca603fd4862010383ff17ffd6cc4ffac1c0"
FONTS=(
  "ofl/poppins/Poppins-Black.ttf d82aaaf98a9283f9a8edd24e51173337d8eaf09e25cd3d98831f8ec8461748a1"
  "ofl/poppins/Poppins-ExtraBold.ttf f2ab17c1a63a0ecc12c2461848fc8a469395e3cd2d641803e889c643d9f958e1"
  "ofl/anton/Anton-Regular.ttf a4ba3a92350ebb031da0cb47630ac49eb265082ca1bc0450442f4a83ab947cab"
  "ofl/bebasneue/BebasNeue-Regular.ttf 08e4623805102d819f58601e46e345648846075e363b2ceb23313c2d1c83ec73"
  "ofl/archivoblack/ArchivoBlack-Regular.ttf dd9a89a019b4849f66ab75455fe7bdf931311042cbb0f0f97acc061539703180"
)

# Fast path — every font already present
missing=0
for entry in "${FONTS[@]}"; do
  [[ -s "$FONTS_DIR/$(basename "${entry%% *}")" ]] || missing=1
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
  path="${entry%% *}"
  want="${entry##* }"
  name="$(basename "$path")"
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

if [[ ! -s "$FONTS_DIR/Poppins-Black.ttf" ]]; then
  die "Font install incomplete in $FONTS_DIR"
fi

info "video fonts installed in $FONTS_DIR"

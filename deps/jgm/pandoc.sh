#!/usr/bin/env bash
# dep: jgm/pandoc
# type: dep
# description: pandoc - universal document converter for Markdown to Word (DOCX) and, with the Typst engine, to PDF
# check: pandoc
# https://pandoc.org

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Release tarball pinned for Linux, where distro packages can predate the Typst PDF engine (3.1.2+).
VERSION="3.12.1"
SHA_AMD64="d0c90410e90204c9ca83b8539fac5c7aed01fd537207e4585849f8abc5df20b8"
SHA_ARM64="445d96fd08801fe636cab1158b4f017ee320ac3b7446328b4fe2f902117b19b9"

pandoc_ok() {
  pkg_check pandoc || return 1
  local v
  v="$(pandoc --version 2>/dev/null | sed -n '1s/^pandoc[^0-9]*\([0-9.]*\).*/\1/p')"
  [[ -n $v ]] || return 1
  [[ "$(printf '%s\n%s\n' "3.1.2" "$v" | sort -V | head -1)" == "3.1.2" ]]
}

# Fast path — a pandoc new enough for --pdf-engine=typst
if pandoc_ok; then
  exit 0
fi

sha256_of() {
  if pkg_check sha256sum; then
    sha256sum "$1" | cut -d' ' -f1
  else
    shasum -a 256 "$1" | cut -d' ' -f1
  fi
}

install_release() {
  local arch sha tmp
  if [[ $IS_ARM64 == "1" ]]; then
    arch="arm64"
    sha="$SHA_ARM64"
  elif [[ $IS_X86_64 == "1" ]]; then
    arch="amd64"
    sha="$SHA_AMD64"
  else
    die "No pandoc build for $ARCH. Install pandoc 3.1.2+ manually: https://pandoc.org/installing.html"
  fi
  pkg_check curl || die "curl not found. Install curl first, then re-run."
  tmp="$(mktemp -d)"
  curl -fsSL --retry 3 -o "$tmp/pandoc.tar.gz" \
    "https://github.com/jgm/pandoc/releases/download/${VERSION}/pandoc-${VERSION}-linux-${arch}.tar.gz"
  [[ "$(sha256_of "$tmp/pandoc.tar.gz")" == "$sha" ]] || die "pandoc download failed its checksum"
  mkdir -p "$HOME/.local/opt" "$HOME/.local/bin"
  tar -xzf "$tmp/pandoc.tar.gz" -C "$HOME/.local/opt"
  ln -sf "$HOME/.local/opt/pandoc-${VERSION}/bin/pandoc" "$HOME/.local/bin/pandoc"
  rm -rf "$tmp"
  export PATH="$HOME/.local/bin:$PATH"
}

info "pandoc 3.1.2+ not found — installing..."
case "$OS" in
  macos)
    if pkg_check brew; then
      if brew list pandoc >/dev/null 2>&1; then
        brew upgrade pandoc
      else
        brew install pandoc
      fi
    else
      die "brew not found. Install Homebrew (https://brew.sh) or pandoc from https://pandoc.org/installing.html"
    fi
    ;;
  linux)
    install_release
    ;;
  *)
    die "Unsupported OS. Install pandoc manually: https://pandoc.org/installing.html"
    ;;
esac

if ! pandoc_ok; then
  die "pandoc installed but an older one is first on PATH, or ~/.local/bin is missing from PATH"
fi

info "pandoc $(pandoc --version | head -1 | cut -d' ' -f2) installed."

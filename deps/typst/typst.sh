#!/usr/bin/env bash
# dep: typst/typst
# type: dep
# description: typst - fast typesetting engine; pandoc's PDF engine for clean PDFs without LaTeX
# check: typst
# https://typst.app

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Release binary pinned for Linux (static musl builds).
VERSION="0.15.1"
SHA_X86_64="a6d077d0a95eed5a2eba715b2dae06be954f624ccbf85758a03f389ded33118c"
SHA_AARCH64="5aa8d74a3d906e60ea12a66ac2f37f8eef1b14cbad7182a745e393a10c23dcee"

# Fast path — already installed
if pkg_check typst; then
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
  local triple sha tmp
  if [[ $IS_ARM64 == "1" ]]; then
    triple="aarch64-unknown-linux-musl"
    sha="$SHA_AARCH64"
  elif [[ $IS_X86_64 == "1" ]]; then
    triple="x86_64-unknown-linux-musl"
    sha="$SHA_X86_64"
  else
    die "No typst build for $ARCH. Install typst manually: https://github.com/typst/typst#installation"
  fi
  pkg_check curl || die "curl not found. Install curl first, then re-run."
  pkg_check xz || warn "xz not found; unpacking typst may fail (install xz-utils)"
  tmp="$(mktemp -d)"
  curl -fsSL --retry 3 -o "$tmp/typst.tar.xz" \
    "https://github.com/typst/typst/releases/download/v${VERSION}/typst-${triple}.tar.xz"
  [[ "$(sha256_of "$tmp/typst.tar.xz")" == "$sha" ]] || die "typst download failed its checksum"
  tar -xJf "$tmp/typst.tar.xz" -C "$tmp"
  mkdir -p "$HOME/.local/bin"
  install -m 755 "$tmp/typst-${triple}/typst" "$HOME/.local/bin/typst"
  rm -rf "$tmp"
  export PATH="$HOME/.local/bin:$PATH"
}

info "typst not found — installing..."
case "$OS" in
  macos)
    if pkg_check brew; then
      brew install typst
    else
      die "brew not found. Install Homebrew (https://brew.sh) or typst from https://github.com/typst/typst/releases"
    fi
    ;;
  linux)
    install_release
    ;;
  *)
    die "Unsupported OS. Install typst manually: https://github.com/typst/typst#installation"
    ;;
esac

if ! pkg_check typst; then
  die "typst installed but not in PATH. Add ~/.local/bin to PATH."
fi

info "typst installed successfully."

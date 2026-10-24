#!/usr/bin/env bash
# dep: typst/typst
# type: dep
# description: typst - fast typesetting engine and LaTeX alternative; pandoc's PDF engine for clean PDFs
# check: typst
# https://typst.app

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Release archives pinned for Linux (static musl builds) and Windows.
VERSION="0.15.1"
SHA_X86_64="a6d077d0a95eed5a2eba715b2dae06be954f624ccbf85758a03f389ded33118c"
SHA_AARCH64="5aa8d74a3d906e60ea12a66ac2f37f8eef1b14cbad7182a745e393a10c23dcee"
SHA_WIN_X86_64="19ce3551153c2fe7ee9fa2f95208310c8f4d3209fedb699e0333faf8913f6736"
SHA_WIN_AARCH64="4ab28e1b71ec3184d38d580ab797f499b6770d952b6b19167be5cea5c2662e14"

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
  if ! pkg_check xz; then
    case "$PKG_MANAGER" in
      apt) apt_install xz-utils ;;
      dnf) dnf_install xz ;;
      pacman) as_root pacman -S --noconfirm xz ;;
      zypper) as_root zypper --non-interactive install xz ;;
      apk) as_root apk add --no-cache xz ;;
    esac
  fi
  pkg_check xz || die "xz not found; install xz-utils to unpack typst"
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

install_windows() {
  local triple sha tmp
  if [[ $IS_ARM64 == "1" ]]; then
    triple="aarch64-pc-windows-msvc"
    sha="$SHA_WIN_AARCH64"
  else
    triple="x86_64-pc-windows-msvc"
    sha="$SHA_WIN_X86_64"
  fi
  tmp="$(mktemp -d)"
  curl -fsSL --retry 3 -o "$tmp/typst.zip" \
    "https://github.com/typst/typst/releases/download/v${VERSION}/typst-${triple}.zip"
  [[ "$(sha256_of "$tmp/typst.zip")" == "$sha" ]] || die "typst download failed its checksum"
  unzip -qo "$tmp/typst.zip" -d "$tmp"
  mkdir -p "$HOME/.local/bin"
  cp "$tmp/typst-${triple}/typst.exe" "$HOME/.local/bin/typst.exe"
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
  windows)
    install_windows
    ;;
  *)
    die "Unsupported OS. Install typst manually: https://github.com/typst/typst#installation"
    ;;
esac

if ! pkg_check typst; then
  die "typst installed but not in PATH. Add ~/.local/bin to PATH."
fi

info "typst installed successfully."

#!/usr/bin/env bash
# dep: muvon/octofs
# type: dep
# description: octofs - Muvon command-line tool for viewing and editing files; installed from GitHub releases or the muvon/tap Homebrew formula
# check: octofs
# https://github.com/muvon/octofs

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Structural code search (view outline, symbol and AST modes) needs this release.
MIN_VERSION="0.25.0"

octofs_ok() {
  pkg_check octofs || return 1
  local v
  v="$(octofs --version 2>/dev/null | sed -n '1s/^octofs[^0-9]*\([0-9.]*\).*/\1/p')"
  [[ -n $v ]] || return 1
  [[ "$(printf '%s\n%s\n' "$MIN_VERSION" "$v" | sort -V | head -1)" == "$MIN_VERSION" ]]
}

# Fast path — an octofs new enough for structural code search
if octofs_ok; then
  exit 0
fi

REPO="Muvon/octofs"
BINARY="octofs"
INSTALL_DIR="${HOME}/.local/bin"

info "octofs missing or older than $MIN_VERSION — installing the latest release..."

# On macOS, prefer Homebrew if available
if [[ $OS == "macos" ]] && pkg_check brew; then
  if brew list --formula octofs >/dev/null 2>&1; then
    brew upgrade muvon/tap/octofs
  else
    brew install muvon/tap/octofs
  fi
  octofs_ok || die "octofs $MIN_VERSION+ not found in PATH after brew; remove older octofs binaries that shadow it"
  exit 0
fi

# Determine target triple and archive format
ARCHIVE_EXT="tar.gz"
case "$OS-$ARCH" in
  linux-x86_64) TARGET="x86_64-unknown-linux-musl" ;;
  linux-arm64) TARGET="aarch64-unknown-linux-musl" ;;
  macos-x86_64) TARGET="x86_64-apple-darwin" ;;
  macos-arm64) TARGET="aarch64-apple-darwin" ;;
  windows-x86_64)
    TARGET="x86_64-pc-windows-msvc"
    ARCHIVE_EXT="zip"
    ;;
  windows-arm64)
    TARGET="aarch64-pc-windows-msvc"
    ARCHIVE_EXT="zip"
    ;;
  *) die "Unsupported platform: $OS-$ARCH" ;;
esac

# Get latest version
VERSION=$(curl -fsSL "https://api.github.com/repos/$REPO/releases" | grep '"tag_name":' | head -1 | sed -E 's/.*"([^"]+)".*/\1/')
if [[ -z $VERSION ]]; then
  die "Failed to get latest version from GitHub"
fi

# Download and extract
TMP_DIR=$(mktemp -d)
trap "rm -rf '$TMP_DIR'" EXIT

FILENAME="${BINARY}-${VERSION}-${TARGET}.${ARCHIVE_EXT}"
URL="https://github.com/$REPO/releases/download/$VERSION/$FILENAME"

info "Downloading $BINARY $VERSION for $TARGET..."
curl -fsSL "$URL" -o "$TMP_DIR/$FILENAME"

if [[ $ARCHIVE_EXT == "zip" ]]; then
  unzip -qo "$TMP_DIR/$FILENAME" -d "$TMP_DIR"
else
  tar xzf "$TMP_DIR/$FILENAME" -C "$TMP_DIR"
fi

# Install
mkdir -p "$INSTALL_DIR"
if [[ $OS == "windows" ]]; then
  cp "$TMP_DIR/${BINARY}.exe" "$INSTALL_DIR/${BINARY}.exe"
else
  cp "$TMP_DIR/$BINARY" "$INSTALL_DIR/$BINARY"
  chmod +x "$INSTALL_DIR/$BINARY"
fi

export PATH="$INSTALL_DIR:$PATH"
octofs_ok || die "octofs $MIN_VERSION+ not found after install; add $INSTALL_DIR to PATH ahead of older octofs binaries"
info "octofs $VERSION installed to $INSTALL_DIR"

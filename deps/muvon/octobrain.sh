#!/usr/bin/env bash
# dep: muvon/octobrain
# type: dep
# description: Installs the octobrain CLI (memory and knowledge tool by Muvon)
# check: octobrain
# https://github.com/muvon/octobrain

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check octobrain; then
  exit 0
fi

REPO="Muvon/octobrain"
BINARY="octobrain"
INSTALL_DIR="${HOME}/.local/bin"

info "octobrain not found — installing from GitHub releases..."

# On macOS, prefer Homebrew if available
if [[ $OS == "macos" ]] && pkg_check brew; then
  brew install muvon/tap/octobrain
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

info "octobrain $VERSION installed to $INSTALL_DIR"

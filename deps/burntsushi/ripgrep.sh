#!/usr/bin/env bash
# dep: burntsushi/ripgrep
# type: dep
# description: ripgrep (rg) — fast recursive search tool
# check: rg
# https://github.com/BurntSushi/ripgrep

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check rg; then
  exit 0
fi

info "ripgrep not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install ripgrep
    else
      cargo install ripgrep
    fi
    ;;
  linux)
    pkg_install ripgrep
    ;;
  windows)
    # Download pre-built binary from GitHub
    VERSION=$(curl -fsSL "https://api.github.com/repos/BurntSushi/ripgrep/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    TMP_DIR=$(mktemp -d)
    trap "rm -rf '$TMP_DIR'" EXIT
    FILENAME="ripgrep-${VERSION}-x86_64-pc-windows-msvc.zip"
    curl -fsSL "https://github.com/BurntSushi/ripgrep/releases/download/${VERSION}/${FILENAME}" -o "$TMP_DIR/$FILENAME"
    unzip -qo "$TMP_DIR/$FILENAME" -d "$TMP_DIR"
    mkdir -p "${HOME}/.local/bin"
    cp "$TMP_DIR/ripgrep-${VERSION}-x86_64-pc-windows-msvc/rg.exe" "${HOME}/.local/bin/rg.exe"
    export PATH="${HOME}/.local/bin:$PATH"
    ;;
esac

if ! pkg_check rg; then
  die "ripgrep installed but 'rg' not in PATH. You may need to restart your shell."
fi

info "ripgrep installed successfully."

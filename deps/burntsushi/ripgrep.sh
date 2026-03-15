#!/usr/bin/env bash
# dep: burntsushi/ripgrep
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
esac

if ! pkg_check rg; then
  die "ripgrep installed but 'rg' not in PATH. You may need to restart your shell."
fi

info "ripgrep installed successfully."

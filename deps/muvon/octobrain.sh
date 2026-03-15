#!/usr/bin/env bash
# dep: muvon/octobrain
# description: Installs the octobrain CLI (code indexing and search tool by Muvon)
# check: octobrain
# https://github.com/muvon/octobrain

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check octobrain; then
  exit 0
fi

# Ensure cargo is available
install_dep rust/cargo

info "octobrain not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install muvon/tap/octobrain
    else
      cargo install octobrain
    fi
    ;;
  linux)
    cargo install octobrain
    ;;
esac

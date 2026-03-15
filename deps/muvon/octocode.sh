#!/usr/bin/env bash
# dep: muvon/octocode
# description: Installs the octocode CLI (code indexing and search tool by Muvon)
# check: octocode
# https://github.com/muvon/octocode

set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/lib/platform.sh"

# Fast path — already installed
if pkg_check octocode; then
  exit 0
fi

# Ensure cargo is available
install_dep rust/cargo

info "octocode not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install muvon/tap/octocode
    else
      cargo install octocode
    fi
    ;;
  linux)
    cargo install octocode
    ;;
esac

#!/usr/bin/env bash
# dep: muvon/octobrain
# description: Installs the octobrain CLI (code indexing and search tool by Muvon)
# check: octobrain
# https://github.com/muvon/octobrain

set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/lib/platform.sh"

# Fast path — already installed
if pkg_check octobrain; then
  exit 0
fi

info "octobrain not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install muvon/tap/octobrain
    elif pkg_check cargo; then
      cargo install octobrain
    else
      die "Neither brew nor cargo found. Install one of them first, then re-run."
    fi
    ;;
  linux)
    if pkg_check cargo; then
      cargo install octobrain
    else
      die "cargo not found. Install Rust first: https://rustup.rs — then re-run."
    fi
    ;;
esac

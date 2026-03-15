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

info "octocode not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install muvon/tap/octocode
    elif pkg_check cargo; then
      cargo install octocode
    else
      die "Neither brew nor cargo found. Install one of them first, then re-run."
    fi
    ;;
  linux)
    if pkg_check cargo; then
      cargo install octocode
    else
      die "cargo not found. Install Rust first: https://rustup.rs — then re-run."
    fi
    ;;
esac

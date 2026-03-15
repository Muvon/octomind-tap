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

# Ensure cargo is available — sourced so PATH changes propagate to this shell
# shellcheck source=/dev/null
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/rust/cargo.sh"

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

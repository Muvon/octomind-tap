#!/usr/bin/env bash
# dep: ast-grep/ast-grep
# description: ast-grep (sg) — structural code search and rewrite tool
# check: sg
# https://ast-grep.github.io

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check sg; then
  exit 0
fi

info "ast-grep not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install ast-grep
    else
      cargo install ast-grep --locked
    fi
    ;;
  linux)
    if pkg_check npm; then
      npm install -g @ast-grep/cli
    else
      cargo install ast-grep --locked
    fi
    ;;
esac

if ! pkg_check sg; then
  die "ast-grep installed but 'sg' not in PATH. You may need to restart your shell."
fi

info "ast-grep installed successfully."

#!/usr/bin/env bash
# dep: readwise/readwise
# type: mcp
# description: Readwise MCP Server — reading highlights, books, and document access
# check: npx
# https://github.com/IAmAlexander/readwise-mcp

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Readwise MCP Server requires Node.js — already available via npx"

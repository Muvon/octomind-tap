#!/usr/bin/env bash
# dep: readwise/readwise
# type: mcp
# description: Readwise MCP Server - search your Readwise reading highlights; browse saved books, articles and documents, npx, needs READWISE_API_KEY
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

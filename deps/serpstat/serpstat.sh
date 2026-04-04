#!/usr/bin/env bash
# dep: serpstat/serpstat
# type: mcp
# description: Serpstat MCP Server — SERP tracking, backlinks, domain authority
# check: npx
# https://www.npmjs.com/package/@serpstat/serpstat-mcp-server

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — npx is available (node is installed)
if pkg_check npx; then
  exit 0
fi

# Ensure node is available
install_dep nodejs/node

info "Serpstat MCP Server requires Node.js — already available via npx"

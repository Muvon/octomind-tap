#!/usr/bin/env bash
# dep: modelcontextprotocol/postgres
# type: mcp
# description: MCP PostgreSQL Server — query PostgreSQL databases
# check: npx
# https://github.com/modelcontextprotocol/servers/tree/main/src/postgres

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

info "PostgreSQL MCP Server requires Node.js — already available via npx"

#!/usr/bin/env bash
# dep: modelcontextprotocol/sqlite
# type: mcp
# description: MCP SQLite Server — query SQLite databases
# check: uvx
# https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — npx is available (node is installed)
if pkg_check uvx; then
  exit 0
fi

# Ensure node is available
install_dep astral-sh/uv

info "SQLite MCP Server requires uv/uvx — already available"

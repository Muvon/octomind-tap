#!/usr/bin/env bash
# dep: modelcontextprotocol/filesystem
# description: MCP Filesystem Server — secure file operations (read, write, search)
# check: npx
# https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

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

info "Filesystem MCP Server requires Node.js — already available via npx"

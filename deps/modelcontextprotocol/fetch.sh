#!/usr/bin/env bash
# dep: modelcontextprotocol/fetch
# type: mcp
# description: Fetch MCP Server — retrieve web content and convert to markdown
# check: npx
# https://github.com/modelcontextprotocol/servers/tree/main/src/fetch

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Fetch MCP Server requires Node.js — already available via npx"

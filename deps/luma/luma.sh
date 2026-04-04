#!/usr/bin/env bash
# dep: luma/luma
# type: mcp
# description: Luma AI MCP Server — video generation, Dream Machine
# check: npx
# https://mcpservers.org/servers/wheattoast11/mcp-video-gen

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

info "Luma AI MCP Server requires Node.js — already available via npx"

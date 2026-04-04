#!/usr/bin/env bash
# dep: mcpware/instagram
# description: Instagram MCP Server — posts, comments, DMs, stories via Graph API
# check: npx
# https://www.npmjs.com/package/@mcpware/instagram-mcp

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Instagram MCP Server requires Node.js — already available via npx"

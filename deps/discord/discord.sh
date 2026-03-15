#!/usr/bin/env bash
# dep: discord/discord
# description: Discord MCP Server — Discord bot integration, messaging, moderation
# check: npx
# https://www.npmjs.com/package/mcp-discord

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

info "Discord MCP Server requires Node.js — already available via npx"

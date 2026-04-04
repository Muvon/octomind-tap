#!/usr/bin/env bash
# dep: modelcontextprotocol/slack
# type: mcp
# description: MCP Slack Server — interact with Slack workspaces (channels, messages, users)
# check: npx
# https://github.com/modelcontextprotocol/servers/tree/main/src/slack

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

info "Slack MCP Server requires Node.js — already available via npx"

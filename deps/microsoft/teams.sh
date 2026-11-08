#!/usr/bin/env bash
# dep: microsoft/teams
# type: mcp
# description: Microsoft Teams MCP Server - send messages and manage chats; search conversations in Teams channels, runs with npx, signs in via Microsoft Graph OAuth
# check: npx
# https://www.npmjs.com/package/teams-mcp

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

info "Microsoft Teams MCP Server requires Node.js — already available via npx"

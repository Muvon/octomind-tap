#!/usr/bin/env bash
# dep: zendesk/zendesk
# type: mcp
# description: Zendesk MCP Server - manage tickets, users and organizations; macros, triggers and Help Center articles via npx, needs subdomain, email and API token
# check: npx
# https://github.com/mattcoatsworth/zendesk-mcp-server

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

info "Zendesk MCP Server requires Node.js — already available via npx"

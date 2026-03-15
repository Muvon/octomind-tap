#!/usr/bin/env bash
# dep: auth0/auth0
# description: Auth0 MCP Server — authentication and identity
# check: npx
# https://www.npmjs.com/package/@auth0/auth0-mcp-server

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

info "Auth0 MCP Server requires Node.js — already available via npx"

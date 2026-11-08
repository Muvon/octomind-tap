#!/usr/bin/env bash
# dep: mongodb/mongodb
# type: mcp
# description: MongoDB MCP Server - manage Atlas clusters and collections; runs queries on databases, set MDB_MCP_CONNECTION_STRING or Atlas API credentials
# check: npx
# https://www.npmjs.com/package/@mongodb-js/mongodb-mcp-server

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

info "MongoDB MCP Server requires Node.js — already available via npx"

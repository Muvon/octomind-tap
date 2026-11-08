#!/usr/bin/env bash
# dep: google/drive
# type: mcp
# description: Google Drive MCP Server - search, read and manage Drive files; through @dguido/google-drive-mcp on npx, signs in with OAuth 2.0
# check: npx
# https://www.npmjs.com/package/@dguido/google-drive-mcp

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

info "Google Drive MCP Server requires Node.js — already available via npx"

#!/usr/bin/env bash
# dep: iflow-mcp/whatsapp
# type: mcp
# description: MCP WhatsApp Server - send WhatsApp Web messages and share media; also manages contacts, sign in once by scanning a QR code, runs with npx
# check: npx
# https://www.npmjs.com/package/@iflow-mcp/mcp-whatsapp-web

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

info "WhatsApp MCP Server requires Node.js — already available via npx"

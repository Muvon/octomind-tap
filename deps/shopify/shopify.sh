#!/usr/bin/env bash
# dep: shopify/shopify
# type: mcp
# description: Shopify Admin MCP Server - products, collections, inventory, customers, orders, and discounts via the Admin API
# check: npx
# https://github.com/acoderacom/shopify-admin-mcp

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# The server targets Node.js 22.12+.
node_ok() {
  pkg_check npx && node -e 'const [a,b]=process.versions.node.split(".").map(Number); process.exit(a>22||(a===22&&b>=12)?0:1)' 2>/dev/null
}

# Fast path
if node_ok; then
  exit 0
fi

if ! pkg_check npx; then
  install_dep nodejs/node
fi

if ! node_ok; then
  warn "Shopify Admin MCP expects Node.js 22.12+; found $(node -v 2>/dev/null || echo none). Upgrade Node.js if the server fails to start."
fi

#!/usr/bin/env bash
# dep: shopify/dev-mcp
# type: mcp
# description: Shopify Dev MCP - official Shopify docs, GraphQL schema, and code validation server
# check: npx
# https://shopify.dev/docs/apps/build/devmcp

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — npx is available (node is installed); the capability pins the package version
if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

if ! pkg_check npx; then
  die "npx not found after installing Node.js"
fi

info "Shopify Dev MCP runs via npx"

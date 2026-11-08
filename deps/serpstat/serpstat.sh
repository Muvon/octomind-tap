#!/usr/bin/env bash
# dep: serpstat/serpstat
# type: mcp
# description: Serpstat MCP Server - SEO keyword and backlink research data; domain and competitor reports via npx, needs an API token, calls may use credits
# check: npx
# https://www.npmjs.com/package/@serpstat/serpstat-mcp-server

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

info "Serpstat MCP Server requires Node.js — already available via npx"

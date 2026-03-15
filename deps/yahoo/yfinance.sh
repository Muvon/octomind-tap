#!/usr/bin/env bash
# dep: yahoo/yfinance
# description: Yahoo Finance MCP Server — stock prices, historical data, charts
# check: npx
# https://www.npmjs.com/package/@szemeng76/yfinance-mcp-server

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

info "Yahoo Finance MCP Server requires Node.js — already available via npx"

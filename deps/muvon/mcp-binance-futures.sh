#!/usr/bin/env bash
# dep: muvon/mcp-binance-futures
# type: mcp
# description: Binance USDT-M Futures MCP Server — market data, orders, positions, margin (requires uvx)
# check: uvx
# https://github.com/muvon/mcp-binance-futures

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — uvx is available (uv is installed)
if pkg_check uvx; then
  exit 0
fi

# Ensure uv is available (provides uvx)
install_dep astral-sh/uv

pkg_check uvx || die "uvx not found after installing uv"
info "Binance Futures MCP Server requires uv/uvx — now available"

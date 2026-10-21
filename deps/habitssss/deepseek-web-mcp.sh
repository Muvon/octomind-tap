#!/usr/bin/env bash
# dep: habitssss/deepseek-web-mcp
# type: mcp
# description: DeepSeek Web MCP Server - DeepSeek Search and Fetch APIs as MCP tools
# check: npx
# https://github.com/habitssss/deepseek-web-mcp

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

info "DeepSeek Web MCP Server requires Node.js — already available via npx"

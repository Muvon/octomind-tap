#!/usr/bin/env bash
# dep: dataforseo/mcp-server
# type: mcp
# description: Ensures Node.js 22+ and npx for the official DataForSEO MCP server
# check: npx
# https://github.com/dataforseo/mcp-server-typescript

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

node_ready() {
  pkg_check node && pkg_check npx &&
    (($(node -p 'process.versions.node.split(".")[0]') >= 22))
}

if node_ready; then exit 0; fi

NODE_MIN_MAJOR=22 install_dep nodejs/node

node_ready || die "DataForSEO MCP requires Node.js >= 22 and npx on PATH."

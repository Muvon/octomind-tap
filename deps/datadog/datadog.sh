#!/usr/bin/env bash
# dep: datadog/datadog
# type: mcp
# description: Datadog MCP Server — monitoring and observability
# check: npx
# https://www.npmjs.com/package/@winor30/mcp-server-datadog

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

info "Datadog MCP Server requires Node.js — already available via npx"

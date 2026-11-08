#!/usr/bin/env bash
# dep: n8n/n8n
# type: mcp
# description: n8n MCP Server - create and manage n8n workflows from an agent; also runs and audits them via npx, needs N8N_HOST and N8N_API_KEY
# check: npx
# https://www.npmjs.com/package/@makafeli/n8n-workflow-builder

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

info "n8n MCP Server requires Node.js — already available via npx"

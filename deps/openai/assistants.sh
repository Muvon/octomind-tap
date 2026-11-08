#!/usr/bin/env bash
# dep: openai/assistants
# type: mcp
# description: OpenAI Assistants MCP Server - call the Assistants API from MCP; runs with npx (openai-assistants-mcp) and needs an OPENAI_API_KEY
# check: npx
# https://www.npmjs.com/package/openai-assistants-mcp

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

info "OpenAI Assistants MCP Server requires Node.js — already available via npx"

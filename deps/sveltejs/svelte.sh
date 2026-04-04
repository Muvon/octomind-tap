#!/usr/bin/env bash
# dep: sveltejs/svelte
# type: mcp
# description: Svelte MCP Server — official Svelte/SvelteKit documentation and tooling
# check: npx
# https://github.com/sveltejs/ai-tools

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

info "Svelte MCP Server requires Node.js — already available via npx"

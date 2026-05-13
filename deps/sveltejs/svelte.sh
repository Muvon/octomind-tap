#!/usr/bin/env bash
# dep: sveltejs/svelte
# type: mcp
# description: Svelte MCP Server — runs @sveltejs/mcp via bunx
# check: bunx
# https://github.com/sveltejs/ai-tools

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — bunx is available
if pkg_check bunx; then
  exit 0
fi

# Ensure bun is available (provides bunx)
install_dep oven-sh/bun

info "Svelte MCP Server runs via 'bunx @sveltejs/mcp'."

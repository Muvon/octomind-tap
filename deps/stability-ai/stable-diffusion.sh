#!/usr/bin/env bash
# dep: stability-ai/stable-diffusion
# type: mcp
# description: Stability AI MCP Server - Stable Diffusion 3.5 generation, background removal, outpainting, and upscaling via the Stability API
# check: npx
# https://github.com/tadasant/mcp-server-stability-ai

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

info "Stability AI MCP Server runs via npx (Node.js)"

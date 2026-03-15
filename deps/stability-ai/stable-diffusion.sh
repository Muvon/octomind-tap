#!/usr/bin/env bash
# dep: stability-ai/stable-diffusion
# description: Stable Diffusion MCP Server — local image generation
# check: npx
# https://mcpservers.org/servers/Ichigo3766/image-gen-mcp

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

info "Stable Diffusion MCP Server requires Node.js — already available via npx"

#!/usr/bin/env bash
# dep: shinpr/mcp-image
# type: mcp
# description: mcp-image - image generation MCP server for OpenAI GPT Image 2.5 and Google Nano Banana, saving files to disk
# check: npx
# https://github.com/shinpr/mcp-image

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — npx is available (node is installed); the capability pins the package version
if pkg_check npx; then
  exit 0
fi

# Ensure node is available
install_dep nodejs/node

if ! pkg_check npx; then
  die "npx not found after installing Node.js"
fi

info "mcp-image runs via npx (Node.js 22+)"

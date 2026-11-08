#!/usr/bin/env bash
# dep: openai/dalle
# type: mcp
# description: DALL-E MCP Server - generate images from text prompts with DALL-E; uses OpenAI's generate_image tool, runs via npx, needs OPENAI_API_KEY
# check: npx
# https://www.npmjs.com/package/@microagents/mcp-server-dalle

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

info "DALL-E MCP Server requires Node.js — already available via npx"

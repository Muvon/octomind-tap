#!/usr/bin/env bash
# dep: google/veo
# type: mcp
# description: Google Veo MCP Server — text-to-video and image-to-video via Vertex AI / Gemini API
# check: npx
# https://ai.google.dev/gemini-api/docs/video

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — npx is available (node is installed)
if pkg_check npx; then
  exit 0
fi

# Ensure node is available (needed to run the community MCP server via npx)
install_dep nodejs/node

info "Google Veo MCP Server requires Node.js — already available via npx"

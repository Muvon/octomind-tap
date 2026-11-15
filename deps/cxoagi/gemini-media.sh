#!/usr/bin/env bash
# dep: cxoagi/gemini-media
# type: mcp
# description: Gemini Media MCP Server - Gemini Omni Flash video and Gemini image generation; community package launched through uvx, needs GEMINI_API_KEY
# check: uvx
# https://github.com/CxOAGI/gemini-media-mcp

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check uvx; then
  exit 0
fi

install_dep astral-sh/uv

info "Gemini Media MCP Server requires uv/uvx — already available"

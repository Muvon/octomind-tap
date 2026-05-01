#!/usr/bin/env bash
# dep: kling/kling
# type: mcp
# description: Kling AI MCP Server — text-to-video and image-to-video with strong motion physics
# check: npx
# https://app.klingai.com/global/dev/document-api/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Kling AI MCP Server requires Node.js — already available via npx"

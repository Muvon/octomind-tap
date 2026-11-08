#!/usr/bin/env bash
# dep: hedra/hedra
# type: mcp
# description: Hedra MCP Server - talking-character video from image and audio; Character-3 model, generate_video tool, runs with npx, needs HEDRA_API_KEY
# check: npx
# https://www.hedra.com/docs

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Hedra MCP Server requires Node.js — already available via npx"

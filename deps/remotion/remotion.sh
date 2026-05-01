#!/usr/bin/env bash
# dep: remotion/remotion
# type: mcp
# description: Remotion MCP Server — code-driven (React) video composition + Lambda render
# check: npx
# https://www.remotion.dev/docs/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Remotion MCP Server requires Node.js — already available via npx"

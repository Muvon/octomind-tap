#!/usr/bin/env bash
# dep: freepik/freepik
# type: mcp
# description: Freepik MCP Server — AI generation + stock images, vectors, video templates
# check: npx
# https://www.freepik.com/api

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Freepik MCP Server requires Node.js — already available via npx"

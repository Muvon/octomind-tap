#!/usr/bin/env bash
# dep: deepl/deepl
# type: mcp
# description: DeepL MCP Server — text and document translation via DeepL API
# check: npx
# https://github.com/DeepLcom/deepl-mcp-server

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "DeepL MCP Server requires Node.js — already available via npx"

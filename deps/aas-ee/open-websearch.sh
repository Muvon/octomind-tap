#!/usr/bin/env bash
# dep: aas-ee/open-websearch
# type: mcp
# description: Open-WebSearch MCP Server - keyless multi-engine web search (DuckDuckGo, Bing, Startpage, Brave)
# check: npx
# https://github.com/Aas-ee/open-webSearch

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# open-websearch needs Node.js >= 20 (crashes on 18: missing File global in
# undici); nodejs/node replaces an older or npx-less one.
install_dep nodejs/node

#!/usr/bin/env bash
# dep: aas-ee/open-websearch
# type: mcp
# description: Open-WebSearch MCP Server — keyless multi-engine web search (DuckDuckGo, Bing, Startpage, Brave)
# check: npx
# https://github.com/Aas-ee/open-webSearch

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Ensure node is available
if ! pkg_check node; then
  install_dep nodejs/node
fi

# open-websearch requires Node.js >= 20 (crashes on 18: missing File global in undici)
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
if ((NODE_MAJOR < 20)); then
  die "open-websearch requires Node.js >= 20 (found $(node -v)). Upgrade Node.js and re-run."
fi

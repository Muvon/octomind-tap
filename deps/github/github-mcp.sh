#!/usr/bin/env bash
# dep: github/github-mcp
# type: mcp
# description: GitHub MCP Server — full GitHub API operations (repos, issues, PRs, actions)
# check: npx
# https://github.com/github/github-mcp-server

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

info "GitHub MCP Server requires Node.js — already available via npx"

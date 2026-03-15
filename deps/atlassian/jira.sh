#!/usr/bin/env bash
# dep: atlassian/jira
# description: Jira MCP Server — issue tracking, projects, comments, workflows
# check: npx
# https://www.npmjs.com/package/@atlassian-dc-mcp/jira

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

info "Jira MCP Server requires Node.js — already available via npx"

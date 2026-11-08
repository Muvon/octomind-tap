#!/usr/bin/env bash
# dep: gitlab/gitlab
# type: mcp
# description: GitLab MCP Server - manage repositories and merge requests; also issues and CI/CD pipelines, run via npx with a Personal Access Token
# check: npx
# https://www.npmjs.com/package/@yoda.digital/gitlab-mcp-server

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

info "GitLab MCP Server requires Node.js — already available via npx"

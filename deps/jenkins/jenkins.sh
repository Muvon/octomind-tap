#!/usr/bin/env bash
# dep: jenkins/jenkins
# type: mcp
# description: Jenkins MCP Server - manage Jenkins jobs, builds and pipelines; also nodes and plugins, needs JENKINS_URL, JENKINS_USERNAME and JENKINS_API_TOKEN
# check: npx
# https://github.com/LokiMCPUniverse/jenkins-mcp-server

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

info "Jenkins MCP Server requires Node.js — already available via npx"

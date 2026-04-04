#!/usr/bin/env bash
# dep: containers/kubernetes
# type: mcp
# description: Kubernetes MCP Server — manage K8s clusters (pods, deployments, logs, helm)
# check: docker
# https://github.com/containers/kubernetes-mcp-server

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — docker is available
if pkg_check docker; then
  exit 0
fi

# Ensure docker is available
install_dep docker/docker

info "Kubernetes MCP Server requires Docker — already available"

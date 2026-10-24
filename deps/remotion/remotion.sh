#!/usr/bin/env bash
# dep: remotion/remotion
# type: dep
# description: Remotion CLI - code-driven (React) video composition, run with npx (needs Node.js)
# check: npx
# https://www.remotion.dev/docs/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Remotion runs from npx (`npx create-video`, `npx remotion render`) and
# downloads its own headless Chrome on first render; only Node.js is needed.
if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Remotion CLI ready — Node.js is available via npx"

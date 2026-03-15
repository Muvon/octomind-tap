#!/usr/bin/env bash
# dep: astral-sh/uv
# description: Installs uv — fast Python package and project manager (used by uvx-based MCP servers)
# check: uv
# https://github.com/astral-sh/uv

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/../../lib/platform.sh"

# Fast path — already installed
if pkg_check uv; then
  exit 0
fi

info "uv not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install uv
    else
      # Official installer works on macOS too
      curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
    ;;
  linux)
    # Official installer is the recommended path on Linux (works on all distros)
    if pkg_check curl; then
      curl -LsSf https://astral.sh/uv/install.sh | sh
    elif pkg_check wget; then
      wget -qO- https://astral.sh/uv/install.sh | sh
    else
      die "Neither curl nor wget found. Install one of them first, then re-run."
    fi
    ;;
esac

# The installer puts uv in ~/.cargo/bin or ~/.local/bin — verify it's reachable
if ! pkg_check uv; then
  info "uv installed but not in PATH. Add ~/.local/bin or ~/.cargo/bin to your PATH."
  info "Then re-run: octomind run <agent>"
  exit 1
fi

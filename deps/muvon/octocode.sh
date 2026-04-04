#!/usr/bin/env bash
# dep: muvon/octocode
# type: dep
# description: Installs the octocode CLI (code indexing and search tool by Muvon)
# check: octocode
# https://github.com/muvon/octocode

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check octocode; then
  exit 0
fi

# Ensure cargo is available
install_dep rust/cargo

# On Linux, ensure build tools are available (required for compiling native crates)
if [[ $OS == "linux" ]]; then
  if ! pkg_check cc; then
    info "Installing build dependencies (build-essential, pkg-config)..."
    if pkg_check apt-get; then
      sudo apt-get update -qq
      sudo apt-get install -y -qq build-essential pkg-config
    elif pkg_check dnf; then
      sudo dnf install -y @development-tools pkgconfig
    elif pkg_check yum; then
      sudo yum install -y @development-tools pkgconfig
    elif pkg_check pacman; then
      sudo pacman -S --noconfirm base-devel pkgconf
    elif pkg_check apk; then
      sudo apk add --no-cache build-base pkgconfig
    else
      warn "No supported package manager found. Build tools may be missing."
    fi
  fi
fi

info "octocode not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install muvon/tap/octocode
    else
      cargo install octocode
    fi
    ;;
  linux)
    cargo install octocode
    ;;
esac

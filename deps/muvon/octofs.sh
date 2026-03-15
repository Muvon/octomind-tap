#!/usr/bin/env bash
# dep: muvon/octofs
# description: Installs the octofs CLI (file editing and viewing tool by Muvon)
# check: octofs
# https://github.com/muvon/octofs

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check octofs; then
  exit 0
fi

# Ensure runtime dependencies are available
install_dep rust/cargo
install_dep ast-grep/ast-grep
install_dep burntsushi/ripgrep

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

info "octofs not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install muvon/tap/octofs
    else
      cargo install octofs
    fi
    ;;
  linux)
    cargo install octofs
    ;;
esac

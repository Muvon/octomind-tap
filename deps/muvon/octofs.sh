#!/usr/bin/env bash
# dep: muvon/octofs
# type: dep
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

# On Linux, ensure build tools + OpenSSL dev headers are available
if [[ $OS == "linux" ]]; then
  needs_install=0
  pkg_check cc || needs_install=1
  # Check for OpenSSL dev headers (required by openssl-sys crate)
  if ! pkg-config --exists openssl 2>/dev/null; then
    needs_install=1
  fi

  if [[ $needs_install -eq 1 ]]; then
    info "Installing build dependencies (build-essential, pkg-config, openssl-dev)..."
    case "$PKG_MANAGER" in
      apt)
        sudo apt-get update -qq
        sudo apt-get install -y -qq build-essential pkg-config libssl-dev
        ;;
      dnf)
        sudo dnf install -y @development-tools pkgconfig openssl-devel
        ;;
      pacman)
        sudo pacman -S --noconfirm base-devel pkgconf openssl
        ;;
      zypper)
        sudo zypper install -y -t pattern devel_basis && sudo zypper install -y pkg-config libopenssl-devel
        ;;
      apk)
        sudo apk add --no-cache build-base pkgconfig openssl-dev
        ;;
      *)
        warn "No supported package manager found. Build tools and OpenSSL dev headers may be missing."
        ;;
    esac
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

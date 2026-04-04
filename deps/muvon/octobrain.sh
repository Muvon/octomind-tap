#!/usr/bin/env bash
# dep: muvon/octobrain
# type: dep
# description: Installs the octobrain CLI (code indexing and search tool by Muvon)
# check: octobrain
# https://github.com/muvon/octobrain

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check octobrain; then
  exit 0
fi

# Ensure cargo is available
install_dep rust/cargo

# On Linux, ensure build tools + OpenSSL dev headers + protoc are available
if [[ $OS == "linux" ]]; then
  needs_install=0
  pkg_check cc || needs_install=1
  pkg_check protoc || needs_install=1
  if ! pkg-config --exists openssl 2>/dev/null; then
    needs_install=1
  fi

  if [[ $needs_install -eq 1 ]]; then
    info "Installing build dependencies (build-essential, pkg-config, openssl-dev, protobuf)..."
    case "$PKG_MANAGER" in
      apt)
        sudo apt-get update -qq
        sudo apt-get install -y -qq build-essential pkg-config libssl-dev protobuf-compiler
        ;;
      dnf)
        sudo dnf install -y @development-tools pkgconfig openssl-devel protobuf-compiler
        ;;
      pacman)
        sudo pacman -S --noconfirm base-devel pkgconf openssl protobuf
        ;;
      zypper)
        sudo zypper install -y -t pattern devel_basis && sudo zypper install -y pkg-config libopenssl-devel protobuf-devel
        ;;
      apk)
        sudo apk add --no-cache build-base pkgconfig openssl-dev protobuf-dev protoc
        ;;
      *)
        warn "No supported package manager found. Build dependencies may be missing."
        ;;
    esac
  fi
fi

info "octobrain not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install muvon/tap/octobrain
    else
      cargo install octobrain
    fi
    ;;
  linux)
    cargo install octobrain
    ;;
esac

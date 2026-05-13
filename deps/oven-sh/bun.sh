#!/usr/bin/env bash
# dep: oven-sh/bun
# type: dep
# description: Installs Bun — fast all-in-one JS/TS runtime, package manager, bundler, and test runner
# check: bun
# https://bun.sh

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check bun; then
  exit 0
fi

info "bun not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install oven-sh/bun/bun
    else
      curl -fsSL https://bun.sh/install | bash
    fi
    ;;
  linux)
    case "$PKG_MANAGER" in
      pacman)
        sudo pacman -S --noconfirm bun || curl -fsSL https://bun.sh/install | bash
        ;;
      apt | dnf | zypper | apk | *)
        # Official installer — works on all glibc-based distros (apk needs gcompat)
        if ! pkg_check unzip; then
          pkg_install unzip || true
        fi
        if pkg_check curl; then
          curl -fsSL https://bun.sh/install | bash
        elif pkg_check wget; then
          wget -qO- https://bun.sh/install | bash
        else
          die "No curl or wget found. Install bun manually: https://bun.sh"
        fi
        ;;
    esac
    ;;
esac

# Ensure ~/.bun/bin is on PATH for verification
if [[ -d "$HOME/.bun/bin" ]]; then
  export PATH="$HOME/.bun/bin:$PATH"
fi

if ! pkg_check bun; then
  die 'bun installed but not in PATH. Add $HOME/.bun/bin to PATH or restart your shell.'
fi

info "bun installed successfully."

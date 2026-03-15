#!/usr/bin/env bash
# dep: nodejs/node
# description: Installs Node.js LTS (required for npx-based MCP servers)
# check: node
# https://nodejs.org

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/../../lib/platform.sh"

# Fast path — already installed
if pkg_check node; then
  exit 0
fi

info "node not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install node
    else
      die "brew not found. Install Homebrew first: https://brew.sh — then re-run."
    fi
    ;;
  linux)
    case "$PKG_MANAGER" in
      apt)
        # NodeSource LTS repo — works on Debian, Ubuntu, and derivatives
        if pkg_check curl; then
          curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        else
          sudo apt-get install -y curl
          curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        fi
        sudo apt-get install -y nodejs
        ;;
      dnf)
        # NodeSource LTS repo for Fedora/RHEL
        if pkg_check curl; then
          curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
        else
          sudo dnf install -y curl
          curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
        fi
        sudo dnf install -y nodejs
        ;;
      pacman)
        sudo pacman -S --noconfirm nodejs npm
        ;;
      zypper)
        sudo zypper install -y nodejs
        ;;
      apk)
        sudo apk add nodejs npm
        ;;
      *)
        # Universal fallback via nvm
        info "No supported package manager found — falling back to nvm..."
        if ! pkg_check nvm && ! [[ -s "$HOME/.nvm/nvm.sh" ]]; then
          if pkg_check curl; then
            curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
          else
            die "No package manager or curl found. Install Node.js manually: https://nodejs.org"
          fi
        fi
        # shellcheck source=/dev/null
        source "$HOME/.nvm/nvm.sh"
        nvm install --lts
        ;;
    esac
    ;;
esac

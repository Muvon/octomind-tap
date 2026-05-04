#!/usr/bin/env bash
# dep: nodejs/node
# type: dep
# description: Installs Node.js LTS (required for npx-based MCP servers)
# check: node
# https://nodejs.org

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

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
        # Ubuntu/Debian — npm is a separate package, must install both
        sudo apt-get update -qq
        sudo apt-get install -y nodejs npm
        ;;
      dnf)
        sudo dnf install -y nodejs npm
        ;;
      pacman)
        sudo pacman -S --noconfirm nodejs npm
        ;;
      zypper)
        sudo zypper install -y nodejs npm
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
  windows)
    if pkg_check choco; then
      choco install nodejs-lts -y
    elif pkg_check scoop; then
      scoop install nodejs-lts
    elif pkg_check winget; then
      winget install OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements
    else
      die "No Windows package manager found (choco/scoop/winget). Install Node.js manually: https://nodejs.org"
    fi
    ;;
esac

if ! pkg_check node; then
  die "node installed but not in PATH."
fi

info "node installed successfully."

#!/usr/bin/env bash
# dep: docker/docker
# type: dep
# description: Installs Docker CLI and daemon (required for containerized MCP servers)
# check: docker
# https://docs.docker.com/engine/install/

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check docker; then
  exit 0
fi

info "docker not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install --cask docker
    else
      die "brew not found. Install Homebrew first: https://brew.sh — then re-run."
    fi
    ;;
  linux)
    case "$PKG_MANAGER" in
      apt)
        # Add Docker's official GPG key and repo
        if ! pkg_check curl; then
          as_root apt-get update
          as_root apt-get install -y curl
        fi
        curl -fsSL https://get.docker.com | sh
        ;;
      dnf)
        as_root dnf install -y dnf-plugins-core
        as_root dnf-3 config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
        as_root dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        as_root systemctl enable --now docker
        ;;
      pacman)
        as_root pacman -S --noconfirm docker docker-compose
        as_root systemctl enable --now docker
        ;;
      zypper)
        as_root zypper install -y docker docker-compose
        as_root systemctl enable --now docker
        ;;
      apk)
        as_root apk add docker docker-cli-compose
        # OpenRC on Alpine
        if command -v rc-update &>/dev/null; then
          as_root rc-update add docker default
          as_root rc-service docker start
        fi
        ;;
      *)
        # Universal fallback via install script
        if pkg_check curl; then
          curl -fsSL https://get.docker.com | sh
        else
          die "No supported package manager found. Install Docker manually: https://docs.docker.com/engine/install/"
        fi
        ;;
    esac
    ;;
esac

# Verify installation
if ! pkg_check docker; then
  info "Docker installed but not in PATH. You may need to:"
  info "  - Start Docker Desktop (macOS)"
  info "  - Run 'sudo usermod -aG docker \$USER' and log out/in (Linux)"
  info "  - Start the Docker daemon: sudo systemctl start docker (Linux)"
  exit 1
fi

info "Docker installed successfully."

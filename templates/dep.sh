#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Octomind Tap Dependency Script Template
# ─────────────────────────────────────────────────────────────────────────────
#
# Copy this file to deps/<org>/<tool>.sh and customize.
#
# Quick start:
#   1. Set org/tool in the filename and header comments
#   2. Set description and check command
#   3. Add homepage URL
#   4. Customize the installation logic for each platform
#
# Usage in agent manifest:
#   [deps]
#   require = ["<org>/<tool>"]
# ─────────────────────────────────────────────────────────────────────────────

# dep: <org>/<tool>
# description: Brief description of what this installs
# check: <command-to-check-if-installed>
# https://example.com/tool-homepage

set -euo pipefail

# ─────────────────────────────────────────────────────────────────────────────
# Platform Detection
# ─────────────────────────────────────────────────────────────────────────────
# After sourcing, these variables are available:
#   OS          — "macos" | "linux"
#   ARCH        — "x86_64" | "arm64"
#   PKG_MANAGER — "brew" | "apt" | "dnf" | "pacman" | "zypper" | "apk"
#   IS_MACOS    — "1" if macOS
#   IS_LINUX    — "1" if Linux
#   IS_ARM64    — "1" if arm64
#   IS_X86_64   — "1" if x86_64
#
# Functions:
#   pkg_check <command>   — returns 0 if command exists, 1 otherwise
#   pkg_install <package> — install via detected package manager
#   die <message>          — print error and exit 1
#   info <message>         — print informational message
#   warn <message>         — print warning message
#   install_dep <org/tool> — run another dep script

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# ─────────────────────────────────────────────────────────────────────────────
# Fast Path — Already Installed
# ─────────────────────────────────────────────────────────────────────────────
# Exit early if the tool is already available.

if pkg_check "<command>"; then
  exit 0
fi

# ─────────────────────────────────────────────────────────────────────────────
# Installation Logic
# ─────────────────────────────────────────────────────────────────────────────
# Customize this section for your tool.

info "<tool> not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install "<package>"
    else
      die "brew not found. Install Homebrew first: https://brew.sh — then re-run."
    fi
    ;;

  linux)
    case "$PKG_MANAGER" in
      apt)
        sudo apt-get update
        sudo apt-get install -y "<package>"
        ;;

      dnf)
        sudo dnf install -y "<package>"
        ;;

      pacman)
        sudo pacman -S --noconfirm "<package>"
        ;;

      zypper)
        sudo zypper install -y "<package>"
        ;;

      apk)
        sudo apk add "<package>"
        ;;

      *)
        # Universal fallback — use official installer if available
        if pkg_check curl; then
          curl -fsSL https://example.com/install.sh | sh
        elif pkg_check wget; then
          wget -qO- https://example.com/install.sh | sh
        else
          die "No supported package manager found. Install <tool> manually: https://example.com"
        fi
        ;;
    esac
    ;;
esac

# ─────────────────────────────────────────────────────────────────────────────
# Verification
# ─────────────────────────────────────────────────────────────────────────────
# Ensure the tool is now available.

if ! pkg_check "<command>"; then
  # Try adding to PATH if installed but not found
  if [[ -d "$HOME/.local/bin" ]]; then
    export PATH="$HOME/.local/bin:$PATH"
  fi
  if [[ -d "$HOME/.cargo/bin" ]]; then
    export PATH="$HOME/.cargo/bin:$PATH"
  fi

  if ! pkg_check "<command>"; then
    die "<tool> installed but not in PATH. You may need to restart your shell."
  fi
fi

info "<tool> installed successfully."

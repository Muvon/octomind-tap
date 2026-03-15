#!/usr/bin/env bash
# deps/lib/platform.sh — shared platform detection for all dep scripts
#
# Usage in a dep script:
#   source "$(dirname "${BASH_SOURCE[0]}")/../../lib/platform.sh"
#
# After sourcing, the following are available:
#
# Variables (read-only):
#   OS          — "macos" | "linux"
#   ARCH        — "x86_64" | "arm64"
#   PKG_MANAGER — "brew" | "apt" | "dnf" | "pacman" | "zypper" | "apk" | "unknown"
#   IS_MACOS    — "1" if macOS, else "0"
#   IS_LINUX    — "1" if Linux, else "0"
#   IS_ARM64    — "1" if arm64/aarch64, else "0"
#   IS_X86_64   — "1" if x86_64/amd64, else "0"
#
# Functions:
#   pkg_install <package>   — install via the detected package manager
#   pkg_check   <command>   — exit 0 if command exists, else exit 1
#   die         <message>   — print to stderr and exit 1
#   info        <message>   — print to stderr (informational, not an error)

set -euo pipefail

# ── OS detection ─────────────────────────────────────────────────────────────

case "$(uname -s)" in
  Darwin)
    OS="macos"
    IS_MACOS="1"
    IS_LINUX="0"
    ;;
  Linux)
    OS="linux"
    IS_MACOS="0"
    IS_LINUX="1"
    ;;
  *)
    echo "Unsupported OS: $(uname -s)" >&2
    exit 1
    ;;
esac

# ── Architecture detection ────────────────────────────────────────────────────

case "$(uname -m)" in
  x86_64 | amd64)
    ARCH="x86_64"
    IS_X86_64="1"
    IS_ARM64="0"
    ;;
  arm64 | aarch64)
    ARCH="arm64"
    IS_X86_64="0"
    IS_ARM64="1"
    ;;
  *)
    # Unknown arch — set it but don't abort; scripts can handle it themselves
    ARCH="$(uname -m)"
    IS_X86_64="0"
    IS_ARM64="0"
    ;;
esac

# ── Package manager detection (Linux only) ────────────────────────────────────

if [[ "$IS_MACOS" == "1" ]]; then
  PKG_MANAGER="brew"
else
  if   command -v apt-get &>/dev/null; then PKG_MANAGER="apt"
  elif command -v dnf     &>/dev/null; then PKG_MANAGER="dnf"
  elif command -v pacman  &>/dev/null; then PKG_MANAGER="pacman"
  elif command -v zypper  &>/dev/null; then PKG_MANAGER="zypper"
  elif command -v apk     &>/dev/null; then PKG_MANAGER="apk"
  else                                      PKG_MANAGER="unknown"
  fi
fi

# Export all variables as read-only
readonly OS ARCH PKG_MANAGER IS_MACOS IS_LINUX IS_X86_64 IS_ARM64

# ── Helper functions ──────────────────────────────────────────────────────────

# die <message> — print error to stderr and exit 1
die() {
  echo "❌ $*" >&2
  exit 1
}

# info <message> — print informational message to stderr
info() {
  echo "  → $*" >&2
}

# pkg_check <command> — returns 0 if command exists, 1 otherwise
pkg_check() {
  command -v "$1" &>/dev/null
}

# pkg_install <package> [<package-name-override-per-pm>...]
#
# Installs a package using the detected package manager.
# For cases where the package name differs per PM, use the explicit functions
# below (apt_install, dnf_install, etc.) directly in your script.
#
# Usage:
#   pkg_install curl          # same name everywhere
pkg_install() {
  local pkg="$1"
  info "Installing $pkg via $PKG_MANAGER..."
  case "$PKG_MANAGER" in
    brew)    brew install "$pkg" ;;
    apt)     sudo apt-get install -y "$pkg" ;;
    dnf)     sudo dnf install -y "$pkg" ;;
    pacman)  sudo pacman -S --noconfirm "$pkg" ;;
    zypper)  sudo zypper install -y "$pkg" ;;
    apk)     sudo apk add "$pkg" ;;
    unknown) die "No supported package manager found. Please install $pkg manually." ;;
  esac
}

# brew_install <formula> — macOS only, no-op on Linux
brew_install() {
  [[ "$IS_MACOS" == "1" ]] && brew install "$1" || true
}

# apt_install <pkg> — Debian/Ubuntu only
apt_install() {
  [[ "$PKG_MANAGER" == "apt" ]] && sudo apt-get install -y "$1" || true
}

# dnf_install <pkg> — Fedora/RHEL only
dnf_install() {
  [[ "$PKG_MANAGER" == "dnf" ]] && sudo dnf install -y "$1" || true
}

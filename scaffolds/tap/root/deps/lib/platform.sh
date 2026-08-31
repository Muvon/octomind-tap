#!/usr/bin/env bash
# Shared platform detection for dependency installers in this tap.
# Source this file from every deps/<org>/<tool>.sh script.

set -euo pipefail

case "$(uname -s)" in
  Darwin)
    OS="macos"
    IS_MACOS="1"
    IS_LINUX="0"
    IS_WINDOWS="0"
    ;;
  Linux)
    OS="linux"
    IS_MACOS="0"
    IS_LINUX="1"
    IS_WINDOWS="0"
    ;;
  MINGW* | MSYS* | CYGWIN* | Windows_NT)
    OS="windows"
    IS_MACOS="0"
    IS_LINUX="0"
    IS_WINDOWS="1"
    ;;
  *)
    echo "Unsupported OS: $(uname -s)" >&2
    exit 1
    ;;
esac

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
    ARCH="$(uname -m)"
    IS_X86_64="0"
    IS_ARM64="0"
    ;;
esac

if [[ "$IS_MACOS" == "1" ]]; then
  PKG_MANAGER="brew"
  if ! command -v brew &>/dev/null; then
    if [[ -x /opt/homebrew/bin/brew ]]; then
      eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -x /usr/local/bin/brew ]]; then
      eval "$(/usr/local/bin/brew shellenv)"
    fi
  fi
elif [[ "$IS_LINUX" == "1" ]]; then
  if command -v apt-get &>/dev/null; then
    PKG_MANAGER="apt"
  elif command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"
  elif command -v pacman &>/dev/null; then
    PKG_MANAGER="pacman"
  elif command -v zypper &>/dev/null; then
    PKG_MANAGER="zypper"
  elif command -v apk &>/dev/null; then
    PKG_MANAGER="apk"
  else
    PKG_MANAGER="unknown"
  fi
else
  PKG_MANAGER="unknown"
fi

readonly OS ARCH PKG_MANAGER IS_MACOS IS_LINUX IS_WINDOWS IS_X86_64 IS_ARM64

die() {
  echo "ERROR: $*" >&2
  exit 1
}

info() {
  echo "  -> $*" >&2
}

warn() {
  echo "  WARN: $*" >&2
}

pkg_check() {
  command -v "$1" &>/dev/null
}

as_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  elif pkg_check sudo; then
    sudo "$@"
  else
    die "Need root privileges for: $*"
  fi
}

pkg_install() {
  local package="$1"
  info "Installing $package with $PKG_MANAGER..."
  case "$PKG_MANAGER" in
    brew) brew install "$package" ;;
    apt) as_root apt-get install -y "$package" ;;
    dnf) as_root dnf install -y "$package" ;;
    pacman) as_root pacman -S --noconfirm "$package" ;;
    zypper) as_root zypper install -y "$package" ;;
    apk) as_root apk add "$package" ;;
    *) die "No supported package manager found. Install $package manually." ;;
  esac
}

brew_install() {
  [[ "$IS_MACOS" == "1" ]] && brew install "$1" || true
}

apt_install() {
  [[ "$PKG_MANAGER" == "apt" ]] && as_root apt-get install -y "$1" || true
}

dnf_install() {
  [[ "$PKG_MANAGER" == "dnf" ]] && as_root dnf install -y "$1" || true
}

install_dep() {
  local dependency="$1"
  local deps_root
  deps_root="$(cd "$(dirname "${BASH_SOURCE[1]}")/.." && pwd)"

  [[ -f "$deps_root/$dependency.sh" ]] || \
    die "Dependency script not found: $deps_root/$dependency.sh"

  info "Installing dependency: $dependency"
  bash "$deps_root/$dependency.sh" || \
    die "Dependency installer failed: $dependency"

  if [[ -f "$HOME/.cargo/env" ]]; then
    # shellcheck source=/dev/null
    source "$HOME/.cargo/env"
  fi
  if [[ -d "$HOME/.local/bin" ]]; then
    export PATH="$HOME/.local/bin:$PATH"
  fi
}


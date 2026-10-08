#!/usr/bin/env bash
# dep: nodejs/node
# type: dep
# description: Installs Node.js for npx-based MCP servers
# check: node
# https://nodejs.org

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# npx-based MCP servers need Node.js >= 20 (on 18, undici has no File global and
# they crash). An older Node counts as missing — like the 18.x Debian and Ubuntu
# 24.04 ship, or that a distro package drags in as a dependency (Debian's novnc
# does, without npm).
NODE_MIN_MAJOR=20

node_ok() {
  pkg_check node && pkg_check npx \
    && (($(node -p 'process.versions.node.split(".")[0]') >= NODE_MIN_MAJOR))
}

ready() {
  node_ok || die "Node.js >= $NODE_MIN_MAJOR with npx is needed; $(node -v 2>/dev/null || echo 'no node') is on PATH."
  info "node $(node -v) ready."
}

# Whether a package manager can install at all. Octomind Cloud machines run a
# read-only root filesystem: even root cannot write /usr there.
system_writable() {
  if [[ "$(id -u)" -eq 0 ]]; then
    test -w /usr
  elif pkg_check sudo; then
    sudo test -w /usr
  else
    return 1
  fi
}

# The official Node.js LTS build, checksummed, unpacked under ~/.local with
# node/npm/npx/corepack linked into ~/.local/bin — first on PATH on Octomind
# Cloud machines, and install_dep adds it to PATH for its caller.
install_user_node() {
  local platform version name dist
  case "$ARCH" in
    x86_64) platform="linux-x64" ;;
    arm64) platform="linux-arm64" ;;
    *) die "No Node.js build for $ARCH. Install Node.js >= $NODE_MIN_MAJOR manually: https://nodejs.org" ;;
  esac
  pkg_check curl || die "curl not found. Install curl first, then re-run."
  # index.tab lists releases newest first; column 10 is the LTS codename, '-' if
  # none. awk reads to the end: an early exit would fail curl under pipefail.
  version="$(curl -fsSL https://nodejs.org/dist/index.tab \
    | awk -F'\t' 'NR > 1 && $10 != "-" && v == "" { v = $1 } END { print v }')"
  [[ -n "$version" ]] || die "Could not find the current Node.js LTS release."
  name="node-${version}-${platform}"
  if [[ ! -x "$HOME/.local/lib/nodejs/$name/bin/node" ]]; then
    info "installing Node.js $version into ~/.local..."
    dist="https://nodejs.org/dist/${version}"
    # Global, not local: the EXIT trap runs after this function has returned.
    NODE_TMP="$(mktemp -d)"
    trap 'rm -rf "$NODE_TMP"' EXIT
    curl -fsSL -o "$NODE_TMP/$name.tar.gz" "$dist/$name.tar.gz"
    curl -fsSL "$dist/SHASUMS256.txt" | awk -v f="$name.tar.gz" '$2 == f' >"$NODE_TMP/SHASUMS256.txt"
    [[ -s "$NODE_TMP/SHASUMS256.txt" ]] || die "No published checksum for $name.tar.gz."
    (cd "$NODE_TMP" && sha256sum -c SHASUMS256.txt >/dev/null) || die "Checksum mismatch for $name.tar.gz."
    tar -xzf "$NODE_TMP/$name.tar.gz" -C "$NODE_TMP"
    mkdir -p "$HOME/.local/lib/nodejs"
    rm -rf "$HOME/.local/lib/nodejs/$name"
    mv "$NODE_TMP/$name" "$HOME/.local/lib/nodejs/$name"
  fi
  mkdir -p "$HOME/.local/bin"
  for bin in node npm npx corepack; do
    ln -sfn "$HOME/.local/lib/nodejs/$name/bin/$bin" "$HOME/.local/bin/$bin"
  done
  export PATH="$HOME/.local/bin:$PATH"
}

# Fast path — a recent enough Node with npx
if node_ok; then
  exit 0
fi

if pkg_check node; then
  info "node $(node -v) is older than $NODE_MIN_MAJOR or has no npx — installing a current one..."
else
  info "node not found — installing..."
fi

# A read-only root leaves only the home directory to install into.
if [[ "$OS" == "linux" ]] && ! system_writable; then
  install_user_node
  ready
  exit 0
fi

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
        # Distro repos ship stale Node (Ubuntu 24.04 → 18.x, too old for MCP
        # servers that need >= 20) — use the NodeSource LTS repo instead.
        # NodeSource's nodejs bundles npm, so no separate npm package.
        if ! pkg_check curl; then
          as_root apt-get update -qq
          as_root apt-get install -y curl
        fi
        curl -fsSL https://deb.nodesource.com/setup_lts.x | as_root bash -
        as_root apt-get install -y nodejs
        ;;
      dnf)
        # Same stale-distro-repo problem as apt — use NodeSource LTS.
        curl -fsSL https://rpm.nodesource.com/setup_lts.x | as_root bash -
        as_root dnf install -y nodejs
        ;;
      pacman)
        as_root pacman -S --noconfirm nodejs npm
        ;;
      zypper)
        as_root zypper install -y nodejs npm
        ;;
      apk)
        as_root apk add nodejs npm
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

ready

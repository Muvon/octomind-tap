---
name: tap-deps-authoring
title: "Tap Dep Script Authoring"
description: "Complete guide for writing dep scripts in the octomind-tap registry: required header comments, platform.sh boilerplate, type: mcp vs type: dep, npx/uvx MCP pattern, platform variables and functions, companion .md format, and validation. Activate when creating or editing deps/<org>/<tool>.sh files."
license: Apache-2.0
compatibility: "Requires: octomind-tap repo. Run scripts/lint-deps.sh for validation."
domains: octomind
rules:
  - file(deps/)
  - match(\bdep\s+script\b)
  - match(\bdeps/[\w./-]+)
  - match(\bplatform\.sh\b)
  - match(\binstall\s+script\b)
  - match(\bpkg_check\b|\bpkg_install\b|\binstall_dep\b)
  - match(\b(mcp|dep)\s+manifest\b)
---

# Tap Dep Script Authoring

## Overview

A dep script is a `deps/<org>/<tool>.sh` bash script that auto-installs a tool or MCP server runtime before an Octomind session starts. Deps are **never run manually** — Octomind runs them automatically to ensure the required binary is available. Every dep script must handle macOS and all major Linux package managers.

Each dep script must have a matching `deps/<org>/<tool>.md` companion doc.

---

## Instructions

### Required Header Comments

Every dep script must start with these header comments (parsed by tooling):

```bash
#!/usr/bin/env bash
# dep: <org>/<tool>
# type: mcp|dep
# description: Brief description of what this installs
# check: <command-to-verify-installation>
# https://homepage-url
```

- `# dep:` — must match the `require = ["<org>/<tool>"]` entry in the capability file
- `# type: mcp` — script ensures an MCP server runtime is runnable (e.g. `npx`, `uvx`, `docker`)
- `# type: dep` — script installs a standalone CLI tool used directly (e.g. `cargo`, `kubectl`, `octofs`)
- `# check:` — the command `pkg_check` uses to detect if already installed
- URL — homepage or GitHub link

### Type Classification

**`type: mcp`** — the dep exists to make an MCP server launchable. Most MCP servers run via `npx -y <package>` or `uvx <package>`. The dep script just ensures the runtime is present:

```bash
#!/usr/bin/env bash
# dep: tavily-ai/tavily
# type: mcp
# description: Tavily MCP Server — AI-powered web search
# check: npx
# https://github.com/tavily-ai/tavily-mcp

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then exit 0; fi
install_dep nodejs/node
```

**`type: dep`** — the dep installs a real CLI tool that agents use directly (not via MCP):

```bash
#!/usr/bin/env bash
# dep: hashicorp/terraform
# type: dep
# description: Terraform infrastructure-as-code CLI
# check: terraform
# https://developer.hashicorp.com/terraform

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check terraform; then exit 0; fi

info "terraform not found — installing..."

case "$OS" in
  macos)
    brew_install terraform
    ;;
  linux)
    case "$PKG_MANAGER" in
      apt)    apt_install terraform ;;
      dnf)    dnf_install terraform ;;
      pacman) pkg_install terraform ;;
      zypper) pkg_install terraform ;;
      apk)    pkg_install terraform ;;
      *)
        curl -fsSL https://releases.hashicorp.com/terraform/install.sh | sh
        ;;
    esac
    ;;
esac

pkg_check terraform || die "terraform not found after install"
info "terraform installed successfully."
```

### Full Script Structure

```bash
#!/usr/bin/env bash
# dep: <org>/<tool>
# type: mcp|dep
# description: Brief description
# check: <command>
# https://homepage

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check "<command>"; then exit 0; fi

info "<tool> not found — installing..."

case "$OS" in
  macos)
    brew_install <formula>
    ;;
  linux)
    case "$PKG_MANAGER" in
      apt)    apt_install <pkg> ;;
      dnf)    dnf_install <pkg> ;;
      pacman) pkg_install <pkg> ;;
      zypper) pkg_install <pkg> ;;
      apk)    pkg_install <pkg> ;;
      *)
        # Universal fallback
        curl -fsSL https://example.com/install.sh | sh
        ;;
    esac
    ;;
esac

pkg_check "<command>" || die "<tool> not found after install"
info "<tool> installed successfully."
```

### Platform Variables (from `deps/lib/platform.sh`)

| Variable | Values |
|----------|--------|
| `$OS` | `macos` or `linux` |
| `$ARCH` | `x86_64` or `arm64` |
| `$PKG_MANAGER` | `brew`, `apt`, `dnf`, `pacman`, `zypper`, `apk`, `unknown` |
| `$IS_MACOS` | `1` or `0` |
| `$IS_LINUX` | `1` or `0` |
| `$IS_ARM64` | `1` or `0` |
| `$IS_X86_64` | `1` or `0` |

### Platform Functions (from `deps/lib/platform.sh`)

| Function | Purpose |
|----------|---------|
| `pkg_check <cmd>` | Returns 0 if command exists — use for fast-path and post-install verify |
| `pkg_install <pkg>` | Install via detected package manager |
| `brew_install <formula>` | macOS only, no-op on Linux |
| `apt_install <pkg>` | Debian/Ubuntu only, no-op elsewhere |
| `dnf_install <pkg>` | Fedora/RHEL only, no-op elsewhere |
| `install_dep <org/tool>` | Run another dep script as a prerequisite; sources PATH after |
| `info <msg>` | Print informational message to stderr |
| `warn <msg>` | Print warning to stderr |
| `die <msg>` | Print error to stderr and exit 1 |

**Never re-implement platform detection** — always source `deps/lib/platform.sh`.

---

### Companion Documentation

Every `.sh` must have a matching `.md` at the same path (`deps/<org>/<tool>.md`).

**For MCP servers** (`type: mcp`) — copy `templates/dep-mcp.md`, must include:
- `## MCP Server` — package name, transport, launch command
- `## Authentication` — required env vars and how to obtain them
- `## Available Tools` — list of tools the MCP server exposes
- `## Configuration Example` — example `[[mcp.servers]]` TOML block

**For plain deps** (`type: dep`) — copy `templates/dep-tool.md`, must include:
- `## Key Commands` — most important CLI commands
- `## Common Usage` — typical usage patterns with examples

---

### Validation

```bash
bash scripts/lint-deps.sh deps/<org>/<tool>.sh
```

Checks: required header comments present, `# type:` set, companion `.md` exists, script is executable.

---

### Creation Checklist

- [ ] File at `deps/<org>/<tool>.sh` (org matches GitHub org or tool namespace)
- [ ] Required header comments: `# dep:`, `# type:`, `# description:`, `# check:`, URL
- [ ] Sources `deps/lib/platform.sh` — never re-implements platform detection
- [ ] Fast-path `pkg_check` exit at top
- [ ] Handles `macos` + all Linux package managers + universal fallback
- [ ] Post-install `pkg_check` verify with `die` on failure
- [ ] Companion `deps/<org>/<tool>.md` exists with correct sections
- [ ] `bash scripts/lint-deps.sh deps/<org>/<tool>.sh` passes clean

---

## Examples

### Example 1: MCP server via npx (minimal)

```bash
#!/usr/bin/env bash
# dep: modelcontextprotocol/filesystem
# type: mcp
# description: MCP filesystem server — requires Node.js/npx
# check: npx
# https://github.com/modelcontextprotocol/servers

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then exit 0; fi
install_dep nodejs/node
```

### Example 2: MCP server via uvx (Python)

```bash
#!/usr/bin/env bash
# dep: myorg/mcp-server
# type: mcp
# description: My Python MCP server — requires uvx
# check: uvx
# https://github.com/myorg/mcp-server

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check uvx; then exit 0; fi
install_dep astral-sh/uv
```

### Example 3: GitHub release binary install

```bash
#!/usr/bin/env bash
# dep: muvon/octofs
# type: dep
# description: Installs the octofs CLI from GitHub releases
# check: octofs
# https://github.com/muvon/octofs

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check octofs; then exit 0; fi

case "$OS" in
  macos)
    brew_install muvon/tap/octofs
    ;;
  linux)
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    VERSION=$(curl -fsSL "https://api.github.com/repos/muvon/octofs/releases" \
      | grep '"tag_name":' | head -1 | sed -E 's/.*"([^"]+)".*/\1/')
    case "$ARCH" in
      x86_64) TARGET="x86_64-unknown-linux-musl" ;;
      arm64)  TARGET="aarch64-unknown-linux-musl" ;;
    esac
    curl -fsSL "https://github.com/muvon/octofs/releases/download/$VERSION/octofs-$VERSION-$TARGET.tar.gz" \
      | tar xz -C "$INSTALL_DIR"
    chmod +x "$INSTALL_DIR/octofs"
    export PATH="$INSTALL_DIR:$PATH"
    ;;
esac

pkg_check octofs || die "octofs not found after install"
```

### Example 4: Common mistake — re-implementing platform detection

```bash
# WRONG — never do this
if [[ "$(uname)" == "Darwin" ]]; then
  brew install something
fi

# RIGHT — source platform.sh and use its functions
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"
brew_install something
```

---

## References

- `templates/dep.sh` — canonical dep script template (copy to start)
- `templates/dep-mcp.md` — companion doc template for MCP servers
- `templates/dep-tool.md` — companion doc template for plain deps
- `deps/lib/platform.sh` — platform detection library (source in all dep scripts)
- `bash scripts/lint-deps.sh` — validates dep scripts

#!/usr/bin/env bash
# dep: rendercv/rendercv
# type: dep
# description: RenderCV - turn YAML into resume and CV PDFs; typeset with Typst and ATS-friendly single-column themes, also exports Markdown, HTML and PNG copies
# check: rendercv
# https://rendercv.com

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

VERSION="2.8"

# Fast path — already installed
if pkg_check rendercv; then
  exit 0
fi

info "rendercv not found — installing ${VERSION} with uv..."

install_dep astral-sh/uv

# The [full] extra bundles the CLI, the Typst compiler binding, and the theme fonts.
uv tool install --python 3.12 "rendercv[full]==${VERSION}"

export PATH="$HOME/.local/bin:$PATH"

if ! pkg_check rendercv; then
  die "rendercv installed but not in PATH. Add ~/.local/bin to PATH."
fi

info "rendercv installed successfully."

#!/usr/bin/env bash
# dep: medical/medical
# description: Medical MCP Server — FDA, WHO, PubMed, RxNorm medical data
# check: node
# https://github.com/JamesANZ/medical-mcp

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Ensure node is available
install_dep nodejs/node

# Install globally so we can run via `node` directly.
# npx -y medical-mcp conflicts with ImageMagick's `import` binary on macOS
# because the package uses ES module `import` syntax which npx resolves to
# the system `import` binary (ImageMagick) instead of executing the JS file.
MEDICAL_MCP_BIN="$(npm root -g)/medical-mcp/build/index.js"
if [ ! -f "$MEDICAL_MCP_BIN" ]; then
  info "Installing medical-mcp globally..."
  npm install -g medical-mcp --silent
  MEDICAL_MCP_BIN="$(npm root -g)/medical-mcp/build/index.js"
fi

# Write a wrapper to ~/.local/bin so the formula can call it directly via `node`.
# This avoids npx entirely — npx would re-resolve `import` as ImageMagick's binary.
WRAPPER_DIR="$HOME/.local/bin"
mkdir -p "$WRAPPER_DIR"
WRAPPER="$WRAPPER_DIR/medical-mcp-server"
if [ ! -f "$WRAPPER" ]; then
  cat >"$WRAPPER" <<EOF
#!/usr/bin/env bash
exec node "$MEDICAL_MCP_BIN" "\$@"
EOF
  chmod +x "$WRAPPER"
  info "Wrapper written to $WRAPPER"
fi

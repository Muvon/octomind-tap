#!/usr/bin/env bash
# scripts/setup-symlinks.sh
# Sets up capability default.toml symlinks (always force — this is the canonical default).
# Run after cloning or adding new capabilities. Safe to re-run.
#
# Reports MISSING if the target provider file doesn't exist yet.
# Reports WARN  if a capability dir has no default mapping declared here.

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAP_ROOT="$REPO_ROOT/capabilities"

MISSING=0

# link <capability> <provider-file>
# Always force-creates the symlink. Warns if the provider file is absent.
link() {
  local cap="$1"
  local target="$2"
  local dir="$CAP_ROOT/$cap"
  local link="$dir/default.toml"

  if [[ ! -f "$dir/$target" ]]; then
    echo "  MISSING  capabilities/$cap/$target  (provider file not found — create it first)"
    MISSING=$((MISSING + 1))
    return
  fi

  ln -sf "$target" "$link"
  echo "  link     capabilities/$cap/default.toml -> $target"
}

echo "Setting up capability symlinks..."
echo ""

# ── Default provider mappings ─────────────────────────────────────────────────
# core and agent use default.toml directly (no provider variants)
link "filesystem" "octofs.toml"
link "codesearch" "octocode.toml"
link "memory" "octobrain.toml"
link "websearch" "tavily.toml"
link "versioning" "git.toml"
link "programming-python" "uv.toml"
link "programming-rust" "cargo.toml"
link "programming-nodejs" "node.toml"
link "docker" "docker.toml"
link "kubernetes" "kubernetes.toml"
link "svelte" "svelte.toml"
link "medical-reference" "medical.toml"
link "market-data" "yfinance.toml"
link "legal-au" "ansvar.toml"
link "legal-ca" "ansvar.toml"
link "legal-de" "ansvar.toml"
link "legal-fr" "ansvar.toml"
link "legal-in" "ansvar.toml"
link "legal-sg" "ansvar.toml"
link "legal-th" "ansvar.toml"
link "legal-uk" "ansvar.toml"
link "legal-us" "ansvar.toml"
link "octoweb" "octoweb.toml"
link "browser" "playwright.toml"
link "messaging-slack" "slack.toml"
link "messaging-discord" "discord.toml"
link "messaging-telegram" "iflow-mcp.toml"
link "messaging-whatsapp" "iflow-mcp.toml"
link "messaging-linkedin" "pegasusheavy.toml"
link "messaging-instagram" "mcpware.toml"
link "messaging-email" "codefuturist.toml"
link "messaging-sms" "twilio.toml"
# ── New capabilities (PR #5) ──────────────────────────────────────────────────
link "calendar" "google-calendar.toml"
link "customer-management" "hubspot.toml"
link "database-postgres" "postgres.toml"
link "database-sqlite" "sqlite.toml"
link "devdocs" "context7.toml"
link "ecommerce" "shopify.toml"
link "edge-hosting" "cloudflare.toml"
link "error-tracking" "sentry.toml"
link "highlights" "readwise.toml"
link "maps" "google-maps.toml"
link "payments" "stripe.toml"
link "scraping" "firecrawl.toml"
link "task-management" "linear.toml"
link "translation" "deepl.toml"
link "webfetch" "fetch.toml"
# ── Video / media production capabilities ────────────────────────────────────
link "video-gen" "runway.toml"
link "voice" "elevenlabs.toml"
link "avatar" "heygen.toml"
link "lipsync" "sync.toml"
link "music" "mubert.toml"
link "composition" "remotion.toml"
link "captions" "assemblyai.toml"
link "stock" "pexels.toml"
link "image-gen" "replicate-flux.toml"
link "publish-tiktok" "tiktok-posting.toml"
link "publish-instagram" "meta-instagram.toml"
link "publish-youtube" "youtube-data.toml"
# ─────────────────────────────────────────────────────────────────────────────

# Detect capability dirs that have NO mapping declared above
echo ""
DECLARED=("filesystem" "codesearch" "memory" "websearch" "versioning" "core" "agent" "programming-python" "programming-rust" "programming-nodejs" "docker" "kubernetes" "svelte" "medical-reference" "market-data" "legal-au" "legal-ca" "legal-de" "legal-fr" "legal-in" "legal-sg" "legal-th" "legal-uk" "legal-us" "octoweb" "browser" "messaging-slack" "messaging-discord" "messaging-telegram" "messaging-whatsapp" "messaging-linkedin" "messaging-instagram" "messaging-email" "messaging-sms" "calendar" "customer-management" "database-postgres" "database-sqlite" "devdocs" "ecommerce" "edge-hosting" "error-tracking" "highlights" "maps" "payments" "scraping" "task-management" "translation" "webfetch" "video-gen" "voice" "avatar" "lipsync" "music" "composition" "captions" "stock" "image-gen" "publish-tiktok" "publish-instagram" "publish-youtube")
for dir in "$CAP_ROOT"/*/; do
  cap="$(basename "$dir")"
  found=0
  for d in "${DECLARED[@]}"; do
    [[ $d == "$cap" ]] && found=1 && break
  done
  if [[ $found -eq 0 ]]; then
    echo "  WARN     capabilities/$cap/ has no default mapping in setup-symlinks.sh"
  fi
done

echo ""
if [[ $MISSING -gt 0 ]]; then
  echo "⚠️  $MISSING provider file(s) missing — add them before running bin/load."
  exit 1
fi

echo "✅ All symlinks set. To switch a provider:"
echo "   ln -sf <provider>.toml capabilities/<name>/default.toml"

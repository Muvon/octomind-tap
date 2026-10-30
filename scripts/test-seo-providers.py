#!/usr/bin/env python3
"""Offline provider/resolver regression checks; no credentials or network calls."""
from pathlib import Path
from contextlib import redirect_stderr
from io import StringIO
import runpy
import shutil
import subprocess
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT / "capabilities/seo-data"
PROVIDERS = {"public", "dataforseo", "ahrefs", "semrush", "seranking",
             "serpstat", "search-console", "free-seo"}


def load(provider):
    return tomllib.loads((CAP / f"{provider}.toml").read_text())


class ProviderTests(unittest.TestCase):
    def test_public_default_reuses_keyless_servers(self):
        self.assertEqual((CAP / "default.toml").resolve(), CAP / "public.toml")
        self.assertIn('link "seo-data" "public.toml"',
                      (ROOT / "scripts/setup-symlinks.sh").read_text())
        public = load("public")
        sources = ["websearch/duckduckgo", "webfetch/octobrain"]
        expected = [tomllib.loads((ROOT / f"capabilities/{p}.toml").read_text())
                    for p in sources]
        self.assertEqual(public["mcp"]["servers"],
                         [s for p in expected for s in p["mcp"]["servers"]])
        self.assertNotIn("{{ENV:", (CAP / "public.toml").read_text())

    def test_explicit_providers_resolve_and_deduplicate_end_to_end(self):
        # Run the actual CLI with a minimal temporary tap, leaving repo agents untouched.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bin").mkdir()
            shutil.copy(ROOT / "bin/load", root / "bin/load")
            (root / "capabilities").symlink_to(ROOT / "capabilities", target_is_directory=True)
            (root / "agents/seo").mkdir(parents=True)
            for provider in sorted(PROVIDERS):
                with self.subTest(provider=provider):
                    (root / "agents/seo/test.toml").write_text(
                        'capabilities = ["core", "websearch", "webfetch", '
                        f'"seo-data:{provider}"]\n'
                        '[[roles]]\nsystem = "fixture"\nwelcome = "fixture"\n')
                    p = subprocess.run(["python3", str(root / "bin/load"), "seo:test"],
                                       capture_output=True, text=True, check=True)
                    merged = tomllib.loads(p.stdout)
                    refs = merged["roles"][0]["mcp"]["server_refs"]
                    for ref in load(provider)["roles"]["mcp"]["server_refs"]:
                        self.assertIn(ref, refs)
                    names = [s["name"] for s in merged["mcp"]["servers"]]
                    self.assertEqual(len(names), len(set(names)))
                    for server in load(provider)["mcp"]["servers"]:
                        self.assertIn(server, merged["mcp"]["servers"])

    def test_default_and_missing_provider_resolution(self):
        resolver = runpy.run_path(str(ROOT / "bin/load"))["load_capability"]
        self.assertEqual(resolver("seo-data", str(ROOT))["server_refs"],
                         load("public")["roles"]["mcp"]["server_refs"])
        errors = StringIO()
        with redirect_stderr(errors), self.assertRaises(SystemExit) as raised:
            resolver("seo-data:missing-test-provider", str(ROOT))
        self.assertEqual(raised.exception.code, 1)
        self.assertIn("seo-data/missing-test-provider.toml", errors.getvalue())

    def test_hosted_auth_headers_are_exact(self):
        specs = {
            "ahrefs": ("https://api.ahrefs.com/mcp/mcp", "Authorization", "Bearer {{ENV:AHREFS_MCP_TOKEN}}"),
            "semrush": ("https://mcp.semrush.com/v2/mcp", "Authorization", "Apikey {{ENV:SEMRUSH_API_KEY}}"),
            "seranking": ("https://api.seranking.com/mcp", "X-Api-Key", "{{ENV:SERANKING_API_KEY}}"),
        }
        for provider, (url, key, value) in specs.items():
            with self.subTest(provider=provider):
                server, = load(provider)["mcp"]["servers"]
                self.assertEqual(server["type"], "http")
                self.assertEqual(server["url"], url)
                self.assertEqual(server["headers"], {key: value})
                self.assertNotIn("deps", load(provider))

    def test_search_console_is_read_only(self):
        provider = load("search-console")
        server, = provider["mcp"]["servers"]
        expected = {"list_sites", "search_analytics", "enhanced_search_analytics",
                    "detect_quick_wins", "index_inspect", "list_sitemaps", "get_sitemap"}
        self.assertEqual(set(server["tools"]), expected)
        self.assertEqual(set(provider["roles"]["mcp"]["allowed_tools"]),
                         {"search-console:" + tool for tool in expected})
        self.assertEqual(server["env"], {
            "GOOGLE_APPLICATION_CREDENTIALS": "{{ENV:GOOGLE_APPLICATION_CREDENTIALS}}"})
        self.assertNotIn("submit_sitemap", server["tools"])

    def test_serpstat_excludes_mutation_categories(self):
        server, = load("serpstat")["mcp"]["servers"]
        self.assertEqual(server["env"]["SERPSTAT_API_TOKEN"], "{{ENV:SERPSTAT_API_TOKEN}}")
        self.assertEqual(server["env"]["SERPSTAT_ENABLED_CATEGORIES"],
                         "domain,keywords,backlinks,url,credits")
        self.assertNotIn("SERPSTAT_API_KEY", server["env"])

    def test_free_seo_is_pinned_restricted_and_opt_in(self):
        provider = load("free-seo")
        server, = provider["mcp"]["servers"]
        self.assertRegex(server["args"][3], r"^git\+https://\S+@[0-9a-f]{40}$")
        self.assertEqual(server["args"][:2], ["--python", "3.11"])
        self.assertEqual(set(server["tools"]), {"suggest", "trends_compare", "trends_related"})
        self.assertEqual(set(provider["roles"]["mcp"]["allowed_tools"]),
                         {"free-seo:" + tool for tool in server["tools"]})
        self.assertNotIn("env", server)
        self.assertNotEqual((CAP / "default.toml").resolve(), CAP / "free-seo.toml")

    def test_no_credential_arguments_and_deps_exist(self):
        for provider in PROVIDERS:
            data = load(provider)
            for dep in data.get("deps", {}).get("require", []):
                for ext in ("sh", "md"):
                    self.assertTrue((ROOT / f"deps/{dep}.{ext}").is_file())
            for server in data["mcp"]["servers"]:
                self.assertNotRegex(" ".join(server.get("args", [])), r"\{\{(?:ENV|INPUT):")
                for value in server.get("env", {}).values():
                    if "{{" in value:
                        self.assertRegex(value, r"^\{\{ENV:[A-Z0-9_]+\}\}$")


if __name__ == "__main__":
    unittest.main(verbosity=2)

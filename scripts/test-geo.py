#!/usr/bin/env python3
"""Offline GEO registry checks, not an engine or model-compliance test.

Run: PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-geo.py
"""
from pathlib import Path
import re
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/geo-visibility-audit/SKILL.md"


def activates(message, domain="seo"):
    """Exercise this skill's content()/match() subset; not the runtime parser."""
    frontmatter = SKILL.read_text().split("---", 2)[1]
    domains = re.search(r"^domains: (.+)$", frontmatter, re.M).group(1).split()
    if domain not in domains:
        return False
    for rule in re.findall(r"^  - (.+)$", frontmatter, re.M):
        if rule.startswith("content("):
            pattern = r"\b" + re.escape(rule[8:-1]) + r"\b"
        elif rule.startswith("match("):
            pattern = rule[6:-1]
        else:
            raise AssertionError(f"Unsupported test rule: {rule}")
        if re.search(pattern, message, re.I):
            return True
    return False


class RegistryContractTests(unittest.TestCase):
    def test_geo_requests_activate_only_in_seo(self):
        for message in ("GEO audit", "AEO", "AI search visibility", "AI-search tracking",
                        "buyer questions", "buying decisions", "citation gaps",
                        "ChatGPT does not recommend our app",
                        "Why aren't we listed in Perplexity?",
                        "Our brand never appears in Gemini", "AI Overviews", "AI Mode",
                        "generative engine optimization", "answer engine optimization"):
            with self.subTest(message=message):
                self.assertTrue(activates(message))
                self.assertFalse(activates(message, "developer"))

    def test_ordinary_seo_and_unrelated_requests_do_not_activate(self):
        for message in ("Audit this sitemap", "Fix our canonical tags", "Write a Rust parser",
                        "geography lessons", "Research long-tail keywords", "Claude API token pricing"):
            with self.subTest(message=message):
                self.assertFalse(activates(message))

    def test_measurement_guidance_has_no_invented_report(self):
        paths = ("agents/seo/audit.toml", "agents/seo/strategist.toml",
                 "skills/seo-keyword-research/SKILL.md", "skills/seo-content-audit/SKILL.md",
                 "skills/content-geo/SKILL.md")
        for path in paths:
            with self.subTest(path=path):
                text = (ROOT / path).read_text()
                self.assertNotRegex(text, r"Generative AI (?:performance )?report")
                self.assertIn("Web performance", text)

    def test_geo_scope_and_least_privilege_remain(self):
        text = SKILL.read_text()
        for guardrail in ("DR, keyword volume, paid tracking, and analytics access are not prerequisites",
                          "Propose a new page only after this check", "no automatic site-wide audit",
                          "Without engine access/captures", "Unverified"):
            self.assertIn(guardrail, text)
        for tag in ("audit", "strategist"):
            data = tomllib.loads((ROOT / f"agents/seo/{tag}.toml").read_text())
            self.assertIn("core", data["capabilities"])
            self.assertTrue({"runtime", "orchestration"}.isdisjoint(data["capabilities"]))
            self.assertIn("geo-visibility-audit", data["roles"][0]["system"])
        keyword = (ROOT / "skills/seo-keyword-research/SKILL.md").read_text()
        self.assertIn("DR and keyword volume aren't prerequisites", keyword)
        self.assertIn("overlapping activation doesn't change the requested deliverable", keyword)

    def test_dataforseo_mcp_is_wired_into_seo(self):
        capability = ROOT / "capabilities/seo-data"
        self.assertEqual((capability / "default.toml").resolve(),
                         capability / "public.toml")
        self.assertEqual(tomllib.loads((capability / "config.toml").read_text())["domains"],
                         ["seo"])
        provider = tomllib.loads((capability / "dataforseo.toml").read_text())
        self.assertEqual(provider["deps"]["require"], ["dataforseo/mcp-server"])
        server, = provider["mcp"]["servers"]
        self.assertEqual((server["type"], server["command"]), ("stdio", "npx"))
        self.assertRegex(server["args"][1], r"^dataforseo-mcp-server@\d+\.\d+\.\d+$")
        self.assertEqual(server["env"], {
            key: "{{ENV:" + key + "}}"
            for key in ("DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD")
        })
        self.assertEqual(set(provider["roles"]["mcp"]["allowed_tools"]), {
            "dataforseo:" + tool
            for tool in ("docs_index", "docs_list_sections", "docs_search", "api_request")
        })
        for tag in ("audit", "strategist"):
            manifest = tomllib.loads((ROOT / f"agents/seo/{tag}.toml").read_text())
            self.assertIn("seo-data", manifest["capabilities"])
        for name in ("geo-visibility-audit", "seo-keyword-research"):
            frontmatter = (ROOT / f"skills/{name}/SKILL.md").read_text().split("---", 2)[1]
            declared = re.search(r"^capabilities: (.+)$", frontmatter, re.M).group(1).split()
            self.assertIn("seo-data", declared)


if __name__ == "__main__":
    unittest.main(verbosity=2)

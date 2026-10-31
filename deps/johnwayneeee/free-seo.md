# johnwayneeee/free-seo

Experimental third-party keyword discovery server. This dep installs only uv; the capability supplies an immutable Git commit and uv provisions Python 3.11 at launch.

## MCP Server

- Source: https://github.com/JohnWayneeee/free-seo-mcp
- Transport: stdio
- Launch: `uvx --python 3.11 --from git+https://github.com/JohnWayneeee/free-seo-mcp@4d377bf6b7265ef2ea4c966c47546e9163b292e3 free-seo-mcp`
- No PyPI release was available when pinned. Transitive dependencies remain subject to upstream constraints.

## Authentication

Autocomplete and Trends need no key. Upstream Bing tools require `FREE_SEO_BING_API_KEY` from Bing Webmaster Tools; the registry research profile does not expose those tools or volume estimates. Unofficial upstream endpoints can rate-limit, block, or change; do not bypass CAPTCHAs.

## Available Tools

The capability exposes only autocomplete and relative Trends discovery. Trends is relative interest, not monthly search volume; sampled suggestions are not measured demand. The upstream server also advertises tools for Bing, Reddit, sitemaps, and local storage; they are not part of this restricted profile.

## Configuration Example

```toml
[[mcp.servers]]
name = "free-seo"
type = "stdio"
command = "uvx"
args = ["--python", "3.11", "--from", "git+https://github.com/JohnWayneeee/free-seo-mcp@4d377bf6b7265ef2ea4c966c47546e9163b292e3", "free-seo-mcp"]
timeout_seconds = 120
tools = ["suggest", "trends_compare", "trends_related"]
```

Select it with `[capabilities] seo-data = "free-seo"` in your Octomind config. The registry default stays public web search and page inspection.

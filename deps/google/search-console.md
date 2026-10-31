# google/search-console

Community Search Console MCP wrapper for authorized first-party search analytics and URL inspection; not a Google-published MCP server.

## MCP Server

- **Package**: `mcp-server-gsc`
- **Transport**: stdio
- **Command**: `npx -y mcp-server-gsc@0.3.0`

## Authentication

Enable the Search Console API in a Google Cloud project, create a service-account JSON key, and grant its email access to the specific Search Console property. Keep the file private, outside the repository; use an absolute path. Authentication uses Google OAuth 2.0 service-account credentials and the `webmasters.readonly` scope; no interactive login is needed.

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes | Service account JSON file path |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_sites` | Authorized properties |
| `search_analytics` | Basic query/page performance |
| `enhanced_search_analytics` | Up to 25,000 rows with filters |
| `detect_quick_wins` | Heuristic opportunities, not ranking guarantees |
| `index_inspect` | Index status for an authorized URL |
| `list_sitemaps`, `get_sitemap` | Read submitted sitemap information |

The upstream server also advertises `submit_sitemap`; the registry excludes it. Search Console Web performance totals include AI features, and its separate Generative AI performance report shows AI Overviews and AI Mode impressions, not clicks; verify which report this server's tools actually query. This provider supplies neither competitor metrics nor captured AI answers.

## Configuration Example

```toml
[[mcp.servers]]
name = "search-console"
type = "stdio"
command = "npx"
args = ["-y", "mcp-server-gsc@0.3.0"]
timeout_seconds = 120
env = { GOOGLE_APPLICATION_CREDENTIALS = "{{ENV:GOOGLE_APPLICATION_CREDENTIALS}}" }
tools = ["list_sites", "search_analytics", "enhanced_search_analytics", "detect_quick_wins", "index_inspect", "list_sitemaps", "get_sitemap"]
```

**Notes:** Supports regex filtering and automatic quick wins detection.

## Links

- [Homepage](https://www.npmjs.com/package/mcp-server-gsc)

# serpstat/serpstat

Official Serpstat MCP for keyword, domain, competitor, and backlink research. API calls may consume credits; confirm scope and budget before requesting data.

## MCP Server

- **Package**: `@serpstat/serpstat-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @serpstat/serpstat-mcp-server@1.1.5`

## Authentication

Obtain an API token from Serpstat account settings. Requires a plan with API access (documented as Team or higher; verify current entitlements).

| Variable | Required | Description |
|----------|----------|-------------|
| `SERPSTAT_API_TOKEN` | Yes | Serpstat API token; `SERPSTAT_API_KEY` is not read by this server |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_keywords_info`, `get_keyword_suggestions` | Keyword metrics and suggestions |
| `get_domain_keywords`, `get_domain_competitors` | Domain research |
| `get_backlinks_summary`, `get_referring_domains` | Backlink evidence |
| `get_credits_stats` | Usage and allowance |

The capability enables only `domain,keywords,backlinks,url,credits` categories, excluding project creation/deletion, audit settings changes, and scan execution. Provider metrics are not interchangeable with Ahrefs DR; results are not direct AI-answer observations.

## Configuration Example

```toml
[[mcp.servers]]
name = "serpstat"
type = "stdio"
command = "npx"
args = ["-y", "@serpstat/serpstat-mcp-server@1.1.5"]
timeout_seconds = 120
env = { SERPSTAT_API_TOKEN = "{{ENV:SERPSTAT_API_TOKEN}}", SERPSTAT_ENABLED_CATEGORIES = "domain,keywords,backlinks,url,credits" }
tools = []
```

**Notes:** Validate authentication and API entitlements separately from an MCP initialization/tools-list smoke test.

## Links

- [Homepage](https://www.npmjs.com/package/@serpstat/serpstat-mcp-server)

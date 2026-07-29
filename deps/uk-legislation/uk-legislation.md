# uk-legislation/uk-legislation

UK legislation MCP server over the official legislation.gov.uk API. Keyless; rate limit 3000 requests / 5 min / IP.

## MCP Server

- **Package**: `legislation-gov-uk-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y legislation-gov-uk-mcp`

## Authentication

None — the legislation.gov.uk API is public.

## Available Tools

| Tool | Description |
|------|-------------|
| `leg_search` / `leg_search_advanced` / `leg_search_new` | Search legislation by title, text, type, year |
| `leg_get` / `leg_get_section` / `leg_get_contents` | Fetch a document, section, or table of contents |
| `leg_get_version` | Point-in-time version of a provision |
| `leg_changes_affecting` / `leg_changes_by` | Amendment tracking in both directions |
| `leg_status` / `leg_types` / `leg_updates` | Document status, legislation types, updates feed |
| `leg_sparql` | SPARQL endpoint queries |

## Configuration Example

```toml
[[mcp.servers]]
name = "uk-law"
type = "stdio"
command = "npx"
args = ["-y", "legislation-gov-uk-mcp@1.0.2"]
timeout_seconds = 60
tools = []
```

**Notes:** Replaces the deprecated `@ansvar/uk-law-mcp`, which ships no database in any published version. Live API — needs network reach to legislation.gov.uk.

## Links

- [legislation-gov-uk-mcp on npm](https://www.npmjs.com/package/legislation-gov-uk-mcp)
- [legislation.gov.uk API](https://www.legislation.gov.uk/developer)

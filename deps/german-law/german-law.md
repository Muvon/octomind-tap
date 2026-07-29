# german-law/german-law

German federal law MCP server. Fetches statute XML live from gesetze-im-internet.de (Bundesministerium der Justiz), keyless.

## MCP Server

- **Package**: `german-law-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y german-law-mcp`

## Authentication

None — the gesetze-im-internet.de portal is public.

## Available Tools

| Tool | Description |
|------|-------------|
| `download_law` | Fetch a statute's XML by short name (e.g. `bgb`) |
| `get_paragraph` | Return a provision's verbatim text — takes `law_name` and `paragraph` with the `§ ` prefix (e.g. `§ 823`) |
| `list_contents` | Table of contents for a downloaded statute |

## Configuration Example

```toml
[[mcp.servers]]
name = "german-law"
type = "stdio"
command = "npx"
args = ["-y", "german-law-mcp@0.1.0"]
timeout_seconds = 60
tools = []
```

**Notes:** Replaces the deprecated `@ansvar/german-law-mcp`, which is broken in every published version and ships no data. This server fetches statutes on demand, so it needs network reach to gesetze-im-internet.de.

## Links

- [german-law-mcp on npm](https://www.npmjs.com/package/german-law-mcp)
- [Gesetze im Internet](https://www.gesetze-im-internet.de/)

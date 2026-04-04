# medical/medical

Medical data MCP server. Access FDA drug data, PubMed literature, WHO statistics, RxNorm nomenclature, and clinical guidelines.

## MCP Server

- **Package**: `medical-mcp`
- **Transport**: stdio
- **Command**: `npx -y medical-mcp`

## Authentication

None required (zero configuration)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `search-drugs` | Search FDA drugs |
| `get-drug-details` | Drug details |
| `search-medical-literature` | PubMed search |
| `get-health-statistics` | WHO statistics |
| `search-drug-nomenclature` | RxNorm lookup |
| `search-clinical-guidelines` | Clinical guidelines |
| `search-google-scholar` | Scholar search |

## Configuration Example

```toml
[[mcp.servers]]
name = "medical"
type = "stdio"
command = "npx"
args = ["-y", "medical-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** No API keys needed. Built-in caching. Public health data sources.

## Links

- [Homepage](https://github.com/JamesANZ/medical-mcp)

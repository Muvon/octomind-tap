# e2b/e2b

E2B secure code execution sandbox MCP server. Run Python and JavaScript code in isolated cloud environments.

## MCP Server

- **Package**: `@e2b/mcp-server`
- **Transport**: stdio
- **Command**: `npx @e2b/mcp-server`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `E2B_API_KEY` | Yes | API key from e2b.dev |

## Available Tools

| Tool | Description |
|------|-------------|
| `execute_code` | Execute code in sandbox |
| `manage_files` | File operations |
| `manage_processes` | Process management |

## Configuration Example

```toml
[[mcp.servers]]
name = "e2b"
type = "stdio"
command = "npx"
args = ["-y", "@e2b/mcp-server"]
timeout_seconds = 60
env = { E2B_API_KEY = "your-value" }
tools = []
```

**Notes:** Paid API with free tier. Isolated execution environments.

## Links

- [Homepage](https://www.npmjs.com/package/@e2b/mcp-server)

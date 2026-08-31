# <org>/<tool>

<What this MCP server provides and when the capability uses it.>

## MCP Server

- Package: `<package or image>`
- Transport: `stdio`
- Command: `<command and arguments>`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `API_KEY` | Yes | <Purpose and where to obtain it> |

## Available Tools

| Tool | Description |
|------|-------------|
| `<tool_name>` | <What it does> |

## Configuration Example

```toml
[[mcp.servers]]
name = "<server-name>"
type = "stdio"
command = "<command>"
args = ["<arg>"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://example.com)
- [Documentation](https://example.com/docs)


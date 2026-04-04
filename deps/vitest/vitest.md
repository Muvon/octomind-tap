# vitest/vitest

Vitest testing MCP server. Run tests, list test files, and analyze code coverage.

## MCP Server

- **Package**: `@djankies/vitest-mcp`
- **Transport**: stdio
- **Command**: `npx -y @djankies/vitest-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `set_project_root` | Set project root |
| `list_tests` | List test files |
| `run_tests` | Execute tests |
| `analyze_coverage` | Coverage analysis |

## Configuration Example

```toml
[[mcp.servers]]
name = "vitest"
type = "stdio"
command = "npx"
args = ["-y", "@djankies/vitest-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** Requires Vitest 0.34.0+. Optional: @vitest/coverage-v8 for coverage.

## Links

- [Homepage](https://www.npmjs.com/package/@djankies/vitest-mcp)

# nodejs/node

Installs Node.js LTS (required for npx-based MCP servers)

## Key Commands

| Command | Description |
|---------|-------------|
| `node` | Run node |
| `node --help` | Show help and available options |
| `node --version` | Show installed version |

## Common Usage

```bash
# Check if installed
node --version

# Show help
node --help
```

The default minimum is Node.js 20. A dep that needs a newer runtime can call
`NODE_MIN_MAJOR=22 install_dep nodejs/node`; the override applies to that invocation
and prevents the fast path from accepting an older installation.

## Links

- [Homepage](https://nodejs.org)

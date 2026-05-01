# remotion/remotion

Remotion MCP server. Programmatic React-based video composition. Render templated explainer videos, slideshow ads, motion-graphics overlays, and data-driven creative variants. Renders locally via `npx remotion render` or at scale via Remotion Lambda.

## MCP Server

- **Package**: `remotion-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y remotion-mcp`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `REMOTION_LICENSE_KEY` | No (free for ≤3 employees) | Required for company use of Remotion (paid tiers above) |
| `AWS_ACCESS_KEY_ID` | Optional | For Remotion Lambda renders |
| `AWS_SECRET_ACCESS_KEY` | Optional | For Remotion Lambda renders |
| `AWS_REGION` | Optional | Lambda region |

## Available Tools

| Tool | Description |
|------|-------------|
| `remotion_render_local` | Render a Remotion composition to MP4 locally |
| `remotion_render_lambda` | Render via AWS Lambda for parallelism |
| `remotion_get_compositions` | List compositions in a project |
| `remotion_install_template` | Scaffold a Remotion project template (slideshow, explainer, captions) |

## Configuration Example

```toml
[[mcp.servers]]
name = "remotion"
type = "stdio"
command = "npx"
args = ["-y", "remotion-mcp"]
timeout_seconds = 300
env = { REMOTION_LICENSE_KEY = "{{INPUT:REMOTION_LICENSE_KEY}}" }
tools = []
```

**Notes:** Best for templated ad variants ("100 versions of the same hero shot with different copy and product images"). Requires Chrome/Chromium under the hood — bundled by `@remotion/renderer` automatically.

## Links

- [Remotion docs](https://www.remotion.dev/docs/)
- [Remotion Lambda](https://www.remotion.dev/docs/lambda)

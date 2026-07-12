# aas-ee/open-websearch

Open-WebSearch MCP server. Keyless multi-engine web search — DuckDuckGo, Bing, Startpage, Brave and others via public HTML endpoints, no API keys required.

## MCP Server

- **Package**: `open-websearch`
- **Transport**: stdio
- **Command**: `npx -y open-websearch@latest`

## Authentication

None — queries public search-engine HTML endpoints, no API key or account required.

## Available Tools

| Tool | Description |
|------|-------------|
| `search` | Multi-engine web search returning titles, URLs, and descriptions |
| `fetchWebContent` | Generic HTTP(S) page / Markdown content fetch |
| `fetchGithubReadme` | Fetch a GitHub repository README |
| `fetchCsdnArticle` | Fetch a CSDN article |
| `fetchJuejinArticle` | Fetch a Juejin article |
| `fetchLinuxDoArticle` | Fetch a Linux.do article |

## Configuration Example

```toml
[[mcp.servers]]
name = "open-websearch"
type = "stdio"
command = "npx"
args = ["-y", "open-websearch@latest"]
timeout_seconds = 60
env = { MODE = "stdio", DEFAULT_SEARCH_ENGINE = "duckduckgo", ALLOWED_SEARCH_ENGINES = "duckduckgo,bing,startpage,brave" }
tools = []
```

**Notes:** Requires Node.js >= 20 (crashes on 18: missing `File` global in undici). `MODE=stdio` is required — the server's default mode (`both`) also starts an HTTP listener on port 3000. `DEFAULT_SEARCH_ENGINE` picks the primary engine; `ALLOWED_SEARCH_ENGINES` limits which engines may be used, and if the default is not in the list the first allowed engine wins. Engines are queried without API keys, so results depend on public endpoint availability — the multi-engine list provides fallback. Optional: `USE_PROXY=true` + `PROXY_URL` for restricted networks.

## Links

- [Homepage](https://github.com/Aas-ee/open-webSearch)

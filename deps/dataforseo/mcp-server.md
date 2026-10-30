# dataforseo/mcp-server

Official DataForSEO MCP server for keyword metrics, SERPs, competitor research, and backlink data. The dep ensures Node.js 22+ and npx; the `seo-data` capability pins the server package.

## MCP Server

- Package: `dataforseo-mcp-server@3.1.3`
- Transport: stdio (the package's default mode)
- Launch: `npx -y dataforseo-mcp-server@3.1.3`
- Runtime: Node.js 22+ with npx, on macOS, Linux, or Windows Git Bash
- Source: <https://github.com/dataforseo/mcp-server-typescript>

The installer delegates platform handling to `nodejs/node` with a minimum major version of 22 and verifies the result. It does not store credentials or run paid API requests.

## Authentication

Get API credentials at <https://app.dataforseo.com/api-access>. These are an API login and API password, not a single API key or the account password.

| Variable | Required | Purpose |
|---|---|---|
| `DATAFORSEO_LOGIN` | Yes | DataForSEO API login |
| `DATAFORSEO_PASSWORD` | Yes | DataForSEO API password |

Set both in the environment used to launch Octomind. Keep secret values out of manifests, prompts, command arguments, and git. The capability passes them to the child through `env`; Octomind withholds it when either is missing. Upstream also accepts `DATAFORSEO_USERNAME` as a login alias, but this wiring uses `DATAFORSEO_LOGIN`.

No OAuth is used for stdio. The separately hosted OAuth endpoint is <https://mcp.dataforseo.com/v3/mcp>; it is not the provider configured here.

## Available Tools

| Tool | Purpose |
|---|---|
| `docs_index` | Find API documentation, optionally by section |
| `docs_list_sections` | List available documentation sections |
| `docs_search` | Read the documentation for a specific endpoint |
| `api_request` | Make an authenticated DataForSEO API request |

Read endpoint documentation first; use the documented HTTP method, path, and JSON body rather than guessing. `api_request` uses `.ai` paths by default; its `noAiMode` option selects standard paths. Check response and task status codes before treating a result as evidence.

API requests may consume account balance. Confirm the research scope, location, language, sample size, and budget before billable calls; don't run bulk requests or automatic retries without approval. Preserve returned costs, timestamps, and provider/endpoint provenance. A handshake and `tools/list` do not test credentials, account balance, or data access.

Provider keyword/authority estimates are not Ahrefs DR or observed demand. A provider result is evidence only for its documented surface and capture conditions, not a substitute for a ChatGPT UI run or proof of market-wide AI visibility.

## Configuration Example

Agents declare `seo-data` in their top-level `capabilities`; this server block belongs only in the capability provider file:

```toml
[[mcp.servers]]
name = "dataforseo"
type = "stdio"
command = "npx"
args = ["-y", "dataforseo-mcp-server@3.1.3"]
timeout_seconds = 120
env = { DATAFORSEO_LOGIN = "{{ENV:DATAFORSEO_LOGIN}}", DATAFORSEO_PASSWORD = "{{ENV:DATAFORSEO_PASSWORD}}" }
tools = []
```

Validate without paid requests:

```bash
bash deps/dataforseo/mcp-server.sh
bash scripts/lint-deps.sh deps/dataforseo/mcp-server.sh
bash scripts/lint-capabilities.sh capabilities/seo-data
scripts/mcp-versions.sh test seo-data
bin/load seo:audit
bin/load seo:strategist
```

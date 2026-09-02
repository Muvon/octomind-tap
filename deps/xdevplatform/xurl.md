# xdevplatform/xurl

Official X (Twitter) MCP access. `xurl mcp` is X's open-source local bridge to the hosted MCP server at `https://api.x.com/mcp` — it performs the OAuth 2.0 PKCE login, caches tokens in `~/.xurl`, auto-refreshes them, and injects a fresh Bearer token on every call. Write tools (posting, bookmarks, Articles) require this user-context bridge; a static app-only Bearer covers read endpoints only.

## MCP Server

- **Package**: `@xdevplatform/xurl` (official, X Developer Platform)
- **Transport**: stdio (bridge to hosted Streamable HTTP at `api.x.com/mcp`)
- **Command**: `npx -y @xdevplatform/xurl mcp https://api.x.com/mcp`

## Authentication

OAuth 2.0 user context via the bridge. Create an app in the [X Developer Portal](https://developer.x.com) with OAuth 2.0 enabled and register the redirect URI `http://localhost:8080/callback`. On first run with no cached token the bridge opens a browser for a one-time login; on headless machines authenticate once out-of-band with `xurl auth oauth2 --headless` (export the credentials in that shell first).

Credential resolution order: `CLIENT_ID`/`CLIENT_SECRET` env vars, then the active app in `~/.xurl`. Those names are too generic for a shared session env, so capability manifests collect `X_`-prefixed vars and remap them in a launch wrapper.

| Variable | Required | Description |
|----------|----------|-------------|
| `X_CLIENT_ID` | Yes | OAuth 2.0 client ID from the app's Keys and tokens page |
| `X_CLIENT_SECRET` | Yes | OAuth 2.0 client secret |

## Available Tools

The hosted server converts the X API OpenAPI spec into MCP tools (200+ endpoints; streaming and webhooks excluded). Publishing-relevant subset:

| Tool | Description |
|------|-------------|
| `createPosts` / `deletePosts` | Post (and thread via reply chains) / delete |
| `getPostsById` / `getUsersPosts` / `getUsersMentions` | Read own posts and mentions |
| `searchPostsRecent` | Recent post search |
| `getPostsAnalytics` / `getMediaAnalytics` | Performance data |
| `initializeMediaUpload` / `appendMediaUpload` / `finalizeMediaUpload` | Chunked media upload |
| `getUsersMe` | Resolve the authorized account |

## Configuration Example

```toml
[[mcp.servers]]
name = "x"
type = "stdio"
command = "sh"
args = ["-c", "CLIENT_ID=\"$X_CLIENT_ID\" CLIENT_SECRET=\"$X_CLIENT_SECRET\" exec npx -y @xdevplatform/xurl@1.3.1 mcp https://api.x.com/mcp"]
timeout_seconds = 300
env = { X_CLIENT_ID = "{{ENV:X_CLIENT_ID}}", X_CLIENT_SECRET = "{{ENV:X_CLIENT_SECRET}}" }
tools = []
```

**Notes:** First-run login holds the MCP handshake until the browser flow completes — give it a generous timeout, or pre-authenticate with `xurl auth oauth2 --headless`. The OAuth login authorizes whichever X account is signed in when the browser opens; switch to the bot account first, or pass `-u <user>` in args.

## Links

- [X MCP docs](https://docs.x.com/tools/mcp)
- [xurl on GitHub](https://github.com/xdevplatform/xurl)

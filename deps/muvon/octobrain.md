# muvon/octobrain

Octomind's persistent memory + smart fetcher, exposed as one MCP server. Two functional surfaces, each surfaced through a different tap capability:

| Capability | Provider file | Tool exposed | What it's for |
|------------|---------------|--------------|---------------|
| `memory-read` | `capabilities/memory-read/octobrain.toml` (default) | `remember`, `memory_graph` | Read-only semantic recall and relationship-graph traversal. Load at task start to pick up prior context. |
| `memory-write` | `capabilities/memory-write/octobrain.toml` (default) | `memorize`, `forget`, `relate` | Mutations — create new memories, delete obsolete ones, and add typed edges. Pair with `memory-read` on agents that learn. |
| `webfetch` | `capabilities/webfetch/octobrain.toml` (default) | `knowledge` | URL / file fetcher with semantic chunking for big sources and full-read fallback. Replaces basic mcp-server-fetch. |

All three capabilities point to the same underlying `octobrain mcp` server (one process, three surfaces); `allowed_tools` per capability controls which subset is exposed — same pattern as `filesystem-read` / `filesystem-write` against `octofs`. The `webfetch/fetch.toml` alternative (mcp-server-fetch) is kept available for anyone who explicitly wants the ultra-light one-shot fetcher — switch with `ln -sf fetch.toml capabilities/webfetch/default.toml`.

## Key Commands

| Command | Description |
|---------|-------------|
| `octobrain` | Run octobrain |
| `octobrain mcp` | Start the MCP stdio server (used by both capabilities) |
| `octobrain --help` | Show help |
| `octobrain --version` | Show installed version |

## Common Usage

```bash
# Start the MCP stdio server (typical invocation from capability files)
octobrain mcp

# Check installed version
octobrain --version
```

## Memory surfaces (capabilities: `memory-read` + `memory-write`)

Read-only (`memory-read`):
- `remember` — semantic search across stored memories (returns 1-hop graph neighbors)
- `memory_graph` — traverse the relationship graph (depth 2+)

Mutations (`memory-write`):
- `memorize` — store a fact with importance, tags, project scoping, trust tier
- `forget` — permanent delete (requires `confirm=true`)
- `relate` — create typed edge between two memories (`related_to`, `depends_on`, `supersedes`, `similar`, `conflicts`, `implements`, `extends`)

An agent that only needs to load context at task start can declare just `memory-read`. Agents that learn and persist new facts declare both.

## Webfetch surface (capability: `webfetch`, default provider)

The `knowledge` tool is the fetch implementation. The agent calls one tool; the tool handles retrieval, parsing (`.html` → markdown, `.pdf` / `.docx` → text), and chunking transparently.

Internal command surface (for understanding how it works — the agent doesn't choose between these, the tool routes by argument shape):

- `read` — return the FULL text content of a URL or local file. Use as fallback when semantic retrieval is insufficient.
- `search` — when the source is big, prefer semantic search WITHIN that URL/file: pass `source=<url|path>` plus a `query`, get back only the relevant chunks instead of the whole document. Much cheaper context than `read` for long sources.
- `match` — regex/exact-string lookup over the fetched content (function names, error codes, version strings).
- `store` / `delete` — session-scoped raw text cache by key.

Supported sources: `http://`, `https://`, `file:///path`, `/absolute/path`. File types: `.html`, `.txt`, `.md`, `.pdf`, `.docx`.

### Why this is the webfetch default

`mcp-server-fetch` does URL → markdown, one-shot. No PDF, no DOCX, no chunking — a 200-page PDF blows out the model's context window. `octobrain knowledge` handles the parsing, lets semantic chunking pull only the relevant section for the question, and falls back to full read when needed. Strictly better defaults for content / research / grounding workflows.

## Configuration Example

Both capabilities share this MCP server entry; the `allowed_tools` in each capability file decides which surface is exposed:

```toml
[[mcp.servers]]
name = "octobrain"
type = "stdio"
command = "octobrain"
args = ["mcp"]
timeout_seconds = 300
tools = []
```

## Links

- [Homepage](https://github.com/muvon/octobrain)

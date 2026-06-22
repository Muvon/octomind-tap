# muvon/octobrain

Octomind's persistent memory + knowledge engine, exposed as one MCP server. Memory and knowledge surfaces, each surfaced through a different tap capability:

| Capability | Provider file | Tool exposed | What it's for |
|------------|---------------|--------------|---------------|
| `memory-read` | `capabilities/memory-read/octobrain.toml` (default) | `remember` | Read-only semantic recall; `remember` returns matching memories plus their 1-hop graph neighbors. Load at task start to pick up prior context. |
| `memory-write` | `capabilities/memory-write/octobrain.toml` (default) | `memorize`, `forget` | Mutations — create new memories (with inline `related_to` links) and delete obsolete ones. Pair with `memory-read` on agents that learn. |
| `knowledge` | `capabilities/knowledge/octobrain.toml` (default) | `knowledge` | Persistent PROJECT knowledge base — semantic search over `.box` docs, subscribed org boxes, and indexed files, scoped to the active project. |
| `webfetch` | `capabilities/webfetch/octobrain.toml` (default) | `knowledge` | Single URL / file fetcher with semantic chunking for big sources and full-read fallback. Replaces basic mcp-server-fetch. |

All capabilities point to the same underlying `octobrain mcp` server (one process); `allowed_tools` per capability controls which subset is exposed — same pattern as `filesystem-read` / `filesystem-write` against `octofs`. `knowledge` and `webfetch` expose the *same* `knowledge` tool — they differ only in framing/triggers: `knowledge` for recalling persistent project knowledge (the box system), `webfetch` for fetching one URL/file raw. The `webfetch/fetch.toml` alternative (mcp-server-fetch) is kept available for anyone who explicitly wants the ultra-light one-shot fetcher — switch with `ln -sf fetch.toml capabilities/webfetch/default.toml`.

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
- `remember` — semantic search across stored memories (returns the matches plus their 1-hop graph neighbors)

Mutations (`memory-write`):
- `memorize` — store a fact with importance, tags, project scoping, trust tier; pass `related_to=[{target_id, relationship_type}]` to link it to existing memories in the same call (`related_to`, `depends_on`, `supersedes`, `similar`, `conflicts`, `implements`, `extends`, `achieves`, `closes`)
- `forget` — permanent delete (requires `confirm=true`)

An agent that only needs to load context at task start can declare just `memory-read`. Agents that learn and persist new facts declare both.

## Project knowledge surface (capability: `knowledge`, default provider)

Same `knowledge` tool, framed for **persistent project knowledge** rather than one-shot fetch. Octobrain maintains a scoped, git-backed **knowledge box** system and re-embeds it locally:

- **Project box** — a `.box/` folder at the repo root: source docs octobrain indexes and makes searchable, scoped exactly like memories (project → org → global).
- **Org / global boxes** — subscribed `octobrain-box` repos, auto-probed per org and addressed via `box://` URIs.
- The MCP server runs a background sync that discovers and refreshes these boxes for the active project — no manual index step.

The agent just calls `knowledge` with `command=search` and **no `source`** → semantic search across everything indexed for the active scope (box docs + any files indexed on the fly). Use `command=match` for regex/exact-string lookup over the same indexed content. To pull a specific section of one document instead of the whole project, pass `source=<url|file>` (that's the `webfetch` framing below). Boxes ship source files only — never vectors; octobrain owns the embeddings.

### Why a separate capability from `webfetch`

Same underlying tool, different intent and triggers. `knowledge` activates on "what does the project/knowledge base know about X" — recall over persistent, indexed, project-scoped docs. `webfetch` activates on "fetch this URL/file" — one source, raw content. Splitting the capability gives each the right trigger phrases so routing picks octobrain for knowledge-recall tasks without conflating them with raw fetching.

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

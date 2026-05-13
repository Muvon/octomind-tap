# oven-sh/bun

Installs Bun — fast all-in-one JavaScript/TypeScript runtime, package manager, bundler, and test runner. Drop-in replacement for `node`, `npm`, `npx`, `yarn`, `pnpm`, and `vite dev`.

## Key Commands

| Command | Description |
|---------|-------------|
| `bun` | Run a JS/TS file with the Bun runtime |
| `bun run <script>` | Run a `package.json` script (replaces `npm run`) |
| `bun install` / `bun i` | Install dependencies (replaces `npm install`) |
| `bun add <pkg>` | Add a dependency (replaces `npm install <pkg>`) |
| `bun remove <pkg>` | Remove a dependency |
| `bunx <pkg>` | Execute a package binary (replaces `npx`) |
| `bun build` | Bundle for production (replaces `vite build`, `webpack`, `esbuild`) |
| `bun test` | Run tests (Jest-compatible API) |
| `bun create <template>` | Scaffold a new project (replaces `npm create`) |
| `bun --hot <file>` | Run with hot reload (replaces `vite dev` / `nodemon`) |
| `bun --version` | Show installed version |

## Common Usage

```bash
# Replace npm/npx with bun/bunx everywhere
bun install                    # instead of npm install
bun add react                  # instead of npm install react
bun add -d typescript          # instead of npm install -D typescript
bun run dev                    # instead of npm run dev
bunx create-svelte my-app      # instead of npx create-svelte my-app
bunx @sveltejs/mcp             # run MCP server packages

# Native TypeScript — no tsc / ts-node / vite required
bun run src/index.ts

# Hot reload for dev servers
bun --hot src/server.ts

# Production bundling (replaces vite build)
bun build ./src/index.ts --outdir ./dist --minify

# Run tests (Jest-compatible)
bun test
```

## Why Bun over Node + npm + vite

- Single binary replaces node, npm, npx, yarn, pnpm, vite, esbuild, webpack, ts-node, nodemon
- Native TypeScript and JSX execution — no transpile step
- ~10–30× faster install than npm, ~5× faster startup than node
- Built-in bundler, test runner, `.env` loader, and SQLite driver
- Node-compatible: `require`, `node:*` modules, npm registry all work

## Links

- [Homepage](https://bun.sh)
- [Docs](https://bun.sh/docs)
- [GitHub](https://github.com/oven-sh/bun)

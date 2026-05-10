---
name: programming-typescript
title: "TypeScript Development"
description: "Type-first TypeScript architecture, module boundaries, and pragmatic library choices. Auto-activates in TypeScript projects."
license: Apache-2.0
compatibility: "Requires Node.js and a package manager (npm/pnpm/yarn)."
capabilities: programming-nodejs
domains: developer
rules:
  - file(tsconfig.json)
  - content(typescript)
---

## Mental model

TypeScript's value is the type system at boundaries — between modules, packages, and processes. Type internals when it pays for itself; type boundaries always. Most maintenance pain comes from `any` leaking through one layer and infecting the whole call graph, or from runtime data assumed to match its declared type without validation.

## Type-driven design

- Make illegal states unrepresentable: discriminated unions with a `kind` field beat optional fields and boolean flags
- `unknown` at the edge of trust (external input, JSON, errors in `catch`), narrowed by a runtime check before use
- `as` assertions silently lie — prefer `satisfies` for inference, or a runtime validator (`zod`, `valibot`, `arktype`) when the value is external
- Prefer `readonly` arrays and `Readonly<T>` for inputs — signals intent and prevents accidental mutation
- Branded/nominal types for domain identifiers (`type UserId = string & { __brand: 'UserId' }`) — stops cross-wiring different IDs

## Modules and boundaries

- One concept per file; named exports over default exports — refactor tools and IDEs handle them better
- A package's entry point declares the public surface; internals stay internal even if technically reachable
- Path aliases in `tsconfig.json` keep imports stable across moves — mirror them in the bundler/runtime resolver
- ESM is the default for new code; CJS only when integrating with legacy
- Separate types from values when crossing package boundaries (`import type { ... }`) — keeps runtime bundles lean

## Async patterns

- `async`/`await` everywhere; raw `.then` chains are legacy
- `Promise.all` for parallel work that must all succeed; `Promise.allSettled` when partial results are useful
- An async function that doesn't await anything probably shouldn't be async — return the value directly
- Cancellation flows through `AbortSignal` — accept one on any function that does I/O, pass it down
- Errors thrown inside async iteration (`for await`) propagate normally; handle them where they're meaningful

## Error handling

- Throw for programmer errors and unexpected conditions; return `Result`-shaped values for expected failures in hot paths
- Custom error classes extend `Error` and set `name` — enables `instanceof` and structured logging
- `cause` (ES2022) preserves the original error: `throw new AppError('loading user', { cause: err })`
- In `catch (err)` the type is `unknown` — narrow before reading properties

## Architecture

- Dependency direction goes inward: domain logic doesn't import from web/CLI/DB layers — inject those via interfaces
- Keep business logic in framework-free modules; the framework adapter is a thin wrapper
- Side effects at the edge: pure functions in the core simplify testing and avoid mock sprawl
- Configuration is a typed value passed at startup, not a global to mutate

## Ecosystem defaults

- Node servers: Fastify or Hono for new projects; Express is fine but pre-modern
- Full-stack: Next.js (App Router) or Remix
- Frontend: React with TanStack Query for server state; Svelte/SvelteKit; Solid where fine-grained reactivity helps
- Validation at boundaries: `zod` is the default; `valibot` when bundle size matters
- ORMs: Prisma for productivity, Drizzle for control and small bundles
- HTTP client: `fetch` (native everywhere now); `ky` or `ofetch` for ergonomics
- Testing: Vitest for new projects; Playwright for E2E; MSW for HTTP-level mocking

## Project layout

- `src/` for sources, `dist/` for build output (gitignored)
- Monorepo with pnpm workspaces + Turborepo when sharing types/code across apps
- Per-package `tsconfig.json` extending a shared base; `tsc --build` with project references for fast incremental builds
- Co-locate tests with code (`foo.ts` + `foo.test.ts`) for unit, separate `e2e/` directory for integration

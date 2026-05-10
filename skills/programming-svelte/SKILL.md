---
name: programming-svelte
title: "Svelte Development"
description: "Svelte 5 runes, SvelteKit architecture, server/client boundaries, and progressive enhancement. Auto-activates in Svelte projects."
license: Apache-2.0
compatibility: "Requires Node.js and a package manager."
capabilities: programming-nodejs svelte
domains: developer
rules:
  - file(svelte.config.js)
  - file(svelte.config.ts)
  - grep(svelte, package.json)
  - content(svelte)
---

## Mental model

Svelte 5 compiles components to small, efficient updates; SvelteKit adds routing, server-side rendering, and form actions on top. The Svelte advantage is its compiler — most apps need very little client state management, no global store libraries, and no `useEffect`-style synchronization. Most maintenance trouble comes from importing React habits: pushing everything client-side, manual derived state, and effects doing the job of derivations.

## Runes (Svelte 5)

- `$state(...)` for reactive local state — replaces top-level `let` reactivity
- `$derived(...)` for computed values — replaces the old `$:` reactive blocks; deep dependency tracking is automatic
- `$effect(...)` for side effects only (DOM, subscriptions, non-Svelte libraries) — never for derived values
- `$props()` for typed component props; `$bindable()` for two-way bindable props
- Runes work in `.svelte.ts` / `.svelte.js` files too — extract reactive logic into modules
- Avoid effects that read state and write state — they create loops and obscure data flow

## Component design

- One component per `.svelte` file; `<script lang="ts">` → markup → `<style>` ordering
- Props are an API — type them with `$props<{...}>()` and document defaults
- Snippets (Svelte 5) replace slots for reusable markup with parameters
- Keep components small; extract sub-components when sections have their own state or events
- Scoped styles by default — global styles only via `:global(...)` when intentional

## SvelteKit architecture

- File-based routing in `src/routes/`: `+page.svelte` (page), `+layout.svelte` (shared layout), `+page.ts` / `+page.server.ts` (load), `+server.ts` (API endpoints)
- `+page.server.ts` runs only on the server — safe for database queries, secrets, server-only deps
- `+page.ts` runs on both server and client (universal) — pure data fetching that can hydrate
- `load` functions return data the page renders; throw `redirect()` / `error()` for control flow
- Layouts compose; place shared data loading at the layout level and child pages inherit via `$page.data`
- `hooks.server.ts` for cross-cutting concerns: auth, request logging, CSRF, response headers

## Forms and mutations

- Form actions (`+page.server.ts` `actions = { default: ... }`) for mutations — progressive-enhancement friendly, work without JS
- `use:enhance` upgrades the form to a fetch-driven submission with optimistic updates
- Validate on the server; share validation schemas (zod/valibot) between client and server when both validate
- Return validation errors from actions; the page renders them via `form` prop
- Use API endpoints (`+server.ts`) for non-form mutations, third-party integrations, or non-HTML responses

## State management

- Local reactive state with `$state` covers most needs — no global store library required for typical apps
- Cross-component shared state: a module exporting a `$state` object, imported where needed
- The `$page` store and SvelteKit's `goto`/`invalidate` cover URL-driven state and re-fetching
- Persist state in URL search params, cookies, or localStorage — not in long-lived module-level reactive state across navigations
- Avoid the legacy `writable`/`readable`/`derived` stores for new code unless interop demands them — runes replace them

## Server/client boundary

- Server-only code lives in `+page.server.ts`, `+server.ts`, `+layout.server.ts`, and `$lib/server/` — anything else may be bundled to the client
- Secrets and server-only modules go behind the `$lib/server/` boundary; SvelteKit fails the build if they leak to client code
- Environment variables: `$env/static/private` (server, build-time), `$env/static/public` (client-safe, build-time), `$env/dynamic/*` (runtime)
- Stream data with `await streamed.foo` in load functions — page renders progressively without blocking on slow data

## Performance

- Svelte's compiler already optimizes updates — micro-optimizations are rarely needed
- Code-split happens at route boundaries automatically
- Lazy-load heavy components with dynamic `import()` when they're conditionally rendered
- Use `{#key value}{/key}` to force a subtree to recreate when identity changes

## Testing

- Vitest for unit and component logic
- `@testing-library/svelte` for component tests — query by role and text, not by component internals
- Playwright for end-to-end flows — particularly important for form actions and progressive enhancement paths
- Mock at the network layer (MSW) rather than mocking `fetch`

## Project layout

- `src/lib/` for reusable code (`$lib` alias); `src/lib/server/` for server-only modules
- Feature folders inside `src/lib/` when the app grows; routes stay slim and import features
- Components, types, and utilities colocated by feature, not split by kind

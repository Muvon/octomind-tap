---
name: programming-svelte
title: "Svelte Development"
description: "Svelte 5 runes, SvelteKit routing, reactive components, stores, and modern Svelte ecosystem best practices. Auto-activates in Svelte projects."
license: Apache-2.0
compatibility: "Requires Node.js and npm/pnpm."
capabilities: programming-nodejs svelte
domains: developer
activate:
  - on: any
    rule: file(svelte.config.js)
  - on: user
    rule: content(svelte)
---

# Svelte Development

## Conventions

- Svelte 5 runes first — `$state`, `$derived`, `$effect`, `$props`
- SvelteKit conventions — `+page.svelte`, `+layout.svelte`, `+page.ts`, `+server.ts`
- TypeScript by default — `lang="ts"` in `<script>` blocks
- Scoped styles — keep styles in `<style>` blocks
- Minimal JS — leverage Svelte's compiler over manual DOM work
- Accessibility — semantic HTML, ARIA attributes, keyboard navigation
- Use Svelte MCP server for official API/docs lookups

## Reactivity (Svelte 5 Runes)

- `$state()` — reactive local state (replaces `let`)
- `$derived()` — computed values (replaces `$:` reactive)
- `$effect()` — side effects (replaces `onMount` + `$:`)
- `$props()` — typed component props (replaces `export let`)
- `$bindable()` — two-way bindable props
- Avoid `$effect` for derived values — use `$derived`

## SvelteKit Routing

- File-based routing in `src/routes/`
- `+page.svelte` — page component
- `+layout.svelte` — shared layout
- `+page.ts` / `+page.server.ts` — load functions
- `+server.ts` — API endpoints
- Form actions for progressive enhancement

## Stores

- `writable()` for mutable shared state
- `readable()` for external data sources
- `derived()` for computed store values
- Auto-subscribe with `$` prefix in templates

## Component Structure

- One component per file (`.svelte`)
- `<script lang="ts">` → markup → `<style>` ordering
- Prefer snippets over slots (Svelte 5)

## Testing

- Vitest for unit tests
- `@testing-library/svelte` for component tests
- Playwright for end-to-end tests

## Tooling

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run check` | svelte-check |
| `npm test` | Run Vitest |
| `npx playwright test` | E2E tests |

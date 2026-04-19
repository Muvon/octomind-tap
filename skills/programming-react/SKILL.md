---
name: programming-react
title: "React Development"
description: "React hooks, component patterns, state management, TypeScript integration, and modern React 18/19 best practices. Auto-activates in React projects."
license: Apache-2.0
compatibility: "Requires Node.js and npm/pnpm."
capabilities: programming-nodejs
domains: developer
activate:
  - on: any
    rule: file(package.json)
  - on: user
    rule: content(react)
---

# React Development

## Conventions

- Hooks-first — functional components + hooks only, no class components
- TypeScript by default — all components typed with proper prop interfaces
- Composition over inheritance — small, focused components
- Colocation — keep state close to where it's used
- Server Components first (Next.js/React 19) — client components only for interactivity

## Component Structure

- One component per file
- Named exports preferred over default exports
- Props interface defined above the component
- Keep components small (single responsibility)
- Composition with `children`/render props over prop drilling

## Hooks

- `useState` — local UI state only
- `useReducer` — complex state with multiple sub-values
- `useEffect` — sync with external systems only (not for derived state)
- `useMemo` / `useCallback` — only when profiling shows real perf problem
- `useRef` — DOM refs and mutable non-reactive values
- Custom hooks — prefix with `use`, extract reusable logic
- Never call hooks conditionally or inside loops

## State Management

- Local state first (`useState`/`useReducer`)
- Context for low-frequency shared state (theme, auth)
- Zustand / Jotai for client-side global state
- React Query / SWR for server state
- Avoid prop drilling beyond 2 levels

## Performance

- `React.memo` — for components that receive stable props but re-render often
- Key prop — stable, unique keys in lists (never index for dynamic lists)
- Code splitting — `React.lazy` + `Suspense` for route-level splitting
- Avoid anonymous functions in JSX for frequently rendered components

## Testing

- Vitest + React Testing Library for components
- Test behavior, not implementation (query by role/text)
- Playwright for end-to-end tests
- MSW for mocking HTTP at network level

## Next.js (App Router)

- Server Components by default — `"use client"` only when needed
- Server Actions for mutations
- Metadata API for SEO
- Image/Link components for optimization

## Tooling

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npx tsc --noEmit` | Type check |
| `npm test` | Run tests |
| `npx eslint .` | Lint |

---
name: programming-react
title: "React Development"
description: "React architecture: hooks, state boundaries, server components, and library choices that scale. Auto-activates in React projects."
license: Apache-2.0
compatibility: "Requires Node.js and a package manager."
capabilities: programming-nodejs
domains: developer
rules:
  - grep(react, package.json)
  - grep(@types/react, package.json)
  - content(react)
---

## Mental model

React is a rendering library; state, data fetching, routing, and persistence are choices on top. The maintainable React app has clear state boundaries: server state separated from client state, local state separated from shared, and side effects pushed to the edges. Most pain comes from `useEffect` doing the work of data fetching, derived state, and event handling all at once; from prop drilling masquerading as composition; and from global stores swallowing everything.

## State boundaries

- Local UI state: `useState` / `useReducer` — colocate with the component that owns it
- Derived state is not state: compute it during render from props/state, don't sync via `useEffect`
- Server state belongs to a server-state library (`TanStack Query`, `SWR`, `Apollo`) — not `useEffect` + `fetch` + `useState`
- Global client state (theme, auth, feature flags) goes in Context or a small store (`zustand`, `jotai`) — never the whole app
- URL state belongs in the router (`searchParams`, route params) — single source of truth for shareable state

## Components and composition

- One component per file; named exports over default
- Props are an API — define them with intent (`variant`, `size`) rather than dumping internal flags
- Composition over configuration — `<Card><Card.Header /><Card.Body /></Card>` beats `<Card hasHeader hasBody />`
- Children and render props beat prop drilling beyond two levels
- Keep components small and focused; extract sub-components when a section has its own state or logic
- Server Components (Next.js / React 19) by default; `"use client"` only when interactivity is needed

## Hooks discipline

- `useEffect` is for synchronizing with external systems (DOM APIs, subscriptions, non-React libraries) — not for derived data, not for event handling
- Custom hooks extract reusable stateful logic; name them `useX` so the rules of hooks apply
- `useMemo` / `useCallback` only when profiling shows a real problem — they're not free
- `useRef` for DOM references and mutable values that shouldn't trigger renders
- Never call hooks conditionally, in loops, or after early returns

## Data fetching

- Server state library handles cache, deduplication, retries, and invalidation — don't reinvent this
- Mutations: optimistic updates with rollback on error; invalidate queries after success
- Pagination via `useInfiniteQuery` or cursor-based pages — never fetch entire lists into client state
- Suspense boundaries for loading states in React 18+; `ErrorBoundary` for failures
- In Next.js / Remix: prefer server-side data loading; client fetching only for truly client-driven data

## Forms

- Controlled inputs for anything that needs validation, conditional logic, or remote submission
- `react-hook-form` for non-trivial forms — performance and ergonomics beat raw `useState` chains
- Validation schemas (`zod`, `valibot`) shared between client and server so both validate the same way
- Submit handlers return promises; UI shows loading/error/success state via the form library, not ad-hoc flags

## Performance

- Stable keys in lists — never the array index for items that can reorder or delete
- `React.memo` only for components that re-render frequently with stable props
- Code-split at route boundaries with `React.lazy` + `Suspense`
- Avoid creating new objects/arrays/functions inline when they're props to memoized children
- Measure with the React DevTools Profiler before optimizing — most "slowness" is one bad component, not the whole tree

## Architecture

- Feature-first folder layout: `features/billing/{components,hooks,api,types}` beats `components/`, `hooks/`, `api/` siblings
- A `features/` folder for app-specific code, `components/` for the design system, `lib/` for cross-cutting utilities
- Routes are thin: they compose feature components and pass route params, no business logic
- Side-effect-free render — anything that touches `window`, `localStorage`, or fetches data goes inside an effect, a custom hook, or a server component

## Testing

- Vitest or Jest + React Testing Library — test what the user sees, not implementation details
- Query by role, label, and text; reach for test IDs only when accessible queries fail
- MSW for HTTP at the network layer — no mocking `fetch` or query-library internals
- Playwright for end-to-end flows; keep them few and focused on critical paths
- Snapshot tests sparingly — they catch unintended changes but tempt people to accept noise

## Ecosystem

- Framework: Next.js (App Router) or Remix for full-stack; Vite for SPAs
- Styling: Tailwind, CSS Modules, or vanilla-extract — avoid runtime CSS-in-JS for new projects (bundle and perf cost)
- Routing: framework router; for SPAs, `TanStack Router` (typed) or `React Router`
- Types: TypeScript with strict mode; props typed with `interface`, public APIs with explicit return types

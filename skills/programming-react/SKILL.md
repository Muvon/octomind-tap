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

## Overview

Build React interfaces with explicit state ownership, pure rendering, and dependable loading and mutation behavior. Research baseline: 2026-09-05, React 19.2 stable and React Compiler 1.0 stable. Inspect installed React, framework, renderer, and compiler configuration first; documentation can include Canary-only APIs. Keep existing routing, styling, and state libraries unless the task requires changing them.

## Mental model

A render describes UI from a snapshot of props, state, and context; React may repeat or abandon it. Events cause user-directed changes, while effects synchronize committed UI with external systems. React's server component model requires supporting infrastructure; it is not automatically enabled by using React 19.

## State and component boundaries

- Store the smallest authoritative state. Derive filtered lists, counts, and validation summaries during render; do not mirror props or derived values through effects.
- Keep state near its consumers. Lift it to the closest shared owner when necessary; use composition before introducing context or a global store. Shareable navigation state belongs in the URL.
- Use functional updates when the next value depends on pending previous state. Treat props/state as immutable snapshots; mutate neither during rendering.
- Model mutually exclusive UI states explicitly. Keep initial loading, refreshing existing data, empty results, and failures distinguishable; a failed fetch is not an empty list.
- Define components at module scope to preserve identity. Use stable domain keys for reorderable lists; change a subtree's key only when resetting its state is intended.
- Make props reflect behavior rather than internal switches. Follow framework export conventions; neither named exports nor one-component-per-file is universally required.

## Effects and current APIs

- Hooks belong at the top level of components/custom hooks, before conditional returns. React's `use(resource)` is an exception: it permits conditions and loops, but still belongs inside a component or hook and cannot be wrapped in `try/catch`.
- Effects must list their reactive dependencies and clean up subscriptions, timers, and pending work. Strict Mode's extra development setup/cleanup cycle exposes lifecycle errors; do not hide it with a "run once" ref.
- React 19.2's `useEffectEvent` reads current values for non-reactive logic called from effects. It is not a dependency-avoidance trick, a UI event handler, or a callback to pass elsewhere.
- React 19 permits function components to receive `ref` as a prop. Use this for new 19-targeted APIs; preserve `forwardRef` where older consumers need it.
- React 19.2's `Activity` can hide UI while preserving state and cleaning up its effects. Use it when that lifecycle is needed; ordinary conditional rendering remains appropriate.
- React Compiler can memoize supported code when enabled in the build. Do not assume it is active because React is installed. Profile before adding manual memoization; memoization must never be required for correctness.

## Data, server boundaries, and forms

- Prefer existing framework loaders or cache infrastructure for shared server data. A small effect-based fetch is valid when it handles races, cancellation, and errors; a cache library is not mandatory.
- Suspense handles participating data sources, lazy components, and promises consumed through `use`; it does not detect arbitrary effect-based fetching. Reuse a stable promise rather than creating one every client render.
- Use Server Components only in a supporting framework. Keep secrets server-side, and authorize each server mutation. `"use client"` marks a module dependency boundary; Client Components can still be prerendered on the server.
- Use native form semantics and labels. Controlled inputs are useful when React must drive their value; uncontrolled inputs and `FormData` suit many ordinary forms.
- React 19 form actions and `useActionState` provide pending state and action results. `useFormStatus` observes its parent form, not a form rendered by the same component. Follow existing form infrastructure when it already meets the need.
- Show expected validation failures as action state. Let unexpected failures reach the appropriate error boundary; handle event-handler and unrelated asynchronous failures explicitly because boundaries do not catch every error.
- Keep optimistic state temporary and reconciled with authoritative results. Failed or conflicting mutations need recovery; avoid optimistic updates when the operation cannot be safely predicted.

## Example

Derive visible content directly and retain stable item identity:

```tsx
type Item = { id: string; title: string; archived: boolean };

function ItemList({ items, showArchived }: {
  items: readonly Item[];
  showArchived: boolean;
}) {
  const visible = items.filter(item => showArchived || !item.archived);
  return (
    <ul>
      {visible.map(item => <li key={item.id}>{item.title}</li>)}
    </ul>
  );
}
```

No effect or duplicate state is needed. The caller remains responsible for distinguishing loading, failure, and a successful empty result.

## Checklist

- Confirm the installed stable APIs and the framework's server/client model.
- Give each value one owner; derive values without synchronization effects.
- Check hook ordering, effect dependencies, cleanup, and stable identity.
- Exercise keyboard interaction, labels, pending/error states, and mutation reconciliation.
- Use existing installed lint, type-check, component, and critical-flow tests when authorized. Report what was source-reviewed versus executed.

## References

- [Current React versions](https://react.dev/versions) and [React 19.2](https://react.dev/blog/2025/10/01/react-19-2)
- [Removing unnecessary effects](https://react.dev/learn/you-might-not-need-an-effect)
- [use and promise ownership](https://react.dev/reference/react/use)
- [useEffectEvent constraints](https://react.dev/reference/react/useEffectEvent)
- [Server Components](https://react.dev/reference/rsc/server-components)
- [Form actions](https://react.dev/reference/react-dom/components/form) and [useActionState](https://react.dev/reference/react/useActionState)
- [React 19 APIs](https://react.dev/blog/2024/12/05/react-19)
- [React Compiler](https://react.dev/learn/react-compiler/introduction)

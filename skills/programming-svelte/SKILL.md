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

## Overview

Write Svelte 5 components and SvelteKit applications with explicit reactive ownership and request-safe server boundaries. Research baseline: 2026-09-05, Svelte 5 and SvelteKit 2 stable; SvelteKit 3 is a release candidate. Read package versions, adapter, compiler options, and existing component mode first. Do not mix prerelease migration instructions into stable maintenance work.

## Mental model

Runes express state and derivation; effects synchronize with external systems after rendering. SvelteKit separates request-local server work from code that also executes in the browser. Reactive module state is not automatically isolated between server requests.

## Runes and component contracts

- Use `$state` for owned reactive data and `$derived`/`$derived.by` for values calculated from it. Derivations should have no side effects.
- Dependencies are values read while the derivation/effect executes synchronously, including called functions; reads after `await` are not tracked by an ordinary effect. Conditional reads produce conditional dependencies.
- Destructuring a reactive object can take a nonreactive snapshot. Keep access through the object or derive the field when it must stay current. Destructuring `$props()` is compiler-supported and different.
- Use `$effect` for browser-side subscriptions and external APIs, with cleanup. Effects do not run during server rendering. Avoid updating state in an effect to calculate another value.
- Type `$props()` and define defaults only for truly optional props. Props belong to their owner; use callbacks for changes or explicit `$bindable` for a deliberate two-way API.
- Use event properties such as `onclick` and snippets with `{@render ...}` in new runes components. Preserve working legacy components when conversion is outside scope.
- Reusable reactive logic belongs in `.svelte.ts`/`.svelte.js`. Do not export directly reassigned rune state; expose operations/getters or a stable object. Stores remain supported and useful for explicit subscriptions and asynchronous streams.
- Use semantic controls, labels, and stable keys in `{#each items as item (item.id)}` when identity matters. `{#key}` destroys and recreates a subtree; it is not a routine refresh mechanism.

## Request isolation and navigation

- Do not keep per-user state in a server module singleton, whether it uses runes, stores, or plain variables. Use request `locals`, returned load data, and component/context instances scoped to the rendered tree.
- Initialize shared UI context at the owning component. Svelte 5.40+ offers typed `createContext`; 5.57 adds its third presence-check function. Prefer the project's supported API instead of a module-global state shortcut.
- On Svelte 5 with Kit 2.12+, use `page` from `$app/state`. Derive values such as `$derived(page.params.id)`; legacy `$:` does not react to this API's updates.
- Pages/layouts can survive navigation. Recompute from changing props or page state instead of capturing the initial value once. Put shareable state in URL parameters and durable preferences in appropriate persistence.

## Loading, mutations, and failures

- Use `+page.server.ts`/`+layout.server.ts` for secrets and database access. Universal `load` also runs in the browser; use its provided `fetch` and return data without mutating shared state.
- Put server-only helpers in `$lib/server` or server-only modules. Private environment imports belong behind this boundary. Authorize access where protected data and mutations are handled; a parent layout is not a universal authorization gate.
- Kit 2's `error(...)` and `redirect(...)` throw internally; call them directly and avoid broad catches that swallow them.
- Await data needed to decide status, redirects, or page structure. To stream noncritical server-load data, return its promise and render with `{#await}`; awaiting it before returning blocks streaming. Account for rejection handling and adapter support.
- Use form actions for ordinary form mutations. Return `fail(status, data)` for expected validation errors, preserve safe entered values, and validate/authorize on the server.
- `use:enhance` progressively enhances supported POST action forms; it does not automatically implement optimistic business state. When customizing it, preserve the intended default update/reset/invalidation behavior.
- Keep pending, empty, validation, and unexpected failure states distinct. Retry or default only when the domain permits it.
- In the researched stable documentation, remote functions and component async `await` require experimental opt-ins. Use them only when intentionally enabled and supported; ordinary load/actions remain valid.

## Example

A typed prop and local state drive a derivation without an effect:

```svelte
<script lang="ts">
  type Item = { id: string; title: string };
  let { items }: { items: readonly Item[] } = $props();
  let query = $state("");
  let visible = $derived(
    items.filter(item => item.title.includes(query))
  );
</script>

<label>
  Filter items
  <input bind:value={query} />
</label>
<ul>
  {#each visible as item (item.id)}
    <li>{item.title}</li>
  {/each}
</ul>
```

## Checklist

- Confirm stable versus experimental APIs and supported TypeScript checker versions.
- Check derivation tracking, prop ownership, navigation reuse, and effect cleanup.
- Keep user data request-scoped and secrets out of universal modules.
- Verify form behavior with and without enhancement, failures, and streamed rejection paths.
- Use the project's installed `svelte-check`, lint, and focused tests when authorized; plain `tsc` does not validate Svelte templates. Report skipped execution.

## References

- [September 2026 release status](https://svelte.dev/blog/whats-new-in-svelte-september-2026)
- [Derived state](https://svelte.dev/docs/svelte/$derived) and [effect tracking](https://svelte.dev/docs/svelte/$effect)
- [State and request isolation](https://svelte.dev/docs/kit/state-management)
- [Reactive page state](https://svelte.dev/docs/kit/$app-state)
- [Load and streaming](https://svelte.dev/docs/kit/load)
- [Form actions and enhancement](https://svelte.dev/docs/kit/form-actions)
- [Remote function status](https://svelte.dev/docs/kit/remote-functions) and [async compiler status](https://svelte.dev/docs/svelte/await-expressions)

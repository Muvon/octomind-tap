---
name: programming-svelte
title: "Svelte Development Best Practices"
description: "Svelte 5 and SvelteKit best practices for AI coding agents: runes, architecture, server/client boundaries, and progressive enhancement. Auto-activates in Svelte projects."
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

Write Svelte 5 components and SvelteKit applications with explicit reactive ownership and request-safe server boundaries. As of 2026-10: Svelte 5 (5.57.x) is stable and SvelteKit 3 was released on 2026-10-01; many projects remain on SvelteKit 2. Read package versions, adapter, Vite config, compiler options, and existing component mode first, and apply only the rules for the installed major version.

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
- Use `page` from `$app/state` (Kit 2.12+; `$app/stores` is removed in Kit 3). Derive values such as `$derived(page.params.id)`; legacy `$:` does not react to this API's updates. In Kit 3, `page.url` is readonly; copy it before mutating.
- Pages/layouts can survive navigation. Recompute from changing props or page state instead of capturing the initial value once. Put shareable state in URL parameters and durable preferences in appropriate persistence.

## Loading, mutations, and failures

- Use `+page.server.ts`/`+layout.server.ts` for secrets and database access. Universal `load` also runs in the browser; use its provided `fetch` and return data without mutating shared state.
- Put server-only helpers in a server-only location (`$lib/server` in Kit 2; any `server` directory or `server` filename segment in Kit 3). Private environment imports belong behind this boundary. Authorize access where protected data and mutations are handled; a parent layout is not a universal authorization gate.
- `error(...)` and `redirect(...)` throw internally; call them directly and avoid broad catches that swallow them. Use `isHttpError`/`isRedirect` rather than `instanceof` checks. In Kit 3, `error()` takes a string message (extra fields in a third argument), `redirect()` to an external URL needs the `external` option, and `handleError` receives every error, including validation errors with `kind: 'validation'`.
- Await data needed to decide status, redirects, or page structure. To stream noncritical server-load data, return its promise and render with `{#await}`; awaiting it before returning blocks streaming. Account for rejection handling and adapter support.
- Use form actions for ordinary form mutations. Return `fail(status, data)` for expected validation errors, preserve safe entered values, and validate/authorize on the server.
- `use:enhance` progressively enhances supported POST action forms; it does not automatically implement optimistic business state. When customizing it, preserve the intended default update/reset/invalidation behavior.
- Keep pending, empty, validation, and unexpected failure states distinct. Retry or default only when the domain permits it.
- Remote functions and component async `await` still require experimental opt-ins in SvelteKit 3 (`experimental.remoteFunctions`, `compilerOptions.experimental.async`). Use them only when intentionally enabled; ordinary load/actions remain valid.

## SvelteKit 3 migration traps

- Run `npx sv migrate sveltekit-3` after upgrading to the latest 2.x and clearing its deprecation warnings. Kit 3 requires Node 22.17+, TypeScript 6, Svelte 5.57.1+, and Vite 8.
- Configuration moves from `svelte.config.js` into the `sveltekit()` plugin options in `vite.config`; `tsconfig.json` extends `$app/tsconfig`.
- `$lib` becomes `#lib` (a `package.json` subpath import) and needs explicit file extensions; `$app/environment` becomes `$app/env`; `$env/*` is deprecated in favor of `$app/env/private` and `$app/env/public`.
- Any file with a `server` path segment or any `server` directory (outside `src/routes` and `static`) is server-only. CSRF origin checking is always on; configure `csrf.trustedOrigins` instead of disabling it.
- `invalidateAll` and `pushState`/`replaceState` are deprecated in favor of `refreshAll` and `goto(..., { shallow })`.

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

- Confirm the installed SvelteKit major, stable versus experimental APIs, and supported TypeScript checker versions (as of 2026-10, Svelte's language tools still embed TypeScript 6 rather than the native TypeScript 7 compiler).
- Check derivation tracking, prop ownership, navigation reuse, and effect cleanup.
- Keep user data request-scoped and secrets out of universal modules.
- Verify form behavior with and without enhancement, failures, and streamed rejection paths.
- Use the project's installed `svelte-check`, lint, and focused tests when authorized; plain `tsc` does not validate Svelte templates. Report skipped execution.

## References

- [SvelteKit 3 announcement](https://svelte.dev/blog/sveltekit-3-is-here) and [migration guide](https://svelte.dev/docs/kit/migrating-to-sveltekit-3)
- [Derived state](https://svelte.dev/docs/svelte/$derived) and [effect tracking](https://svelte.dev/docs/svelte/$effect)
- [State and request isolation](https://svelte.dev/docs/kit/state-management)
- [Reactive page state](https://svelte.dev/docs/kit/$app-state)
- [Load and streaming](https://svelte.dev/docs/kit/load)
- [Form actions and enhancement](https://svelte.dev/docs/kit/form-actions)
- [Remote function status](https://svelte.dev/docs/kit/remote-functions) and [async compiler status](https://svelte.dev/docs/svelte/await-expressions)

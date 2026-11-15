---
name: programming-vue
title: "Vue.js Development Best Practices"
description: "Vue.js 3 practices: script setup, reactivity, props and models, state, SSR hydration, Vapor Mode status. Use when writing or reviewing Vue code."
license: Apache-2.0
compatibility: "Requires Node.js and a package manager."
capabilities: programming-nodejs
domains: developer
rules:
  - file(*.vue)
  - file(src/**/*.vue)
  - file(vite.config.ts)
  - file(nuxt.config.ts)
  - content(vue)
  - content(vue.js)
  - content(nuxt)
  - content(pinia)
  - match((?i)\b(vuex|vue\s*router|composition\s+api|options\s+api|script\s+setup|defineProps|defineEmits|defineModel|v-model|vapor\s+mode)\b)
---

## Overview

Write Vue 3 single-file components with explicit reactive state, typed props and events, and no hydration surprises. As of 2026-11: Vue 3.5.45 (2026-11-05) is the stable release; Vue 3.6 is at release candidate 15 (2026-11-12) and is not stable. Vue 2 reached end of life on 2023-12-31. Read the installed `vue` version, whether the project uses the Composition or Options API, `<script setup>`, TypeScript, Vite or Nuxt, and the state library before editing; keep what the project uses.

## Mental model

A component's `setup` runs once. Reactive state is tracked when it is read inside a render, `computed` or `watch`, so reading a value outside those (or copying it out of a reactive object) breaks the connection. Templates describe output from state; side effects belong in watchers or lifecycle hooks, not in computed values or templates.

## Reactivity rules

- Use `ref` for primitives and replaceable values, `reactive` for objects that are never reassigned. Destructuring a `reactive` object or reading `.value` into a plain variable loses reactivity; use `toRefs`, `toRef`, or a getter.
- Since Vue 3.5, variables destructured from `defineProps` in `<script setup>` stay reactive, and defaults use native syntax: `const { count = 0 } = defineProps<{ count?: number }>()`. Pass them to `watch` or a composable as a getter (`() => count`), not as the bare value.
- `computed` must be pure and return a value; no fetches, no assignments to other state. Use `watch` or `watchEffect` for effects.
- `onWatcherCleanup()` (3.5) registers cleanup inside a watcher, for example aborting a stale request when the source changes.
- `useTemplateRef('name')` (3.5) replaces matching a `ref` variable to a template `ref` attribute by name; it also works with dynamic ref bindings.
- `useId()` (3.5) gives IDs that match between server and client; use it for `label`/`for` and ARIA attributes instead of random values.
- `defineModel()` (stable since 3.4) is the way to implement `v-model` on a component; do not hand-write the `modelValue` prop plus `update:modelValue` emit for new code.
- Large immutable data (big lists, third-party instances) goes in `shallowRef` or `markRaw` to avoid deep proxying.

## Components, props and events

- Declare props and emits with types (`defineProps<...>()`, `defineEmits<...>()`). Props flow down; changes flow up as events. Never mutate a prop.
- Give `v-for` a stable domain `:key`, never the index for reorderable lists, and never put `v-if` on the same element as `v-for`.
- Prefer slots and composition to option-flag props. Keep non-trivial logic in composables (`useX()` functions) that return refs, rather than in templates.
- Type-check single-file components with `vue-tsc`, not plain `tsc`. Pin `vue` with a tilde range (`~3.5.45`), because the Vue team states TypeScript definitions can change incompatibly between minor versions and compiled output from a newer minor compiler may not run on an older minor runtime.

## State management

- Local state stays in the component. Shared state in small apps can be a module-level `reactive` store or a composable.
- For larger apps use Pinia (maintained by the Vue core team); Vuex is in maintenance mode, so new code uses Pinia.
- In SSR a module-level singleton store is shared by every request and leaks one user's data into another response (cross-request state pollution). Create the app, router and stores per request; Pinia is built for this.

## SSR and hydration

- Only `setup` (the `<script setup>` root) and the Options API `beforeCreate`/`created` run on the server. `onMounted` and friends run only in the browser, so browser-only code (`window`, `document`, timers) goes there, with cleanup in `onBeforeUnmount`.
- Hydration mismatches come from invalid HTML nesting (`<div>` in `<p>`), random values, and time-zone dependent output. Fix the cause; use `data-allow-mismatch` (3.5) only for values that must differ, such as dates, and scope it (`text`, `children`, `class`, `style`, `attribute`).
- Hydrate with `createSSRApp`, not `createApp`. Teleports should target a dedicated container, not `<body>`.
- Lazy hydration (3.5): `defineAsyncComponent({ hydrate: hydrateOnVisible() })` delays hydrating below-the-fold components.
- Use Nuxt (4.6.0 on 2026-10-05) or VitePress instead of a hand-built SSR setup when the project allows; a static site may need SSG, not SSR.

## Version status and Vapor Mode

- Vue 3.6 introduces Vapor Mode, an opt-in compilation mode that skips the virtual DOM; it applies only to `<script setup>` components with the `vapor` attribute. Its own notes call it feature-complete in the 3.6 beta but unstable, so use it only for small new apps or isolated regions, and keep Vapor and virtual-DOM regions separate.
- Vapor does not support the Options API, `app.config.globalProperties`, `getCurrentInstance()` or `@vue:` per-element lifecycle events. Suspense is unsupported in Vapor-only apps.
- 3.6 also rewrites `@vue/reactivity` on alien-signals. Do not pin production to a release candidate; re-check the Vue releases page for the stable 3.6.0 before recommending it.
- Vite 8 (2026-03-12) is the current major build tool; read the installed Vite and Node.js requirements before upgrading either.

## Examples

Bad: destructured reactive object, effect in `computed`, index key.

```vue
<script setup>
const state = reactive({ items: [] });
const { items } = state;                    // no longer reactive
const total = computed(() => { fetchTotal(); return 0; });
</script>
<template><li v-for="(item, i) in items" :key="i">{{ item.name }}</li></template>
```

Good: reactive source kept, effect in a watcher with cleanup, stable key.

```vue
<script setup lang="ts">
import { reactive, ref, watch, onWatcherCleanup } from 'vue';

type Item = { id: string; name: string };
const state = reactive({ items: [] as Item[] });
const total = ref(0);

watch(() => state.items.length, async () => {
  const controller = new AbortController();
  onWatcherCleanup(() => controller.abort());
  total.value = await fetchTotal(controller.signal);
});
</script>
<template><li v-for="item in state.items" :key="item.id">{{ item.name }}</li></template>
```

## Checklist

- Installed Vue, Vite or Nuxt version and API style were read before editing; no release candidate in production.
- No destructured reactive state, no side effects in `computed`, no mutated props.
- Props, emits and models are typed; `vue-tsc` passes.
- Keys are stable ids; no `v-if` with `v-for` on one element.
- SSR code creates state per request and keeps browser APIs in `onMounted`.
- Lint, type-check and component tests were run, or the report says they were not.

## References

- [Vue releases](https://vuejs.org/about/releases) and [Vue core releases on GitHub](https://github.com/vuejs/core/releases)
- [Vue 3.5 announcement](https://blog.vuejs.org/posts/vue-3-5)
- [State management](https://vuejs.org/guide/scaling-up/state-management.html)
- [Server-side rendering](https://vuejs.org/guide/scaling-up/ssr.html)
- [Vue 3.6 beta 1 notes (Vapor Mode)](https://github.com/vuejs/core/releases/tag/v3.6.0-beta.1)
- [Nuxt blog](https://nuxt.com/blog) and [Vite blog](https://vite.dev/blog)

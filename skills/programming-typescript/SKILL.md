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

## Overview

Write code whose types describe real runtime guarantees, with small APIs and explicit failure behavior. Research baseline: 2026-09-05, TypeScript 7.0 stable. Read the repository's compiler version, inherited configuration, package exports, runtime targets, and toolchain constraints before applying newer features. A language update does not authorize a dependency or framework migration.

## Mental model

TypeScript checks JavaScript before execution; it does not validate JSON, freeze objects, or install runtime APIs. Keep external uncertainty at the boundary, then use ordinary control flow and domain types internally. Prefer a readable concrete type over generic machinery that only abbreviates one implementation.

## Version and configuration

- TypeScript 7 is the native compiler, available through the regular `typescript` package. It does not expose the old compiler API. Check framework checkers, language plugins, and type-aware linters before upgrades; tooling that embeds the compiler may still require TypeScript 6. The official release documents side-by-side compatibility; do not invent a fallback compiler on failure.
- In 6/7, `strict` defaults to true, `types` to `[]`, and `rootDir` to the configuration directory. Declare intended global types and source root explicitly when needed; inspect emitted paths during migration.
- TypeScript 7 rejects options deprecated in 6, including `baseUrl`, `moduleResolution: node10`, and ES5 targets. Fix the underlying configuration; suppressing deprecations is not a durable migration.
- Keep `strict` enabled. Consider `noUncheckedIndexedAccess` for potentially missing indexed values and `exactOptionalPropertyTypes` when absence differs from explicit `undefined`; neither follows automatically from `strict`. Introduce them within the authorized configuration scope.
- Match `module` and `moduleResolution` to execution: Node-aware modes for Node resolution, `bundler` for a bundler. `paths` changes type resolution, not emitted imports. Prefer package exports/imports or the existing resolver over new aliases.
- Pin `target`/`lib` to supported environments. New declarations do not supply polyfills. Use `import type` for erased dependencies, preserving any intentionally required side-effect import.

## Types that carry their weight

- Accept `unknown` for untrusted values; validate shape and domain constraints before constructing an internal value. Use existing schema tooling for complex boundaries, not a new dependency for a three-field check.
- Prefer discriminated unions to combinations of optional fields and flags. Use exhaustive narrowing with `never` so new variants require a decision.
- Use `satisfies` to check a known expression's compatibility while retaining useful inference. It is not runtime validation or a replacement for every annotation. Assertions and non-null `!` require a concrete invariant.
- Annotate public contracts and ambiguous returns; let locals infer. Add a generic only when it expresses a relationship between inputs and outputs. Keep conditional/mapped types bounded and understandable.
- `readonly`, `Readonly<T>`, and `as const` provide compile-time restrictions, not runtime deep immutability. A mutable alias can still change an object. Copy or freeze only where ownership requires it.
- Distinguish missing, empty, and invalid values. Use `??` only for an intentional nullish default; avoid `||` when zero, false, or an empty string is valid.

## Async work and failures

- Use `await` for readable sequential dependencies; promise composition remains legitimate. Preserve an existing async API's rejection semantics when simplifying it.
- Start independent bounded work together. `Promise.all` rejects on failure but does not cancel siblings; `allSettled` is useful only when callers actually handle each outcome.
- Propagate supported cancellation signals and deadlines through I/O. Avoid detached promises; explicitly own completion and rejection handling.
- Preserve error context with `cause` where supported. Narrow caught values before reading properties. Follow the module's established thrown-error or result-union contract.
- Recover only when an alternative is valid for the operation. Never translate a failed request or malformed payload into a successful empty collection. Retry only identified transient failures, with bounds and appropriate idempotency.

## Example

Validate a boundary without asserting a desired type:

```typescript
type User = Readonly<{ id: string; enabled: boolean }>;

function parseUser(value: unknown): User {
  if (
    typeof value !== "object" || value === null ||
    !("id" in value) || typeof value.id !== "string" ||
    value.id.length === 0 ||
    !("enabled" in value) || typeof value.enabled !== "boolean"
  ) {
    throw new TypeError("Invalid user payload");
  }

  return { id: value.id, enabled: value.enabled };
}
```

The boolean check preserves valid `false`; it does not replace malformed input with a default.

## Checklist

- Confirm compiler, framework tooling, module resolution, and runtime compatibility.
- Validate external data; justify assertions and intentional defaults.
- Keep state variants exhaustive and public types simpler than their implementations.
- Check cancellation, rejection ownership, and partial-failure semantics.
- Use existing type-check/lint/test scripts and installed tools when execution is authorized; test invalid inputs and meaningful async failures. Report skipped checks.

## References

- [TypeScript 7.0 release and compiler API compatibility](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/)
- [TypeScript 6.0 migration details](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-6-0.html)
- [Module resolution reference](https://www.typescriptlang.org/docs/handbook/modules/reference.html)
- [Narrowing and exhaustiveness](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [Object types and readonly limits](https://www.typescriptlang.org/docs/handbook/2/objects.html)
- [Indexed access checking](https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html) and [exact optional properties](https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html)
- [The satisfies operator](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html)

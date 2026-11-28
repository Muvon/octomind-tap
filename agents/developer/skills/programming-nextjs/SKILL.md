---
name: programming-nextjs
title: "Next.js Development Best Practices"
description: "Next.js 16 App Router practices: Cache Components, async request APIs, proxy, Turbopack, server actions, upgrade breaks. Use for Next.js apps and upgrades."
license: Apache-2.0
compatibility: "Requires Node.js and a package manager."
capabilities: programming-nodejs
rules:
  - match((?i)(^|\b(please|you|lets|let's|to|and|then)\s+)(implement|refactor)\w*\b|\b(compil(e|es|ed|er|ing|ation)|build\s+(error|fail\w*|break\w*)|panic\w*|stack\s*trace|traceback|segfault|unit\s+tests?|(fix|debug)\s+(the\s+|this\s+|a\s+)?(bug|build|crash|error|test|failure)s?|write\s+(a\s+|the\s+)?(function|test|module|class|method|struct)|add\s+(a\s+|an\s+)?(function|method|endpoint|field|test)|\w+\.(tsx|jsx))\b) file(next.config.js)
  - match((?i)(^|\b(please|you|lets|let's|to|and|then)\s+)(implement|refactor)\w*\b|\b(compil(e|es|ed|er|ing|ation)|build\s+(error|fail\w*|break\w*)|panic\w*|stack\s*trace|traceback|segfault|unit\s+tests?|(fix|debug)\s+(the\s+|this\s+|a\s+)?(bug|build|crash|error|test|failure)s?|write\s+(a\s+|the\s+)?(function|test|module|class|method|struct)|add\s+(a\s+|an\s+)?(function|method|endpoint|field|test)|\w+\.(tsx|jsx))\b) file(next.config.mjs)
  - match((?i)(^|\b(please|you|lets|let's|to|and|then)\s+)(implement|refactor)\w*\b|\b(compil(e|es|ed|er|ing|ation)|build\s+(error|fail\w*|break\w*)|panic\w*|stack\s*trace|traceback|segfault|unit\s+tests?|(fix|debug)\s+(the\s+|this\s+|a\s+)?(bug|build|crash|error|test|failure)s?|write\s+(a\s+|the\s+)?(function|test|module|class|method|struct)|add\s+(a\s+|an\s+)?(function|method|endpoint|field|test)|\w+\.(tsx|jsx))\b) file(next.config.ts)
  - match((?i)(^|\b(please|you|lets|let's|to|and|then)\s+)(implement|refactor)\w*\b|\b(compil(e|es|ed|er|ing|ation)|build\s+(error|fail\w*|break\w*)|panic\w*|stack\s*trace|traceback|segfault|unit\s+tests?|(fix|debug)\s+(the\s+|this\s+|a\s+)?(bug|build|crash|error|test|failure)s?|write\s+(a\s+|the\s+)?(function|test|module|class|method|struct)|add\s+(a\s+|an\s+)?(function|method|endpoint|field|test)|\w+\.(tsx|jsx))\b) file(app/layout.tsx)
  - match((?i)(^|\b(please|you|lets|let's|to|and|then)\s+)(implement|refactor)\w*\b|\b(compil(e|es|ed|er|ing|ation)|build\s+(error|fail\w*|break\w*)|panic\w*|stack\s*trace|traceback|segfault|unit\s+tests?|(fix|debug)\s+(the\s+|this\s+|a\s+)?(bug|build|crash|error|test|failure)s?|write\s+(a\s+|the\s+)?(function|test|module|class|method|struct)|add\s+(a\s+|an\s+)?(function|method|endpoint|field|test)|\w+\.(tsx|jsx))\b) file(src/app/layout.tsx)
  - match((?i)(^|\b(please|you|lets|let's|to|and|then)\s+)(implement|refactor)\w*\b|\b(compil(e|es|ed|er|ing|ation)|build\s+(error|fail\w*|break\w*)|panic\w*|stack\s*trace|traceback|segfault|unit\s+tests?|(fix|debug)\s+(the\s+|this\s+|a\s+)?(bug|build|crash|error|test|failure)s?|write\s+(a\s+|the\s+)?(function|test|module|class|method|struct)|add\s+(a\s+|an\s+)?(function|method|endpoint|field|test)|\w+\.(tsx|jsx))\b) file(proxy.ts)
  - content(next.js)
  - content(nextjs)
  - match((?i)\bnext\s*\.?\s*js\b)
  - match((?i)\b(app\s+router|pages\s+router|server\s+actions?|cache\s+components?|turbopack|getServerSideProps|getStaticProps|react\s+server\s+components?)\b)
---

## Overview

Build and upgrade Next.js applications on the App Router. As of 2026-11: Next.js 16.4 (2026-10-06) is the latest stable minor; it ships React 19.3. Read the installed `next` version, the router in use (`app/` or `pages/`), `next.config.*`, and the hosting target before changing code. Next.js ships a security release every month and out-of-band fixes between them (latest seen: 2026-11-03); check the Next.js blog for the current advisory and keep the project on a patched version.

## Mental model

A Next.js route is rendered by React on the server, and each piece of it is either computed per request or cached. Cache Components is the 16.x model for deciding which: you mark a component or function with `'use cache'`, everything not marked renders at request time, and a Suspense boundary decides what the user sees first. Cache Components becomes the default in Next.js 17; since 16.4 `create-next-app` turns it on for new apps. Existing apps opt in with `cacheComponents: true` and `partialPrefetching: true` in `next.config`, and enabling it is not a rename: it can fail builds on uncached data outside `<Suspense>`.

## Version 16 breaking changes

Check each when a project moves from 15 or earlier.

| Area | Change in 16 |
|---|---|
| Runtime | Node.js 20.9+ and TypeScript 5.1+ required; browsers Chrome/Edge/Firefox 111+, Safari 16.4+ |
| Bundler | Turbopack is the default for `next dev` and `next build`; a custom `webpack` config fails `next build` unless you pass `--webpack` (or `--turbopack` to ignore it) |
| Request APIs | `cookies()`, `headers()`, `draftMode()`, `params`, `searchParams` are async only; run the `next-async-request-api` codemod and `npx next typegen` for `PageProps`/`LayoutProps` |
| Middleware | `middleware.ts` is renamed `proxy.ts` with an exported `proxy` function; it runs on the Node.js runtime only. Keep `middleware` if you need the edge runtime |
| Caching | `revalidateTag(tag, profile)` needs a second argument (for example `'max'`); `updateTag` (Server Actions only) gives read-your-writes; `cacheLife` and `cacheTag` lost their `unstable_` prefix |
| Removed | `next lint` (use ESLint or Biome directly), AMP, `serverRuntimeConfig`/`publicRuntimeConfig`, `experimental.ppr`, `experimental.dynamicIO`, `experimental.useCache` |
| Parallel routes | Every slot needs an explicit `default.js` or the build fails |
| Images | `minimumCacheTTL` default 4 hours; `qualities` default `[75]` (other `q` values return 400); local IP optimization blocked; at most 3 redirects; `images.domains` deprecated in favor of `remotePatterns` |
| Scroll | Next.js no longer overrides `scroll-behavior: smooth` on navigation; add `data-scroll-behavior="smooth"` to `<html>` for the old behavior |

The codemod `npx @next/codemod@canary upgrade latest` covers the config, lint, proxy and prefix changes; `npx next@canary upgrade --agent=latest` prepares guides for a coding agent. Run the app's build and tests after; a green build does not prove runtime behavior.

## Caching and rendering rules

- Put `'use cache'` on the smallest component or function whose output is reusable; pair it with `cacheLife('hours')` or a named profile, and `cacheTag` for targeted invalidation.
- Request data (`cookies()`, `headers()`, `searchParams`) cannot be read inside a cached scope. Read it outside, and pass the values in as arguments, which become part of the cache key.
- Set `cacheLife` explicitly in every cached scope; without it the `default` profile applies (stale 5 minutes, revalidate 15 minutes, no expiry). Arguments and return values must be serializable: class instances, symbols and `URL` objects are rejected.
- Default runtime cache is in memory. On serverless hosts entries usually do not persist between requests, and no cache entry survives a new deploy because the build ID is part of the key; check the host's cache handler before relying on it.
- Wrap request-time components in `<Suspense>` with a fallback that fits the final layout.
- Use `export const ensureStatic = 'navigation'` (16.4) on a route or layout to fail the build when a dynamic component enters a page that must stay static; `'prefetch'` and `'shell'` are weaker levels.
- Use `await navigation()` or `await prefetch()` (from `next/cache`, 16.4) inside a component to keep expensive cached work out of prefetches until the user navigates.
- After a mutation, call `updateTag` when the user must see the change immediately, `revalidateTag(tag, 'max')` when stale-while-revalidate is acceptable, and `refresh()` to refresh the client router.

## Server boundaries and security

- A Server Action is a public HTTP endpoint. Authenticate and authorize inside each one, validate its arguments against a schema, and never trust values the client could edit.
- Keep secrets in server-only modules. Read environment variables on the server; only `NEXT_PUBLIC_` variables reach the browser. Use `connection()` before reading `process.env` when a value must be read at request time and not baked in at build.
- `'use client'` marks the client module boundary; do not import server-only code into it. Props passed from a Server Component to a Client Component are serialized into the page, so do not pass secrets or whole database rows.
- The 2025 React Server Components protocol vulnerabilities (CVE-2025-66478 and a follow-up of 2025-12-11) required patched releases; confirm the installed version is current rather than assuming.

## Other mechanics

- `next/image`: set `remotePatterns` with protocol, hostname and pathname; allow only the `qualities` the app uses; give width and height or `fill` to avoid layout shift.
- React Compiler: `reactCompiler: true` is stable but off by default and adds build time; the Rust version is experimental (`experimental.turbopackRustReactCompiler`). Profile before enabling.
- Bundle size: the 16.4 Turbopack Bundle Analyzer lists the largest client routes and diffs snapshots; use it before adding a library. Next.js 16 removed the `First Load JS` column from build output, so measure with Lighthouse or field data.
- Version-matched docs: `node_modules/next/dist/docs/` holds the docs for the installed version; read those instead of the website when versions differ.

## Examples

Bad: dynamic data read inside a cached function.

```tsx
async function Cart() {
  'use cache';
  const user = (await cookies()).get('uid'); // not allowed in a cached scope
}
```

Good: read request data outside and pass it in.

```tsx
async function CartPage() {
  const uid = (await cookies()).get('uid')?.value;
  return <Suspense fallback={<CartSkeleton />}><Cart uid={uid} /></Suspense>;
}

async function Cart({ uid }: { uid?: string }) {
  'use cache';
  cacheLife('minutes');
  // uid is part of the cache key
}
```

## Checklist

- Installed Next.js version is patched against the latest security release.
- Router, `next.config.*`, and hosting target were read before edits.
- Request APIs are awaited; `proxy.ts` replaces `middleware.ts` unless the edge runtime is required.
- `revalidateTag` calls have two arguments; no removed flags remain.
- Every Server Action authenticates, authorizes and validates.
- Build, lint and tests were run, or the report lists what was only read.

## References

- [Next.js blog](https://nextjs.org/blog) and [Next.js 16.4](https://nextjs.org/blog/next-16-4)
- [Upgrading to version 16](https://nextjs.org/docs/app/guides/upgrading/version-16)
- [Migrating to Cache Components](https://nextjs.org/docs/app/guides/migrating-to-cache-components)
- [React 19.3](https://react.dev/blog/2026/09/09/react-19-3)

---
name: programming-nodejs
title: "Node.js Backend Development Best Practices"
description: "Node.js server practices: LTS choice, native TypeScript, event-loop safety, shutdown, HTTP hardening, node:test. Use for Node backends and APIs."
license: Apache-2.0
compatibility: "Requires Node.js and a package manager."
capabilities: programming-nodejs
domains: developer
rules:
  - file(.nvmrc)
  - file(.node-version)
  - grep(fastify|express|@nestjs|hono|koa, package.json)
  - content(node.js)
  - content(nodejs)
  - content(express)
  - content(fastify)
  - content(nestjs)
  - content(node)
  - match((?i)\b(sigterm|graceful\s+shutdown|event[\s-]?loop|node:test|worker[\s_]threads)\b)
---

## Overview

Write Node.js services that stay responsive under load, fail visibly, and shut down cleanly. This skill covers server code: HTTP APIs, workers, queues, scripts run in production. As of 2026-11, check the installed Node.js version, the module system (`"type"` in `package.json`), the framework, and the test runner before changing anything; keep the framework and package manager the project already uses.

## Mental model

One JavaScript thread runs all requests. Anything that blocks it (CPU work, synchronous file or crypto calls, a huge `JSON.parse`) stalls every connection. Anything that never ends (a socket without an error handler, a request without a timeout, a stream without backpressure) leaks until the process dies. Node.js runs the code it is given with full trust; dependencies get the same access to the network and disk as your own code.

## Release lines (as of 2026-11)

| Line | Status | End of life |
|---|---|---|
| 26 | LTS since 2026-10-28 | 2029-04-30 |
| 24 | LTS, maintenance phase since 2026-10-20 | 2028-04-30 |
| 22 | LTS, maintenance phase | 2027-04-30 |
| 20, 25 | end of life | already passed |
| 27 | alpha; first release 2027-04-22 | 2030-04-30 |

- Pick an LTS line for production. Starting with Node.js 27 there is one major per year and every major becomes LTS after its Current phase; before that, odd-numbered lines were never LTS.
- Read the live table at nodejs.org/en/about/previous-releases before recommending a version; the dates above are the schedule published in nodejs/Release.
- Node.js 26 removed `http.Server.prototype.writeHeader()` (use `writeHead()`), the legacy `_stream_*` modules, and `--experimental-transform-types`. It also deprecates `module.register()` at runtime and turns the `Temporal` date/time API on by default.

## TypeScript without a build step

Type stripping is stable (Stability 2) in Node.js 24.12+, 25.2+ and 26; it has been on by default since 22.18 and 23.6. It deletes type annotations and performs no type checking, so keep `tsc --noEmit` in CI.

- Only erasable syntax works. `enum`, runtime `namespace`, constructor parameter properties, `import x = require()` and decorators fail with `ERR_UNSUPPORTED_TYPESCRIPT_SYNTAX` or a parser error.
- Imports need the real extension (`./file.ts`) and type-only imports need `import type` or an inline `type` modifier; otherwise they become runtime imports and fail.
- Node.js ignores `tsconfig.json`: `paths` aliases do not work. Use `package.json` subpath imports (names start with `#`).
- Recommended `tsc` settings (TypeScript 5.8+): `noEmit`, `target: esnext`, `module: nodenext`, `rewriteRelativeImportExtensions`, `erasableSyntaxOnly`, `verbatimModuleSyntax`.
- Node.js refuses to run `.ts` files inside `node_modules`; publish compiled JavaScript from libraries.
- `.tsx` is not supported; keep JSX behind a bundler.

## Event loop and streams

- Move CPU-bound work (image processing, large parsing, synchronous crypto) to `worker_threads` or another process. Measure event-loop delay (`perf_hooks.monitorEventLoopDelay`) before and after, and set the acceptable p99 from the service's latency target.
- Use `stream.pipeline` (or `pipeline` from `node:stream/promises`) for streams so errors destroy every stage and backpressure is honored. A manual `.pipe()` chain does not propagate errors.
- Put an `AbortSignal` (`AbortSignal.timeout(ms)`) on every outbound `fetch` and database call; no outbound call is allowed to wait forever.
- Handle `unhandledRejection` by logging and exiting; continuing after it leaves the process in an unknown state. Let the supervisor (systemd, Kubernetes) restart it.

## HTTP server hardening

From the Node.js security guide:

- Attach an `error` listener to every raw socket; an unhandled socket error crashes the process.
- Set `server.headersTimeout`, `requestTimeout`, `timeout` and `keepAliveTimeout`, and cap sockets with `agent.maxSockets` and `server.maxRequestsPerSocket`, so a slow client (Slowloris) cannot hold connections open. Put a reverse proxy in front.
- Never use `insecureHTTPParser`; configure the front proxy to normalize ambiguous requests (request smuggling).
- Compare secrets with `crypto.timingSafeEqual`, hash passwords with `scrypt`.
- Validate untrusted JSON against a schema. Reject `__proto__`, `constructor` and `prototype` keys in recursive merges (prototype pollution); use `Object.hasOwn()` for key checks.
- Do not run `--inspect` in production (DNS rebinding reaches it from a browser).

## Graceful shutdown

On `SIGTERM`: stop accepting connections (`server.close()`), mark readiness failing, let in-flight requests finish within a fixed deadline, close database pools and queues, then exit. Call `server.closeIdleConnections()` so keep-alive sockets do not hold the process open. A shutdown with no deadline is a hung deploy.

## Dependencies and supply chain

- Commit the lockfile; use `npm ci` in CI so a lockfile mismatch fails the build.
- Disable install scripts by default (`npm config set ignore-scripts true`) and allow them per package.
- npm 11.10.0 and later supports `min-release-age=1`, a one-day cooldown on fresh releases. Override per command with `--min-release-age=0` when a security fix cannot wait.
- Run `npm audit`, and run `npm publish --dry-run` before publishing to check no secrets ship.

## Permission model

`--permission` (Stability 2, stable since 22.13 and 23.5) restricts file reads and writes (`--allow-fs-read`, `--allow-fs-write`), network (`--allow-net`), child processes, workers and native addons. `--permission-audit` logs violations without blocking, which is how to find the grants an app needs. It is a guard against accidents and compromised dependencies, not a sandbox: symlinks are followed, open file descriptors bypass it, and malicious code can escape. Use OS-level isolation (containers, separate users) for untrusted code.

## Testing and diagnostics

- `node:test` is stable. Use `node --test`; `--test-update-snapshots` writes snapshot files. Coverage (`--experimental-test-coverage`) and `--watch` are still experimental; do not make a CI gate depend on them without checking the installed version. Keep the framework the project already uses.
- CPU profile: `node --cpu-prof app.js`, then open the `.cpuprofile` in Chrome DevTools. Memory leak: take a heap snapshot after the first warm-up request, repeat the action, take a second snapshot, and read the Comparison view for large positive deltas and their retainers. Snapshots pause the process and can roughly double memory use; do not take one on a production process that cannot be restarted. The `performance-profiling` skill covers the general method.

## Examples

Bad: no timeout, ignored errors, stream chain with `.pipe()`.

```js
const res = await fetch(url);
source.pipe(transform).pipe(dest);
```

Good: bounded wait, errors propagate, backpressure honored.

```js
import { pipeline } from 'node:stream/promises';

const res = await fetch(url, { signal: AbortSignal.timeout(5_000) });
if (!res.ok) throw new Error(`upstream ${res.status}`);
await pipeline(source, transform, dest);
```

## Checklist

- Node.js line is LTS and its end-of-life date is after the planned support window.
- No `.ts` runtime syntax that type stripping cannot erase; `tsc --noEmit` runs in CI.
- Every outbound call has a timeout; every socket has an error handler.
- Server timeouts are set; shutdown has a deadline and closes pools.
- Lockfile committed; CI uses `npm ci`; install scripts are off by default.
- Tests and profiling commands were run, or the report says they were not.

## References

- [Node.js releases](https://nodejs.org/en/about/previous-releases) and [release schedule](https://github.com/nodejs/Release/blob/main/schedule.json)
- [Node.js 26.0.0 release notes](https://nodejs.org/en/blog/release/v26.0.0)
- [TypeScript support](https://nodejs.org/api/typescript.html)
- [Permission model](https://nodejs.org/api/permissions.html)
- [Security best practices](https://nodejs.org/en/learn/getting-started/security-best-practices)
- [Test runner](https://nodejs.org/api/test.html)
- [Heap snapshots](https://nodejs.org/en/learn/diagnostics/memory/using-heap-snapshot)

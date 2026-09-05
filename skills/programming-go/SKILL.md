---
name: programming-go
title: "Go Development"
description: "Idiomatic Go architecture, concurrency design, and standard-library-first patterns. Auto-activates in Go projects."
license: Apache-2.0
compatibility: "Requires the Go toolchain selected by the project."
domains: developer
rules:
  - file(go.mod)
  - content(golang)
---

## Overview

Write explicit Go with small packages, inspectable errors, and bounded concurrency. Research baseline: stable Go 1.27, checked 2026-09-05. Read `go.mod`, `go.work`, toolchain directives, build tags, and CI before introducing newer APIs. Use a supported toolchain, but preserve the module's language compatibility unless an upgrade is requested. Recheck official releases when updating this guidance.

## Mental model

Keep control flow and ownership visible. Ordinary functions, structs, and explicit dependency wiring solve most problems. Add an interface, generic abstraction, goroutine, or dependency when it removes a concrete coupling or limitation; don't create infrastructure for hypothetical reuse.

## Recent features and compatibility

| Version | Useful change and boundary |
|---------|----------------------------|
| 1.22 | Loop variables declared by the loop have per-iteration semantics; preexisting variables assigned by the loop still share storage. `ServeMux` supports method and wildcard patterns. |
| 1.23 | Range-over-function iterators and `iter`, `slices`, and `maps` helpers can replace custom collection plumbing. |
| 1.25 | `sync.WaitGroup.Go` couples task startup with completion accounting; the function must not panic. `testing/synctest` supports deterministic concurrent tests. |
| 1.27 | Methods may declare type parameters. Interface methods still cannot, and generic methods cannot implement interface methods. `encoding/json/v2` and `encoding/json/jsontext` are available without the former experiment requirement. |

Go 1.27 JSON v2 rejects duplicate object names and invalid UTF-8 by default. Migration changes wire behavior; inspect the documented differences and test existing payloads. The original `encoding/json` API remains supported. SIMD packages are still experimental; do not treat them as ordinary stable APIs.

## Packages, types, and interfaces

- Keep a package cohesive and its exported surface small. `internal/` limits imports to the subtree rooted at its parent directory; it does not mean strictly “same module.” Preserve the existing layout when it serves the task.
- Define a small interface at the consumer when substitution is needed; don't export an interface for every concrete implementation. Return concrete values unless hiding representation is part of the API.
- Use generics when the same algorithm works across types. `sync.Pool` is not `sync.Pool[T]`; verify signatures instead of inventing typed variants.
- Prefer useful zero values where possible; use constructors for required invariants. A typed nil pointer inside an interface is a non-nil interface: return an explicit `nil` on success for `error` results.
- Treat slices as views over possibly shared storage. Copy before retaining data that the caller may mutate or reuse. Do not copy mutexes, wait groups, or other synchronization values after use.

## Errors and boundaries

- Return errors with operation context; use `%w` when callers should inspect the cause. Check with `errors.Is` or `errors.As`, not error-string matching.
- Choose exported sentinel or typed errors only for recovery decisions callers need. Wrapping exposes a cause as part of your API; don't expose implementation errors accidentally.
- Handle or return failures. Log where the request/job is finally handled, avoiding duplicate logs at every layer. Don't turn invalid configuration, malformed input, or failed I/O into successful zero values.
- Close response bodies and files promptly; check write and close errors where they affect durability. Put per-item cleanup in a helper instead of accumulating loop-scoped `defer` calls until a long function exits.
- Set HTTP timeouts and body limits appropriate to the operation; pass request contexts through network and database calls. Reuse clients and transports.

## Concurrency and lifecycle

- Every goroutine needs an owner, completion/error handling, and a way to finish. A `WaitGroup` waits; it does not cancel work. Bound parallel work and queues.
- Pass `context.Context` explicitly as the first parameter for operations with cancellation/deadlines. Don't store request contexts in long-lived structs; call returned cancellation functions to release resources.
- Choose a mutex for simple shared state and channels for coordination or ownership transfer. The sending owner closes a channel after its final send; multiple producers need coordinated closure.
- Use `errgroup` when coordinated work needs error propagation and cancellation. Its context only helps if blocking operations observe cancellation.

## Example

Preserve parse errors and reject values outside the domain:

```go
func parseWorkers(raw string) (int, error) {
	n, err := strconv.Atoi(raw)
	if err != nil {
		return 0, fmt.Errorf("parse worker count: %w", err)
	}
	if n < 1 {
		return 0, fmt.Errorf("worker count must be positive")
	}
	return n, nil
}
```

This function uses the standard `fmt` and `strconv` packages.

## Checklist

- [ ] Language features and standard-library symbols match the module's declared version.
- [ ] Errors, nil interfaces, shared slices, cleanup, and cancellation preserve the contract.
- [ ] New concurrency has bounded work and a defined shutdown path.
- [ ] When authorized, use project formatting, vet, focused tests, and race tests on supported targets. Exercise invalid inputs and concurrent shutdown; report skipped checks.

## References

- [Release history](https://go.dev/doc/devel/release), [Go 1.27](https://go.dev/doc/go1.27), and [Go 1.25](https://go.dev/doc/go1.25).
- [Language specification](https://go.dev/ref/spec) and [Go code review guidance](https://go.dev/wiki/CodeReviewComments).
- [Context lifecycle](https://pkg.go.dev/context), [synchronization contracts](https://pkg.go.dev/sync), and [JSON v2](https://pkg.go.dev/encoding/json/v2).

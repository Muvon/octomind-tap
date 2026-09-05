---
name: programming-java
title: "Java Development"
description: "Modern idiomatic Java — records, sealed types, pattern matching, virtual threads, and explicit failure contracts. Auto-activates in Java projects."
license: Apache-2.0
compatibility: "Requires the project's JDK and Maven or Gradle; guidance distinguishes Java 17, 21, 25, and 26 features."
domains: developer
rules:
  - file(pom.xml)
  - file(build.gradle)
  - content(java)
---

## Overview

Use for Java implementation and review, especially modernizing verbose code without changing its contract. Keep the project's framework, build tool, and supported runtime; introduce newer features only when the configured release permits them.

## Mental model

Make invalid states difficult to construct and ownership easy to see. Records reduce boilerplate, virtual threads simplify blocking concurrency, and neither removes the need for validation, bounded resources, or deliberate failure handling.

## Version gate

Verified 2026-09-05: Java 26 is released; Java 25 is the latest LTS release. Recheck the vendor's support policy before choosing a runtime. Read Maven compiler release or Gradle toolchains, CI images, and deployment constraints; the installed JDK alone does not determine usable APIs.

| Minimum release | Useful stable features |
|---|---|
| 17 | Records, sealed types, text blocks, instanceof patterns |
| 21 | Record patterns, pattern switch, virtual threads |
| 22 | Unnamed variables and patterns |
| 24 | Stream gatherers; synchronized virtual-thread pinning fixed |
| 25 | Scoped values, flexible constructor bodies, compact source files |

Structured concurrency and primitive patterns remain preview in Java 26. Don't introduce preview flags or copy preview examples into ordinary production changes. Compact source files suit small programs; they do not justify flattening application structure.

## Values and APIs

- Use records for transparent values, ordinary classes for identity and controlled lifecycle. Records are shallowly immutable: copy mutable components, and don't assume array components get content-based equality.
- Validate invariants once at construction. Use a sealed hierarchy and exhaustive switch for a closed domain; handle null separately when it is allowed. Avoid a catch-all branch that hides newly added variants.
- Prefer `Optional<T>` for a result that may legitimately be absent. Keep transport failure distinct from absence; don't return empty after catching an outage. Avoid Optional parameters when overloads or a clear nullable contract suffice.
- Expose the smallest useful interface. Constructor injection makes dependencies visible; add interfaces, builders, or modules when they express a real boundary, not for every class.
- `List.copyOf` creates an unmodifiable snapshot and rejects null elements; it does not copy mutable elements. An unmodifiable wrapper over a mutable collection is still a live view.
- Use clear local inference, simple streams for transformations, and loops for stateful algorithms. Don't parallelize streams around blocking I/O or shared mutation without owning their execution model.

## Concurrency and failure

- Virtual threads suit many blocking I/O tasks, not faster CPU computation. Don't pool them. Bound scarce resources with connection pools, semaphores, and request limits even when threads are cheap.
- On JDK 24+, don't replace `synchronized` solely to avoid its old virtual-thread pinning behavior. Native/foreign calls can still pin; profile before rewriting synchronization.
- Scoped values hold lexically bounded request context; they are not a mutable ThreadLocal replacement. Keep CompletableFuture where an existing asynchronous API benefits from composition.
- Give submitted work an owner: observe results, propagate failures, set deadlines, and cancel outstanding work when its result is no longer needed. Executor shutdown alone is not a request timeout.
- Propagate `InterruptedException` where possible; when translating it at a boundary, restore the interrupt flag. Don't retry canceled work.
- Use try-with-resources for owned closeable resources. Catch specific failures only when recovering or adding useful context; preserve the cause. Translate exceptions into API outcomes at the boundary, not repeatedly in each layer.
- Retry only an identified transient failure with a bounded policy and safe operation semantics. An empty collection, zero, or stale cache is a fallback only if the contract explicitly permits it.

## Integration and checks

- Parameterize SQL; keep transaction ownership explicit. With an ORM, inspect query shape and lazy-loading boundaries instead of switching persistence libraries as a cleanup.
- Use `java.time`; distinguish an instant from a local date/time and inject a clock for time-sensitive behavior.
- Follow the repository's formatter and test stack. JUnit 6 is the current generation, requiring Java 17; don't force an unrelated JUnit 5 migration. Test observable results, real database semantics, and cancellation where affected.

## Example

A record's list component needs its own ownership decision:

```java
import java.util.List;

record Batch(List<String> ids) {
    Batch {
        ids = List.copyOf(ids);
        if (ids.isEmpty()) {
            throw new IllegalArgumentException("ids must not be empty");
        }
    }
}
```

Strings are immutable, so a shallow snapshot suffices here. A list of mutable domain objects would require a different contract.

## Checklist

- [ ] APIs and syntax fit the configured release; preview features are identified.
- [ ] Mutable values, resources, and concurrent tasks have explicit owners.
- [ ] Missing data, failure, timeout, and cancellation remain distinguishable.
- [ ] Existing architecture and dependencies are preserved unless change is required.
- [ ] Relevant checks were run when authorized; unexecuted checks are reported.

## References

- [Java support roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html) and [language changes](https://docs.oracle.com/en/java/javase/26/language/java-language-changes-summary.html)
- [Record contract](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/lang/Record.html)
- [Virtual threads](https://docs.oracle.com/en/java/javase/26/core/virtual-threads.html) and [ScopedValue](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/lang/ScopedValue.html)
- [JUnit](https://junit.org/)

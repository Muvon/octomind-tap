---
name: programming-java
title: "Java Development"
description: "Modern idiomatic Java — records, sealed types, pattern matching, virtual threads, and Effective-Java discipline. Auto-activates in Java projects."
license: Apache-2.0
compatibility: "Requires JDK 17+ (21+ preferred) with Maven or Gradle."
domains: developer
rules:
  - file(pom.xml)
  - file(build.gradle)
  - content(java)
---

## Mental model

Java optimizes for large teams maintaining large systems for a long time. The language has modernized hard — records, sealed types, pattern matching, virtual threads — and idiomatic 2026 Java uses them; writing 2008-style Java (anonymous-class listeners, getters on everything, thread pools for I/O) in a modern codebase is the main anti-pattern. Effective Java's discipline still rules: minimize mutability, design APIs deliberately, favor composition.

## Language — write current Java

- Records for data carriers — no Lombok, no handwritten equals/hashCode; a record with compact-constructor validation replaces a 60-line bean
- Sealed interfaces + record implementations for closed hierarchies; exhaustive `switch` pattern matching over visitor patterns and `instanceof` chains
- Pattern matching everywhere it clarifies: `if (obj instanceof User(var name, _))`, switch with guards (`case Order o when o.total() > 100`)
- `Optional` as a return type only — never a field, parameter, or collection element; never `Optional.get()` without a presence check
- `var` for locals when the right side makes the type obvious; spelled-out types at API boundaries
- Text blocks for SQL/JSON/HTML literals; `String.formatted` over concatenation chains
- Streams for transformation pipelines; a plain loop when it's clearer or has side effects — stream gymnastics that need comments should be loops

## Immutability and API design

- Fields `final` by default; collections exposed as unmodifiable (`List.copyOf`) — defensive copies at trust boundaries
- Constructor injection only; no field injection, no setters for dependencies — objects are valid at construction or they throw
- Static factory methods (`of`, `from`, `parse`) over telescoping constructors; builders only past ~4 parameters
- Package-private is the default visibility; `public` is an API commitment

## Concurrency — virtual threads changed the defaults

- I/O-bound work: virtual threads (`Executors.newVirtualThreadPerTaskExecutor()`) — thread-per-request is idiomatic again; do NOT pool virtual threads, they're cheap by design
- Never `synchronized` around blocking I/O on hot virtual-thread paths in pre-24 JDKs (carrier pinning) — use `ReentrantLock` there; JDK 24+ removed most pinning
- CPU-bound work still gets a sized platform-thread pool
- Shared state: prefer immutable snapshots and `ConcurrentHashMap` over manual locking; `volatile` is for flags, not compound state
- `CompletableFuture` chains are legacy glue — with virtual threads, straight-line blocking code is both simpler and correct

## Errors

- Unchecked exceptions by default; checked exceptions only where the caller has a real recovery path
- Never swallow: catch specific types, add context, rethrow or handle — `catch (Exception e) {}` is a bug
- try-with-resources for anything `AutoCloseable`; suppressed exceptions are preserved for free

## Ecosystem defaults

- Build: Maven for boring-and-standard, Gradle (Kotlin DSL) where builds are complex — match the repo, never mix
- Spring Boot is the mainstream frame: constructor injection, `@ConfigurationProperties` records over `@Value` scatter, profiles for environment split
- Persistence: prefer JDBC/JdbcTemplate or jOOQ for SQL-shaped problems; JPA/Hibernate only with somebody owning its complexity (N+1, lazy sessions, dirty checking)
- `java.time` exclusively — `Instant` for machine time, `LocalDate`/`ZonedDateTime` for human time; `Date`/`Calendar` are forbidden in new code

## Testing

- JUnit 5 + AssertJ (`assertThat(x).isEqualTo(y)`) — readable failure messages are the point
- `@ParameterizedTest` for input matrices — the table-driven idiom
- Testcontainers for real databases/brokers in integration tests; mock only at process boundaries you don't own
- Test behavior through the public API; a test that breaks on refactor without behavior change is testing structure, not behavior

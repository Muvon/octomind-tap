---
name: programming-php
title: "PHP Development"
description: "Write and review concise, typed PHP 8.x code with version-aware features through PHP 8.5, explicit validation, and practical quality checks."
license: Apache-2.0
compatibility: "PHP 8.2+ and Composer. Newer features require the corresponding PHP version and compatible tooling."
domains: developer
rules:
  - file(composer.json)
  - content(php)
---

## Overview

Write clear PHP with explicit types, validated inputs, and small, cohesive functions and objects. Apply modern features where they simplify the task; preserve existing project conventions except for the brace rule below.

## Mental model

PHP is dynamically typed with optional declarations and opt-in strict scalar checking. Types describe values; validation checks inputs; constructors and mutations enforce business invariants.

## Runtime

- Checked 2026-09-05: PHP 8.5 is the latest stable branch. Recheck the official support table when choosing a new baseline; prereleases are not production defaults.
- Determine the minimum runtime from Composer requirements, `config.platform`, CI, and deployment. Match syntax, extensions, dependencies, and analyzer settings to that minimum. A runtime condition cannot hide unsupported syntax in the same file.
- Composer's platform setting simulates dependency resolution, not runtime compatibility. Verify with `composer check-platform-reqs` in the target environment. Preserve version constraints unless an upgrade is requested.

## Style and design

- Always place function, method, and closure opening braces on the final signature line: `function name(): void {`. For multiline signatures, place the brace after the closing parenthesis and any return type. This overrides PER/PSR-12 brace placement.
- Follow other repository formatting rules. Without an existing standard, use PHP-FIG PER Coding Style (3.1 at research time) with this brace exception.
- Use descriptive names, guard clauses, and focused functions. Prefer a clear loop to clever callbacks or nested ternaries. Add abstractions for real responsibilities, not pattern compliance.
- Inject dependencies; separate calculations from I/O. Preserve framework/ORM conventions and Composer PSR-4 mappings. Don't introduce layers, repository wrappers, or a message bus for simple CRUD.
- Keep request state out of shared long-running services. Respect ORM/proxy requirements before adding `final`, readonly properties, or hooks.

## Types and correctness

- Use `declare(strict_types=1);` in new PHP files; assess coercion changes before adding it to existing files. Scalar argument strictness follows the caller's file and does not validate external data.
- Type parameters, returns, and properties. Narrow external `mixed`; use PHPDoc only for additional contracts such as `list<User>`, array shapes, and generics. PHPDoc is not runtime validation.
- Prefer constructor promotion and readonly value objects for stable data. Readonly is shallow: contained objects can still mutate. Prefer `DateTimeImmutable` for immutable dates.
- Enforce invariants at construction and mutation, including CLI/queue callers. An `int` is not necessarily positive. Use integer minor units or decimal arithmetic for exact money.
- Use enums for closed sets, backed enums for scalar serialization, and constants for independent values. Validate scalar types before `tryFrom()`; use `from()` when invalid values should throw.
- Prefer `===`, strict `in_array(..., true)`, and explicit absence checks. `empty()` conflates zero/false with absence; `isset()` and `??` conflate null with missing keys. Use `array_key_exists()` when needed.
- Use `match` for strict selection and `?->` for expected absence. Don't hide unhandled enum cases with a fallback. Named arguments couple callers to parameter names.

## Modern features

Use only when the minimum runtime and tooling support them.

| PHP | Useful features | Important limits |
|-----|-----------------|------------------|
| 8.3 | Typed class constants; `#[\Override]` on methods | Preserve parent/interface contracts. |
| 8.4 | Property hooks; `public private(set)` | Keep hooks local and free of I/O. Hooked properties cannot be readonly; restricted setters still permit internal mutation. |
| 8.4 | `array_find()`, `array_find_key()`, `array_any()`, `array_all()`; native lazy objects | Use the key variant to distinguish a matched null from absence. Let compatible frameworks manage lazy objects. |
| 8.5 | `\|>` pipelines; `array_first()`, `array_last()` | Prefer ordinary calls when clearer. Endpoint helpers return null for empty arrays or stored null values. |
| 8.5 | `clone($object, [...])`; `#[\NoDiscard]` | Cloning is shallow and does not rerun constructor validation. Preserve invariants. NoDiscard warns about ignored results, not failed operations. |
| 8.5 | `Uri\Rfc3986\Uri`, `Uri\WhatWg\Url` | Choose the required standard; parsing alone does not prevent SSRF or authorize destinations. |

During upgrades, read each crossed version's migration guide. Avoid ordinary dynamic properties (deprecated in 8.2); preserve intentional framework magic. Use explicit `?T $value = null` (implicit nullability deprecated in 8.4). Use canonical casts such as `(int)` and `(bool)`; noncanonical casts and backtick execution are deprecated in 8.5.

## Boundaries and errors

- Decode JSON with `JSON_THROW_ON_ERROR`, then validate shape and values. Don't cast malformed input into plausible data or deserialize untrusted PHP objects.
- Preserve established exception/result conventions. Catch specific failures, retain exception causes, and use `finally` for owned resources. Catch `Throwable` at execution boundaries where appropriate; don't turn programming bugs into success.
- Bind SQL values; allowlist identifiers and sort directions. Use transactions, database constraints, and appropriate locking for related writes. Bound queries, prevent N+1 access, and preserve applied migrations.
- Make retried mutations idempotent and coordinate external effects with durable state. Validate and authorize separately; serialize explicit responses and escape output for its destination. Use password hashing APIs and cryptographic random tokens; exclude secrets from logs.

## Example

Validate a positive integer without coercing strings, floats, or booleans:

```php
<?php

declare(strict_types=1);

function positiveInt(mixed $value): int {
    if (!is_int($value) || $value < 1) {
        throw new InvalidArgumentException('Expected a positive integer.');
    }

    return $value;
}
```

`positiveInt(2)` succeeds; `'2'`, `2.5`, `true`, `0`, and `null` fail. Domain objects must also enforce their own invariants.

## Checklist

- [ ] Runtime, dependencies, syntax, and analyzer targets agree.
- [ ] Braces follow the same-line rule; new abstractions improve clarity.
- [ ] Inputs, invariants, authorization, and persistence behavior are checked.
- [ ] Relevant syntax/style checks, PHPStan or Psalm, and PHPUnit or Pest pass using existing project tooling and execution permissions. Test behavior and failure cases; use strict assertions where types matter.
- [ ] Dependency changes include Composer validation, platform checks, and an advisory audit. Report unexecuted checks; don't suppress findings or broadly update dependencies to make checks pass.

## References

- Versions and upgrades: [support table](https://www.php.net/supported-versions.php), [8.3 migration](https://www.php.net/manual/en/migration83.php), [8.4 migration](https://www.php.net/manual/en/migration84.php), [8.5 migration](https://www.php.net/manual/en/migration85.php), [8.5 features](https://www.php.net/releases/8.5/en.php).
- Language semantics: [types](https://www.php.net/manual/en/language.types.declarations.php), [properties](https://www.php.net/manual/en/language.oop5.properties.php), [hooks](https://www.php.net/manual/en/language.oop5.property-hooks.php), [cloning](https://www.php.net/manual/en/language.oop5.cloning.php).
- Tooling: [PER style](https://www.php-fig.org/per/coding-style/), [PHPStan types](https://phpstan.org/writing-php-code/phpdoc-types), [Composer platform](https://getcomposer.org/doc/06-config.md#platform).

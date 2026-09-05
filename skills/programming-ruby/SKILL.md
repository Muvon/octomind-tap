---
name: programming-ruby
title: "Ruby Development"
description: "Idiomatic Ruby and Rails architecture: objects, services, ActiveRecord boundaries, and modern Hotwire patterns. Auto-activates in Ruby projects."
license: Apache-2.0
compatibility: "Requires a supported Ruby and Bundler; Rails guidance applies only to Rails projects."
domains: developer
rules:
  - file(Gemfile)
  - content(ruby)
---

## Overview

Write idiomatic Ruby with explicit data contracts and predictable persistence. Research baseline: 2026-09-05, Ruby 4.0 stable; Rails guidance below targets supported Rails 8 APIs. Check `.ruby-version`, the Gemfile/lockfile, Ruby implementation, and Rails version before using newer features. Preserve existing application conventions and dependencies; a small change does not need a new service layer or gem extraction.

## Mental model

Ruby's flexibility makes names and failure contracts important. Keep domain behavior near the object that owns it; extract orchestration only when it has independent responsibilities. Rails conventions reduce boilerplate, but callbacks, transactions, and asynchronous jobs have distinct timing and failure semantics.

## Current language features

- Ruby 3.2+ `Data.define` describes fixed value records; members cannot be reassigned, but referenced strings/arrays/hashes are not deeply frozen. `Struct` is mutable unless frozen. Copy/freeze nested values only when the contract needs it.
- Ruby 3.4's implicit block parameter `it` suits a short, obvious block; use named parameters for nested or nontrivial logic. New syntax should improve readability rather than demonstrate novelty.
- Ruby 4 makes `Set` a core class and adds `Array#rfind` for reverse search. Keep older-version `require "set"` compatibility when the repository supports older Rubies.
- Ruby 4's Ruby Box and Ractor remain experimental; ZJIT is also experimental. Do not introduce them or switch JITs as routine cleanup.
- Keep frozen-string policy explicit and consistent with the project. `# frozen_string_literal: true` freezes literals, not all strings; use `+""` or an owned duplicate when mutation is intended.

## Values and control flow

- Use keyword arguments where positional arguments hide intent. Forward positional arguments, keywords, and blocks accurately; Ruby 3 distinguishes a positional hash from keyword arguments.
- Prefer `fetch` for required hash/configuration keys; use `[]`, `dig`, and `&.` only where absence is valid. A chain of nil-tolerant operations must not conceal a missing invariant.
- Ruby treats only `nil` and `false` as falsey. `||=` does not cache a valid false/nil result; use an explicit initialization check when those results matter.
- Use explicit parsing such as `Integer(text, 10)` for validated integer input; `to_i` can silently accept malformed data. Keep absence distinct from invalid syntax.
- Use `map` for transformation, `each` for effects, and `filter_map` only when discarding both nil and false is intended. Keep long chains readable with named intermediate values.
- A `return` inside a normal block exits its enclosing method; an escaped proc can raise `LocalJumpError` when that method has returned. A lambda's `return` exits the lambda. Use `next` for the current block invocation.
- Predicate methods conventionally end in `?`; `!` identifies a more dangerous counterpart, not a universal promise to mutate or raise. Follow the specific method contract.

## Errors and resources

- Rescue the specific error where recovery or translation is meaningful. Ordinary custom errors derive from `StandardError`; do not broadly rescue `Exception`, which includes shutdown and interrupt conditions.
- Preserve causes when wrapping failures. Avoid rescue modifiers, empty rescues, and fallback empty collections that convert broken I/O or invalid data into success.
- Use block forms of resource APIs, or `ensure` when cleanup must span custom control flow. Do not return from `ensure`, which can replace results or suppress errors.
- Bound retries to identified transient failures and account for side effects already performed. Prefer an explicit not-found result only where the caller expects one.

## Rails persistence and jobs

- Keep entity behavior on the model when cohesive; extract a query, form, or orchestration object only when it clarifies a real boundary. Controllers should adapt HTTP and authorize operations, not dictate arbitrary class counts.
- Rails 8's `params.expect` can require and permit an expected parameter shape together. Strong Parameters filter assignment; they do not authorize access or validate all domain constraints.
- Back uniqueness and cross-record invariants with database constraints and appropriate locking. A model validation alone cannot prevent races. Choose eager loading based on accessed relationships.
- Transactions cover database work on their connection; they do not roll back HTTP calls or restore in-memory objects. Use raising persistence methods when failure must abort; ordinary `save` returning false does not trigger rollback automatically.
- `ActiveRecord::Rollback` rolls back but is swallowed by the transaction boundary. Do not rescue database statement errors inside a transaction and continue using a potentially aborted transaction.
- Schedule external effects after commit when appropriate; use durable coordination when delivery must survive a process crash. Make jobs safe under duplicate execution and bounded retries.
- Active Job supports records via GlobalID, which reloads them later. Choose IDs, records, or explicit snapshots according to desired semantics and handle deletion before execution. Verify enqueue-after-commit behavior for the actual adapter/database setup.

## Example

Preserve a legitimate false value and reject a malformed required value:

```ruby
# frozen_string_literal: true

def read_settings(input)
  enabled = input.fetch("enabled")
  unless enabled == true || enabled == false
    raise ArgumentError, "enabled must be boolean"
  end

  attempts = Integer(input.fetch("attempts"), 10)
  raise ArgumentError, "attempts must be positive" unless attempts.positive?

  { enabled: enabled, attempts: attempts }
end
```

This boundary expects string input for `attempts`, such as form/config text. Missing keys and malformed values remain explicit failures.

## Checklist

- Check Ruby/Rails version gates and retain the project's formatter and testing conventions.
- Distinguish nil/false/missing from invalid data; check mutation and block-return semantics.
- Verify transaction failure, database constraints, job duplication, and commit timing.
- Use installed project commands through `bundle exec` or binstubs when authorized; test observable behavior with the existing Minitest/RSpec setup. Do not replace fixtures or test libraries by preference.

## References

- [Ruby release lines](https://www.ruby-lang.org/en/downloads/releases/)
- [Ruby 4.0 features and experimental status](https://www.ruby-lang.org/en/news/2025/12/25/ruby-4-0-0-released/)
- [Ruby 3.4 changes](https://www.ruby-lang.org/en/news/2024/12/25/ruby-3-4-0-released/)
- [Data immutability](https://docs.ruby-lang.org/en/4.0/Data.html), [Proc control flow](https://docs.ruby-lang.org/en/4.0/Proc.html), and [Hash access](https://docs.ruby-lang.org/en/4.0/Hash.html)
- [Strong Parameters](https://api.rubyonrails.org/classes/ActionController/Parameters.html)
- [Active Record transactions](https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html)
- [Active Job and transaction behavior](https://guides.rubyonrails.org/active_job_basics.html)

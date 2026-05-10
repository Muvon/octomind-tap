---
name: programming-ruby
title: "Ruby Development"
description: "Idiomatic Ruby and Rails architecture: objects, services, ActiveRecord boundaries, and modern Hotwire patterns. Auto-activates in Ruby projects."
license: Apache-2.0
compatibility: "Requires Ruby 3.x and Bundler."
domains: developer
rules:
  - file(Gemfile)
  - content(ruby)
---

## Mental model

Ruby rewards expressive, intention-revealing code; Rails rewards convention. The maintainable Rails app keeps controllers thin, models focused on persistence and small associated behaviors, and business logic in service objects, form objects, or domain modules. Most pain comes from fat models (every concern bolted on), fat controllers (logic inlined), and callbacks that fire side effects whenever a record saves.

## Idiomatic Ruby

- Expressive method names — `user.active?` over `user.is_active`, `users.empty?` over `users.size == 0`
- Blocks and iterators express intent — `each`, `map`, `select`, `reduce`, `tap`, `then`
- Pattern matching (`case/in`) for destructuring nested data; cleaner than chained `if`/`elsif`
- Safe navigation `&.` for nil-tolerant chains; `dig` for nested hashes/arrays
- Keyword arguments for clarity on methods with more than one or two parameters
- Frozen string literals (`# frozen_string_literal: true`) at the top of every file — cheap immutability
- Modules for shared behavior (mixins) and namespacing; classes for things with state

## Object design

- Small, focused classes — a class that does one thing is easier to test and change than a "manager" doing five
- Plain Ruby objects (POROs) for domain concepts that aren't tables; they don't need to inherit from anything
- Value objects (`Data.define` in Ruby 3.2+ or `Struct`) for immutable bundles of attributes
- Duck typing — accept anything that responds to the method you call; don't pre-declare interfaces unless they earn their keep
- Composition over inheritance; reach for inheritance only when the "is-a" relationship is genuine and stable

## Errors

- Rescue `StandardError`, never `Exception` (it catches `SignalException`, `SystemExit`)
- Custom exception classes inherit from `StandardError`; name them after the failure (`UserNotFound`, `PaymentDeclined`)
- Catch specific errors first, then fall back if needed; empty `rescue` blocks are bugs
- `raise` with a class plus message — `raise UserNotFound, "id=#{id}"`
- Don't use exceptions for predictable control flow — return `nil`, a Result-shaped value, or use a method ending in `?` / `!` to signal intent

## Rails architecture

- Controllers: parse input, call one application method, render — five lines, not fifty
- Strong Parameters for input filtering; never `params.permit!`
- Models: persistence, validations, scopes, and behaviors that genuinely belong to the entity; everything else moves out
- Service objects (`app/services/`) for orchestration: one class per use case (`CreateInvoice`, `ChargePayment`)
- Form objects when a form spans multiple models or carries validation distinct from persistence
- Query objects when ActiveRecord scopes start composing into something hard to read
- Concerns for genuinely shared behavior across multiple models — not as a hiding place for fat-model code

## ActiveRecord discipline

- Avoid lifecycle callbacks for side effects (sending email, hitting other services) — they make tests slow and behavior surprising; move them into service objects
- Validations belong on the model; cross-record consistency belongs in transactions
- Eager-load relationships explicitly (`includes`, `preload`) to kill N+1
- Wrap multi-step writes in `transaction do ... end`; handle `ActiveRecord::Rollback` deliberately
- Migrations are forward-only in production; new changes are new migrations

## Async and background work

- ActiveJob with Solid Queue (Rails 8 default), Sidekiq, or Resque — pick one and stick with it
- Jobs are idempotent — they may run more than once
- Pass IDs to jobs, not records — the record may have changed by the time the job runs
- Long-running tasks belong in jobs, not in request handlers

## Hotwire and views

- Turbo Drive, Frames, and Streams for progressive enhancement — most Rails UI doesn't need a SPA
- Stimulus controllers for sprinkles of interactivity scoped to elements
- Partials with locals for reusable templates; ViewComponent or Phlex for component-style views with their own tests
- I18n for user-facing strings from day one

## Testing

- RSpec or Minitest — both are fine; pick one per project
- Model specs test validations, scopes, and methods; controller/request specs test HTTP behavior; system specs (Capybara) test critical user flows
- FactoryBot for test data, not fixtures
- `let` and `let!` for shared setup; `shared_examples` and `shared_context` for cross-spec reuse
- Don't mock what you don't own — wrap third-party libraries in a thin adapter and mock the adapter

## Project layout

- Standard Rails layout for Rails apps; `lib/` for code that's genuinely framework-free
- Engines for in-app modular boundaries when the app grows large
- Gems for code shared across multiple apps — extract sooner than feels comfortable

## Common pitfalls

- `return` inside a block (not a lambda) raises `LocalJumpError` — use `next` to exit the iteration
- `respond_to_missing?` must accompany every `method_missing` override
- `require` searches `$LOAD_PATH`; `require_relative` is path-relative — mixing them up causes load-order bugs
- `bundle exec` for any command that depends on the project's gems

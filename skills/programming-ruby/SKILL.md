---
name: programming-ruby
title: "Ruby Development"
description: "Ruby conventions, Rails patterns, RSpec testing, RuboCop linting, and idiomatic Ruby best practices. Auto-activates in Ruby projects."
license: Apache-2.0
compatibility: "Requires Ruby and Bundler."
domains: developer
rules:
  - file(Gemfile)
  - content(ruby)
---

# Ruby Development

## Conventions

- Idiomatic Ruby — expressive, readable, convention-over-configuration
- Duck typing — if it responds to the method, it works
- `# frozen_string_literal: true` — at top of every file
- 2-space indentation, `snake_case` methods/variables, `CamelCase` classes, `SCREAMING_SNAKE` constants
- Rescue `StandardError`, NEVER rescue `Exception` — it catches `SignalException`/`SystemExit`
- Safe navigation operator `&.` for nil-safe method calls
- Pattern matching (`case/in`) for complex destructuring (Ruby 3.x)

## Error Handling

- Custom exceptions inherit from `StandardError`, not `Exception`
- Rescue specific errors first: `rescue SpecificError => e`
- `retry` with counter — always cap retries
- Never empty rescue blocks — at minimum log the error
- `raise CustomError, "message"` for specific types

## Blocks & Iterators

- Prefer blocks: `items.each { |i| process(i) }`
- `do...end` for multi-line, `{ }` for single-line
- `&method(:name)` for method-to-proc conversion
- Lambda (strict arity) over `Proc.new` (loose arity)

## Testing (RSpec)

- `describe`/`context`/`it` structure with `let` (lazy) and `let!` (eager)
- `expect(x).to eq(y)` — not `assert_equal`
- FactoryBot for test data, not fixtures
- `before` blocks for setup, `shared_examples` for reuse

## Rails Conventions

- Convention over configuration — naming dictates behavior
- Resourceful routes and controllers
- Strong Parameters: `params.require(:user).permit(:name, :email)`
- Service objects in `app/services/` for complex business logic
- Jobs (ActiveJob/Solid Queue) for async work
- Turbo + Stimulus (Hotwire) for modern frontend
- Rails 8: Solid Queue/Cache/Cable, Kamal deploy, built-in auth

## Common Pitfalls

- `return` in blocks causes `LocalJumpError` — use `next`
- `require` vs `require_relative`: `require` searches `$LOAD_PATH`
- `method_missing` without `respond_to_missing?` — always define both
- Don't forget `bundle exec` for gem commands

## Tooling

| Command | Purpose |
|---------|---------|
| `bundle install` | Install dependencies |
| `bundle exec rspec` | Run RSpec tests |
| `bundle exec rubocop -A` | Lint and auto-fix |
| `rails test` | Run Minitest |
| `rails db:migrate` | Run migrations |
| `rails console` | Interactive console |

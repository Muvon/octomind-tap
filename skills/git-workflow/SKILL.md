---
name: git-workflow
title: "Git Workflow: Commits, Branches, Rebasing"
description: "Git commit message conventions, branch naming, and workflow best practices for clean version history. Activate when committing, branching, rebasing, or reviewing git history."
license: Apache-2.0
compatibility: "Requires git. Works with any git-based project."
capabilities: versioning
domains: developer devops
rules:
  - file(.git)
---

## Overview

This skill encodes git commit conventions (Conventional Commits), branch naming rules, and workflow best practices. Activate it when you need to commit changes, name a branch, clean up history, or review git practices in a project.

## Instructions

### Commit Message Format

Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<scope>): <short summary>

[optional body]

[optional footer]
```

Types: the spec itself defines only `feat` (maps to a SemVer MINOR) and `fix` (PATCH). The common extended set comes from commitlint's `config-conventional`:
- `feat` — new feature
- `fix` — bug fix
- `refactor` — code change that neither fixes a bug nor adds a feature
- `perf` — performance improvement
- `test` — adding or updating tests
- `docs` — documentation only
- `style` — formatting, no behavior change
- `build` — build system or dependencies
- `ci` — CI/CD changes
- `chore` — other maintenance
- `revert` — reverts a previous commit

If the repo already enforces a type list (commitlint config, CONTRIBUTING), that list wins.

Breaking changes (MAJOR): add `!` right before the colon — `feat(api)!: drop v1 endpoints` — and/or a footer `BREAKING CHANGE: <what breaks and how to migrate>`. The footer token is uppercase; `BREAKING-CHANGE` is equivalent.

Rules:
- Summary line: imperative mood ("add" not "added"), aim for ~50 characters, hard limit 72
- No period at end of summary
- Body: wrap at 72 characters, explain why not what
- Footers use `Token: value` with hyphenated tokens (`Reviewed-by:`, `Co-authored-by:`, `Signed-off-by:`); reference issues as `Fixes #123` / `Closes #456` so the forge auto-closes them

### Branch Naming

```
<type>/<short-description>
```

- `feat/user-profile-page`
- `fix/login-redirect-loop`
- `refactor/extract-auth-middleware`
- `chore/upgrade-tokio-1.47`

Use kebab-case. Keep it short but descriptive. Match the commit type.

### Workflow Rules

1. Never commit directly to `main` — always use a short-lived branch
2. Keep commits atomic — one logical change per commit
3. Update your branch by rebasing onto the fresh remote: `git fetch origin && git rebase origin/main`. Rebase only branches nobody else has built on
4. After rewriting a pushed branch, push with `git push --force-with-lease --force-if-includes` — never plain `--force`
5. Clean up before opening a PR: make corrections as `git commit --fixup=<sha>`, then fold them with `git rebase --autosquash origin/main` (Git 2.44+ applies autosquash without `-i`, so it runs non-interactively)
6. Stacked branches: `git rebase --update-refs` moves every branch in the stack in one pass
7. Tag releases with semantic versioning (`v1.2.3`), annotated (`-a`) or signed (`-s`)

## Examples

### Good commit message

```
feat(auth): add JWT refresh token rotation

Prevents token reuse after logout by invalidating the previous
refresh token on each use.

Closes #89
```

### Bad commit message → fix it

```
# Bad
fixed stuff
update
WIP
```

```
# Good
fix(api): handle empty response body in error parser

The parser panicked when the server returned a 500 with no body.
Added a fallback to use the status text instead.
```

### Common commands

```bash
# Start a feature (git switch replaces checkout for branches)
git switch -c feat/my-feature

# Stage only relevant changes (interactive; agents stage explicit paths instead)
git add -p

# Amend last commit (before push)
git commit --amend --no-edit

# Fix an earlier commit, then fold it in without an editor
git commit --fixup=<sha>
git rebase --autosquash origin/main

# Check what will be committed
git diff --staged

# Tag a release
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3
```

## References

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [git-rebase documentation](https://git-scm.com/docs/git-rebase)

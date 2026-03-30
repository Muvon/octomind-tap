---
name: git-workflow
title: "Git Workflow"
description: "Git commit conventions, branch naming, and workflow best practices for clean version history. Activate when committing, branching, rebasing, or reviewing git history."
license: Apache-2.0
compatibility: "Requires git. Works with any git-based project."
---

# Git Workflow Skill

## Overview

This skill encodes git commit conventions (Conventional Commits), branch naming rules, and workflow best practices. Activate it when you need to commit changes, name a branch, clean up history, or review git practices in a project.

---

## Instructions

### Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <short summary>

[optional body]

[optional footer]
```

**Types:**
- `feat` — new feature
- `fix` — bug fix
- `refactor` — code change that neither fixes a bug nor adds a feature
- `perf` — performance improvement
- `test` — adding or updating tests
- `docs` — documentation only
- `chore` — build process, tooling, dependencies
- `ci` — CI/CD changes

**Rules:**
- Summary line: max 72 characters, imperative mood ("add" not "added")
- No period at end of summary
- Body: wrap at 72 characters, explain *why* not *what*
- Reference issues in footer: `Fixes #123`, `Closes #456`

### Branch Naming

```
<type>/<short-description>
```

- `feat/user-profile-page`
- `fix/login-redirect-loop`
- `refactor/extract-auth-middleware`
- `chore/upgrade-tokio-1.40`

Use kebab-case. Keep it short but descriptive. Match the commit type.

### Workflow Rules

1. **Never commit directly to `main`** — always use a branch
2. **Keep commits atomic** — one logical change per commit
3. **Rebase before merging** — keep history linear: `git rebase main`
4. **Squash WIP commits** before opening a PR
5. **Tag releases** with semantic versioning: `v1.2.3`

---

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
# Start a feature
git checkout -b feat/my-feature

# Stage only relevant changes
git add -p

# Amend last commit (before push)
git commit --amend --no-edit

# Interactive rebase to clean up
git rebase -i HEAD~3

# Check what will be committed
git diff --staged

# Tag a release
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3
```

---

## References

- [Conventional Commits specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

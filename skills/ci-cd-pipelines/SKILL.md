---
name: ci-cd-pipelines
title: "CI/CD Pipelines and Supply-Chain Hardening"
description: "Write and debug GitHub Actions and GitLab CI pipelines: triggers, caching, concurrency, OIDC to the cloud, token permissions and action pinning."
license: Apache-2.0
compatibility: "Needs the repository's workflow files; GitHub Actions and GitLab CI syntax. Hosted runners or self-managed runners."
domains: developer devops security-analyst
rules:
  - content(github actions)
  - content(gitlab ci)
  - content(ci/cd)
  - content(pipeline) content(workflow)
  - match((?i)\bgithub\s+actions?\b|\bgitlab[\s-]?ci\b|\bci\s*/\s*cd\b|\bcicd\b)
  - match((?i)\b(ci|build|deploy|deployment|release)\s+(pipeline|workflow)s?\b)
  - match((?i)\bpull_request_target\b|\bdependabot\b|\b(pin|pinned|pinning)\b.{0,30}\bactions?\b|\b(oidc|id[\s-]?token)\b.{0,40}\b(aws|gcp|azure|github|gitlab)\b)
---

## Overview

Use this when you write, debug or harden a CI/CD pipeline on GitHub Actions or GitLab CI. The outcome is a pipeline that is fast, deterministic, and cannot hand its credentials to untrusted code. Platform facts below carry an as-of date; read the vendor documentation before relying on one that affects a decision.

## Mental model

A pipeline is code that runs with credentials on someone else's trigger. Three questions decide every design choice: who can cause this job to run (the trigger), what can that job reach (token permissions, secrets, cloud role), and what code does it execute (your code, a pull request's code, a third-party action). Hardening means that untrusted triggers never meet powerful credentials, and that every executed dependency is fixed to an exact version.

## Rules

### Triggers and untrusted input (GitHub Actions)

- `pull_request` from a fork runs with a read-only token and no secrets. `pull_request_target` and `workflow_run` run with the base repository's privileges: don't check out or build code from the pull request in them. Split privileged work into a separate `workflow_run` workflow and treat its artifacts as untrusted.
- Expression values such as `github.event.pull_request.title`, branch names and issue bodies are attacker-controlled. Don't write `${{ ... }}` of such a value inside a `run:` script. Pass it through `env:` and use the quoted shell variable, or use an action that takes it as an input.
- Self-hosted runners almost never belong on public repositories. Where they are used, make them ephemeral (one job per runner).

### Token permissions

- Set the workflow default to read-only, then raise per job:

```yaml
permissions:
  contents: read
jobs:
  release:
    permissions:
      contents: write
      id-token: write
```

- GitLab: use job tokens with the narrowest allowlist, protected variables only on protected branches and tags, and masked variables for secrets.

### Cloud access without stored keys

- Federate with OpenID Connect (OIDC) instead of long-lived keys. On GitHub, the job needs `id-token: write`; the cloud role trusts the issuer `token.actions.githubusercontent.com`, the audience (`sts.amazonaws.com` for AWS), and a `sub` condition that names the repository and one ref or environment, for example `repo:org/repo:environment:prod` or `repo:org/repo:ref:refs/heads/main`. A trust policy without a `sub` condition lets any workflow that reaches the issuer assume the role.
- On GitLab, declare `id_tokens:` with an `aud:` per target service; the token's claims include `ref_protected`, so the cloud side can require a protected ref. Use `id_tokens`, not the deprecated `CI_JOB_JWT` variables.
- Apply to production through a protected environment with required reviewers.

### Pin what executes

| Item | Rule |
|---|---|
| Third-party actions | Pin to a full commit SHA from the action's own repository (not a fork), with the tag in a trailing comment. Tags can be moved. Dependabot does not alert on SHA-pinned actions, so enable version updates for `github-actions`. |
| Transitive actions | SHA pinning covers only the top-level reference. GitHub's workflow lockfile (`.github/workflows/actions.lock`, made with the `gh actions-lock` extension) records commits for actions and their dependencies; it was announced in public preview on 2026-10-14 and became generally available on 2026-10-28 (GitHub changelog). Check the current docs; GitHub says a lockfile supersedes SHA pinning for repositories that adopt it. |
| Container images | By digest (`image@sha256:...`), not by tag. |
| Scanners and security tools | By exact version or digest. Trivy's releases and action tags were hijacked in March 2026 (CVE-2026-33634); a tag alone is not a fixed version, so pin the digest or commit. |
| Fresh releases | Delay adoption. Dependabot `cooldown` skips updates released within N days (default 3 for version updates; security updates are exempt): `cooldown: { default-days: 7 }`. |
| GitLab includes and components | Pin `include:component` to a version (`@1.2.0`) or SHA, `include:project` to a ref, never `main`. |

- Don't run `curl | sh` in a pipeline; download a pinned release and verify its checksum or signature.
- Protect `.github/workflows/` with CODEOWNERS so workflow changes get review.

### Speed and correctness

- GitHub concurrency: `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }` for builds; for deploy jobs use a group without cancel so a deploy is never cut in half.
- GitLab: `workflow:rules` decides whether the pipeline exists; job `rules` decide each job. `interruptible: true` lets a newer commit cancel a job. `needs:` starts a job before earlier stages finish. `resource_group:` serializes deploys.
- Cache keys come from the lockfile: GitHub `key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}`; GitLab `cache:key:files: [package-lock.json]`. A cache holds dependencies; an artifact holds build output passed between jobs. Set `retention-days` (GitHub) or `expire_in` (GitLab) on artifacts.
- Matrix builds: set `fail-fast: false` when you need every result; keep the matrix to supported versions.
- Reuse: GitHub reusable workflows (`on: workflow_call`) and composite actions; GitLab components with `spec: inputs:`. Pin the caller's reference to a tag or SHA.
- Release provenance: build in CI, attach a build attestation or SBOM, sign, and deploy by digest. The workflow identity that publishes needs `id-token: write` plus `attestations: write` on GitHub.

### Debugging a failed pipeline

| Symptom | First check |
|---|---|
| Works locally, fails in CI | Tool versions, working directory, missing env var, case-sensitive paths, shallow clone (`fetch-depth`) |
| Job never starts | Trigger filter (branches, paths), `if:` condition, `rules` match, runner label or tag |
| Permission denied or 403 on push or API | Token `permissions`, fork pull request, protected branch rule |
| Cloud auth fails with OIDC | `sub` claim in the trust policy against the real token, audience, missing `id-token: write` |
| Cache never hits | Key changes every run, cache scope by branch, key built from a file that is not committed |
| Flaky | Network calls to unpinned resources, shared state between parallel jobs, time-dependent tests |

Read the failing step's log from the first error, not the last line. Reproduce with the same image or runner OS before changing the workflow.

## Examples

Bad: `uses: some-org/deploy@v3` with `permissions` unset and `run: echo "${{ github.event.issue.title }}"`.

Good: `uses: some-org/deploy@<40-character commit SHA> # v3.1.0`, workflow-level `permissions: contents: read`, and the title passed as `env: TITLE: ${{ github.event.issue.title }}` then `echo "$TITLE"`.

## Checklist

- [ ] Every trigger that can run for a fork has no secrets and no write token.
- [ ] No attacker-controlled expression is interpolated into a shell script.
- [ ] Workflow `permissions` default to read-only; each job states what it adds.
- [ ] Cloud access uses OIDC with a `sub` (or protected-ref) condition; no stored cloud keys.
- [ ] Actions pinned to a SHA or locked; images by digest; tools by version; update cooldown set.
- [ ] Deploys are serialized, and production needs approval.
- [ ] Caches key off lockfiles; artifacts have an expiry.
- [ ] Anything not verified against the live platform documentation is marked unverified.

## References

- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) and [OIDC in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [Workflow lockfiles changelog, 2026-10-14](https://github.blog/changelog/2026-10-14-github-actions-workflow-lockfiles-in-public-preview/)
- [Workflow lockfiles generally available, 2026-10-28](https://github.blog/changelog/2026-10-28-github-actions-workflow-lockfiles-are-generally-available/)
- [Dependabot cooldown](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference)
- [GitLab ID token authentication](https://docs.gitlab.com/ci/secrets/id_token_authentication/) and [GitLab CI/CD YAML reference](https://docs.gitlab.com/ci/yaml/)

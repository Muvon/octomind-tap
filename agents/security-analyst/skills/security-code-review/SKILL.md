---
name: security-code-review
title: "Secure Code Review: OWASP Top 10 and ASVS"
description: "Reviews code and config against the OWASP Top 10:2025 and ASVS 5.0: vulnerability assessment, secure-coding fixes, supply-chain audits."
license: Apache-2.0
compatibility: "Requires: a code checkout. Scanners (npm audit, pip-audit, cargo audit, osv-scanner, semgrep, gitleaks) help when installed."
capabilities: shell codesearch-semantic codesearch-structural codesearch-graph
rules:
  - match((?i)\b(owasp|asvs|cwe-\d+)\b)
  - match((?i)\b(review|audit|check|scan|assess|find)\b.{0,60}\b(code|codebase|repo|pull request|pr|endpoint|api|config\w*|workflows?|dockerfile|module|service)\b.{0,60}\b(security|vulnerab\w+|insecure|exploit\w*|flaws?|injection|access[- ]control)\b)
  - match((?i)\b(sql injection|injection|xss|cross[- ]site scripting|csrf|ssrf|idor|insecure deserialization|path traversal|command injection|broken access control|access[- ]control flaws?)\b)
  - match((?i)\b(threat[- ]model\w*|stride)\b)
  - match((?i)\b(typosquat\w*|lockfile|package\.json|requirements\.txt|unpinned|pin(ning)? (actions|packages|dependencies)|supply[- ]chain|sbom)\b|\bdependenc(y|ies)\b.{0,40}\b(audit|vulnerab\w+|risk\w*|attack|compromise\w*)\b)
  - match((?i)\bis (this|my) (code|app|endpoint|login|api|function)\b.{0,30}\b(secure|vulnerable|safe)\b)
  - semantic(review this code for security vulnerabilities and suggest fixes, 0.74)
  - semantic(audit my dependencies for supply chain risks)
  - semantic(is this login or upload endpoint safe against common web attacks)
---

## Overview

This skill reviews application source code and configuration for security flaws against the OWASP Top 10:2025 and ASVS 5.0, and delivers verified findings with fixes. It covers vulnerability assessment, secure-coding remediation, and dependency and supply-chain audits. The outcome is a short list of demonstrated vulnerabilities, each with the fix, and no speculative noise.

## Mental model

Security-first development: defense in depth, least privilege, secure and fail-closed defaults, allowlist input validation, context-aware output encoding, authorization on every request, security events logged without sensitive data, and proven crypto libraries only. Simple, readable security code is auditable code. No security through obscurity; delete dead code to shrink the attack surface; comments explain security decisions (why, not what); secure first, optimize later.

## Rules

### Method

- Verify a vulnerability exists before reporting it. Report only what you can demonstrate.
- For existing code, ask whether a finding is a vulnerability or intended behavior.
- Missing information on the first request: ask briefly, don't guess. "X not working" could mean missing, broken, wrong behavior, or a misunderstanding: clarify first.
- Not covered here: alert and log triage, phishing analysis, incident investigation, privacy and compliance frameworks, and offensive work (writing an exploit or payload against a system the user isn't authorized on).
- Multi-step remediation across files, new security controls, and complex fixes get a compact plan (one line per step) that the user confirms before you execute. Pure queries and single-step changes (fix a typo, add a header, update a config value) need no plan. When the brief is autonomous or non-interactive, apply the recommended option, execute, and list the assumptions in the final report.
- Scope discipline: "fix X" means find X, fix only X, stop. "Investigate Z" means report findings, no changes. No "while I'm here" extras.
- Finding code: start with AST-pattern search for vulnerable patterns and semantic code search for security-related code. Outline an unfamiliar or large file (over 200 lines) before reading ranges; read a small known file in full. Run independent searches together.
- Security tools: AST-pattern search finds vulnerable patterns; semantic code search finds security-related code; the shell runs scanners (npm audit, pip-audit, cargo audit, osv-scanner, semgrep, gitleaks, and so on); file reads inspect configuration.

### OWASP Top 10:2025: what to look for and the fix

| ID | Category | Look for | Fix |
|----|----------|----------|-----|
| A01 | Broken Access Control (now includes SSRF) | Missing object- or function-level checks (IDOR), privilege escalation, CORS misconfig, server fetching user-supplied URLs | Deny by default; authorize every request server-side against the object's owner; URL allowlists and egress limits for server-side fetches |
| A02 | Security Misconfiguration | Default creds, debug on, verbose errors, permissive cloud/IAM, XXE-enabled parsers, missing headers | Hardened repeatable config, IaC review, unused features removed |
| A03 | Software Supply Chain Failures | Unpinned or unvetted dependencies, typosquats, hijacked maintainers and self-spreading npm worms, over-privileged CI tokens, no SBOM | Lockfiles, SBOM, provenance and signing (SLSA, Sigstore), a short cooldown before adopting fresh releases; CI hardening (commit-SHA action pins, least-privilege tokens and secrets) per the `ci-cd-pipelines` skill |
| A04 | Cryptographic Failures | Weak or legacy algorithms, hardcoded secrets, plaintext sensitive data, home-made crypto | Vetted libraries, TLS everywhere, KMS or secret manager, Argon2id/scrypt/bcrypt for passwords |
| A05 | Injection (incl. XSS) | SQL/NoSQL/OS/LDAP/template injection, XSS | Parameterized queries, context-aware output encoding, CSP, no shell string interpolation |
| A06 | Insecure Design | Business-logic flaws, no rate limits on sensitive flows, trust-boundary violations | Threat model before building, using the `threat-modeling` skill; abuse cases as tests |
| A07 | Authentication Failures | Credential stuffing, weak recovery flows, session fixation, missing MFA | Passkeys or other phishing-resistant MFA; NIST SP 800-63B-4 passwords (length over composition, breached-password check, no forced rotation); rate limits; secure sessions |
| A08 | Software or Data Integrity Failures | Unsigned updates, insecure deserialization, trusting unverified data | Signature verification, safe deserialization, integrity checks |
| A09 | Security Logging and Alerting Failures | Security events unlogged, secrets in logs, logs nobody alerts on | Log authn/authz/admin events without sensitive data, alert on them, tamper-resistant storage |
| A10 | Mishandling of Exceptional Conditions | Fail-open error paths, unhandled exceptions leaking state, half-applied transactions | Fail closed, roll back atomically, generic errors outward, detail in internal logs |

### Related OWASP standards

- ASVS 5.0 (May 2025): requirement-level verification at levels 1-3. Use it when the user wants a verifiable checklist rather than a risk list.
- API Security Top 10 (2023), for APIs: broken object-level and property-level authorization, unrestricted resource consumption, unrestricted access to sensitive business flows.
- LLM Top 10 (2026 edition, published August 2026), for LLM features: prompt injection, excessive agency, improper output handling; treat model output as untrusted input. The `ai-prompt-injection-defense` skill holds the ID table; always write the edition with the ID (LLM03:2026).

### Security review checklist

Authentication and authorization:

- [ ] Password policy per NIST SP 800-63B-4 (length, breached-password check, no composition or rotation rules)
- [ ] MFA available, phishing-resistant (passkeys/FIDO2) for admins
- [ ] Session timeout implemented
- [ ] Authorization checks on every endpoint
- [ ] Role-based access control (RBAC)
- [ ] Principle of least privilege

Input validation:

- [ ] All input validated on allowlist
- [ ] Input length limits enforced
- [ ] Special characters handled
- [ ] File upload validation
- [ ] Content-Type validation

Data protection:

- [ ] Sensitive data encrypted at rest
- [ ] TLS for data in transit
- [ ] Secrets in secure storage (not code)
- [ ] PII handling compliant
- [ ] Data minimization

Security headers:

- [ ] Content-Security-Policy (frame-ancestors covers what X-Frame-Options did)
- [ ] X-Content-Type-Options: nosniff
- [ ] Strict-Transport-Security
- [ ] Referrer-Policy
- [ ] X-XSS-Protection omitted or set to 0 (deprecated; rely on CSP)

Error handling:

- [ ] Generic error messages
- [ ] No stack traces in production
- [ ] Security events logged
- [ ] No sensitive data in errors

Dependencies:

- [ ] Dependency and secret scanning enabled in CI
- [ ] Known vulnerabilities patched (CISA KEV entries first)
- [ ] Lockfiles committed, CI actions pinned by SHA
- [ ] Minimal dependencies, SBOM generated

## Examples

Finished task, zero fluff: "Found 3 vulnerabilities. Remediation steps provided." Then stop. No explanations unless asked, and no duplicated findings.

## Output format

Each finding: location, category (OWASP ID), the demonstrated flaw, and the fix. Don't create files (docs, Markdown reports) unless asked.

## Checklist

- [ ] Every reported vulnerability was demonstrated, not suspected.
- [ ] Findings are not duplicated.
- [ ] Multi-step remediation was confirmed with the user before execution, or the assumptions were listed for an autonomous brief.
- [ ] Only the requested scope was touched.
- [ ] Durable vulnerability patterns and remediation strategies were saved to memory after meaningful work, not transient state.

## Composition / References

- `threat-modeling` skill: design-level review before building.
- `ci-cd-pipelines` skill: CI hardening for supply-chain findings.
- `ai-prompt-injection-defense` skill: LLM Top 10 ID table.
- `secret-leak-response` skill: when a secret has already been exposed.

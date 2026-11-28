---
name: secret-leak-response
title: "Secret Leak Response: Leaked API Keys and Tokens"
description: "Steps after a leaked API key, token or password: revoke first, check audit logs, purge git history, add push protection. Use when a secret is exposed."
license: Apache-2.0
compatibility: "Needs git; git-filter-repo for history rewrites. Provider CLIs (for example the AWS CLI) speed up revocation and log searches."
rules:
  - match((?i)\b(committed|pushed|leaked|exposed|compromised|posted|pasted|uploaded|published)\b.{0,60}(\b(api[\s-]?keys?|(access|secret|signing|ssh|private)\s+keys?|(access|auth|bearer|secret|api|github|slack)\s+tokens?|secrets?|passwords?|credentials?)\b|(?:^|\s)\.env\b))
  - match((?i)(\b(api[\s-]?keys?|(access|secret|signing|ssh|private)\s+keys?|(access|auth|bearer|secret|api|github|slack)\s+tokens?|secrets?|passwords?|credentials?)\b|(?:^|\s)\.env\b).{0,60}\b(leaked|exposed|compromised|committed|pushed|uploaded|posted)\b)
  - match((?i)(\b(api[\s-]?keys?|(access|secret|signing|ssh|private)\s+keys?|tokens?|secrets?|passwords?|credentials?)\b|(?:^|\s)\.env\b).{0,60}(\b(in|on|to)\s+(a\s+|the\s+|my\s+)?public\s+(repo|repository|gist|bucket)\b|\bon\s+(github|pastebin)\b|\bin\s+(the\s+)?git\s+history\b))
  - match((?i)\b(gitleaks|trufflehog|secret\s+scanning|push\s+protection|git[\s-]?filter[\s-]?repo|bfg\s+repo[\s-]?cleaner)\b)
---

## Overview

A secret that reached a public place, or any place outside its intended audience, counts as copied. Deleting the commit or the message does not take the copy back. This skill gives the order of actions after a leak, so the secret stops working before anyone spends time on cleanup. The outcome is a dead secret, a known blast radius, a cleaned repository, and a guard against a repeat.

## Mental model

Three separate problems, solved in this order:

1. Stop the secret working (revoke). Takes minutes and ends the risk.
2. Learn what it did while it was exposed (blast radius). Needs logs, so do this before deleting anything.
3. Remove the copies you control (history rewrite). Cosmetic for security: forks, clones, caches and scrapers keep their copy.

People do step 3 first because it feels like undoing the mistake. It does not reduce risk.

## Rules

### Response order

| Step | Action | Done when |
|---|---|---|
| 1 | Revoke or deactivate the secret at the provider | The old secret fails a test call |
| 2 | Issue a replacement and deploy it | The service works with the new secret only |
| 3 | Set the exposure window: first commit or post time to revocation time | Two timestamps written down |
| 4 | Search the provider audit log for use of the old secret inside that window | Every hit is explained or escalated |
| 5 | Rewrite history and notify holders of copies | Secret absent from all refs on the remote |
| 6 | Add prevention (push protection, scanner, ignore rules) | A test secret is blocked on push |
| 7 | Record cause, window, findings and fix | One written entry exists |

### Step 1: revoke

- Deactivate when the provider offers it, delete after step 4. Deactivation is reversible if a production job breaks, and the key stays visible in the audit trail. AWS documents this order for access keys: set the key to `Inactive`, confirm nothing needs it, then delete it ([AWS IAM, update access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id-credentials-access-keys-update.html)). On AWS: `aws iam update-access-key --access-key-id <id> --user-name <user> --status Inactive`, and `aws iam get-access-key-last-used --access-key-id <id>` shows last use.
- Revoke in the provider console for every other secret type. Look up the current revoke steps in that provider's documentation; they change.
- Rotate everything that shared the secret: a leaked `.env` file means every value in it, not only the one you noticed.
- A leaked password or token that unlocks a user account: also end all sessions and refresh tokens, and review MFA methods and OAuth grants.
- Don't wait for a convenient moment. If production breaks on revocation, fix forward with the new secret.

### Step 4: blast radius

- Search the provider audit log (CloudTrail on AWS, audit logs in GitHub and Google Cloud, equivalents elsewhere) for the key ID inside the exposure window. Look for first-seen source IPs, regions you never use, and calls that list or create resources, users, keys, or compute.
- No log source or no retention for the window: say "unknown", not "no misuse". Treat the secret's full permission set as the worst case.
- Anything created with the secret (extra keys, users, servers, forwarding rules) is part of the incident: list it, remove it, then rotate again if the secret could mint new credentials.
- Confirmed misuse, personal data reachable by the secret, or customer data: escalate as a security incident. Breach-notification clocks belong to the compliance owner.

### Step 5: git history

- Use `git filter-repo`, which the git project recommends over `git filter-branch` ([git-filter-repo](https://github.com/newren/git-filter-repo)). It refuses to run outside a fresh clone unless forced. For a GitHub repository, GitHub's removal guide asks for git-filter-repo 2.47 or later and its `--sensitive-data-removal` option; read GitHub's page for the exact command and what to send to Support. Read the tool's manual for the path-removal and text-replacement options; don't invent flags.
- After rewriting, force-push all branches and tags, then have every collaborator re-clone. A pull from an old clone can push the secret back.
- GitHub keeps some copies after a rewrite ([GitHub docs, removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)):

| Copy | Action |
|---|---|
| Forks | Ask each fork owner to remove it or delete the fork; GitHub does not share their contact details |
| Cached views reachable by commit hash | GitHub Support can remove them |
| Pull requests referencing the commits | Support can delete or dereference them; text quoted in PR bodies or comments stays until edited |

- GitHub Support generally helps only after other references are cleaned and when rotating the credential cannot contain the risk. Revocation is the real fix.
- Private repositories: rewrite only if the secret grants access beyond the repository's audience. Otherwise rotate, record, and move on.

### Step 6: prevention

- GitHub push protection blocks a push that contains a detected secret. For users it is on by default for public repositories; for repositories it needs GitHub Secret Protection and is off by default, set by an admin ([GitHub docs, push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)). Bypasses by someone with write access create an alert and an audit log entry.
- Providers in GitHub's secret scanning partner program are told when their token pattern appears in a public repository ([supported patterns](https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns)). Don't rely on it: a notified provider may act late or not at all.
- Add a local scanner as a pre-commit hook and a CI job (gitleaks, trufflehog), plus `.env` and key files in `.gitignore`.
- Replace long-lived keys with short-lived credentials (cloud roles, OIDC from CI) so a leak expires on its own. AWS itself advises roles over long-term access keys.

## Examples

Bad: "Removed the .env file in a new commit and force-pushed. Done." The secret still works and still sits in old commits, forks and clones.

Good: "Deactivated the key at 14:05 UTC. New key deployed 14:12. Exposure window 09:40 to 14:05. CloudTrail shows one call from an unknown IP at 11:02 (`ListBuckets`), no data reads. Rewrote history with git filter-repo, force-pushed, asked two fork owners to delete. Push protection now enabled on the org."

## Checklist

- [ ] The old secret fails a test call (revocation confirmed, not assumed)
- [ ] Replacement deployed and the service verified on it
- [ ] Every secret that shared the file or store was rotated
- [ ] Exposure window written as two UTC timestamps
- [ ] Audit log searched for the window, or "unknown" stated with the reason
- [ ] Resources created with the secret listed and removed
- [ ] History rewritten, all refs force-pushed, collaborators told to re-clone
- [ ] Forks, cached views and pull requests handled or listed as open
- [ ] Prevention added and tested with a dummy secret
- [ ] Incident entry written; escalation made if misuse or personal data is involved

## Composition / References

- [AWS IAM: update access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id-credentials-access-keys-update.html) (read 2026-11-15)
- [GitHub: removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [GitHub: about push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- [GitHub: supported secret scanning patterns](https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns)
- [git-filter-repo](https://github.com/newren/git-filter-repo)
- [GitHub: removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

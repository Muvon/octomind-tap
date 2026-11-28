---
name: devops-cloud-engineering
title: "Cloud IAM & Cost: AWS, Azure, Google Cloud"
description: "Write least-privilege IAM policies, debug cloud networks, cut spend and triage audit logs on AWS, Azure and Google Cloud, starting read-only."
license: Apache-2.0
compatibility: "Needs the provider CLI (aws, az or gcloud) with a configured profile; works read-only first and never needs write permissions to analyze."
rules:
  - match((?i)\b(aws|azure|gcp|google\s+cloud)\b.{0,60}\b(iam|polic(y|ies)|roles?|permissions?|bill|costs?|spend|vpc|security\s+groups?|cloudtrail|audit)\b)
  - match((?i)\b(least[\s-]privilege|iam\s+(polic(y|ies)|roles?|permissions?|review))\b)
  - match((?i)\b(cloudtrail|activity\s+log|cloud\s+audit\s+logs?|access\s*denied|not\s+authorized\s+to\s+perform)\b)
  - match((?i)\b(cloud|aws|azure|gcp)\s+(bill|costs?|spend)\b)
  - semantic(why is my cloud bill so high, 0.72)
  - semantic(write a least privilege IAM policy for this service, 0.72)
  - semantic(debug why these cloud instances cannot reach each other, 0.72)
  - semantic(find what is driving the cost in our AWS account, 0.72)
  - semantic(go through the cloud audit logs for suspicious activity, 0.72)
---

## Overview

Use this skill for cloud work on AWS, Azure and Google Cloud: IAM policies and role bindings, network debugging, cost reduction, audit-log triage and architecture review. Work from evidence taken with the provider CLIs and separate what you read from what you assume. Be cautious with credentials, precise with policy syntax, and plain about cost.

## Mental model

Every cloud question has a provider, an account, and a time window. Confirm the first two before anything else and bound the third. Start read-only: observation costs nothing and changes nothing, while a change needs an exact command, its effect, its risk and its rollback.

## Rules

### Method

1. Identify the target: provider, account or subscription or project, region, and which CLI profile is active (`aws sts get-caller-identity`, `az account show`, `gcloud config list`). Confirm it is the intended one before anything else.
2. Observe read-only: `describe`, `list`, `get` and `show` calls only. Save raw output to a file when it is long and work from the file.
3. Analyze against the rules below and state each finding with its evidence: the resource ID, the log event, the number.
4. Deliver the artifact (policy, cost report or architecture review) as a file or fenced block.
5. Changes: list each command with its effect, risk and rollback, then wait for approval of that exact command. Run one at a time and re-check the result.

### Safety

- Read-only first. Any verb that creates, updates, deletes, attaches, detaches, puts or sets (including `put-role-policy`, `add-iam-policy-binding`, `set-iam-policy`, `az role assignment create`, `delete-*`, `terminate-*`) is a change and needs approval of that exact command.
- Prefer a dry run or a simulator when one exists (`--dry-run` on EC2 calls, the IAM policy simulator) and say when none exists.
- Don't print or store secrets, keys or tokens. Redact access keys and account IDs when you paste output into a deliverable unless the user needs them.
- Cost and log queries can bill or be slow: bound the date range and state it.

### IAM least privilege

- Start from the job: list the exact API actions the workload calls, then grant those on named resources. A wildcard action or resource needs a written reason.
- AWS: build from access evidence. IAM Access Analyzer can generate a policy from CloudTrail for up to 90 days. A trail must exist, and it does not capture `iam:PassRole` or give action-level detail for every data event, so add those by hand. `generate-service-last-accessed-details` shows unused services per role.
- AWS review checks: `Principal: "*"` without a condition, `NotAction`, `iam:*` or `sts:AssumeRole` on `*`, `iam:PassRole` on `*`, long-lived access keys on humans, and trust policies without an external ID or source condition for cross-account roles.
- Azure: assign built-in roles at the narrowest scope (resource, then resource group, then subscription). A custom role needs the actions list and `NotActions` checked. Check `az role assignment list --all` for Owner and User Access Administrator.
- Google Cloud: bind predefined or custom roles to groups or service accounts at the lowest resource level. Flag primitive roles (Owner, Editor, Viewer) and user-managed service-account keys. Use the IAM recommender and the Policy Troubleshooter for denials.
- Prefer short-lived credentials (roles, workload identity, federation from CI) over keys.

### Network debugging order

Name resolution, then route, then filter, then the service. Check in this order: DNS answer, route table or effective routes, security group or firewall rule and network ACL (both directions, and the return path), then the target's listener and health. State which layer fails before proposing a change.

### Cost reduction

- Get the bill by service, then by usage type, then by resource tag. Fix the biggest line first. List tag coverage, because untagged spend cannot be assigned.
- Look for idle or unattached volumes and addresses, oversized instances (utilization from monitoring over at least two weeks), old snapshots, non-production running at night, data transfer across zones or regions, and storage in the wrong tier.
- Commitment discounts (savings plans, reservations, committed use) only after rightsizing, and only for the steady baseline. State the break-even and never promise a saving without a measured baseline.
- Prices and discount terms change. Read the current pricing page or the provider's cost tool before quoting a number, and don't quote a price, limit or retention figure from memory.

### Audit-log triage

- Retention differs. CloudTrail event history keeps 90 days of management events only. The Azure activity log keeps 90 days, records changes but usually not reads, and does not record requests rejected before they started. Google Cloud Data Access audit logs are off by default except for BigQuery (as of 2026-11). Check what is enabled before concluding an event did not happen.
- Triage in order: who (principal, session, access key), what (event name, resource), when (UTC, first and last), from where (source IP, user agent), result (error codes such as AccessDenied). Build one timeline. Mark every gap in logging as a gap, not as absence.

### Architecture review

Check account, subscription or project separation by environment and by blast radius; central logging and an audit trail that members cannot disable; identity federation; network segmentation; backup and a tested restore; the failure domain of each component (zone, region); managed service versus self-run, with the operating burden stated.

### Common requests

| Request | Response |
|---|---|
| Provider or account unclear | Ask one question, then run the identity check. |
| "Make it least privilege" | Gather access evidence first, then draft; don't guess actions. |
| "Why is my bill high" | Run the cost breakdown, report, propose; change nothing. |
| "Fix it" | Propose the exact commands and wait for approval. |

### Guards

- Don't run a state-changing command without approval of that exact command.
- Don't write a wildcard action or resource without a stated reason.
- State what you could not see (missing logs, missing permissions) instead of filling the gap with a guess.

### Scope limits

Writing infrastructure-as-code modules, container images and cluster workloads, live incident command, security forensics beyond triage, and cloud pen-testing are covered elsewhere.

## Output format

- IAM policy: the JSON or role definition in a fenced block, then a table of action, resource, reason, and the evidence it is needed. Unverified actions are marked.
- Cost report: baseline period and total, top five lines with amounts, each recommendation with estimated monthly saving, how it was measured, effort and risk, then a ranked list.
- Architecture review: findings table with severity (high, medium, low), evidence, recommended change, and an explicit list of what was not checked.
- Audit triage: timeline table (UTC time, principal, action, resource, source) and a short conclusion with confidence.

## Checklist

- [ ] Provider, account and region were confirmed with an identity check.
- [ ] All observation was read-only and every finding cites evidence.
- [ ] Wildcards in policies carry a written reason.
- [ ] Date ranges are bounded and stated.
- [ ] Gaps in logs or permissions are listed as gaps.
- [ ] Every proposed change lists effect, risk and rollback and awaits approval.

## Composition / References

- `infrastructure-change` covers the shared plan-and-verify procedure for infrastructure definitions.
- `devops-terraform-iac` covers writing the policy as Terraform.

---
name: devops-incident-response
title: "Incident Response: Triage, Mitigation & Postmortems"
description: "Run an incident from severity triage through mitigation-first response to a blameless postmortem, using error tracking, kubectl, docker and git history."
license: Apache-2.0
compatibility: "Uses an error-tracking service, kubectl, docker and git history when available; otherwise names the missing signal."
domains: devops
capabilities: versioning error-tracking docker kubernetes
rules:
  - match((?i)\b(post[\s-]?mortems?|blameless|sev[\s-]?[1-4]|(classify|assign|declare)\w*\s+(a\s+)?severity|blast\s+radius|incident\s+(response|command|commander|timeline|review|report|assessment)|active\s+incident|live\s+incident|resolved\s+incident|on[\s-]?call)\b)
  - match((?i)\b(production|prod)\s+(is\s+)?(down|broken|outage|erroring|failing)\b|\boutage\b.{0,30}\b(users?|customers?|production|prod)\b)
  - match((?i)\b(errors?|5xx|500s|502s?|latency|p99)\b.{0,40}\b(spik\w+|surg\w+|jump\w+|regress\w+|elevated|throwing|rose|went\s+from)\b|\b(spike|surge)\s+in\s+(errors?|5xx|500s|latency))
  - match((?i)\b(alert|alerts|pager|pagerduty|sentry)\b.{0,60}\b(fired|firing|paged|triage|what\s+do\s+i\s+do|lit\s+up|shows)\b)
  - match((?i)\b(crash[\s-]?loop\w*|crashloopbackoff|flapping|restarts?\s+every)\b)
  - match((?i)\b(rollback|roll\s+back)\b.{0,60}\b(safer|feature\s+flag)\b|\bmitigation[\s-]first\b|\bresolved\b.{0,30}\b(incident|outage)\b)
  - match((?i)\b(correlate|correlation)\b.{0,60}\b(commits?|deploys?|releases?|git\s+log)\b|\b(git\s+log|recent[\s-]change)\b.{0,60}\b(window|regression|incident)\b)
  - semantic(production is down and users are affected, help me respond, 0.72)
  - semantic(we have an outage, help me triage severity and mitigate, 0.72)
  - semantic(write a blameless postmortem for last night's incident, 0.72)
  - semantic(the service is returning errors in production what do I check first, 0.72)
---

## Overview

Use this skill to take an alert, error spike or reported symptom through the incident lifecycle: assess severity and blast radius, mitigate first, diagnose with real signals (error tracking, kubectl, docker, logs), and close the loop with a blameless postmortem. It follows Google SRE practice. Stay calm, methodical and evidence-only.

## Mental model

Mitigation before root cause, always. The system back to serving users outranks understanding why it broke. Every claim carries its evidence, and one operator makes changes one at a time.

## Rules

### Method

1. Assess: what is broken, for whom, since when. Pull error-tracking events and check `kubectl get pods` and events and service state read-only. Declare severity: SEV1 (user-facing outage or data loss), SEV2 (major degradation, no workaround), SEV3 (partial, workaround exists), SEV4 (minor or cosmetic). Google's incident test: recommend declaring a formal incident on any yes to these: does fixing need a second team, is the outage customer-visible, is it unsolved after an hour of focused analysis?
2. Stabilize the picture: keep a live incident record from the first minute (current state, impact, timestamped actions, next steps). It is the coordination surface now and the postmortem's raw material later. Build the timeline: first occurrence, deploys and config changes in the window (`git log`, release history), correlated alerts. State the leading hypothesis and confidence.
3. Mitigate first: propose the fastest safe path to stop user pain (rollback beats debugging in prod). Present the commands, the expected effect and the risk. Execute state-changing commands only after approval.
4. Verify mitigation: re-check error rates, pod health and the original symptom, and state plainly whether impact stopped. Track every temporary divergence (flags flipped, traffic pinned, capacity added) explicitly so it gets reverted after resolution.
5. Diagnose: with users no longer affected, find the root cause chain: change, mechanism, symptom, each link backed by a signal.
6. Close: draft the blameless postmortem and concrete prevention actions. Store durable facts (recurring failure modes, fragile components, environment quirks) in memory.

### Principles

- Severity is impact-based, never effort-based. When between two levels, take the higher until evidence lowers it.
- Measure impact against the service's SLOs where they exist: error-budget burn rate says how urgent it is. Page on fast burn with multiwindow, multi-burn-rate alerts (for example 14.4x over 1 h confirmed by 5 min spends 2% of a 30-day budget) and ticket on slow burn. An exhausted budget triggers the team's error budget policy. When alerts fire on causes rather than user-visible symptoms, note it as a postmortem action. For SLI and SLO definition, burn-rate alerts and cardinality limits, use the `observability-setup` skill.
- Read-only first: `get`, `describe`, `logs` and `events` run freely. Anything mutating (`rollout undo`, `scale`, `delete`, `restart`, `exec`) is proposed, approved, then run, one command at a time during an incident.
- Every claim in the timeline carries its evidence: the error-tracking event, the log line, the deploy SHA. "Probably" appears only in the hypothesis section.
- Most incidents follow a recent change. Check deploys, config, dependencies and traffic shifts in the window before exotic theories.
- One change at a time during mitigation, through one operational owner. Uncoordinated parallel changes are the classic incident-response failure (Google's SRE practice: a single operations role is the only party modifying the system).
- Preserve evidence before destroying state: capture logs, metrics snapshots and pod state before any restart or delete.
- Postmortems are blameless: name systems, gaps and mechanisms, never people. Assume everyone acted in good faith on the information they had. Action items are specific, owned and dated, split into mitigative (closes this gap) and preventive (kills the class). Include What went well, What went wrong, and Where we got lucky.
- If the incident outgrows the session (multi-team, communications needed), say so and recommend declaring formal incident command rather than absorbing it silently.

### Common requests

| Request | Response |
|---|---|
| Alert or error pasted | Assess and return the status block with severity. |
| "Fix it" | Still propose the mitigation with risk before executing; approval per state-changing command. |
| Mitigation confirmed | Verify with signals, then continue to root cause. |
| "Write it up" | Postmortem from the session's evidence trail. |
| Symptom without access to signals | Say exactly which signal is missing and what to run to get it. |

### Guards

- Don't run a mutating command without explicit approval of that command.
- Don't present a root cause you cannot trace change, mechanism, symptom with evidence.
- Don't debug in production while users are affected; mitigate first.
- State confidence honestly. A wrong confident diagnosis costs more than "unconfirmed".

### Scope limits

Application feature development, non-incident refactoring, infrastructure provisioning and IaC design are not covered here.

## Examples

Weak: "The deploy probably broke checkout, I'll look at the code."

Strong: "SEV2. Checkout error rate 18% since 14:02 UTC (Sentry issue linked), 4 minutes after deploy a1b2c3d. Hypothesis, medium confidence: the new payment client times out. Proposed mitigation: `kubectl rollout undo deployment/checkout -n prod`. Effect: returns to the previous release. Risk: loses the new feature flag state. Approve?"

## Output format

- During an incident, a status block: Severity / Impact / Timeline so far / Leading hypothesis (confidence) / Proposed next action with risk.
- Postmortem: Summary, Impact (numbers), Timeline (timestamped), Root cause chain, What went well and poorly, Action items (owner and verification).
- Runbooks: symptom, checks, mitigation, in fenced command blocks.

## Checklist

- [ ] Severity is declared and the reason is impact.
- [ ] Mitigation was proposed before root-cause work started.
- [ ] Every mutating command had approval, one at a time.
- [ ] Evidence was captured before any restart or delete.
- [ ] Temporary divergences are listed for reversal.
- [ ] The postmortem names systems, not people, and every action item has an owner and a date.

## Composition / References

- `observability-setup` covers SLOs, burn-rate alerts and dashboards after an incident.
- `devops-kubernetes-operations` covers cluster debugging in depth.
- Google SRE Book and Workbook: incident management and postmortem culture.

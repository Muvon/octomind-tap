---
name: security-operations-triage
title: "Security Operations: Alert and Phishing Triage"
description: "Triages alerts, logs, and phishing emails, ranks scanner findings by exploitability, and investigates incidents with evidence-cited timelines and writeups."
license: Apache-2.0
compatibility: "Requires: a shell for local artifact analysis and web access for IOC, CVE, and advisory lookups."
capabilities: shell
rules:
  - match((?i)\b(email headers?|spf|dkim|dmarc|return-path|iocs?|indicators of compromise)\b)
  - match((?i)\b(phish\w*|credential[- ]harvest\w*)\b.{0,80}\b(headers?|employees?|company|company's|mailbox|staff|accounting)\b|\b(employees?|company|mailbox|staff|headers?)\b.{0,80}\bphish\w*)
  - match((?i)\b(incident (timeline|report|writeup)|timeline\b.{0,40}\b(logs?|incident|compromise\w*|logins?)|root cause|containment)\b)
  - match((?i)\b(logs?|siem|edr|zeek|auth\.log|sign-in)\b.{0,100}\b(compromise\w*|intrusion|suspicious|impossible travel|malicious|incident)\b|\b(compromise\w*|intrusion|suspicious|impossible travel)\b.{0,100}\b(logs?|siem|edr)\b)
  - match((?i)\b(someone got into|unknown (cron job|user account|process)|new user account|compromised (admin )?(token|account|server|host)|we (think|believe|were|got|have been|may have been) (we('re| are| were)? )?(breached|hacked|compromised|attacked)|ransomware|business email compromise)\b)
  - match((?i)\b(nessus|qualys|openvas|cves?|cvss|kev|epss|ssvc)\b|\b(rank|prioriti[sz]e)\b.{0,40}\b(findings|vulnerabilit\w+|patch)\b)
  - match((?i)\b(sigma rules?|mitre att&ck|att&ck|detection rules?)\b)
  - semantic(triage these security alerts and tell me which ones matter, 0.74)
  - semantic(is this email a phishing attempt, analyze the headers, 0.74)
  - semantic(investigate this suspicious activity in our logs and write the incident timeline)
---

## Overview

This skill performs security operations analysis, the defensive kind: it triages alerts and logs, analyzes suspicious emails and artifacts, prioritizes vulnerability-scanner output by real exploitability, investigates incidents methodically, and writes findings that stand up in a postmortem. Think in evidence chains: every verdict (malicious, benign, or undetermined) cites the specific indicators that produced it, and "undetermined" is an honest, common answer. Work for the defender, on systems the user is authorized to protect.

## Rules

### What this skill covers

Alert and log triage, phishing and email analysis, IOC extraction and lookups, vulnerability-report prioritization, security-incident investigation and timeline reconstruction, detection-rule drafting (Sigma, ATT&CK-mapped), containment and eradication guidance, hardening checklists (SSH, cloud storage, IAM basics, exposed services), and incident writeups.

Not covered: application-security code review and OWASP remediation, compliance frameworks and breach-notification law (handle the technical incident; the 72-hour clock is a compliance question), reliability incidents without a security dimension, LLM prompt-injection defense, consumer and personal scams, fraud, and identity theft, and offensive work. Exploitation, payload writing, and attack tooling are out, full stop.

### Steps

1. Establish the authorization context: whose system, and what the user's role is. Analysis of artifacts they have received (a phish, logs from their infrastructure) proceeds directly; anything targeting third-party systems doesn't.
2. Collect before concluding: get the raw artifacts, meaning full headers (not screenshots of them), the log window around the event (not the one scary line), and the scanner's actual output. Triage on summaries is how both false positives and real intrusions survive.
3. Triage: classify against the patterns below, with verdict, confidence, and the indicators behind it. Prioritize by blast radius: internet-facing, exploited in the wild, and touching crown jewels first.
4. Investigate: build the timeline from evidence: initial vector, foothold, movement, objective. Claim each hop only when an artifact shows it; label gaps as gaps. Use the shell for local artifact analysis (grep or awk over logs, hash computation, decoding) and web search and fetch for IOC reputation, CVE details, and vendor advisories.
5. Contain with care: order containment recommendations by reversibility, with the evidence-preservation step before the cleanup step (wiping the box also wipes the answer to "how did they get in"). Destructive or business-interrupting actions are recommendations for the user to execute, with tradeoffs stated.
6. Write it up: the incident report (output format below), and lessons turned into hardening actions with owners. Save the environment (stack, prior incidents, accepted risks) to memory for continuity.

### Phishing triage: the four checks in order

1. Sender authenticity: return-path versus display name, SPF/DKIM/DMARC results in headers, lookalike domains (homoglyphs, extra hyphens, wrong TLD).
2. Link and attachment reality: hover targets versus text, redirectors, QR codes, and file types that execute or render (.html and .svg attachments, macro docs, .iso and .lnk).
3. Pressure pattern: urgency plus authority plus an unusual channel plus a payment or credential ask is the social core.
4. Context: does the claimed business event exist?

Give a verdict with indicators. Current lures that defeat checklists: adversary-in-the-middle kits that relay a real login and steal the session cookie (MFA does not stop them), device-code phishing ("enter this code at microsoft.com/devicelogin"), ClickFix and fake-CAPTCHA pages that make the user paste a command into Run or a terminal, and callback phishing that moves to a phone call.

If credentials or a code were entered: revoke all sessions and refresh tokens (a password reset alone leaves a stolen session alive), rotate the password, and review MFA methods, OAuth consents, and inbox rules, immediately, before further analysis. Phishing-resistant MFA (passkeys, FIDO2) is the durable fix.

### Log triage heuristics

Anchor on time (what else happened within 5 minutes across systems), rarity (first-seen binaries, service accounts doing interactive logins, geo-impossible travel), and volume shifts (authentication failures spiking and then one success; outbound data 10 times baseline). A single scary line without corroboration means collect more; a corroborated chain is an incident. Preserve originals read-only; work on copies.

### Vulnerability prioritization: CVSS is the start, not the answer

Priority = severity x exposure x exploit status x asset value. A 9.8 on an internal box behind a VPN with no published exploit ranks below a 7.5 on the internet-facing login service listed in CISA KEV. Check KEV (known exploited) and EPSS (FIRST's 30-day exploitation probability) via web search before ranking. SSVC is a good decision tree when a defensible act, attend, or track call is needed. Edge devices (VPNs, firewalls, file-transfer appliances) are among the most-exploited targets: treat their KEV entries as same-week work. Patching order: internet-facing exploited, then internet-facing critical, then crown-jewel-adjacent, then the rest on cadence. "Accept" is a valid verdict when cost exceeds risk, written down with an owner and a review date.

### Incident severity and escalation

- SEV1: active compromise of production or data. Containment now, notify leadership now, and check the compliance clock (the legal side is a separate compliance question).
- SEV2: confirmed malicious activity, contained or limited.
- SEV3: suspicious, under investigation.

Declare severity early and revise openly. Quiet severity inflation and quiet minimization are both lies with different politics.

### Detection engineering

Map findings and proposed detections to MITRE ATT&CK (v20, released 2026-10-13; read the current version on attack.mitre.org before mapping; v19 split Defense Evasion into Stealth and Defense Impairment, and v20 added the first Enterprise techniques for prompt injection and AI-enabled exfiltration, so update older mappings) and use ATT&CK's Detection Strategies and Analytics as a starting point. Write portable detections as Sigma rules and convert them to the user's SIEM query language. Each rule names its log source, the false positives it expects, and a test event that should fire it. A detection nobody has tested is a hope, not a control.

### Incident writeups

Facts and timestamps, not adjectives: timeline (UTC, evidence-cited per entry, ATT&CK technique IDs where they help), impact (what was accessed or changed, stated only as far as evidence shows: "no evidence of exfiltration" is not "no exfiltration", so say which one you have), root cause, actions taken, and hardening follow-ups with owners. Blameless: processes fail people before people fail processes.

### Hardening quick wins (recommend proactively when you see the gap)

Phishing-resistant MFA on everything external (admins first); SSH keys, no password auth, no root login; cloud storage buckets private by default with public access audited; IAM least privilege with a quarterly access review; a patching cadence with an SLA for KEV entries; centralized logs with retention of at least 90 days; offline-tested backups; egress monitoring on crown jewels.

## Examples

- "Is this email, link, or file suspicious?": the four checks on the real artifact (ask for full headers or the URL if given a screenshot), then a verdict with indicators.
- "Something weird in the logs": collect the window, corroborate across sources, then a verdict or a specific list of what else to pull.
- "Scanner says 400 criticals": the prioritization math, the top 10 with reasoning, and the accept or defer candidates named.
- "We think we're breached": severity call, evidence preservation first, containment ordered by reversibility, compliance handoff flagged. Calm and fast.
- "I committed a key" or "a token leaked": the `secret-leak-response` skill: revoke first, then exposure window and audit-log search, then history cleanup.
- Ambiguous: ask one question (usually "what artifact do you actually have?"), then proceed.

## Output format

- Triage verdicts: artifact, verdict (malicious, benign, undetermined), confidence, indicators (each traceable to the evidence), recommended action.
- Investigations: `incident-<id>.md` with the writeup structure above.
- Vulnerability reviews: a ranked table with columns CVE, asset, exposure, exploit status (sourced), action, deadline.
- Shell analysis is shown with the commands used, so it is reproducible.

## Checklist

- [ ] Defensive work only: no exploits, payloads, phishing lures, or attack tooling, and nothing analyzed or probed on a system the user isn't authorized on.
- [ ] Preservation came before eradication; originals were kept read-only.
- [ ] "No evidence of X" was not presented as "X didn't happen".
- [ ] Destructive or business-interrupting containment was recommended, not executed.
- [ ] Exploited-in-the-wild status was checked before ranking vulnerabilities.
- [ ] Breach-notification law was flagged for compliance review the moment personal data was plausibly involved.

## Composition / References

- `secret-leak-response` skill: leaked keys, tokens, and passwords.
- `threat-modeling` skill: design-level threat analysis.

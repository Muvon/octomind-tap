---
name: browser-backlink-submission
title: "Browser Backlink Submission Execution"
description: "Operational playbook for EXECUTING backlink submissions via a headless browser — driving directory/listing/Web2.0 forms with Playwright, mapping a single site profile to per-target fields, handling signup + email verification + captchas, throttling to avoid spam flags, and producing an auditable submission log. Activate ONLY when the user has a qualified prospect list and wants the browser to actually submit. Prospect discovery and qualification belong to marketing-backlink-prospecting; copy/anchor writing belongs to content skills via tap."
license: Apache-2.0
compatibility: "Requires browser:general agent with browser (Playwright) capability and filesystem-write. Assumes a prospect list already qualified for safety and topical fit."
domains: browser
rules:
  - session(browser) content(backlink)
  - session(browser) content(backlinks)
  - session(browser) content(directory)
  - session(browser) content(directories)
  - match(\bsubmit\s+(our\s+|the\s+)?(site|product|startup|tool|app|business|company)\s+to\b)
  - match(\bdirectory\s+submission\b)
  - match(\bsubmit\s+to\s+(\d+\s+)?directories\b)
  - match(\b(backlink|listing)\s+submission\b)
  - match(\bfill\s+(out\s+)?(the\s+)?directory\s+(form|listing)\b)
  - match(\bsubmit\s+(my|our)\s+(saas|startup|product|tool)\s+to\b)
  - semantic(submit our site to a list of directories using the browser)
  - semantic(automate filling directory submission forms for backlinks)
  - semantic(execute a backlink submission run from this prospect list)
metadata:
  tags: "browser playwright backlinks seo directories submission"
---

## Overview

Given a qualified prospect list and a single source-of-truth site profile, drive each target's submission form to completion, capture evidence, and emit an auditable log. This skill is execution-only — it assumes prospects are already vetted (use `marketing-backlink-prospecting` first) and assumes anchor / description copy is either pre-supplied or fetched from a content specialist via `tap`.

Outcome: a `submission-log.json` with one row per attempt (status, evidence, live URL once verified) plus screenshots under `./out/backlinks/`. No fabricated successes, no fire-and-forget, no link-farm targets ever.

## Mental model

A submission run is a pipeline: profile → per-target field mapping → form drive → evidence capture → verification follow-up. Most failures are not bugs — they are signals: captcha walls, login-required, paid-only, dead form, off-topic category. The skill's job is to detect, classify, and log these honestly so the user gets a reliable picture of what shipped.

Three immovable invariants:
1. Never submit to a target the prospect list did not qualify. If a target looks shady mid-run (hidden links, casino/pharma neighbours, "1000 directories for $5" footer), skip and log `skipped:quality`.
2. One identity per run. Reuse the same email, brand name, contact, anchor pool — directories that detect inconsistency flag listings. The profile is the source of truth.
3. Evidence or it didn't happen. Every `submitted` row needs a post-submit screenshot and either a confirmation URL or a confirmation-email subject line.

## Rules

### The site profile (input contract)

The user (or an upstream step) supplies one JSON file. If any required field is missing, stop and ask — do not invent values.

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Brand / site / product name as it should appear |
| `url` | yes | Canonical URL, no UTM, https |
| `tagline` | yes | ≤ 80 chars |
| `description_short` | yes | ≤ 160 chars |
| `description_long` | yes | 300–600 chars, neutral tone |
| `description_alt` | recommended | A second long variant — rotate to avoid duplicate-content footprint |
| `category_primary` | yes | Map to each directory's taxonomy |
| `category_alt` | recommended | Fallback when primary doesn't exist on a target |
| `tags` | yes | 5–10 keywords, lowercase |
| `logo_path` | yes if any target requires image | Local file; PNG ≥ 256 px square preferred |
| `screenshot_path` | recommended | For directories asking for a product preview |
| `contact_email` | yes | Real, monitored — verification mail lands here |
| `contact_name` | yes | Real human; some directories reject "Admin" |
| `pricing` | recommended | "free" / "freemium" / "paid" — startup directories ask |
| `founded_year`, `location`, `team_size` | recommended | Business directories ask |
| `social.twitter`, `social.linkedin`, `social.github` | recommended | Many forms require ≥ 1 social URL |
| `anchors` | yes | Array of 3–6 anchor texts: brand, brand+keyword, naked URL, generic ("learn more"). Rotate; never reuse same anchor more than 30% of the run. |

### Target classification (per prospect, before driving the form)

| Target type | Treat as | Notes |
|---|---|---|
| Free general directory (BOTW free tier, niche aggregators) | submit | Verify it's still live and indexed |
| Business directory (GMB, Yelp, BBB, Apple Maps) | submit, ownership-verify | Often needs phone/postcard verification — log as `pending:ownership-verify` |
| Startup / SaaS directory (BetaList, F6S, AlternativeTo, SaaSHub, Tools Directory style) | submit | Usually needs account + email verify |
| Web2.0 property (Medium, Tumblr, WordPress.com, Notion public, Bear) | publish, not submit | Different flow — author a short on-topic post linking once, naturally |
| Niche industry list (curated GitHub awesome lists, vertical aggregators) | PR / issue, not form | Reroute: open issue / PR — out of this skill's scope, log `skipped:not-a-form` |
| Q&A / forum (Quora, Reddit, Stack Exchange) | NOT this skill | Persona / on-topic answers are out of scope — log `skipped:not-a-form` |
| Paid-only ($/listing) | skip unless user pre-approved budget | Log `skipped:paid` with the price |
| Link farm / "submit to 500 directories" / spammy ad-laden / hidden links / unrelated niche | skip, hard | Log `skipped:quality` with the reason |
| Captcha-walled (hCaptcha, reCAPTCHA v2, Cloudflare Turnstile) | stop and escalate | Do not attempt to bypass. Log `skipped:captcha`; the user solves manually if they want |
| Login-required and we have no account | escalate | Either user supplies creds, or log `skipped:auth` |

### Field-mapping rules

- `name` → "Site Name", "Title", "Project", "Tool name", "Company". Match what the form asks; never invent prefixes/suffixes.
- `url` → "URL", "Website", "Homepage". Always canonical https; never with tracking params.
- `description_short` → "Tagline", "Short description", "Pitch", fields with ≤ 160 char limit.
- `description_long` / `description_alt` → "Description", "About", "Details" (300+ chars). Rotate variants across the run; don't paste the identical paragraph 50 times.
- `category` → match to directory taxonomy by exact label first, then nearest synonym. If nothing fits, pick the closest and log `category_mapping`.
- `tags` → split into the form's expected separator (comma, space, enter-per-tag). Trim to the form's max count.
- `anchors` → only used when the target lets you choose anchor text on the link. Rotate per-target from `anchors[]`; track usage to keep brand-anchor share ≥ 50%.
- `logo` / `screenshot` → upload via `setInputFiles` on the file input; verify the upload preview appears before submit.

### Drive protocol (per target)

1. Pre-flight — open URL, confirm it's the submission form (not 404, not paywall, not "submissions closed"). If wrong, log and move on.
2. Account check — if the form requires an account: look up cached creds for that domain in this session's profile vault; if absent, ask user once, then proceed. Never store creds to disk.
3. Captcha check — if a captcha is on the submit page, stop. Do not iterate.
4. Field walk — accessibility-tree first; fill in the order the form lays them out; verify each value sticks (re-read the input).
5. Category mapping — if a select / radio is required, pick by label match; if no match, pick the nearest sibling and record the mapping in the log row.
6. Upload check — for image fields, confirm the preview thumbnail rendered before submit.
7. Submit — click the actual submit button; wait for a success state: redirect, success message, confirmation page selector, or verification email.
8. Evidence — screenshot the post-submit state (full page) to `./out/backlinks/<domain>-<UTC>.png`; capture the confirmation URL or message text.
9. Verification — if the target sends a confirmation email, poll the user's mailbox via the supplied flow (out of scope of this skill — escalate if no flow available); record the verified URL when it goes live.
10. Log — append one row to `./out/backlinks/submission-log.json`.

### Throttling and identity hygiene

- Spread across time: never submit to more than 5 targets in a row from the same IP without a 60-second cool-off.
- Pace per day: cap free-directory submissions at 20 per day per identity; business directories at 5; web2.0 publishes at 2.
- Rotate anchor variants — track use counts in-memory; never let one anchor exceed 30% of the run.
- Rotate description variants — alternate `description_long` and `description_alt` per target.
- One profile, one email, one contact name across the entire run. Inconsistency is a flag.

### Submission log schema

`./out/backlinks/submission-log.json` is an array of rows. Append-only.

```
{
  "target_url": "https://example-directory.com/submit",
  "target_domain": "example-directory.com",
  "target_type": "saas-directory",
  "submitted_at": "2026-05-10T18:32:11Z",
  "status": "submitted | pending:email | pending:ownership-verify | live | rejected | skipped:captcha | skipped:paid | skipped:quality | skipped:auth | skipped:not-a-form | failed:selector | failed:timeout",
  "anchor_used": "the brand name",
  "description_variant": "long | alt",
  "category_mapping": { "requested": "Developer Tools", "selected": "Tools / Dev" },
  "live_url": null,
  "screenshot_path": "./out/backlinks/example-directory-com-20260510T183211Z.png",
  "confirmation_url": null,
  "confirmation_email_subject": null,
  "notes": "Selector for category was a custom dropdown; mapped Tools → Tools / Dev."
}
```

### Hand-offs (use `tap`)

- Need fresh, on-topic descriptions per niche → `tap(action="run", role="content:<...>", prompt="...")` or `content-humanize` skill output via the agent's main loop. Do NOT write copy here.
- Need to qualify fresh prospects mid-run → stop, escalate to `marketing-backlink-prospecting`. This skill does not vet new targets on the fly.
- Q&A / forum / community work → out of scope. Persona / on-topic answers are not this skill's job.

## Examples

### Example 1: Bad → Good (description handling)

❌ Bad:
```
For all 50 directories, paste description_long verbatim. Reuse "TheBrand" anchor every time.
```

✅ Good:
```
Alternate description_long and description_alt across submissions.
Rotate anchors from profile.anchors[]; track use, cap brand-anchor share at 50%, naked-URL at 20%, generic at 30%.
```

What changed: identical copy + identical anchor across many targets is the duplicate-footprint signal Google uses to discount or penalize.

### Example 2: Edge case — category not in taxonomy

The site is a `Developer Tools` SaaS but the directory only offers `Software / Other`, `Business / Productivity`, `Lifestyle`. Pick `Software / Other`, record `category_mapping: { requested: "Developer Tools", selected: "Software / Other" }`, do not pick `Business / Productivity` because it's slightly broader — closer is better than larger.

### Example 3: Edge case — captcha on submit

Form filled cleanly, "Submit" button reveals an hCaptcha challenge. Stop. Screenshot. Log `skipped:captcha`. Do not refresh and retry; do not attempt an OCR/solver. Move to the next target.

## Checklist

- [ ] Site profile JSON validated — all required fields present, anchors[] has ≥ 3 entries, logo file exists if any target needs it
- [ ] Prospect list classified — each target has a `target_type`; link-farm / unrelated targets pre-filtered out
- [ ] Output directory `./out/backlinks/` exists; previous `submission-log.json` either rotated or appended to deliberately
- [ ] Per submission: post-submit screenshot saved, log row appended, status reflects reality (no "submitted" without evidence)
- [ ] Anchor and description rotation is enforced — no anchor or description variant exceeds its share cap
- [ ] Throttling respected — pace caps and cool-offs honored
- [ ] Captcha / paid / login-required targets skipped, not faked
- [ ] No credentials persisted to disk after the run
- [ ] Final report summarizes: total attempted, submitted, pending verification, skipped (by reason), failed (by reason)

## Composition / References

- Pairs with `browser-form-filling-patterns` (selector resilience, file uploads, multi-step forms) — base layer.
- Run after `marketing-backlink-prospecting` has produced a vetted prospect list. This skill does not discover prospects.
- For copy generation (descriptions, anchor variants), call out to a content specialist via `tap`; do not author copy inside this skill.
- [Google Search Essentials — Link spam](https://developers.google.com/search/docs/essentials/spam-policies#link-spam)
- [Google: Qualifying outbound links to your site](https://developers.google.com/search/docs/essentials/spam-policies#user-generated-spam)

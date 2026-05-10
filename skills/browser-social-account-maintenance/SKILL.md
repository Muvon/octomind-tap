---
name: browser-social-account-maintenance
title: "Browser Social Account Maintenance Ops"
description: "Operational playbook for RECURRING social-account hygiene executed via a headless browser — profile/bio sync across networks, cross-posting a pre-written piece to N platforms, scheduled-post audits, follower/connection cleanup, notification triage, archive/delete of old posts, DM-inbox housekeeping. Activate ONLY when the user wants the browser to actually drive social account ops as maintenance work. Authoring new post copy is NOT this skill — text must be supplied as input or fetched from a content specialist via tap."
license: Apache-2.0
compatibility: "Requires browser:general agent with browser (Playwright) capability and filesystem-write. Assumes user has authenticated sessions or supplies credentials this session."
domains: browser
rules:
  - session(browser) content(profile)
  - session(browser) content(bio)
  - session(browser) content(crosspost)
  - session(browser) content(cross-post)
  - match(\b(sync|update)\s+(my\s+)?(bio|profile)\s+(across|on)\b)
  - match(\bcross[-\s]?post\s+(this|the\s+post|to\s+(twitter|x|linkedin|mastodon|bluesky|threads))\b)
  - match(\b(audit|clean(\s*up)?|review)\s+(my\s+)?(scheduled|drafts|old\s+(posts|tweets))\b)
  - match(\b(unfollow|cleanup|prune)\s+(inactive|spam|bot)\s+(followers|following|connections)\b)
  - match(\btriag\w+\s+(my\s+)?(notifications|mentions|inbox)\b)
  - match(\barchive\s+(old\s+)?(posts|tweets)\s+older\s+than\b)
  - semantic(sync my bio and links across all my social accounts)
  - semantic(cross-post this same piece to twitter linkedin and mastodon)
  - semantic(clean up my old social posts and inactive followers)
metadata:
  tags: "browser playwright social ops crossposting profile-sync"
---

## Overview

Drive recurring social-account operations across X, LinkedIn, Mastodon, Bluesky, Threads, Instagram, YouTube, TikTok, Reddit and similar — when the work is mechanical hygiene, not voice work. The skill covers six operations: profile sync, cross-post, scheduled-post audit, follower/connection cleanup, notification triage, archive/delete. Each follows the same shape: pull current state per platform, diff against the user's source-of-truth profile or task spec, drive the per-platform UI, capture evidence, log.

This skill explicitly does NOT write new posts. New copy is supplied as input or authored by content specialists called via `tap`. This skill takes already-written copy and ships it.

## Mental model

Treat each social network as a target with three things: (1) a profile surface (display name, bio, links, avatar, banner), (2) a publish surface (compose box / scheduler), (3) an admin surface (followers, notifications, archive). Every operation is the same loop: read current state → compare to spec → drive the UI to converge → screenshot → log. Per-platform quirks live in a small lookup table; the loop stays identical.

Three immovable invariants:
1. One source of truth per operation. Profile sync reads `profile.json`; cross-post reads `post.json`; cleanup reads `cleanup-rules.json`. Never invent values; never paraphrase the user's bio.
2. Confirm-before-destructive. Delete, unfollow, archive, mass-block — confirm the count and a sample with the user before executing, even if the rules file says "auto".
3. Per-platform compliance > convenience. Twitter/X 280-char limit, LinkedIn URL-penalty, Bluesky 300-char, Mastodon CW conventions — honor each. If a piece doesn't fit, log and skip that platform; do NOT silently truncate.

## Rules

### Per-network compose limits and quirks

| Network | Compose limit | Link handling | Image / video | Notes |
|---|---|---|---|---|
| X (Twitter) | 280 chars (free) / 25k (premium) | Counts as ~23 chars | 4 imgs / 1 video / 1 GIF | Threads: post 1, then reply with 2..N to own root |
| LinkedIn | 3000 chars; 210-char "see more" fold | Naked links suppress reach ~60% — put link in first comment | 9 imgs / 1 video | Personal profile vs page have different composers |
| Mastodon | 500 chars (instance default; varies) | No penalty | 4 imgs / 1 video | CW (content warning) is a culture norm, not optional for sensitive content |
| Bluesky | 300 chars | No penalty | 4 imgs / 1 video | Threads via reply-to-self |
| Threads | 500 chars | No penalty | 10 imgs / 1 video | Cross-post toggle to Instagram exists |
| Instagram | Caption 2200 chars; bio 150 chars | Only one clickable URL in bio | Feed / Reels / Stories all separate composers | Posting requires mobile-style flow even on web |
| YouTube (community / Shorts metadata) | Community 500 chars | URLs allowed | N/A for community | Use Studio composer, not the consumer site |
| Reddit | Title 300 / body 40k | Allowed; subreddit rules vary | 1 img/video per post | NEVER mass-post; subreddit-by-subreddit only |
| TikTok | Caption 2200 chars | Bio link only | Vertical video required | Captions accept hashtags, no naked URLs in caption-link form |
| Mastodon / Bluesky / Threads | — | — | — | Treat as the "open social" trio for low-risk cross-posting |

### Operation 1 — Profile sync

Input: `profile.json` source-of-truth.

```
{
  "display_name": "Jane Doe",
  "bio": "Building things. Writing things.",
  "bio_per_platform": { "x": "...", "linkedin": "..." },   // optional override
  "links": ["https://janedoe.com"],
  "location": "Berlin",
  "pronouns": "she/her",
  "avatar_path": "./assets/avatar.png",
  "banner_path": "./assets/banner.png",
  "platforms": ["x", "linkedin", "mastodon", "bluesky", "threads"]
}
```

For each listed platform:
1. Open settings / edit-profile route.
2. Read current values.
3. Diff against spec; build a change set.
4. If diff is empty → log `noop` and skip.
5. Apply changes one field at a time; verify each landed.
6. Save, screenshot the post-save profile page.
7. Log row: `{ platform, fields_changed, status, screenshot_path }`.

Per-platform bio cap: truncate ONLY if the user supplied `bio_per_platform.<platform>`; otherwise skip platforms where the bio doesn't fit and log `skipped:bio-too-long`.

### Operation 2 — Cross-post

Input: `post.json` — one piece, multiple targets.

```
{
  "platforms": ["x", "linkedin", "mastodon", "bluesky"],
  "variants": {
    "x": { "text": "...", "thread": ["...", "..."] },
    "linkedin": { "text": "...", "link_in_first_comment": "https://..." },
    "default": { "text": "...", "link": "https://..." }
  },
  "media": ["./assets/img1.png"],
  "schedule": "now" | "2026-05-10T18:00:00Z"
}
```

Per platform:
1. Pick variant (`variants[platform]` else `variants.default`).
2. Validate length against the table above. If too long and no platform variant is given → skip, log `skipped:length`.
3. Open native composer (NOT a third-party scheduler unless the user specified one).
4. Paste text; attach media; for LinkedIn, post link in first comment if `link_in_first_comment` set.
5. If `schedule` is a future timestamp, use the platform's native scheduler; if `now`, publish.
6. Capture the published-post URL (or scheduled-post id) — this is critical evidence.
7. Log: `{ platform, post_url, scheduled_for, status, char_count, screenshot_path }`.

For X threads: post root, capture URL, then post each reply against the captured root URL. If any reply fails, stop the thread (do not orphan replies).

### Operation 3 — Scheduled-post audit

Pull the platform's scheduled queue, output a table: `{platform, scheduled_for, preview, length, has_media, post_id}`. Do not modify anything; this is a read operation. User decides what to delete / reschedule; if they say "execute the deletes" the skill confirms count + sample first.

### Operation 4 — Follower / connection cleanup

Input: `cleanup-rules.json`.

```
{
  "platform": "x",
  "criteria": [
    { "field": "last_post_age_days", "op": ">", "value": 365 },
    { "field": "has_default_avatar", "op": "=", "value": true },
    { "field": "follower_count", "op": "<", "value": 5 },
    { "field": "bio_contains_any", "op": "in", "value": ["crypto signals", "DM for promo"] }
  ],
  "logic": "any | all",
  "action": "unfollow | block | mute | report",
  "max_actions": 50,
  "dry_run": true
}
```

Always start with `dry_run: true` regardless of input — produce a candidates list with reasons. Then ask the user to confirm before running with `dry_run: false`. Cap actions per session at 50 even if `max_actions` is larger; rate-limit one action per ~3 seconds; abort on first rate-limit warning from the platform.

### Operation 5 — Notification triage

Input: `triage-rules.json` — patterns + intent (reply / like / archive / ignore).

For each notification:
- Match against rules.
- `intent: reply` → DO NOT compose here; collect into a queue. Hand the queue to a content specialist via `tap` for batch-drafted replies. This skill never writes the reply text itself.
- `intent: like` → click like, log.
- `intent: archive` / `ignore` → mark read, log.

### Operation 6 — Archive / delete old posts

Input: `archive-rules.json` — age threshold, keyword excludes, platform.

1. Page through user's post history.
2. Build candidate list: `{post_url, posted_at, preview, engagement, matches_rule}`.
3. Always present sample + count + irreversible-warning, ask user to confirm.
4. If confirmed: action one by one, ≥ 2 s spacing, screenshot per action, log.
5. Stop on any platform error or rate-limit warning.

### Auth and session hygiene

- Use existing browser sessions if available. If a platform requires login mid-run, prompt the user once for that platform and continue.
- 2FA: prompt the user; never attempt to bypass.
- Never persist cookies or tokens to disk after the run.
- One identity per run. Don't switch accounts mid-operation.

### Output artifacts

Write to `./out/social/<operation>/<UTC>/`:
- `log.json` — one row per platform/action.
- `<platform>-before.png` and `<platform>-after.png` for sync/cleanup ops.
- `<platform>-published-<post_id>.png` for cross-post ops.

## Examples

### Example 1: Bad → Good (cross-post length handling)

❌ Bad:
```
The post is 480 chars. For X, truncate silently to 280 and add an ellipsis. Move on.
```

✅ Good:
```
For X, the post is 480 chars and no x-variant was supplied → log `skipped:length` for X, continue with the other platforms,
report at the end: "X skipped — supply variants.x or shorten to ≤ 280 chars."
```

What changed: silent truncation produces broken posts in the user's name. Skip and report — never mangle copy.

### Example 2: Edge case — LinkedIn link-in-first-comment

LinkedIn down-ranks posts with naked external URLs in the body by ~60%. If `variants.linkedin.link_in_first_comment` is set: post body without the URL → after publish, capture the post URL → reopen the post → add the link as the first comment from the same account → screenshot. Log both actions in one row.

### Example 3: Edge case — cleanup dry-run

User says "unfollow all bots, do it now." Skill still runs `dry_run: true` first, returns: "Found 117 candidates by your rules. Sample: @x, @y, @z. Confirm to execute (will action max 50 this session, ~3 s spacing)." Only after explicit confirmation does the skill execute.

## Checklist

- [ ] Inputs validated — `profile.json` / `post.json` / `cleanup-rules.json` / `triage-rules.json` / `archive-rules.json` exists and required fields are present
- [ ] Authenticated session confirmed for every target platform; 2FA prompts handled by the user
- [ ] Per-platform compose limits checked BEFORE driving the UI; over-limit posts skipped with a `skipped:length` row, not truncated
- [ ] Destructive operations (delete, unfollow, block, archive) ran a dry-run first and got explicit user confirmation
- [ ] Each action has evidence: post URL captured for publishes, screenshots for profile/cleanup, log row for everything
- [ ] Anchor / link / variant rotation respected for cross-post (no identical paste across all platforms when variants exist)
- [ ] Rate limits honored: ≥ 2 s between actions, ≤ 50 destructive actions per session, abort on platform warning
- [ ] Reply / comment composition was NOT done inside this skill — handed to content specialists via `tap`
- [ ] No credentials, cookies, or tokens persisted to disk after the run
- [ ] Final report: per platform, what changed, what was skipped (with reason), what failed (with reason), artifact paths

## Composition / References

- Pairs with `browser-form-filling-patterns` (selector resilience, file upload, multi-step UI).
- For ANY new copy (post bodies, replies, comments, DMs): call a content specialist via `tap`. This skill ships copy; it does not author it.
- For follower / engagement analysis or growth strategy: out of scope. Hand to a marketing specialist via `tap`.
- [X Help — Tweet length](https://help.x.com/en/using-x/x-tweet-character-counter)
- [LinkedIn Help — Post length](https://www.linkedin.com/help/linkedin/answer/a522537)
- [Bluesky — Post length](https://bsky.social/about)

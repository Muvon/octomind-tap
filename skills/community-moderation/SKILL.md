---
name: community-moderation
title: "Discord Moderation: Ladder, AutoMod & Community Rules"
description: "Enforcement ladder, channel structure, Discord permission names, AutoMod limits with example rule sets, and dated age rules. Use for rules or setup."
license: Apache-2.0
compatibility: "Needs web access to re-check Discord limits before quoting them."
domains: community-manager
rules:
  - match((?i)\b(draft|write|design|revise)\b.{0,40}\b(automod\s+config\w*|moderation\s+(policy|rules)|escalation\s+ladder|server\s+rules|code of conduct)\b)
  - match((?i)\b(verification level|automod\b.{0,30}\blimits?)\b)
---

## Overview

Use this skill when you write moderation rules, an enforcement ladder or an AutoMod rule set, or when you set up the channels, roles and permissions of a Discord server. It gives one shared ladder, the Discord permission names that matter for moderation, the AutoMod limits, example rule sets, and the age rules, each with an as-of date.

Platform figures change. Every number below is "as of 2026-11". Re-check it on the pages listed under References before you quote it to a user.

## Mental model

Enforcement is a ladder with defined review points, not a mood. The same rule, evidence and consequence apply to friends, staff and strangers. Tooling carries the first line (AutoMod), humans decide everything that is not mechanical, and every action is logged with the rule it cites. Channels stay few so that newcomers find a human reply quickly.

## Rules

### Draft a policy pack

Use this procedure when the brief asks for rules or a moderation policy. A server template uses approved policy text and records missing approval as a dependency.

1. Establish audience, size, languages, age range, staffing coverage, likely abuse patterns, and tolerance for promotional content; inspect supplied rules and anonymized incident summaries before prescribing.
2. Research current official Discord Community Guidelines, safety guidance, and AutoMod documentation with live search, verifying supported triggers, actions, exemptions, limits, and permissions before naming settings.
3. Write concise member-facing rules with concrete allowed and prohibited examples, then map every rule to a moderator procedure rather than relying on vague demands to be nice.
4. Build the escalation ladder with severity-based bypasses, evidence requirements, private notice copy, appeals, and a review owner; tune response expectations to the team's actual coverage.
5. Draft native AutoMod rule configurations and setup steps, separating automated actions from human judgment and explaining false-positive risks and exceptions.
6. Test the policy on benign and abusive sample cases, review exemptions and appeal paths, then write the policy pack with sources, owner approvals, and unverified settings clearly marked.

- Define warnings, timeouts and bans with review points. Keep severity-based bypasses accountable to an authorized human and apply the same standards to members and staff. Document conflict-of-interest handoffs and assign an independent appeal reviewer where staffing permits.
- For each AutoMod rule state its name, risk addressed, trigger type, exact proposed values, supported action, alert destination, exempt roles/channels, required permissions, test cases, and rollback steps.
- Verify native support before recommending keyword, spam, mention-spam, or profile-name filtering; identify unsupported needs as human-review gaps, not imaginary settings or bot code.
- Treat regexes and keyword lists as proposals until checked against Discord's current supported syntax and tested; avoid broad identity terms, blanket staff exemptions, or filters that punish ordinary discussion of abuse.
- Keep reports private and public notices minimal; record only necessary evidence, access controls, and a proposed retention period for owner review, without promising legal compliance or encouraging redistribution of harmful material.
- Protect minors and vulnerable members; verify current age restrictions, prohibit evasion, and direct credible imminent-danger situations to appropriate emergency services and platform reporting channels rather than promising confidential crisis care.
- Don't apply sanctions. For a live incident, return a containment and reporting draft for authorized humans, keep incident evidence minimal and private, and require accountable human review and appeals.
- No sockpuppets, undisclosed staff posing as members, or AI presented as a human moderator; automation does not replace accountable review.
- Cite live sources by title, URL, and access date for platform behavior and external claims; never invent prices, specifications, laws, references, incident evidence, or enforcement results.
- Health, legal, and financial statements are general information, not diagnosis, legal advice, or financial advice; flag qualified review when the policy depends on those judgments.

Write `discord-<community-slug>-moderation-policy.md`: audience and risk assumptions; ready-to-post rules draft; private moderator playbook; severity/escalation matrix; report, notice, and appeal templates; AutoMod configuration table and numbered setup steps; benign/abuse test cases and expected outcomes; weekly filter review checklist; sources and approval dependencies. Label the configuration a manual settings draft, not an importable file, installed bot, or active protection.

### Enforcement ladder

| Rung | Action | When | Log |
|---|---|---|---|
| 0 | Note | Borderline behaviour, no rule broken yet | Moderator note, no notice to member |
| 1 | Private warning | First clear rule break | Rule cited, message link, date |
| 2 | Timeout | Repeat after a warning, or a heated pile-on | Duration, rule, evidence |
| 3 | Kick | Repeat after a timeout, or evading a timeout | Rule, evidence, reviewer |
| 4 | Ban | Repeat after a kick, or any skip-rung offence | Rule, evidence, reviewer, appeal route |

Skip-rung offences go straight to timeout or ban: credible threats, scams and phishing links, raid participation, targeted harassment, sexual content involving minors (also report it to the platform and, where required, to law enforcement). An authorised human decides and logs the reason. Pick timeout lengths per community and write them down; there is no universal duration. The appeal reviewer is a different person from the one who acted, where staffing allows. A moderator steps back from any case that involves a friend or a personal dispute.

### Channel structure

- Start with 4 to 6 channels: start-here, announcements, one main lounge, one or two topic rooms, help. This is a design heuristic, not a Discord limit.
- Split a channel only when one topic reliably drowns another. Archive channels that stay empty.
- Put the rules, onboarding and help in channels that every member can read, including members who cannot enter age-restricted spaces.
- Route repeat help questions to a forum channel with tags and a "solved" tag.
- Staff channels (mod log, mod chat) are hidden from @everyone and from every self-assigned interest role.

### Discord permissions that matter for moderation

Names as listed in Discord's developer documentation (as of 2026-11).

| Permission | What it allows | Give it to |
|---|---|---|
| Moderate Members | Time out members; a timed-out member keeps only View Channel and Read Message History | Moderators |
| Manage Messages | Delete other members' messages; pin | Moderators |
| Kick Members, Ban Members | Remove or ban members | Senior moderators |
| View Audit Log | Read the server audit log | Moderators |
| Manage Guild | Edit the server; required to create or edit AutoMod rules | Admins only |
| Manage Roles | Create and edit roles below the holder's highest role | Admins only |
| Mention Everyone | Use @everyone and @here | Admins; keep it off @everyone |
| Administrator | Every permission; ignores channel overrides | Owner only |

Rules that follow from this:

- Keep @everyone minimal: read and send in public channels, no mention-everyone, no external invites if the community does not need them.
- A bot or member can only manage roles below their own highest role. Place the bot role above the roles it must assign and below every staff role.
- Channel overrides apply regardless of role position. Test the effective permissions of each role in each channel with "View Server As Role".
- Manage Messages, Kick Members, Ban Members, Manage Guild, Manage Roles and Administrator are covered by the server-wide two-factor requirement. Moderate Members, Mention Everyone and View Audit Log are not. Ask the owner to turn the requirement on, which needs two-factor on the owner's own account.

### Community prerequisites

Enabling the Community feature unlocks the welcome screen, Membership Screening, stage channels and discovery, and it needs the Administrator permission to switch on or off (developer documentation). AutoMod requires Community to be enabled (Discord's moderation guide). The setup wizard asks for a rules channel, a moderator-updates channel, a verification level and media scanning; read the wizard in the current client and write down what it asks, because the list is not in the developer documentation.

Verification levels (developer documentation):

| Level | Requirement before a member can speak |
|---|---|
| None | None |
| Low | Verified email on the account |
| Medium | Registered on Discord for more than 5 minutes |
| High | Member of this server for more than 10 minutes |
| Very high | Verified phone number |

Explicit media filter levels: disabled; members without roles; all members. Default for a public community: all members.

### AutoMod limits (developer documentation, as of 2026-11)

| Item | Limit |
|---|---|
| Custom keyword rules per server | 6 through the API; Discord's in-app guide says up to 3 custom keyword filters, so check the server settings screen |
| Spam, preset words, mention spam, profile rules | 1 each per server |
| Keywords per custom rule | 1000, each up to 60 characters |
| Regex patterns per rule | 10, each up to 260 characters, Rust-flavoured syntax; a valid pattern can still be rejected as too complex |
| Allow-list entries | 100 per custom rule; 1000 for the preset-words rule |
| Mention limit | Up to 50 unique mentions per message |
| Actions | Block message (custom notice up to 150 characters), send alert to a channel, timeout up to 4 weeks (keyword and mention-spam rules only) |
| Exemptions | Up to 20 roles and 50 channels per rule |
| Who is exempt | Members with Manage Server or Administrator, bots and webhooks |
| Who can set rules up | Manage Server; timeout actions also need Moderate Members |

Because staff are exempt, test every rule with a member account that has no staff permission.

### Example rule sets

Starter set for a small public community. Names, values and actions are proposals; test each one before turning it on.

| Rule | Trigger | Values | Action | Exempt |
|---|---|---|---|---|
| Scam links | Custom keyword | `*free nitro*`, `*gift card*`, `*airdrop*`, `*claim your prize*` | Block, alert to mod-log | Mod role |
| Mention spam | Mention spam | Limit 5 unique mentions | Block, alert, timeout 10 minutes | Mod role |
| Spam content | Spam | Discord model | Block, alert | Mod role, bots channel |
| Slurs | Commonly flagged words (Insults and Slurs list) | Preset list | Block, alert | None |
| Profile names | Member profile | Slur and impersonation words, staff names | Alert only | None |

Rule set for a support or developer community, adding: a custom keyword rule for pasted tokens (`*sk-*`, `*api_key=*`) that blocks and alerts, and a mention-spam limit of 3.

Rule set for a community with minors likely present: set the explicit media filter to all members, send alerts for the preset sexual-content list, and keep the verification level at Medium or higher.

False-positive routine: review the alert channel weekly; add legitimate hits to the allow-list; remove a rule that blocks real members more than it blocks abuse.

### Age rules (Discord, as of 2026-11)

- Discord requires every user to be at least 13. Teens are 13 to 17, adults 18 and over (Discord Safety News Hub).
- Discord's blog post of 2026-02-24 delayed its global age-assurance launch to the second half of 2026; Discord marks that post as out of date and points to a newer one.
- Discord's update of 2026-09-22 says more than 90 percent of users will not be asked to confirm their age: Discord estimates an age group from account signals. Teens can still use friends, DMs, voice and servers that are not age-restricted, and are blocked from age-restricted content and spaces.
- In the UK, Australia and Brazil, adults seeking age-restricted content had to verify through a vendor such as k-ID (Discord blog, 2026-02-24, marked out of date by Discord; the 2026-09-22 update does not repeat it, so read Discord's current page). Elsewhere, adults whose age cannot be inferred may be asked to verify.
- Design consequence: keep the rules, onboarding, help and events outside age-restricted channels, and label genuinely adult channels age-restricted instead of relying on a rules line.
- Do not help a member bypass age restrictions. Direct imminent danger to emergency services and platform reporting.

## Examples

Bad: "Be nice or you will be banned. Mods decide."
Good: "Rule 3, harassment. First clear break: private warning citing rule 3. Repeat within 30 days: 24-hour timeout. Credible threats or doxxing: ban, logged by the moderator and reviewed by a second moderator within 48 hours. Appeal: reply to the notice within 14 days; a moderator who did not act decides."

Bad: AutoMod keyword rule `*ass*`.
Good: AutoMod keyword rule on the exact scam phrases in the table above, plus alert-only for the broader list so a moderator reads the hits for a week before any word is blocked.

## Checklist

- [ ] Every limit and date in the output carries "as of" and a source, or is marked unverified.
- [ ] Ladder has a review point, a skip-rung list, a log entry format and an appeal reviewer.
- [ ] Each AutoMod rule states trigger, values, action, alert channel, exempt roles, required permissions, test cases and rollback.
- [ ] No Administrator granted for convenience; bot role sits below staff roles.
- [ ] Onboarding and help sit outside age-restricted channels.
- [ ] Nothing was applied to a live server without the owner's approval.

## Composition / References

Checked 2026-11-15:

- Discord developer docs, AutoMod: https://docs.discord.com/developers/resources/auto-moderation
- Discord developer docs, permissions: https://docs.discord.com/developers/topics/permissions
- Discord developer docs, guild (verification levels, Community feature): https://docs.discord.com/developers/resources/guild
- Discord moderation guide, Auto Moderation in Discord: https://discord.com/moderation/1500000178701-321-auto-moderation-in-discord
- Discord Safety News Hub: https://discord.com/safety-news
- Discord blog, Getting Global Age Assurance Right (2026-02-24): https://discord.com/blog/getting-global-age-assurance-right-what-we-got-wrong-and-whats-changing
- Discord announcement, age group update (2026-09-22): https://discord.com/announcements/889960284020699156/1552019390554312714

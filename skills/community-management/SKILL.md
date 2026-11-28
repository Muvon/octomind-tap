---
name: community-management
title: "Community Management: Onboarding, Rituals, Health Audits"
description: "Runs a live community: revival plans, onboarding, engagement rituals, moderator recruitment, incident handling and monthly health metrics."
license: Apache-2.0
compatibility: "Reads live server activity through a connected Discord server when one is available; otherwise works from exports the user supplies."
capabilities: messaging-discord memory-read memory-write variety
domains: community-manager
rules:
  - match((?i)\b(live|existing|connected|our)\b.{0,60}\b(discord|server|community)\b.{0,200}\b(audit|health|incident|raid|moderation review|automod|onboarding|churn|retention|lurkers?|metrics|ritual|playbook|code of conduct|rule changes?|announcement)\b)
  - match((?i)\b(audit|review|tune|tuning)\b.{0,60}\b(live|connected)\b.{0,40}\b(discord|server|community)\b)
  - match((?i)\b(recruit\w*|onboard\w*)\b.{0,40}\b(moderators?|mods|volunteers?)\b)
  - match((?i)\b(mod[- ]?log|post-mortem|incident\s+(write-up|review|follow-up))\b)
  - match((?i)\b(revive|revitali[sz]e)\b.{0,40}\b(community|discord|server)\b)
  - match((?i)\b(moderators?|mods?)\s+(recruit\w*|onboarding)\b|\bprogram\w*\s+(engagement\s+)?rituals?\b)
  - match((?i)\b(our|my)\s+(discord|server|community)\b.{0,80}\b(dead|quiet|healthy|health|talking)\b|\bhit by a\b.{0,15}\braid\b)
  - match((?i)\b(playbook|code of conduct|rituals?|metrics|audit)\b.{0,80}\b(our|live|existing|connected)\b.{0,30}\b(discord|server|community)\b)
  - semantic(we had a raid last night, write up the incident and what to change)
  - semantic(build a monthly health report for our community with engagement metrics, 0.77)
  - semantic(recruit volunteer moderators and set up weekly engagement rituals, 0.80)
---

## Overview

Use this skill to run a community that already exists or is about to launch: decide whether it should exist, read its real activity, shape structure and onboarding, program a sustainable weekly rhythm, recruit and protect moderators, handle incidents, and measure health with metrics that predict survival. The output is a ranked, evidence-based plan or audit, plus drafts of announcements and rules for the owner to approve.

This skill does not cover posting to public social feeds, a product's launch campaign, paid acquisition or support-ticket resolution that happens to live in the community. It owns where the tickets flow, not the ticket craft.

## Mental model

Most members never post, so a healthy community works for readers first. Member-to-member value is the engine, not brand content. Rituals that a small team can sustain beat ambitious events. Rules protect the atmosphere, and the atmosphere is the product. Measure trends in return and reply speed, not snapshots of size.

## Rules

Procedure:

1. Define the why. Who is the community for, what do members get from each other (not from the brand), and what does the host get? With no honest answer to all three, say the community should not exist yet; a newsletter or a forum-free launch may serve better.
2. Read the room. For an existing community, pull real activity from the connected server before prescribing: message volume by channel, who talks, response times, dead zones. Don't diagnose from impressions.
3. Design the structure. Use the minimum viable rooms, onboarding that gets a new member to a first interaction within minutes, and roles that mean something. Search how comparable communities in the niche structure themselves when the territory is unfamiliar.
4. Write the law. Plain-language code of conduct, the moderation ladder and a moderator playbook with edge cases, tuned to the room's real activity and incident history. Use the moderation skill for the ladder, permission names, AutoMod limits and age rules.
5. Program the rhythm. Recurring rituals over one-off events, on a calendar the team can sustain. A skipped ritual costs more than a small one earns.
6. Measure and report. Run the health metrics monthly. Record the community's patterns, personalities and incident history in memory. Draft every announcement and member-facing message for approval before posting.

Structure, start smaller than feels right: launch with 4 to 6 channels at most (welcome or start-here, announcements, one main lounge, one or two topic rooms, help). Empty channels signal that nobody is home. Split a channel only when one topic reliably drowns another, and archive dead channels. Use voice, stage and threads for events, not as permanent furniture.

Onboarding: the distance from join to first human interaction is the retention lever. Use Discord's native Community Onboarding: a short rules screen, a few customization questions that hand out roles and channels by interest, default channels a newcomer needs, and a Server Guide with a welcome message, new-member to-dos and resource pages. Add an intros prompt ("what are you building or stuck on") and a greeter habit: moderators or bots tag a human, and humans answer. A member who gets a reply in the first hour is a member; one who posts into silence is a visitor who left. Onboarding options change, so check the current server settings before prescribing exact steps.

The 90-9-1 reality: a long-standing heuristic, not a measured law. Roughly 90 percent lurk, 9 percent react, 1 percent create. Lurkers need spectator value (good threads, recaps, showcases). Reactors need low-friction participation (polls, emoji votes, one-word prompts). Creators need recognition (roles, spotlights, early access). Judging health by the share of members who post kills good communities; judge by return rate and reply speed. Route recurring help questions into a forum channel with tags and a solved convention, so answers stay searchable and feed the docs.

Moderation in practice: document the ladder and apply it identically to friends and strangers: note, private warning citing the rule, mute or timeout, kick, ban (appealable, logged). Spam, scams and harassment skip rungs. Safety comes first, process second. Log every action with the rule cited and move public drama to private quickly. Let tooling carry the first line: AutoMod keyword, spam, mention-spam and profile-name rules, plus the raid security actions that pause invites or DMs during an attack. Review AutoMod hits weekly so filters don't silently remove real members. Recruit moderators from consistently helpful members, give them the playbook and rotate them before burnout. An exhausted mod team is a dying community's first symptom.

Age and safety defaults: keep onboarding, rules, help and events outside age-restricted spaces so teen and unverified members can take part, and mark genuinely adult spaces as age-restricted instead of relying on a rule line. Re-check dated Discord age rules before quoting them.

Programming, rituals beat events: weekly beats monthly. Examples: a show-your-work thread, office hours, a themed question, a wins recap. One sustainable ritual beats three ambitious ones that die by week 6. Tie rituals to member value, not brand content. Recap threads let lurkers feel the pulse without attending live.

Health metrics, monthly and as trends: return rate (members active this month who were active last month), first-response time to new-member posts, DAU/MAU stickiness, the share of messages from the top 10 posters (rising concentration means fragility), new-member first-week activation, and moderator-action volume. Growth in member count without growth in active members is a bigger room, not a bigger community.

Never fake it: no sockpuppets, no staged questions from alt accounts, no undisclosed paid enthusiasm. Honest seeding is fine: founders visibly present, teammates labeled as team, early members personally invited. Bots and AI helpers are visibly bots, named as such, and never pose as a human member or moderator.

Situations:

- Start a community: the three-way value question first, then an honest verdict, the minimum structure and a four-week launch rhythm.
- My server is dead: pull real activity, diagnose (structure, onboarding, rituals, reason to return), then the revival sequence, usually shrinking first.
- Write the rules: code of conduct, ladder, moderator playbook and AutoMod settings, tuned to the community's actual risk profile.
- Handle this incident: the immediate containment step, then the ladder-consistent response and the log entry.
- Ambiguous: ask one question (usually who it is for and what they get from each other), then proceed.
- Brief marked AUTONOMOUS or non-interactive: skip the opening question, read the connected server if available, state assumptions about audience and value at the top, and deliver drafts. Posting, DMs and moderator actions still wait for explicit approval.

## Output format

Strategy and audits go in `community-<name>-<topic>.md`: verdict up front, evidence from real server data, changes ranked by effort and impact. Structures are channel trees with one-line purposes. Policies are ready-to-post rules text with a separate moderator playbook. Messages and announcements are drafts in fenced blocks awaiting approval.

## Checklist

- [ ] The three-way value question has an honest answer, or the verdict says the community should not exist yet.
- [ ] Every prescription for an existing community cites real activity data.
- [ ] Channel count, rituals and moderator load are sustainable for the actual team.
- [ ] Health is reported as trends: return rate, reply speed and activity concentration.
- [ ] The ladder is applied the same way to every member, and each action is logged with its rule.
- [ ] No fake members, staged enthusiasm or AI presented as a person.
- [ ] Nothing was posted, sent or enforced without approval of that exact message or action.

## Composition / References

- The `community-moderation` skill: ladder, permission names, AutoMod limits and dated age rules.
- The `community-discord-server-blueprint` skill: a ready-to-apply server template for a new or redesigned server.

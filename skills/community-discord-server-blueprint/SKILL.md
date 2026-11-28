---
name: community-discord-server-blueprint
title: "Discord Server Template: Channels, Roles, Onboarding"
description: "Writes a manually applied Discord server template: channel tree, role hierarchy, permission matrix, onboarding, setup steps and role-view tests."
license: Apache-2.0
compatibility: "Needs web access to check current Discord documentation before quoting permissions, onboarding or age rules."
domains: community-manager
rules:
  - match((?i)\b(design|draft|create|plan|build|make|set\s*up)\b.{0,30}\b(server|discord)\s+(template|blueprint|layout|structure|setup)\b)
  - match((?i)\b(channel\s+tree|role\s+hierarchy|permission\s+matrix|server\s+guide|interest[- ]roles?)\b)
  - match((?i)\b(set\s*-?up|setup)\s+(runbook|instructions|guide|checklist|steps)\b)
  - match((?i)\b(map out|lay out|redesign|restructure|shrink)\b.{0,50}\b(channels?\b.{0,30}\broles?|roles?\b.{0,30}\bchannels?|categories)\b|\bwho can see what\b)
  - match((?i)\b(welcome\s+(message|screen|copy|text)|onboarding\s+(questions|flow))\b.{0,60}\broles?\b)
  - match((?i)\b(pre-launch|access)\s+(access\s+)?(checklist|test\w*)\b)
  - match((?i)\bapply\w*\b.{0,40}\btemplate\b)
  - semantic(design the channel layout and roles for a new discord server, 0.80)
  - semantic(who should see which channels, give me a permission matrix)
  - semantic(write setup steps so I can build this server template by hand)
  - semantic(plan the welcome flow and onboarding questions that assign roles, 0.73)
---

## Overview

Use this skill when the user wants a new Discord server designed from scratch, or an existing one redesigned, as a ready-to-apply template. The result is one Markdown file an owner applies by hand: categories and channels, a role hierarchy with narrow permissions, an onboarding path, welcome copy, ordered setup steps and tests for each role's view. It is a manual setup blueprint, not a Discord-importable template or a generated template link, and nothing is applied to a live server.

This skill does not cover ongoing community strategy, engagement calendars, health audits or incident coordination, and it does not build bots, decide live enforcement cases or administer a live server.

## Mental model

A server starts with the smallest set of rooms that each have a purpose, an audience and an owner. Permissions are narrow by default and widened only for a stated reason. Newcomers must reach welcome, rules, help and a first interaction without needing a role that unlocks sensitive spaces. A policy the template depends on comes from the owner; a missing policy is recorded as a dependency, not invented.

## Rules

Procedure:

1. Define the brief: audience, member-to-member value, expected size, age range, languages, public or private access, accessibility needs and available moderator time. Read supplied files before designing.
2. Check current Discord documentation through live search for permissions, Community Onboarding, Server Guide, feature eligibility and age restrictions. Cite the official pages and separate verified behavior from assumptions. The `community-moderation` skill holds the permission names, verification levels, Community prerequisites and dated age rules.
3. Draft the smallest useful channel tree and role hierarchy. Give each room a purpose, an audience and an owner instead of filling space with empty rooms.
4. Build the permission matrix, the onboarding path and the welcome copy. Use approved policy text when supplied; mark missing policy as a dependency and draft a new policy only when the user asks.
5. Write the template file with ordered setup steps, feature prerequisites, manual copy blocks, and tests for the newcomer, member, moderator and restricted-access views.
6. Review inherited permissions and onboarding visibility, then report what is ready, what needs owner approval and what has not been tested in a live server.

If the user asks for both a template and a policy, draft the policy and mark it pending approval inside the template.

Design rules:

- Start with roughly 4 to 6 useful channels for a small community. Expand only when distinct traffic or privacy needs justify another room. Label this a design heuristic, not a Discord limit.
- Show category to channel nesting, channel type, a one-line purpose, read and send access, and whether permissions stay synced. Document every intentional override.
- Keep @everyone minimal. Separate staff duties from cosmetic and interest roles. Avoid Administrator as a convenience. Check effective permissions across inherited settings, role combinations, overrides and hierarchy.
- Keep welcome, rules, help and a first interaction reachable for eligible newcomers. Test that self-selected roles cannot unlock staff or sensitive spaces.
- Verify current age and safety requirements rather than assuming every account can use every feature. Keep essential onboarding outside adult-only spaces and do not bypass age restrictions.
- Explain optional paid features or bots only when needed, with current prices and specifications and citations. Prefer native features when they meet the brief.
- Link sources with page titles and access dates beside changeable claims. Never invent prices, specifications, laws, references or successful setup results; label unavailable evidence as unverified.
- Don't copy private member data into welcome examples or expose staff notes. Label automation honestly and never recommend fake members or staged enthusiasm.
- Health, legal and money questions get general information only, not diagnosis, legal advice or financial advice. Flag the need for specialist review and put member safety ahead of growth.

Situations:

- Clear brief: write the blueprint and summarize its location and unresolved dependencies.
- Missing audience or access decision: ask one focused question. When no answer is possible, use labeled conservative assumptions and leave sensitive settings pending approval.
- Brief marked AUTONOMOUS or non-interactive: ask nothing; write the artifact with labeled conservative assumptions, leave sensitive settings pending approval, and report the path and the open dependencies.
- Existing server redesign: use supplied channel and role exports, propose a migration plan and leave destructive changes unapplied.

## Output format

Create `discord-<community-slug>-server-template.md` with these sections: brief and assumptions; category and channel tree; role hierarchy and permission matrix; onboarding sequence and welcome copy; numbered Discord server setup checklist; role-view acceptance tests; policy dependencies; sources and verification limits. Explain that the file is a manual setup blueprint. Read an existing file before updating it and preserve unrelated content.

## Checklist

- [ ] Every channel has a purpose, an audience and an owner; the tree has no empty filler rooms.
- [ ] Permission matrix lists effective permissions per role; no Administrator for convenience.
- [ ] Newcomer, member, moderator and restricted-access views each have an acceptance test.
- [ ] Onboarding and help sit outside age-restricted spaces.
- [ ] Changeable claims carry a source and an access date, or are marked unverified.
- [ ] Missing policy is listed as a dependency, and nothing was applied to a live server.

## Composition / References

- The `community-moderation` skill: permission names, verification levels, Community prerequisites, AutoMod limits and age rules, plus the policy pack a template links to.
- Discord developer documentation and the Discord moderation guide, as listed in the `community-moderation` skill.

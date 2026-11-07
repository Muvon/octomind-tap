---
name: writing-variety
title: "Avoid Repeated AI Writing Patterns"
description: "Keep a run of posts, replies, articles, emails, ad angles, scripts, or release notes for one account from sounding the same. Get an approach and form from the variety tools before each piece, then check the draft for AI writing tells and repeated openings. Activate for batches and recurring writing jobs."
license: Apache-2.0
compatibility: "Needs the variety capability: either the local variety server or the hosted unsame server. Network access only for unsame."
domains: content marketing sales video developer support community launch
rules:
  - content(variety)
  - match(\b(sound|read)s?\s+(all\s+)?the\s+same\b)
  - match(\bdifferent\s+(angle|approach|opening)\s+(for|on)\s+(each|every)\b)
  - match(\b(batch|series|week|month|set)\s+of\s+(posts|replies|emails|newsletters|articles|blog\s+posts|scripts|ads|hooks|updates|release\s+notes)\b)
  - match(\bwrite\s+(\d+|ten|twenty|five|a\s+few|several)\s+(posts|replies|emails|articles|scripts|ads|hooks|variants)\b)
  - semantic(my posts all sound the same and I need each one to take a different approach)
  - semantic(write a batch of replies without repeating the same opening)
---

## Overview

Use this when one job produces many pieces for the same account or channel: a week of posts, a queue of replies, a blog series, a run of newsletters or outreach emails, a set of ad angles, a series of video scripts, release notes for every version. Written one at a time, such pieces drift into the same opening, the same length, and the same closing line. Before each piece, ask a variety tool which approach and form to use, write to it, and check the result. A single one-off piece gains little; skip the tool for it unless the user asks.

## Mental model

An approach is the angle of the piece, such as a question, a small story, or a plain claim with one example. A form is its shape: how it opens, how long it runs, and how it ends. A variety tool remembers the combinations used recently for a scope and hands out one that was not. The scope is a label for the account or channel, for example "brand-x-posts": letters, digits, `_`, `:`, `.` and `-` only, no spaces. Reuse the exact same label on every call for that job, or the tool cannot see the history.

The local server needs a kind. Match it to the piece, not to the agent:

| Piece | Kind |
|---|---|
| Social post, thread, ad copy angle | `post` |
| Reply to a comment, mention, review, community or support message | `reply` |
| Blog post or long article | `article` |
| Newsletter, campaign or cold outreach email | `email` |
| Short video, UGC or ad script | `script` |
| Release notes, product update, changelog summary for users | `update` |

One call covers one finished piece: one call per article, not per section; one call per ad angle when a campaign needs several.

Two providers exist. The unsame server matches each input to a fitting approach with an AI judge, uses the user's own playbook for the goal, and learns from the results the user reports. The local variety server needs no account and picks from a built-in list by kind. Use whichever server is connected. If both are, use unsame.

## Rules

1. Pick a scope label once, tell the user what it is, and reuse it for every piece in the job. Ask the user for it if the account or channel is unclear.
2. Get the protocol before drafting each piece, not once per batch. Skipping a call is how repeats come back.
3. Follow the protocol as given. Do not soften the opening, add a closing line it did not ask for, or merge two forms.
4. Keep the user's voice and facts. The approach decides the shape, not the content. Never invent a story, number, quote, or result to fit an approach.
5. If the approach does not fit the input, ask again with the rejected id in `avoid`, or tell the user no fitting approach exists. Do not bend the facts.
6. With the local server, show the draft only after `variety_check` passes.

## With the unsame server

1. Call `advise` with `goal` (the playbook the user set up for this job, found with `goal_list` if needed), `input` as an object `{"text": "..."}` holding the thing to write about or reply to, and `scope`.
2. Write the piece exactly as the returned protocol says. Keep the `draw_id` from the response.
3. If the user says how the piece did, call `report` with that `draw_id` and an `outcome`: `{"chosen": true}` when they picked it, `{"rejected": true}` when they threw it away, `{"edited": 0..1}` for how much they changed it, or `{"reward": 0..1}` for how well it performed. Do not report guesses.

## With the local variety server

1. Call `variety_kinds` once if unsure which kind applies. The kinds are post, reply, article, email, script, and update.
2. Call `variety_pick` with `kind` and `scope`. Follow the approach and form it returns.
3. If the approach does not suit the input, call `variety_pick` again with `avoid` set to a list holding that approach id.
4. After drafting, call `variety_check` with the `text` and the same `scope`. Fix every issue it lists, then check again until it is clean.

## Examples

Replies to five comments on one account. Scope "acme-support-replies". For each comment, call `variety_pick` with kind "reply". The first returns a short answer that opens with the fix. The second returns a question back to the commenter. Write each as returned, with the facts from the comment and the product docs only. The third pick asks for a personal anecdote the user never gave. Call again with `avoid` set to that id rather than inventing a story.

Weekly update emails. Scope "founder-update". With unsame, call `advise` with the goal "weekly_update", `{"text": <this week's notes>}` as `input`, and the scope. Follow the protocol. The user says the email went out unchanged, so call `report` with its `draw_id` and `{"chosen": true}`.

## Checklist

- [ ] One scope label, reused on every call in the job.
- [ ] A protocol or pick was fetched before each piece, not once for the batch.
- [ ] The draft follows the approach and form as given.
- [ ] No fact, story, number, or quote was added to fit the approach.
- [ ] Local server: `variety_check` ran on the final text and every issue is fixed.
- [ ] Unsame: `report` was called only for results the user actually gave.
- [ ] Rejected approaches were retried with `avoid`, not forced.

## Composition

Pair with a voice or humanizing skill when the user wants a stricter match to their own style. This skill decides the shape of each piece; those decide the wording inside it.

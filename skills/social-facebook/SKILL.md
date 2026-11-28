---
name: social-facebook
title: "Facebook Posts and Reels: Caption Writing Guide"
description: "Write and revise Facebook Page posts, Reels and captions in the author's voice, with a publishing package. Use when drafting or auditing for Facebook."
license: Apache-2.0
compatibility: "Network access for current platform checks; a Facebook Page for composer previews and Insights."
domains: writer
rules:
  - content(facebook)
  - match((?i)\bfacebook\s+(post|page|reel|reels|caption|video|copy)\b)
  - match((?i)\b(fb)\s+(post|page|reel|reels|caption)\b)
  - match((?i)\b(post|publish|write)\s+(on|to|for)\s+facebook\b)
---

## Overview

Draft from supplied facts and proof, then the author's documented voice, then platform conventions. Use `content-voice` for generic editing; this playbook adds Facebook packaging and the distribution rules Meta publishes. Never invent experience or results. Writing a package does not authorize posting. Facebook has no text-publishing tool in this registry, so an approved package goes to the browser domain or to the user's own composer.

Meta changes Facebook rules often. The limits below carry a source date; check the live page before relying on one.

## Mental model

Facebook ranks and reduces distribution by content quality, not only by engagement. Meta states that content which does not break its Community Standards can still lose distribution when it is low quality (Meta Transparency Center, updated 2025-04-25). For a Page, the writing job is to avoid the listed low-quality shapes and to give a reason to watch or read that does not depend on a request for reactions.

## Rules

### What Meta says it reduces

Meta's page on lowering distribution lists these shapes (Meta Transparency Center, updated 2025-04-25):

| Shape Meta lists | Writing consequence |
|---|---|
| "Clickbait and engagement bait" | No "like if", "share to", "tag a friend", reaction-vote prompts, or a headline that withholds the point. Ask a real question only when the answer matters. |
| Links to websites "covered with ads, slow to load or broken" | Open the destination before packaging; a slow or broken page is a reason to drop the link. |
| Comments "repeatedly copied and pasted" | Reply plans use distinct replies, not one pasted answer. |
| "Limited originality content that is principally repurposed from other sources" | Every post adds something of the author's own (see below). |
| "Low-quality videos that abuse video or live video formats" | Do not stretch a thin clip to fill length or loop it. |
| Content by creators that "repeatedly violate our policies" | One policy miss is not the end; a pattern is. Keep a pre-publish check. |

### Originality

Meta's creator post of 2025-07-14 says accounts that repeatedly reuse others' videos, photos or text lose monetization eligibility for a period and get reduced distribution; duplicate videos detected by its systems get reduced distribution. Not treated as unoriginal: resharing, commentary on reaction videos, joining trends with your own perspective, and permitted material with your own meaningful input such as creative editing, voiceover or annotation. Trimming a clip or adding a watermark is not meaningful input. Each package names what the author adds to any source material.

### Video and Reels

- Since September 2025, Meta's Help Center says videos on Facebook are shared as Reels "regardless of length or orientation" (Facebook Help, "Create a reel on Facebook"). Do not write to an older 60-second or 90-second cap in the app.
- Publishing through the Reels Publishing API is narrower: duration 3 to 90 seconds, 9:16 recommended, 1080 x 1920 recommended and 540 x 960 minimum, fixed 24 to 60 fps; a reel shared as a Page story is capped at 60 seconds (Meta for Developers, Reels Publishing API guide, read 2026-11). If the package may go through a scheduler built on that API, cut a 90-second version.
- The API accepts a description with hashtags and a separate title. Meta states no description length in that guide; test the composer.

### Paid and AI-made content

Branded content is posted with Meta's branded content tool and the Paid Partnership label. The label meets Meta's platform rule, and it does not replace the legal disclosure in the author's country; follow the `content-disclosure` skill for both, and for the AI-content label.

## Examples

Weak Page post: "Big news! Like and share if you want to see more of this! Link in comments."
Revised: state the news in the first line, give one concrete detail, put the link in the post, and end without a reaction request.

Weak Reel plan: a 20-second clip re-uploaded from another account with a watermark added.
Revised: the author adds a voiceover and a correction or result of their own, and the package names that addition.

## Checklist

- [ ] First line carries the point; no engagement-bait prompt (vote, tag, share-to-unlock).
- [ ] Link destination opened and loads; link sits in the post copy.
- [ ] Any reused material has permission and a named author contribution.
- [ ] Reel duration fits the publishing path (any length in the app; 3 to 90 seconds via the API).
- [ ] Paid partnership and AI-content disclosure checked through the `content-disclosure` skill.
- [ ] Alt text or captions supplied for images and video.
- [ ] Reply owner named; replies are individual, not pasted.
- [ ] Publishing stays a separate approved step.

## References

- [Meta Transparency Center, reducing the distribution of problematic content](https://transparency.meta.com/enforcement/taking-action/lowering-distribution-of-problematic-content/), updated 2025-04-25.
- [Meta, combating unoriginal content](https://creators.facebook.com/blog/combating-unoriginal-content), 2025-07-14.
- [Facebook Help, create a reel](https://www.facebook.com/help/android-app/2862139500770200), read 2026-11.
- [Meta for Developers, Reels Publishing API](https://developers.facebook.com/documentation/video-api/guides/reels-publishing), read 2026-11.
- [Meta Business Help, Branded Content Policies](https://www.facebook.com/business/help/221149188908254).

Re-validate when Meta changes its distribution, originality or branded content pages.
Validated: 2026-11

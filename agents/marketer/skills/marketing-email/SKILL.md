---
name: marketing-email
title: "Email Newsletters and Lifecycle Email Flows"
description: "Writes email newsletters and campaigns, designs lifecycle email flows, and sets segmentation and list-health rules. Use for welcome or win-back work."
license: Apache-2.0
compatibility: "Needs web search to check current bulk-sender rules. Sending needs an email-capable tool and the user's approval. Any OS."
capabilities: messaging-email variety
rules:
  - match((?i)\b(welcome|onboarding|win-?back|drip|nurture|abandon\w*|post-purchase|trial-ending|re-?engagement|lifecycle)\s+emails?\b|\bemail\s+(series|sequence|flow|campaign)s?\b)
  - match((?i)\b(write|draft|produce|deliver|edition|issue)\b.{0,60}\bnewsletters?\b|\bpreheaders?\b|\bsubject\s+lines?\b)
  - match((?i)\b(SPF|DKIM|DMARC)\b)
  - match((?i)\b(deliverability|spam folder|inbox placement|sender score|complaint rate|warm(ing)?[- ]?up)\b)
  - match((?i)\bsegments?\b.{0,40}\bcampaigns?\b|\bcampaigns?\b.{0,40}\bsegments?\b|\bsegment\w*\b.{0,30}\b(email|subscribers?|mailing list)\b)
  - match((?i)\b(email|newsletter)\s+(open|click)\s+rates?\b|\bwhy\s+(are\s+)?(my\s+)?(opens|clicks)\b.{0,20}\bdown\b)
  - semantic(design email flows and write newsletters for subscribers, 0.70)
  - semantic(write a welcome email series for new signups)
  - semantic(why are my newsletter opens down and how do I fix list health)
  - semantic(design a post-purchase email flow and a sunset policy for inactive subscribers, 0.70)
---

## Overview

Use this skill to design lifecycle flows (welcome, onboarding, win-back, post-purchase), write campaigns and newsletters, segment a list, and guard deliverability and trust. The outcome is a flow file or a ready-to-send draft that earns clicks and replies, on a sending foundation that keeps it out of spam. Subscriber attention is borrowed, not owned: every email earns its open, and the unsubscribe link is a feature.

## Mental model

A brilliant campaign on a rotten foundation lands in spam, so the order is always foundation, then flow, then copy. Measure clicks, replies and conversions, never opens.

## Rules

### Workflow

1. Situate: product, audience, list size and source, sending platform, and what success means in revenue or action terms. Recall the brand voice and program history from memory.
2. Check the foundation before any campaign: SPF, DKIM and DMARC in place, list consented and recent, current complaint and bounce rates. When the foundation is the problem, fix it first and say so.
3. Design the flow or campaign: trigger, audience segment, sequence timing, and the single job of each email. One email, one job, one primary call to action.
4. Write: subject and preheader as a unit, body in the brand's voice, plain-text-first structure. Draft everything for approval; never send autonomously.
5. Test with the `marketing-experiments` skill: one variable, a sample size per arm from its table, and a decision rule declared in advance. A list too small for the table ships its best guess and tests the next send.
6. Measure honestly: click rate, reply rate, conversions, unsubscribe and complaint rates. Report what underperformed as plainly as what worked, and memorize the learnings per audience.

### Deliverability: the non-negotiables

- Bulk-sender rules (check the providers' pages with web search before advising): Gmail, Yahoo and Microsoft Outlook.com (since May 2025, 5,000+ messages a day) require SPF, DKIM and DMARC (at least p=none, aligned with the From domain). Google says it has been ramping up enforcement on non-compliant traffic since November 2025, with temporary or permanent rejection possible. Outlook.com has routed non-compliant high-volume mail to Junk since 2025-05-05 and will reject it later, on a date Microsoft has yet to announce (as of 2026-11, Microsoft Tech Community post "Strengthening email ecosystem: Outlook's new requirements for high-volume senders"). Rejected mail carries error 550 5.7.515.
- Marketing mail needs one-click unsubscribe (RFC 8058 List-Unsubscribe-Post). Yahoo requires unsubscribes honored within 2 days and Google recommends within 48 hours.
- Keep the spam rate in Google Postmaster Tools under 0.1% and never reach 0.3%.
- The `outreach-deliverability` skill holds the sending-infrastructure detail.
- BIMI (brand logo in the inbox) needs DMARC at quarantine or reject plus a VMC or CMC certificate. It is a trust signal, not a deliverability fix.
- Opens are a broken metric since Apple Mail Privacy Protection (2021) inflates them. Decide on clicks, replies and conversions.
- List hygiene: remove hard bounces immediately. Sunset the disengaged: no click in about 90 to 180 days, then one win-back series, then suppress. Sending to the dead hurts delivery to the living.
- Never buy, scrape or import unconsented lists. It hurts deliverability and a bought list is not consent. The FTC's CAN-SPAM guide does not address purchased lists; it treats harvesting addresses as an aggravated violation and still requires opt-out handling (FTC CAN-SPAM compliance guide, Aug 2023, edited Jan 2024). Apply the `outreach-compliance` skill for consent rules by region. Canada's CASL requires consent, express or implied, before a commercial electronic message is sent (CRTC FAQ, crtc.gc.ca/eng/com500/faq500.htm, as of 2026-11). That FAQ has no question on purchased lists, so look up the CRTC or Office of the Privacy Commissioner guidance on whether a seller's consent covers a buyer of the list before advising. Other regions differ; flag legal specifics for legal review.
- Warm up new domains and IPs gradually. Volume spikes look like spam because they usually are.

### Subject lines and preheaders

Keep subject lines under about 50 characters for mobile truncation. The preheader continues the thought and is never "View in browser". Specific beats clever ("Your March invoice is ready" beats "Big news inside"). Curiosity works only when the email pays it off; clickbait trains people to stop opening. No FROM-name games: people open senders they recognize.

### Flow design (the money is in the automation)

- Welcome series: 3 to 5 emails. Email 1 sends immediately (highest open of the relationship): deliver the promised value and set expectations. Then story and value, best content, soft offer.
- Cadence: consistency beats frequency. Keep whatever rhythm you promise. Increase volume only behind engagement.
- Win-back: 2 to 3 emails with honest framing ("still want these?"), then actually suppress. A shrinking engaged list beats a large dead one.
- Every flow has an exit condition: purchased leaves the nurture; replied hands over to a human.
- Segmentation: start with RFM (recency, frequency, monetary value) or its software equivalent. Score each of the three on 1 to 5 and send the top and bottom groups different flows. Without purchase data, segment by lifecycle stage (trial, new customer, active, lapsing) and by the action taken last.
- Onboarding (trial or new account): trigger on the activation event, not the signup date, and stop the sequence when the user reaches the activation milestone. Send an email on day 0, then at most one every 2 to 3 days until activation or day 14 (a starting default, not a platform rule), each pointing to one next step.
- Cart or checkout abandonment: first email 1 hour after abandonment, second at about 24 hours, optional third at 72 hours with an incentive only if margin allows; exit on purchase. These timings are starting defaults, not platform rules.
- Trial-ending: emails at 3 days and 1 day before the end (starting defaults, not platform rules), stating the exact date and price charged. State renewal and cancellation terms plainly, because auto-renewal laws apply to trials that convert to paid.
- Post-purchase: order confirmation and delivery notices are transactional (sent to everyone, no promotion beyond a light mention). The review request, cross-sell and replenishment emails are marketing and honor unsubscribes. Keep the two on separate streams or sending domains.

### Email craft

One job per email and one primary call to action (repeated is fine, competing is not). Write to one reader, not "you all". Front-load the point: most people read the first two lines in preview. Buttons say the outcome ("Get the template"), not "Click here". Heavy-image emails fail dark mode, screen readers and image-blocking clients, so text carries the message and images decorate. Always set a real reply-to: replies are both signal and a deliverability boost.

### Benchmarks (directional, vary by list and vertical)

Click rate of about 2 to 4% is healthy for broadcasts. Unsubscribes stay under about 0.5% per send. Complaints stay under 0.1% (comfortable) with 0.3% as the hard ceiling. A high-open, low-click email had a good subject and a weak body. Diagnose per funnel stage: delivery, open, click, convert.

### Guards

- Never send without explicit approval of the exact draft and segment. Never import or mail an unconsented list.
- Don't hide the unsubscribe or add friction to it. Fast exits protect the sender score of everyone who stays.
- Keep cold outbound and consented marketing lists strictly separate. Blending them poisons both.
- Cold outreach to people who never opted in is a different craft and is not covered here; the `outreach-cold-copy` skill covers it.

## Output format

- Flows as `flow-<name>.md`: trigger, segment, exit conditions, then each email (timing, subject and preheader, body, call to action).
- Campaigns as ready-to-send drafts in fenced blocks headed by segment and send time.
- Program reviews as: foundation check, funnel numbers per stage, the one bottleneck, fixes ranked by effort and impact.

## Examples

- "Write a newsletter or campaign": voice check from memory, then draft subject, preheader and body with one call to action.
- "Set up a welcome flow": the 3 to 5 email sequence with timing and exit conditions.
- "Why are opens or clicks down?": diagnose in order: deliverability foundation, list health, subject, body, offer. Evidence before prescription.
- "Grow the list": consented-capture tactics (lead magnets, embedded forms, referral loops), never purchased lists.
- Ambiguous request: ask one question, usually the audience and the goal of this send, then proceed.

## Checklist

- [ ] Authentication, list consent and complaint rates checked before any campaign copy.
- [ ] Each email has one job and one primary call to action.
- [ ] Every flow has an exit condition.
- [ ] Success measured on clicks, replies and conversions, not opens.
- [ ] Unsubscribe is visible and one-click.
- [ ] Drafts are marked for approval; nothing was sent.

## Composition / References

- `marketing-experiments` skill: sample sizes and decision rules for subject-line and send tests.
- `outreach-deliverability` skill: sending infrastructure, warm-up and volume caps.
- `outreach-compliance` skill: consent and opt-out rules by region.

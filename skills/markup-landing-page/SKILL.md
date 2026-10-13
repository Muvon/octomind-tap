---
name: markup-landing-page
title: "Landing Page Craft: UI, Conversion, and System Patterns"
description: "Production playbook for building modern lightweight landing pages that sell. Covers automatic dark/light theming via CSS custom properties, system-font Apple-style typography, opinionated section anatomy (hero, features, comparison, pricing, FAQ, footer CTA), conversion-focused copy hierarchy, SEO/OG/JSON-LD baseline, and the structural patterns that move visitors to purchase. Activate whenever drafting, designing, or implementing a marketing or product landing page."
license: Apache-2.0
compatibility: "Stack-agnostic — examples use SvelteKit + plain CSS but rules apply to any HTML/CSS framework."
domains: developer
rules:
  - content(landing page)
  - content(landing-page)
  - content(marketing site)
  - content(product page)
  - match(\blanding\s+page\b)
  - match(\bbuild.*landing\b)
  - match(\bdesign.*landing\b)
  - match(\bproduct\s+page\b)
  - match(\bmarketing\s+site\b)
  - match(\bhero\s+section\b)
  - match(\bpricing\s+page\b)
---

## Overview

A landing page has one job: turn a stranger into a buyer or trial user; everything else is decoration. This skill covers a token-level design system with automatic dark/light mode, a section order that walks visitors to the buy decision, copy rules against AI-generic language, and the SEO/structured-data baseline.

Pair with `content-voice`, which owns how the words sound; this skill owns structure, design system and conversion mechanics.

## Tech Stack Baseline

Use the lightest stack: heavy frameworks slow time-to-interactive, hurt SEO and add maintenance to what should be ~80% prerendered HTML.

Recommended: SvelteKit + adapter-static (or Astro) for prerendered HTML (zero JS on most pages, full SEO, instant LCP); plain CSS custom properties + `prefers-color-scheme` for free theming; system font stack `system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif` (zero font load, native feel); TypeScript in `<script>`; Vite; Cloudflare Pages or Vercel (static + edge functions).

Avoid unless needed: React + Next.js for a marketing site (hydration cost); Tailwind for a single-domain landing (class soup, scattered tokens); GSAP or Framer Motion for fade-ins (CSS does it in 4 lines); web fonts (system fonts beat 90% of imports on Apple devices); Radix, shadcn and other component libraries (landing pages need brand-specific UI).

## Design System (Single Source of Truth)

All tokens live in one CSS file as `:root` custom properties read via `var(--token)`; hardcoded colors, spacing or radii in components are a smell.

### Color tokens

```css
:root {
  /* Neutrals — Apple-style cold grays */
  --gray-50: #fbfbfd;
  --gray-100: #f5f5f7;
  --gray-200: #e8e8ed;
  --gray-300: #d2d2d7;
  --gray-400: #aeaeb2;
  --gray-500: #86868b;
  --gray-600: #6e6e73;
  --gray-700: #48484a;
  --gray-800: #3a3a3c;
  --gray-900: #1d1d1f;

  /* Brand accent — ONE primary, use shades */
  --accent-50:  #eef2ff;
  --accent-100: #dbe4ff;
  --accent-200: #bfcfff;
  --accent-400: #6d8aff;
  --accent-500: #4a6cf7;  /* primary — buttons, links */
  --accent-600: #3451d1;  /* hover */

  /* Semantic — what components reference */
  --bg: var(--white);
  --bg-muted: var(--gray-100);
  --card-bg: var(--white);
  --text-primary: var(--gray-900);
  --text-secondary: var(--gray-600);
  --text-muted: var(--gray-500);
  --border: var(--gray-200);
  --border-light: var(--gray-100);
  --on-accent: #ffffff;  /* does NOT invert */
  --nav-bg: rgba(255, 255, 255, 0.72);

  --green-500: #30d158;  /* privacy/security trust signals */
}
```

### Typography, spacing (8px base), effects

```css
:root {
  --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
               Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'SF Mono', SFMono-Regular, ui-monospace, 'Cascadia Code', Menlo, monospace;

  --text-xs: 0.75rem;  --text-sm: 0.875rem;  --text-base: 1rem;  --text-lg: 1.125rem;
  --text-xl: 1.25rem;  --text-2xl: 1.5rem;    --text-3xl: 2rem;   --text-4xl: 2.5rem;

  --space-1: 0.25rem;  --space-2: 0.5rem;  --space-3: 0.75rem;  --space-4: 1rem;
  --space-5: 1.25rem;  --space-6: 1.5rem;  --space-8: 2rem;     --space-10: 2.5rem;
  --space-12: 3rem;    --space-16: 4rem;   --space-20: 5rem;    --space-24: 6rem;

  --radius-sm: 0.5rem;  --radius-md: 0.75rem;  --radius-lg: 1rem;  --radius-full: 9999px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.08);
  --transition: 0.2s ease;
  --nav-height: 56px;
  --max-width: 1100px;
}
```

## Automatic Dark/Light Mode

Non-negotiable. Implement once at the token level — components shouldn't know which mode they're in.

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #000000;
    --bg-muted: #0a0a0a;
    --card-bg: #111113;
    --text-primary: #f5f5f7;
    --text-secondary: #a1a1a6;
    --text-muted: #6e6e73;
    --border: #2a2a2e;
    --border-light: #1c1c1f;
    --nav-bg: rgba(0, 0, 0, 0.72);
    --accent-500: #6d8aff;  /* brighter for contrast */
    --shadow-md: 0 4px 12px rgba(0,0,0,0.4);  /* heavier on dark */
    --shadow-lg: 0 12px 32px rgba(0,0,0,0.6);
  }
}
```

Rules:
- Never hardcode colors in components.
- `--on-accent` does NOT invert — text on a colored button stays white in both modes.
- Test both modes; dark reveals contrast bugs. Component-specific values (e.g. a `rgba(0,0,0,0.4)` overlay) need dark overrides inside the component.
- Match the OS chrome:
  ```html
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)" />
  <meta name="color-scheme" content="light dark" />
  ```
- Shorter alternative for current browsers: `:root { color-scheme: light dark; --bg: light-dark(#fff, #000); }` (`light-dark()` is Baseline 2024).

## Section Anatomy (Top to Bottom)

The page is a sales conversation; each section answers the next objection.

1. Nav — fixed, ~56px; logo + 1–3 links + one accent CTA pill; `backdrop-filter: blur(20px)` on a translucent background; border/shadow appears on scroll. Mobile: smaller paddings, no hamburger unless > 5 items.

2. Hero — conversion is decided here.
   - Badge above headline: tiny, uppercase, muted context tag ("macOS 14+ · Apple Silicon").
   - Headline: `clamp(2.5rem, 6vw, 3.5rem)`, weight 700, letter-spacing -0.035em, line-height 1.08, `text-wrap: balance` (Baseline 2024) instead of `<br>`.
   - Subtitle: one sentence, ≤ ~30 words, `--text-lg`, `--text-secondary`, naming 2–3 features.
   - Primary CTA: accent pill, `--text-lg`, generous padding; trust line under it with trial limits ("100 free dictations · No credit card"), `--text-sm` muted.
   - Optional `brew install ...` monospace block; system requirements last, muted.
   - `min-height: calc(100svh - var(--nav-height))` (`svh` avoids the mobile URL-bar jump of `100vh`); subtle radial gradient to accent-50 at top.

3. How It Works — three cards numbered 01/02/03, headline + 1–2 sentences; card-bg, 1px border, radius-lg, padding-8; hover `translateY(-2px)` + shadow-md.

4. Modes / use cases — if the product has 3+ distinct jobs (dictation + meetings + notes), introduce them early as cards.

5. Feature deep-dives — one section per major feature, text beside visual, alternating sides: heading (`--text-4xl`, 700, letter-spacing -0.03em), 2–4 sentences, 3 accent-dot specifics, a real screenshot, demo card or stylized illustration.

6. Privacy / trust — any privacy/local/data angle gets its own section; people scroll for trust.

7. Pricing — two+ cards: yours (highlighted, "Best Value" badge) vs the alternative (cloud subscription): price (`--text-4xl`), period ("once" vs "/month"), year-2 cost line (the kicker), checkmarks (you) vs X marks (them).

8. Competitor table — feature-by-feature vs named competitors, your column on `--accent-50`, strikethrough promo prices, cost-after-2-years row in a heavier border. Often the highest-converting section.

9. Stats (if applicable) — one big number ("150x realtime") with a simple you-vs-them bar chart.

10. Compatibility — pill grid of supported apps/integrations.

11. About / made by — "Built by [team] in [city]. Selectively shipped." plus company link.

12. FAQ — 8–12 questions in `<details name="faq">`: zero JS, accessible, exclusive accordion via shared `name` (Baseline 2024). Animating open state (`::details-content` + `interpolate-size`) isn't cross-browser in 2026 — enhancement only. Cover: what it is (headline echoed differently), privacy/data, platform/requirements, free trial, pricing, how each major feature works, objections ("What if X doesn't work?"), refund/cancellation.

13. Footer CTA — same CTA and trust line under a different, summarizing headline ("Local. Fast. Yours.").

14. Footer — brand + tagline left; 3–4 columns max right (Product, Company, Legal, Connect); copyright at bottom.

## CTA Hierarchy

One primary action, zero or one secondary; equal-weight CTAs = no CTA.

1. Primary — accent-filled pill, white text, for the conversion goal (Download, Buy, Sign up); same label and color in Nav, Hero and Footer CTA.
2. Secondary — outline pill (accent border + text) for alternate paths (Learn more, Buy after free trial), different label.
3. Tertiary — text links, underline on hover.

Rules:
- Never two filled accent CTAs in the same viewport.
- No red, orange or yellow primary CTAs unless brand-justified — they read as warnings.
- Pill radius (9999px) is the default for software CTAs — a brand choice, not a proven conversion lever; test it if it matters.

## Conversion Patterns

- Show the price. Hidden price reads as "expensive" or "talk to sales"; complex pricing still shows a starting number.
- Compare against the alternative (subscription vs one-time, tool vs status quo, you vs named competitors) with visible math: "$49 vs $200 over 2 years".
- Specific over abstract: "150x realtime" beats "blazingly fast", "$24.50 with VEXT50" beats "Save big". Every claim should be checkable.
- Layer trust throughout: requirements badge in hero, "No credit card" in trial copy, privacy section mid-page, real screenshots, company name + jurisdiction in footer.
- Explicit trial limits: "100 dictations, 50 notes, 10 meeting recordings — no credit card" outperforms "Try free".
- Real urgency only (pulsing dot pill, deadline date, strikethrough price). Fake countdowns or deadlines kill trust, and regulators treat fake scarcity as a deceptive dark pattern.

## Copy Rules (on top of `content-voice`)

- Headlines: outcome not feature, two lines max, verb-driven ("Capture a thought before it's gone." > "Voice notes feature."); no "revolutionary", "next-generation", "ultimate", "powerful" — use words a customer would tell a friend.
- Subtitles: one or two sentences, 2–3 named features, ending on a trust signal ("No cloud. No subscription.") or differentiator.
- Section headings: 1–4 words ending with a period for calm ("How it works." "What you earn."); no "Discover", "Unlock", "Experience", "Explore".
- Body: contractions, dramatic rhythm, concrete examples, one idea per paragraph, bullets only for 3+ parallel items.
- CTAs: 1–3 words, verb + outcome; never "Click here", "Learn more", "Submit". Match what happens next ("Buy" to checkout, "Download Free" to trial, "Start" to signup).

## SEO + Social Baseline

Every page sets:

```html
<title>Page Name — Brand</title>
<meta name="description" content="..." />  <!-- under 160 chars, unique per page -->
<link rel="canonical" href="https://domain.com/path" />

<meta property="og:type" content="website" />  <!-- "article" for blog posts -->
<meta property="og:url" content="..." />
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:image" content="https://domain.com/og/page.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:site_name" content="Brand" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="..." />
<meta name="twitter:description" content="..." />
<meta name="twitter:image" content="..." />
<meta name="twitter:site" content="@handle" />
```

OG images: build-time 1200×630 SVG → PNG per page (`@resvg/resvg-js` or similar); PNG only, since Facebook, Slack and LinkedIn don't render SVG. Layout: dark background, accent gradient bar top/bottom, logo top-left, headline center-left, domain footer; titles auto-wrap with dynamic sizing (80 → 64 → 52px). Gitignore the generated files.

JSON-LD for a software product:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "...",
  "description": "...",
  "url": "...",
  "applicationCategory": "UtilitiesApplication",
  "operatingSystem": "macOS 14+",
  "offers": {
    "@type": "Offer",
    "price": 49,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "publisher": { "@type": "Organization", "name": "...", "url": "..." }
}
```

Add `Organization`. `FAQPage` is harmless, but since 2023 Google shows FAQ rich results only for authoritative government and health sites. The software-app rich result needs a real `aggregateRating` or `review` (otherwise no stars, though other parsers still benefit). Never invent ratings or review counts — it violates Google's structured-data policy and the US FTC fake-review rule.

Canonical and sitemap: `<link rel="canonical">` on every page; static `sitemap.xml` of all routes with accurate `lastmod` (Google ignores `priority` and `changefreq`); `robots.txt` allowing everything except `/api/` and `/_`.

## Error Pages (404, 5xx)

One error component (`+error.svelte`, `error.tsx` or equivalent) branching on `status`: 404 a light on-brand line ("Page not found."), 5xx an honest "Something broke on our end", others the real message in a plain frame.

- Monospace status pill, friendly headline, one human sentence (no stack trace), "Back home" primary CTA + one secondary path, 3–5 common links.
- Same nav, footer, tokens and dark mode; `<title>404 — Brand</title>`; `<meta name="robots" content="noindex">`; no third-party calls, so it renders when APIs are down.
- Static sites emit `404.html` from the same component (SvelteKit: `adapter({ fallback: '404.html' })`); Cloudflare Pages, Netlify, Vercel and S3 serve it for unknown routes.
- Don't: timed auto-redirects, a search box with no backend, stock "lost robot" art, blaming the user ("You typed the wrong URL").

## Animation (Restrained)

Default to none; add only when it serves communication.

```js
const observer = new IntersectionObserver(
  (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add('visible')),
  { threshold: 0.1 }
);
document.querySelectorAll('.animate-on-scroll').forEach((el) => observer.observe(el));
```

```css
.animate-on-scroll { opacity: 0; transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease; }
.animate-on-scroll.visible { opacity: 1; transform: translateY(0); }
@media (prefers-reduced-motion: reduce) {
  .animate-on-scroll { opacity: 1; transform: none; transition: none; }
}
@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.4); } }
.dot { animation: pulse 1.6s ease-in-out infinite; }  /* live indicators: recording, launch promo */
```

Rules:
- Use sparingly — every section animating is annoying.
- Never animate above-the-fold content, and never start the LCP element at `opacity: 0`.
- Same-document View Transitions are Baseline since Oct 2025, fine for state changes. Scroll-driven animations (`animation-timeline`) lack stable Firefox in 2026: only inside `@supports (animation-timeline: view())`, IntersectionObserver as default.
- Honour `prefers-reduced-motion: reduce`.
- Hover: buttons `translateY(-1px)` + accent shift; cards `translateY(-2px)` + shadow upgrade; links color shift only, no underline-fade gimmicks.

## Responsive Rules

Two breakpoints cover ~95% of cases: `@media (max-width: 768px)` (tablet) and `@media (max-width: 640px)` (mobile).

- 3-column grids → 1 column on mobile, max-width 480px centered; 2-column feature blocks stack on tablet, both full-width.
- Components living in different column widths (pricing cards, feature blocks) can use container queries (`@container`, Baseline since 2023).
- Hero `clamp()` handles headline sizing — no manual mobile override.
- Tap targets ≥ 44×44px on mobile; WCAG 2.2 AA's floor is 24×24px with spacing.
- Tables: `overflow-x: auto` wrapper, `min-width` on the table.

## Performance Targets (Core Web Vitals, 2026)

Google judges Core Web Vitals on field data at p75, mobile and desktop separately: LCP ≤ 2.5s, INP ≤ 200ms (replaced FID in 2024), CLS ≤ 0.1. Lab Lighthouse is a smoke test — the verdict is CrUX / Search Console or your RUM.

- LCP: aim ≤ 1.5s — prerendered HTML, system fonts, LCP image with `fetchpriority="high"`, never `loading="lazy"` on it.
- INP: under ~50KB gzipped JS, no hydration of static sections, defer or drop third-party tags (chat widgets, heatmaps, tag managers), break up long tasks.
- CLS: explicit width/height (or `aspect-ratio`) on images and embeds; reserve space for late-injected content.
- Images: AVIF or WebP via `<picture>` with `srcset`/`sizes`, SVG for illustrations, PNG only for pixel-exact screenshots.
- Inline critical above-the-fold CSS if your stack supports it.

## Accessibility (WCAG 2.2 AA)

WCAG 2.2 AA is the bar; the EU European Accessibility Act has effectively required it for consumer e-commerce and services since 28 June 2025.

- Contrast: 4.5:1 body text, 3:1 large text and UI boundaries, in both themes.
- Focus: visible ring on every interactive element, never hidden behind the sticky nav (2.4.11) — set `scroll-padding-top: var(--nav-height)` on `html`.
- Semantics: one `<h1>`, ordered headings, `<header>/<nav>/<main>/<footer>` landmarks, real `<button>` and `<a>`.
- Motion: honour `prefers-reduced-motion`; no auto-moving content over 5s without a pause control.
- Media: captions on video with speech, meaningful `alt`, decorative images `alt=""`.

## Forms (signup, waitlist, checkout)

Every field costs conversions; ask only what the next step needs — usually just email.

- Visible `<label>` per field; placeholder is not a label.
- Correct `type`, `autocomplete` (`email`, `name`, `tel`, `one-time-code`) and `inputmode`, so autofill and the right mobile keyboard work.
- Single column, primary button right under the last field, label repeating the outcome ("Get the download link").
- Validate on blur, not per keystroke; error next to the field, linked via `aria-describedby`; keep the user's input.
- Don't block paste, don't ask for the same data twice (3.3.7), no puzzle CAPTCHAs (3.3.8) — use an invisible bot check or honeypot.
- Say what happens after submit and how often you'll email.

## Anti-Patterns (Don't)

- Autoplay video with sound or a heavy hero video (a muted `playsinline` loop only with poster, small file and pause control); full-bleed background videos dominate LCP and bandwidth
- Price gated behind "Contact us" unless you genuinely sell enterprise
- Newsletter modals that interrupt reading
- Stock photos of laptops/teams/handshakes; "Award winning" or trust-badge soup in the hero; "Trusted by X companies" without real logos and numbers
- CTA buried below 4 sections
- AI-sounding copy (see `content-voice`)
- Scroll-jacking the wheel event; hiding nav on scroll (visitors lose orientation)
- Non-essential analytics cookies — cookieless analytics avoids the EU consent banner; otherwise consent comes first

## When to Break the Rules

Patterns are calibrated for $20–200 indie/SaaS products for individuals or small teams; add depth and proof as price rises.

- Premium (>$500): case studies, named customers, ROI calculator; one page may not be enough.
- Enterprise B2B: gate pricing behind a demo if the sales motion needs qualification.
- High-emotion products (luxury, lifestyle): typography and imagery outweigh spec lists.
- Developer tools: code samples in hero, GitHub stars badge, technical spec sheet upfront.

## Examples

Hero:
- ❌ "Revolutionary AI-Powered Voice Recognition Software for Modern Professionals"
- ✅ "Talk to your computer, don't type." Subtitle: Voice to text with smart cleanup, live translation, meeting summaries. No cloud. No subscription. Your voice never leaves your Mac.

Pricing:
- ❌ "Get a quote" or "Starting at $—"
- ✅ Vext: $49 once · $0 in year 2 vs cloud voice tools: $10–30 /month · $120–360/year

CTA:
- ❌ "Click here", "Submit", "Get started"
- ✅ "Download Free" (verb + outcome), "Buy for $24.50" (verb + price clarity), "Apply to join" (verb + commitment level)

Comparison row:
- ❌ "Cloud-dependent · Account required"
- ✅ "Audio sent to third-party servers · Requires monthly subscription · Account + login required"

## Pre-Ship Checklist

- [ ] Hero passes the 3-second test: what it is and what to do
- [ ] Primary CTA visible without scrolling on a 13" laptop
- [ ] Dark mode tested — no contrast bugs
- [ ] Mobile tested at 375px and 414px
- [ ] All copy passes `content-voice` rules (no dead vocabulary)
- [ ] New-tab links use `target="_blank"` (`noopener` is now default; `rel="noreferrer"` only to hide the referrer)
- [ ] Every image has descriptive `alt`
- [ ] OG image renders in https://www.opengraph.xyz preview
- [ ] Lighthouse lab: Performance ≥ 95, SEO 100, Accessibility 100; field data (when available) passes LCP, INP and CLS at p75
- [ ] Keyboard-only pass: every control reachable, focus visible and never under the sticky nav; usable at 200% zoom
- [ ] Tested on an actual mobile device (not just DevTools)
- [ ] No console errors in production build
- [ ] Form submissions / CTAs work end-to-end
- [ ] 404 page exists and matches brand
- [ ] Sitemap.xml lists every page
- [ ] Canonical URL set on every page
- [ ] At least one trust signal in hero, one mid-page, one footer

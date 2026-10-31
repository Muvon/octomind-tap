---
name: repo-social-preview
title: "GitHub Social Preview Card in the Repo's Brand"
description: "Designs and renders a custom GitHub social preview (the 1280x640 card shown when a repository link is shared on X, Slack, LinkedIn, Reddit, Hacker News, or Discord) from the repository's own brand: logo, colors, fonts, tagline, install command, and open-source facts discovered in the repo and its website. Renders deterministically with the social-preview CLI, checks it at feed size, and hands over the web-only upload plus a gh check that it took. Use when a repo shows GitHub's generic card, when a visibility audit flags a missing social preview, or when asked for an Open Graph image for a repository."
license: Apache-2.0
compatibility: "Requires: python3 and typst (installed with the social-preview capability); gh, authenticated, for reading the repo and checking the upload. macOS/Linux."
capabilities: shell social-preview image-view
domains: developer
rules:
  - match((?i)social[- ]preview)
  - match((?i)\b(og|open ?graph)[ :-]?(image|card)\b)
  - semantic(make a social preview image for this github repo)
  - semantic(our repo link shows a generic card when shared)
---

## Overview

A repository link shared anywhere unfurls into a card. Without a custom image GitHub generates one from the owner avatar, name, and description, which only works for brands people already know. A project still earning its audience needs the card to say what it is. This skill reads the brand from the repository, writes the card's copy, renders it with the `social-preview` command, checks it at the size people see it, and hands over the upload.

## Mental model

- The card is read in under a second at 400–600 px wide in a feed. It carries a name, one claim, and at most two supporting lines. Everything else is noise at that size.
- The repo already has a brand. Find it and reuse it; never invent colors, a logo, or a tagline the project doesn't use.
- It is an open-source card. It says what the project is and how to get it, not what it costs or how popular it is today.
- `social-preview` lays out a fixed, tested composition: wordmark top-left, badge under it, tagline fitted to two lines, subline, install pane, URL footer, logo on the right, faint grid, accent bars top and bottom. It renders with system fonts ignored and only the fonts it is given, so the same inputs give the same PNG on every machine. Fonts default to Inter and JetBrains Mono from `~/.local/share/octomind/fonts`. `social-preview --help` lists every option.

## Rules

### Read the current state

```bash
gh repo view OWNER/REPO --json name,description,homepageUrl,primaryLanguage,licenseInfo,usesCustomOpenGraphImage,openGraphImageUrl
```

If `usesCustomOpenGraphImage` is true, look at the current image first and ask whether to replace it.

### Discover the brand

Search the repository, and the website's repository when one is checked out or linked from `homepageUrl`; the website is the source of truth when the two disagree.

| Input | Where to look | Flag |
|---|---|---|
| Name | Logo wordmark, README H1, site header; keep the brand's exact casing | `--name`, `--wordmark mono` when the brand's wordmark is monospaced or pixel, else `sans` |
| Logo | A square mark, not the horizontal lockup (the name is already set as text): `assets/`, `.github/`, `docs/`, `static/`, `public/`, the README's top `<img>`. SVG first | `--logo`, plus `--pixelated` for pixel-art PNGs |
| Accent | A brand or design doc (BRANDING, DESIGN, brand guidelines), CSS custom properties (`--primary`, `--brand`, `--accent`), Tailwind theme colors, `<meta name="theme-color">`, the logo's main non-neutral fill, README badge colors | `--accent`, optionally `--accent-2`, `--highlight`, `--pop` from the documented ramp |
| Background | The site's dark surface when it has one; otherwise the near-black default | `--bg`, `--fg` |
| Fonts | TTF or OTF files in the repo or site (`fonts/`, `static/fonts/`) and the family names in `@font-face`. Typst can't read WOFF/WOFF2; fall back to the defaults instead of guessing | `--font`, `--mono`, `--font-path` |
| House style | An existing Open Graph generator or card on the website: match its background, texture, and bar treatment through the color flags | colors only |

Report each value with the file it came from. Where nothing was found, say so and use the default rather than inventing one.

### Write the copy

- Tagline: what it is, for whom, in 60 characters or fewer. Start from the README's hero line or the repo description. A category plus the differentiator beats adjectives ("Two-way sync between Postgres and spreadsheets", not "A blazing-fast, powerful tool").
- If a better-known project already owns the plain category line, lead with what differs instead.
- Subline (optional): up to three short value points joined with " · ", 48 characters or fewer.
- Badge: `Open source · <primary language> · <license>` from `gh repo view`.
- Install (optional): the shortest canonical command from the README (`brew install`, `npm i -g`, `cargo install`, `pipx install`, `go install`), 44 characters or fewer, without `$`. Skip `curl ... | sh` one-liners that don't fit.
- URL: `github.com/OWNER/REPO` for the repository card.
- Leave out star counts, download numbers, versions, benchmark scores, prices, and cloud or paid-plan offers. They go stale or turn an open-source card into an ad. The renderer warns on counts, versions, and percentages.
- Propose the copy and the discovered brand values to the user before rendering when any choice is a judgment call (tagline wording, which logo).

### Render and check

```bash
social-preview -o <out>/social-preview.png --preview <out>/social-preview-preview.png \
  --name "<Name>" --wordmark mono --tagline "<tagline>" --subline "<a · b · c>" \
  --badge "Open source · <Lang> · <License>" --install "<install command>" --url github.com/OWNER/REPO \
  --logo <path/to/mark.svg> --accent "#rrggbb" [--bg ... --fg ... --font ... --font-path ...]
```

- Write outputs outside the repository (a temp or output dir) unless the maintainer asks to keep the card in the repo.
- Resolve every warning: contrast below WCAG AA, text over length, stale numbers. Fix the input; don't ignore a warning without telling the user why.
- The command fails on an unknown font family, a size other than 1280x640, or a file over GitHub's 1 MB limit. Fix the cause; never resize or recompress the PNG afterwards.
- View both PNGs with `read_media_file`. At 480 px the tagline must read and the logo must be recognizable; if not, shorten the tagline or drop the subline. If an image can't be viewed, list the files and tell the user legibility is unverified.

### Upload and verify

Upload has no API. Hand the maintainer these steps with the PNG path:

1. Open `https://github.com/OWNER/REPO/settings`.
2. General, Social preview, Edit, Upload an image, choose the PNG.

Then confirm it took:

```bash
gh repo view OWNER/REPO --json usesCustomOpenGraphImage,openGraphImageUrl
```

`usesCustomOpenGraphImage` must be `true`. Links already posted keep their old card, and X, Slack, and LinkedIn cache unfurls; LinkedIn's Post Inspector forces a refresh. Report the card as uploaded only after the check passes.

## Examples

### Example 1: logo-only card for an unknown project

❌ The mark centered on a gradient with no text. It works for a household name; for everyone else the card says nothing.

✅ Wordmark, "Open source · Rust · MIT" badge, a 40-character tagline, and the mark on the right, in the colors from the site's CSS.

### Example 2: numbers on the card

❌ `--subline "10k stars · v2.3 · 40% faster"`: the renderer warns three times, and all three facts are wrong in a few months.

✅ `--subline "One binary · Any database · No glue code"`: properties that stay true.

### Example 3: invented brand

❌ No brand doc found, so the card gets a purple-to-pink gradient and a generated icon.

✅ The accent comes from the logo SVG's fill, the defaults cover the rest, and the report says "no brand doc; accent taken from assets/logo.svg fill #0969da".

## Checklist

- [ ] Current state read with `gh repo view`; an existing custom card was shown before replacing it.
- [ ] Every brand value traced to a file, or reported as a default.
- [ ] Name on the card in the brand's casing; tagline 60 characters or fewer; no counts, versions, scores, prices, or cloud offers.
- [ ] Rendered with `social-preview` at 1280x640 under 1 MB; every warning resolved or explained.
- [ ] Full card and 480 px preview viewed, or reported as unverified.
- [ ] Upload steps handed over; `usesCustomOpenGraphImage` checked true before reporting done.

## Composition / References

- `markup-landing-page` covers per-page Open Graph images for a website; this skill covers the repository card.
- [GitHub Docs: customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
- [Typst](https://typst.app)

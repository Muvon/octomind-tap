---
name: design-graphics-kit
title: "Logo and Brand Kit: SVG and PNG Assets"
description: "Make logos, social graphics, posters, and a simple brand kit as SVG and PNG files with a usage sheet (sizes, colours, clear space). Use for brand visuals."
license: Apache-2.0
compatibility: "Needs a shell with an SVG renderer (rsvg-convert, magick, or inkscape) for PNG export, an image generator for text-free pictures, and web access for platform size pages."
capabilities: shell webfetch image-gen image-view
domains: designer
rules:
  - match((?i)\b(make|design|create|draw|generate)\b.{0,25}\b(a\s+|my\s+|our\s+)?(logo|brand\s+kit|poster|flyer|social\s+(media\s+)?graphics?|banner|icon\s+set)\b)
  - match((?i)\b(brand\s+kit|logo\s+(design|concepts?|variations?|versions?)|usage\s+sheet)\b)
  - match((?i)\b(svg|png)\b.{0,30}\b(logo|poster|banner|icon)\b)
  - semantic(design a simple brand kit with colours and fonts, 0.72)
  - semantic(make a logo for my project as SVG, 0.72)
  - semantic(create social media graphics and a poster for my event, 0.72)
  - semantic(put together a brand kit with logo sizes and clear space, 0.72)
  - semantic(design a banner image in our brand colours, 0.72)
---

## Overview

This skill delivers finished image files: logos, social graphics, posters and flyers, covers and banners, icon sets of a few glyphs, and a simple brand kit (colours, fonts, logo versions) that a small team can use without a designer in the room. A mark has to work at 16 px and on a poster, in one colour and on a dark background, before it is called done.

The approach is a designer with a terminal: a short concept first, then vector files written by hand (SVG) for anything with shapes or type, and generated images only for text-free pictures. Never ask an image model to spell a word, and say plainly when a file is a draft for a human designer to refine.

It does not cover brand strategy, naming, or voice; video thumbnails; interface design and UX review; presentation decks; trademark clearance; print production and press-ready files; or photography and retouching of real people.

## Mental model

A logo is one idea executed simply. Constraints decide quality: small size, one colour, dark background. Platform sizes change, so they come from the platform's own page, not memory.

## Rules

Method:

1. Intake: brand or project name, what it does, audience, where each graphic appears, existing colours, fonts, or logo, three adjectives, and anything to avoid. Recall earlier brand colours, logo, and style decisions. Read supplied files first.
2. Check current platform sizes: before naming any pixel size for a social network or marketplace, look it up on the platform's own help page and record the page and date.
3. Concepts: three one-line directions that differ in one variable (symbol versus wordmark, geometric versus hand-drawn, one colour versus two). Wait for a pick unless the brief is non-interactive.
4. Build: write SVG by hand for marks, type, layouts, and posters, with text as live `<text>` in a font the user can install, or converted to outlines for the final logo. Use `generate_image` only for text-free backgrounds, textures, or illustrations, with "no text, no letters, no logos" in the prompt.
5. Render and look: export PNG with an installed renderer (check with `command -v rsvg-convert magick inkscape`; if none exists, deliver the SVG and say PNG export is pending). Open each export and look at it: test the mark at 16, 32, and 64 px, on white and on a dark background, and in one colour.
6. Write the usage sheet, then record the approved palette, fonts, and logo direction.

Defaults:

| Decision | Default |
|---|---|
| Logo | One idea, 2 colours at most, readable in one colour; shapes before effects, no gradients or shadows in the master |
| Palette | 1 primary, 1 accent, 2 neutrals; give HEX and RGB; text on background at 4.5:1 or better (3:1 for large text), checked by computing the ratio |
| Type | At most 2 families, both with a licence that allows commercial use; name the licence |
| Clear space | A margin on every side equal to the height of the logo's main symbol element, or half the mark's height when it has no element to measure; write the rule with a diagram |
| Minimum size | State the smallest width at which the logo stays legible, from the 16 / 32 / 64 px test |
| Files | SVG master, PNG at 1x and 2x of each stated size, transparent background unless the use needs a fill |
| Text in images | Set as SVG text or outlines, never drawn by an image model |

Likeness and ownership:

- Don't generate or edit the likeness of a real person without the person's consent and a real photo supplied by the user. Fictional characters stay clearly fictional.
- Don't imitate the style of a living artist by name, and don't copy or approximate an existing brand's mark, colours-plus-shape combination, or trade dress. If the brief names a competitor's logo as the model, take the quality bar, not the shapes.
- Don't depict minors in sexualised, unsafe, or exploitative contexts; keep any figure of a child to neutral, clearly illustrated, non-identifying characters.
- Check the finished mark against the brief's industry for lookalikes with a reverse-image or trademark search link the user can run, and say that a search is not clearance. Never claim a logo is trademark-cleared or unique.
- Generated images carry the provider's terms. Tell the user to read them before commercial use, and don't claim copyright or exclusivity the terms don't give.
- Don't deliver a logo that exists only as a raster. Report anything not rendered or not checked in the final message.

## Examples

- "Make me a logo": run intake, show three directions, then build the full set after the pick.
- A reference logo or style is named: take the quality bar and the mood, never the shapes, and say so in one line.
- A real person's photo is supplied for a poster: confirm the person agreed to its use before editing.
- "Make it pop": raise contrast, simplify, enlarge the focal element; don't add effects.
- A non-interactive brief: pick the strongest direction, deliver the full set, and list the assumptions at the top of `concepts.md`.

## Output format

Files go under `./design-out/<slug>/`: `concepts.md` (three directions and the pick), `logo/` (`logo.svg`, `logo-mono.svg`, `logo-reversed.svg`, PNG exports), `social/`, `poster/`, and `usage-sheet.md`.

`usage-sheet.md` holds: logo versions and when to use each; the clear-space rule and minimum size; a palette table (name, HEX, RGB, use, contrast pair and ratio); fonts with licence; a sizes table per platform with source page and date; a do and don't list (stretch, recolour, busy backgrounds); and open items for a human designer.

## Checklist

- [ ] Three directions shown and one picked, or assumptions listed
- [ ] Every mark tested at 16, 32, and 64 px, in one colour, and on dark
- [ ] No text drawn by an image model; the logo exists as SVG
- [ ] Platform sizes cite the platform page and the date
- [ ] Contrast ratios computed for every text and background pair
- [ ] Usage sheet written with sizes, colours, and clear space
- [ ] Anything not rendered or not checked is reported

## Composition / References

- The `design-ux-review` skill covers interface review; this skill covers visual brand assets only.

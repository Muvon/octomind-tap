---
name: document-export
title: "Markdown to Word and PDF: Submission-Ready Documents"
description: "Markdown to Word and PDF that meets submission rules: write the document once in Markdown, export DOCX with a generated reference document (exact font, size, heading style, line spacing, page size, margins) and PDF through pandoc's Typst engine with the same settings, then check the PDF's page count against the limit, embedded fonts, and the text layer before sending. Covers RFP and proposal formatting instructions, cover letters, reports, page breaks, tables of contents, and using a client's Word template. Use whenever a deliverable must leave as a .docx or .pdf rather than Markdown."
license: Apache-2.0
compatibility: "Requires: python3, pandoc 3.1.2+, typst, and poppler-utils (pdftotext, pdfinfo, pdffonts). Optional: LibreOffice for DOCX page counts. macOS/Linux."
capabilities: shell documents
domains: sales coach
rules:
  - session(proposals)
  - session(resume)
  - content(docx)
  - content(pdf)
  - match(\b(word|docx|pdf)\s+(file|document|version|format)\b)
  - match(\b(page\s+limit|font\s+size|margins?)\b)
  - semantic(export this proposal to word and pdf)
  - semantic(the rfp requires 12 point times new roman and one inch margins)
---

## Overview

Buyers, recruiters, and portals receive files, not Markdown. This skill keeps one Markdown source and produces the Word and PDF versions from it with the formatting the recipient demands, then verifies the PDF the way a reviewer or a parser will see it. The `doc-export` command does the conversion and the checks; no hand-built HTML-to-PDF scripts, no "copy this into Word yourself".

## Mental model

- Source of truth: `<name>.md`. Edits happen there; both files are regenerated from it.
- Word output takes its look from a reference document. `doc-export` builds one from flags (font, size, heading color, line spacing, paper, margins) or uses the client's template with `--reference`.
- PDF output goes through Typst with the same settings: real text, embedded fonts, consistent spacing.
- Checking is part of exporting: page count against the limit, every font embedded, a text layer that reads in order.

`doc-export` is installed on PATH with the `documents` capability (the same file is the bundled `scripts/doc_export.py`, listed under Skill Resources). `doc-export <docx|pdf|reference|check> --help` lists options.

## Rules

### Pipeline

1. Read the formatting instructions first (RFP Section L or the submission guide, a portal's upload rules, a template the client sent). Write them down: font, size, margins, line spacing, paper, page limit, file type, file naming, what counts toward the limit.
2. Write the Markdown with real headings (`#`, `##`) so Word gets heading styles and a navigation pane, tables as pipe tables, and footnotes as `[^1]`.
3. Export both formats with identical settings:

```bash
doc-export docx proposal.md -o "Acme_RFP-2026-117_Vol1_Technical.docx" --font "Times New Roman" --size 12 --margins 1in --paper us-letter
doc-export pdf  proposal.md -o "Acme_RFP-2026-117_Vol1_Technical.pdf"  --font "Times New Roman" --size 12 --margins 1in --paper us-letter --max-pages 20
```

4. Read the `pdf` report: page count, page size, words in the text layer. Fix and re-export until it is clean.
5. When the deliverable is Word only, still export the PDF once to count pages; Word may paginate a little differently, so leave a margin of half a page under a hard limit.

### Formatting decisions

| Situation | Setting |
|---|---|
| RFP specifies font, size, margins | Use exactly those; `--line-spacing 1.0` unless spacing is specified |
| No instructions, business document | `--font Calibri --size 11 --line-spacing 1.15 --margins 1in` |
| Formal letter, legal-style document | `--font "Times New Roman" --size 12 --margins 1in` |
| Outside the US and Canada | `--paper a4` |
| Client sent a Word template | `doc-export docx in.md -o out.docx --reference their-template.docx` |
| House style reused across documents | `doc-export reference -o house.docx --font ... --heading-color 0B3D91`, then `--reference house.docx` |
| Long proposal or report | `--toc`, and `--numbered` when the instructions number sections |

Check the font exists before relying on it: `typst fonts` for PDF. When Calibri, Cambria, Arial, Times New Roman, or Courier New is missing, the PDF uses its metric-compatible clone (Carlito, Caladea, Liberation), so line breaks and page counts hold; any other missing font gets a warning. Word substitutes silently on the reader's machine when a font is missing, so prefer Calibri, Arial, Times New Roman, or Georgia for files that leave the organization.

### Markdown that converts well

- Page break: a raw block per format, e.g. `` ```{=openxml} `` with `<w:p><w:r><w:br w:type="page"/></w:r></w:p>` for Word and `` ```{=typst} `` with `#pagebreak()` for PDF.
- Images: `![Caption](figures/arch.png){width=80%}`; pass `--resource-path` when images live elsewhere.
- Title block: YAML front matter with `title`, `subtitle`, `author`, `date`.
- Avoid raw HTML; it is dropped in both formats.

### Verification

`doc-export check file.pdf --max-pages N --text 30` reports:
- pages over the limit,
- fonts not embedded (some portals reject them),
- little or no text (an image-only PDF: parsers and screen readers read nothing),
- private-use glyphs (icon fonts that turn into junk characters in parsers),
- the first lines of the text layer in reading order (contact details, headings, and bullets should come out in the order a reader expects).

## Examples

### Example 1: page limit

❌ Draft exported once, sent: 21 pages against a 20-page limit; the evaluator stops reading at page 20, or the proposal is non-compliant.

✅ `doc-export pdf ... --max-pages 20` flags 21 pages; the agent tightens the weakest section and re-exports at 19 pages.

### Example 2: font rules

❌ "Converted to Word" with pandoc defaults: Aptos 12, blue headings, no page setup, against an RFP requiring Times New Roman 12 with 1-inch margins.

✅ `doc-export docx ... --font "Times New Roman" --size 12 --margins 1in` sets theme fonts, sizes, and margins in the file itself.

## Checklist

- [ ] Formatting instructions captured before writing (font, size, spacing, margins, paper, page limit, naming).
- [ ] One Markdown source; DOCX and PDF both regenerated from it with identical settings.
- [ ] PDF report clean: within the page limit, fonts embedded, text layer present and in order.
- [ ] Files named as the instructions require.
- [ ] Both files and the Markdown source saved in the working directory.

## Composition / References

- [pandoc manual](https://pandoc.org/MANUAL.html)
- [pandoc: --reference-doc](https://pandoc.org/MANUAL.html#option--reference-doc)
- [Typst documentation](https://typst.app/docs/)

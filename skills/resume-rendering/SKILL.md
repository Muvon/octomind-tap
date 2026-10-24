---
name: resume-rendering
title: "Resume PDF Builder: ATS-Friendly Resumes with RenderCV"
description: "Build the resume file, not just the text: the tailored resume as RenderCV YAML, typeset to a clean single-column PDF with an ATS-safe theme (plain-text links, no icon fonts, no header note), paper size by market, a page-count check, a text-layer check that shows what an applicant tracking system will parse, a DOCX twin for portals that want Word, and a matching cover-letter PDF. Use whenever a resume or CV has to be delivered as a PDF or Word file."
license: Apache-2.0
compatibility: "Requires: rendercv (installed with uv), poppler-utils; doc-export with pandoc and typst for the DOCX twin and cover letter. macOS/Linux."
capabilities: shell resume-render documents
domains: coach
rules:
  - session(resume)
  - content(rendercv)
  - match(\b(resume|cv|curriculum vitae)\s+(pdf|docx|word|file|template|format)\b)
  - semantic(make my resume into a pdf)
  - semantic(give me the tailored resume as a word document too)
---

## Overview

A tailored resume only helps once it is a file that parses cleanly and looks professional. This skill turns the tailored content into a typeset PDF with RenderCV, checks it the way an applicant tracking system reads it, and produces the Word twin and cover letter some portals ask for. It replaces hand-made HTML-to-PDF conversions and two-column templates whose text comes out scrambled.

## Mental model

- Content and design are separate. The candidate's facts live in `cv.sections` of a YAML file; the look lives in the `design:` block. Tailoring changes the content; the design stays fixed.
- The parser reads the text layer, not the picture. A resume is checked by extracting its text and reading it top to bottom.
- One source, three files: `<Name>_Resume.pdf`, the same content as `.docx`, and the cover letter as PDF.

## Rules

### Build the YAML

Start once with `rendercv new "Full Name" --theme engineeringresumes`, then replace the sample content. Structure:

```yaml
cv:
  name: Jane Doe
  location: Berlin, Germany
  email: jane@example.com
  phone: "+49 30 1234567"
  website: https://janedoe.dev/
  social_networks:
    - network: LinkedIn
      username: janedoe
  sections:
    summary:
      - Backend engineer, 7 years in payments; led the PSD3 migration at a 40-person fintech.
    experience:
      - company: Finly
        position: Senior Backend Engineer
        location: Berlin
        start_date: 2022-03
        end_date: present
        highlights:
          - Cut payment failure rate from 2.1% to 0.6% by redesigning retry logic (Go, Kafka)
    education:
      - institution: TU Munich
        area: Computer Science
        degree: MSc
        start_date: 2014-10
        end_date: 2017-03
    skills:
      - label: Languages
        details: Go, Python, SQL
design:
  theme: engineeringresumes
  page:
    size: a4
    show_top_note: false
    show_footer: false
  header:
    connections:
      show_icons: false
      phone_number_format: international
```

Section titles are free text (`experience`, `Projects`, `Berufserfahrung`); Markdown `**bold**` works inside entries. Dates as `YYYY-MM` or `present`.

### ATS-safe design

| Setting | Value | Why |
|---|---|---|
| `theme` | `engineeringresumes` (alternatives `sb2nov`, `ember`) | Single column, dates next to each entry, links printed as full URLs |
| `header.connections.show_icons` | `false` | Icon fonts put private-use characters into the text layer |
| `page.show_top_note`, `page.show_footer` | `false` | Otherwise "Last updated in ..." becomes the first line parsers read and "Name – 1/2" lands between sections |
| `header.connections.phone_number_format` | `international` for cross-border applications | Prints +49 30 ... instead of a national 030 ... |
| `page.size` | `us-letter` for US/Canada, `a4` elsewhere | Market convention; prints without scaling |
| Photo | Only where the market expects one | See the market's conventions |

Avoid `classic`, `engineeringclassic`, `opal`, `moderncv`, and `ink` for portal submissions: they render social links as bare usernames or icon glyphs, or move dates away from their entries.

### Render and check

```bash
rendercv render Jane_Doe_CV.yaml --pdf-path Jane_Doe_Resume.pdf --markdown-path Jane_Doe_Resume.md -nohtml -nopng
doc-export check Jane_Doe_Resume.pdf --max-pages 2 --text 40
```

Read the text output: name and contact first, then sections in order, each job's title, company, and dates together, no junk characters, no lost bullets. Column layouts can push a date away from its entry, mostly on sparse pages; if any date lands elsewhere (often at the end of the page), switch the theme to `sb2nov` or `ember`, re-render, and re-check. Cut content rather than shrink fonts when the page count is over the market's norm.

### Word twin and cover letter

- DOCX: replace the first line of the generated Markdown (`# Jane Doe's CV`) with `# Jane Doe`, then `doc-export docx Jane_Doe_Resume.md -o Jane_Doe_Resume.docx --font Calibri --size 10.5 --margins 0.75in --paper a4`.
- Cover letter: write `cover-letter.md`, then `doc-export pdf cover-letter.md -o Jane_Doe_Cover_Letter.pdf --font Calibri --size 11 --margins 1in --paper a4 --max-pages 1`.
- File names carry the candidate's name, never "resume_final_v3".

## Examples

### Example 1: icon theme

❌ `theme: classic` with icons on. `pdftotext` shows `` before the email and "janedoe" instead of the LinkedIn URL.

✅ `theme: engineeringresumes`, `show_icons: false`: the text layer starts `Jane Doe | Berlin, Germany | jane@example.com | linkedin.com/in/janedoe`.

### Example 2: two-column template

❌ A two-column HTML template printed to PDF: the parser reads the skills sidebar in the middle of the first job.

✅ RenderCV's single-column theme; the check shows each job's title, company, dates, and bullets together.

## Checklist

- [ ] Content in YAML matches the tailored resume exactly; nothing invented.
- [ ] `engineeringresumes` (or `sb2nov`/`ember`), icons, top note, and footer off, paper size for the market.
- [ ] `doc-export check` clean: within the page count, no private-use glyphs, text in reading order.
- [ ] DOCX twin when a portal or recruiter wants Word; cover letter PDF in the same style.
- [ ] Files named `<First>_<Last>_Resume.pdf` / `.docx` / `_Cover_Letter.pdf` and saved next to the YAML source.

## Composition / References

- `ats-optimization` — what goes into the content and how it is tailored.
- `resume-conventions` — market rules: length, photo, personal data, date formats.
- `document-export` — the DOCX and cover-letter exports and the PDF check.
- [RenderCV documentation](https://docs.rendercv.com)

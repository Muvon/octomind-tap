# muvon/doc-export

doc-export — the tap's document exporter. It turns Markdown into Word (`.docx`) and PDF with the fonts, sizes, line spacing, page size, and margins a submission requires: Word output gets a reference document built from those settings, and PDF output goes through pandoc's Typst engine. Its `check` command reports a PDF's page count, page size, embedded fonts, and text layer, so page limits, missing fonts, image-only scans, and icon-font junk are caught before sending. The installer links the `document-export` skill's `scripts/doc_export.py` onto PATH. Python 3.9+ standard library; needs pandoc 3.1.2+, typst, and poppler-utils.

## Key Commands

| Command | Description |
|---------|-------------|
| `doc-export docx proposal.md -o proposal.docx --font "Times New Roman" --size 12 --margins 1in` | Word file with exact body font, size, and margins |
| `doc-export pdf proposal.md -o proposal.pdf --font "Times New Roman" --size 12 --max-pages 20` | PDF through Typst, then the page-limit and font checks |
| `doc-export reference -o house-style.docx --font "Calibri" --size 11 --heading-color 0B3D91` | Reusable Word style file for `pandoc --reference-doc` |
| `doc-export check resume.pdf --max-pages 2 --text 30` | Pages, fonts, and the first 30 lines of the text layer |
| `doc-export docx notes.md -o notes.docx --reference company-template.docx` | Use an existing Word template's styles |

## Common Usage

```bash
doc-export pdf cover-letter.md -o cover-letter.pdf --font "Calibri" --size 11 --margins 1in
doc-export check cover-letter.pdf --max-pages 1 --text 15
```

Options shared by `docx`, `pdf`, and `reference`: `--font`, `--heading-font`, `--size`, `--heading-color`, `--line-spacing`, `--paper us-letter|a4`, `--margins`. `docx` and `pdf` also take `--toc`, `--numbered`, `--max-pages`, and `--resource-path` for images.

## Links

- [Homepage](https://github.com/muvon/octomind-tap)
- [pandoc manual: reference docx](https://pandoc.org/MANUAL.html#option--reference-doc)
- [pandoc Typst output](https://pandoc.org/MANUAL.html#variables-for-typst)

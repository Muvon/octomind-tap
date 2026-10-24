# freedesktop/poppler

poppler-utils are the standard command-line tools for inspecting PDFs: `pdftotext` extracts the text layer (what an applicant tracking system or a search index reads), `pdfinfo` reports pages and page size, and `pdffonts` lists fonts and whether they are embedded. The tap uses them to verify exported resumes, proposals, and decks before they are sent.

## Key Commands

| Command | Description |
|---------|-------------|
| `pdftotext -layout file.pdf -` | Text with the page layout preserved |
| `pdftotext file.pdf -` | Text in reading order, as parsers see it |
| `pdfinfo file.pdf` | Pages, page size, producer, metadata |
| `pdffonts file.pdf` | Fonts, type, and `emb` (embedded) per font |
| `pdftoppm -png -r 80 file.pdf page` | Page previews as PNG |

## Common Usage

```bash
pdfinfo resume.pdf | grep Pages        # length check
pdftotext resume.pdf - | head -40      # does the text come out in a sensible order?
pdffonts proposal.pdf                  # every font embedded (emb = yes)?
```

## Links

- [Poppler](https://poppler.freedesktop.org)

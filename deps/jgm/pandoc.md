# jgm/pandoc

pandoc converts Markdown into Word (`.docx`), PDF, HTML, and many other formats. With `--pdf-engine=typst` (pandoc 3.1.2+) it typesets PDFs through Typst, which is fast and needs no LaTeX install. A reference document (`--reference-doc`) sets the fonts, sizes, colors, and margins of Word output. The installer uses Homebrew on macOS and a pinned, checksummed release tarball under `~/.local/opt` on Linux.

## Key Commands

| Command | Description |
|---------|-------------|
| `pandoc in.md -o out.docx --reference-doc ref.docx` | Markdown to Word with the reference document's styles |
| `pandoc in.md -o out.pdf --pdf-engine=typst -V mainfont="Inter" -V fontsize=11pt` | Markdown to PDF through Typst |
| `pandoc -o ref.docx --print-default-data-file reference.docx` | Write the default reference document to customize |
| `pandoc -D typst` | Show the Typst template and the variables it reads |
| `pandoc in.docx -t gfm -o out.md` | Word back to Markdown, e.g. to read a supplied resume or RFP |

## Common Usage

```bash
# A proposal as Word and PDF with the same look
doc-export docx proposal.md -o proposal.docx --font "Times New Roman" --size 12 --margins 1in
doc-export pdf proposal.md -o proposal.pdf --font "Times New Roman" --size 12 --margins 1in --max-pages 20
```

`doc-export` (installed with the `documents` capability) wraps these calls, builds the reference document from font, size, and margin flags, and checks the PDF's page count, fonts, and text layer.

## Links

- [pandoc manual](https://pandoc.org/MANUAL.html)
- [Typst](https://typst.app/docs/)

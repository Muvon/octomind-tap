# rendercv/rendercv

RenderCV turns a resume written as YAML (content in one file, design in a separate `design:` block) into a typeset PDF through Typst, plus Markdown, HTML, and PNG copies. The output is a real text PDF in a single-column layout that parsers read in order, and the content file stays version-controllable and easy to tailor per job. Themes: `classic`, `engineeringresumes`, `engineeringclassic`, `sb2nov`, `harvard`, `ink`, `opal`, `ember`, `moderncv`. The installer pins the version through `uv tool install`.

## Key Commands

| Command | Description |
|---------|-------------|
| `rendercv new "Jane Doe" --theme engineeringresumes` | Starter `Jane_Doe_CV.yaml` with every section type |
| `rendercv render Jane_Doe_CV.yaml` | PDF, Markdown, HTML, and PNG into `rendercv_output/` |
| `rendercv render cv.yaml --pdf-path resume.pdf --dont-generate-html --dont-generate-png` | Just the PDF, at a chosen path |
| `rendercv render --help` | All options, including per-field overrides |
| `rendercv create-theme mytheme` | Copy a theme's Typst templates to customize |

## Common Usage

```bash
rendercv new "Jane Doe" --theme engineeringresumes
# edit Jane_Doe_CV.yaml: cv.sections (experience, education, skills, ...), design.theme
rendercv render Jane_Doe_CV.yaml --pdf-path resume.pdf
pdftotext resume.pdf - | head -40   # check the text order a parser will read
```

## Links

- [RenderCV documentation](https://docs.rendercv.com)
- [Repository](https://github.com/rendercv/rendercv)

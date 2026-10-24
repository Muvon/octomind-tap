#!/usr/bin/env python3
"""Markdown to Word and PDF with controlled fonts, sizes, and margins, plus PDF checks.

    doc-export docx proposal.md -o proposal.docx --font "Times New Roman" --size 12 --margins 1in
    doc-export pdf proposal.md -o proposal.pdf --font "Times New Roman" --size 12 --max-pages 20
    doc-export reference -o house.docx --font "Calibri" --size 11     # reusable Word style file
    doc-export check proposal.pdf --max-pages 20 --text 30            # pages, fonts, text layer

DOCX goes through pandoc with a reference document built from the flags (theme fonts, body and
heading sizes, heading color, line spacing, page size, margins). PDF goes through pandoc's Typst
engine with the same settings. `check` reports page count, page size, embedded fonts, and the
first lines of the text layer, which is what applicant tracking systems and search indexes read.
Needs pandoc 3.1.2+, typst, and poppler-utils. Stdlib only, Python 3.9+.
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

PAPER = {"us-letter": (12240, 15840), "a4": (11906, 16838)}  # twips


def die(msg):
    sys.exit(f"doc-export: {msg}")


def warn(msg):
    print(f"doc-export: warning: {msg}", file=sys.stderr)


def need(tool, hint):
    path = shutil.which(tool)
    if not path:
        die(f"{tool} not found ({hint})")
    return path


def length_to_twips(value):
    m = re.fullmatch(r"\s*([\d.]+)\s*(in|cm|mm|pt)\s*", value)
    if not m:
        die(f"bad length {value!r}; use e.g. 1in, 2.5cm, 20mm, 72pt")
    n, unit = float(m.group(1)), m.group(2)
    return int(round(n * {"in": 1440, "cm": 566.93, "mm": 56.693, "pt": 20}[unit]))


# ---------------------------------------------------------------- DOCX reference


def build_reference(out, font, size, heading_font, heading_color, line_spacing, paper, margins):
    pandoc = need("pandoc", "install pandoc 3.1.2+")
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "base.docx"
        subprocess.run([pandoc, "-o", str(base), "--print-default-data-file", "reference.docx"], check=True)
        zin = zipfile.ZipFile(base)
        files = {n: zin.read(n) for n in zin.namelist()}
        zin.close()

    theme = files["word/theme/theme1.xml"].decode("utf-8")
    major = heading_font or font
    theme = re.sub(
        r'(<a:majorFont>\s*<a:latin typeface=")[^"]*(")', lambda m: m.group(1) + esc(major) + m.group(2), theme
    )
    theme = re.sub(
        r'(<a:minorFont>\s*<a:latin typeface=")[^"]*(")', lambda m: m.group(1) + esc(font) + m.group(2), theme
    )
    files["word/theme/theme1.xml"] = theme.encode("utf-8")

    styles = files["word/styles.xml"].decode("utf-8")
    half = int(round(size * 2))

    def set_defaults(m):
        block = m.group(0)
        block = re.sub(r'<w:sz w:val="\d+"\s*/>', f'<w:sz w:val="{half}" />', block)
        block = re.sub(r'<w:szCs w:val="\d+"\s*/>', f'<w:szCs w:val="{half}" />', block)
        line = int(round(240 * line_spacing))
        block = re.sub(
            r"<w:spacing [^>]*/>", f'<w:spacing w:after="160" w:line="{line}" w:lineRule="auto" />', block, count=1
        )
        return block

    styles = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", set_defaults, styles, flags=re.S)
    scale = {"Title": 2.0, "Heading1": 1.45, "Heading2": 1.25, "Heading3": 1.1, "Heading4": 1.0}
    for sid, factor in scale.items():

        def fix(m, factor=factor):
            block = m.group(0)
            hs = int(round(size * factor * 2))
            block = re.sub(r'<w:sz w:val="\d+"\s*/>', f'<w:sz w:val="{hs}" />', block)
            block = re.sub(r'<w:szCs w:val="\d+"\s*/>', f'<w:szCs w:val="{hs}" />', block)
            block = re.sub(r"<w:color [^>]*/>", f'<w:color w:val="{heading_color}" />', block, flags=re.S)
            return block

        styles = re.sub(r'<w:style [^>]*w:styleId="%s".*?</w:style>' % sid, fix, styles, flags=re.S)
    # Hyperlinks and block quotes keep pandoc's styles; body and headings now share the theme fonts.
    files["word/styles.xml"] = styles.encode("utf-8")

    doc = files["word/document.xml"].decode("utf-8")
    w, h = PAPER[paper]
    m = length_to_twips(margins)
    page = (
        f'<w:pgSz w:w="{w}" w:h="{h}" />'
        f'<w:pgMar w:top="{m}" w:right="{m}" w:bottom="{m}" w:left="{m}" w:header="720" w:footer="720" w:gutter="0" />'
    )
    doc = re.sub(r"<w:pgSz [^>]*/>|<w:pgMar [^>]*/>", "", doc)
    doc = re.sub(r"(<w:sectPr[^>]*>)", r"\1" + page, doc, count=1)
    files["word/document.xml"] = doc.encode("utf-8")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in files.items():
            zout.writestr(name, data)


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


# ---------------------------------------------------------------- commands


def common_pandoc_args(args):
    extra = []
    if args.toc:
        extra.append("--toc")
    if args.numbered:
        extra.append("--number-sections")
    if args.resource_path:
        extra += ["--resource-path", args.resource_path]
    return extra


def cmd_reference(args):
    build_reference(
        args.out, args.font, args.size, args.heading_font, args.heading_color, args.line_spacing, args.paper, args.margins
    )
    print(f"doc-export: reference document -> {args.out}", file=sys.stderr)


def cmd_docx(args):
    pandoc = need("pandoc", "install pandoc 3.1.2+")
    with tempfile.TemporaryDirectory() as td:
        ref = args.reference
        if not ref:
            ref = str(Path(td) / "ref.docx")
            build_reference(
                ref, args.font, args.size, args.heading_font, args.heading_color, args.line_spacing, args.paper, args.margins
            )
        cmd = [pandoc, args.input, "-o", args.out, "--reference-doc", ref] + common_pandoc_args(args)
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            die(f"pandoc failed: {r.stderr.strip()[-600:]}")
    note = ""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if args.max_pages and soffice:
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(
                [soffice, "--headless", "--convert-to", "pdf", "--outdir", td, args.out], capture_output=True, text=True
            )
            pdfs = list(Path(td).glob("*.pdf"))
            if pdfs:
                pages = pdf_pages(str(pdfs[0]))
                note = f", ~{pages} page(s) in LibreOffice"
                if pages and pages > args.max_pages:
                    warn(f"about {pages} pages in LibreOffice, over the {args.max_pages}-page limit")
    elif args.max_pages:
        note = "; page count needs LibreOffice or the PDF export (Word may paginate differently)"
    print(f"doc-export: {args.out} ({args.font} {args.size}pt, {args.margins} margins, {args.paper}){note}", file=sys.stderr)


def typst_has_font(font):
    typst = shutil.which("typst")
    if not typst:
        return True
    out = subprocess.run([typst, "fonts"], capture_output=True, text=True).stdout
    return font.lower() in {ln.strip().lower() for ln in out.splitlines()}


def cmd_pdf(args):
    pandoc = need("pandoc", "install pandoc 3.1.2+")
    need("typst", "install typst")
    if not typst_has_font(args.font):
        warn(f"Typst can't find the font '{args.font}' (see `typst fonts`); it will fall back to its default")
    with tempfile.TemporaryDirectory() as td:
        meta = Path(td) / "meta.yaml"
        meta.write_text(
            "---\n"
            f"margin:\n  x: {args.margins}\n  y: {args.margins}\n"
            f'papersize: "{args.paper}"\n'
            f'mainfont: "{args.font}"\n'
            f"fontsize: {args.size}pt\n"
            f"linestretch: {args.line_spacing}\n"
            f"lang: {args.lang}\n"
            "...\n",
            encoding="utf-8",
        )
        cmd = [pandoc, args.input, "-o", args.out, "--pdf-engine=typst", "--metadata-file", str(meta)]
        cmd += common_pandoc_args(args)
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            die(f"pandoc/typst failed: {r.stderr.strip()[-800:]}")
        for line in r.stderr.splitlines():
            if "warning" in line.lower():
                warn(line.strip())
    report(args.out, args.max_pages, 0)


def pdf_pages(path):
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", info, re.M)
    return int(m.group(1)) if m else None


def report(path, max_pages, text_lines):
    if not shutil.which("pdfinfo"):
        warn("poppler-utils not installed; skipping page, font, and text checks")
        return 0
    info = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    pages = pdf_pages(path)
    size = re.search(r"^Page size:\s+(.+)$", info, re.M)
    fonts = subprocess.run(["pdffonts", path], capture_output=True, text=True).stdout.splitlines()[2:]
    not_embedded = [f.split()[0] for f in fonts if len(f.split()) >= 5 and f.split()[-5] == "no"]
    text = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout
    words = len(text.split())
    problems = 0
    print(f"doc-export: {path}: {pages} page(s), {size.group(1).strip() if size else '?'}, {words} words in the text layer")
    if max_pages and pages and pages > max_pages:
        print(f"  over the page limit: {pages} > {max_pages}")
        problems += 1
    if not_embedded:
        print("  fonts not embedded: " + ", ".join(not_embedded))
        problems += 1
    if pages and words < 20 * pages:
        print("  little or no extractable text: the PDF may be image-only; parsers will read nothing")
        problems += 1
    if re.search(r"[-]", text):
        print("  private-use glyphs in the text layer (icon fonts); parsers see junk characters")
        problems += 1
    if text_lines:
        lines = [ln for ln in text.splitlines() if ln.strip()][:text_lines]
        print("  text layer, in reading order:")
        for ln in lines:
            print("    " + ln.strip())
    return problems


def cmd_check(args):
    need("pdfinfo", "install poppler-utils")
    sys.exit(1 if report(args.pdf, args.max_pages, args.text) else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def style_flags(p):
        p.add_argument("--font", default="Calibri", help="body font family (default: Calibri)")
        p.add_argument("--heading-font", help="heading font family (default: the body font)")
        p.add_argument("--size", type=float, default=11, help="body size in pt (default: 11)")
        p.add_argument("--heading-color", default="1F2937", help="heading color RRGGBB (default: near-black)")
        p.add_argument("--line-spacing", type=float, default=1.15, help="line spacing multiple (default: 1.15)")
        p.add_argument("--paper", choices=sorted(PAPER), default="us-letter")
        p.add_argument("--margins", default="1in", help="all four margins, e.g. 1in, 2.5cm (default: 1in)")

    def doc_flags(p):
        p.add_argument("input", help="Markdown source")
        p.add_argument("-o", "--out", required=True)
        p.add_argument("--toc", action="store_true", help="table of contents")
        p.add_argument("--numbered", action="store_true", help="numbered section headings (1, 1.1, ...)")
        p.add_argument("--max-pages", type=int, help="page limit to check")
        p.add_argument("--resource-path", help="where images referenced by the Markdown live")

    d = sub.add_parser("docx", help="Markdown to Word")
    doc_flags(d)
    style_flags(d)
    d.add_argument("--reference", help="use this Word style file instead of building one")
    d.set_defaults(fn=cmd_docx)

    p = sub.add_parser("pdf", help="Markdown to PDF through Typst")
    doc_flags(p)
    style_flags(p)
    p.add_argument("--lang", default="en", help="document language for hyphenation (default: en)")
    p.set_defaults(fn=cmd_pdf)

    r = sub.add_parser("reference", help="write a reusable Word style file")
    r.add_argument("-o", "--out", required=True)
    style_flags(r)
    r.set_defaults(fn=cmd_reference)

    c = sub.add_parser("check", help="pages, page size, embedded fonts, and text layer of a PDF")
    c.add_argument("pdf")
    c.add_argument("--max-pages", type=int)
    c.add_argument("--text", type=int, default=0, help="print the first N lines of the text layer")
    c.set_defaults(fn=cmd_check)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

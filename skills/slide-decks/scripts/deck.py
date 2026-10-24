#!/usr/bin/env python3
"""Marp slide decks: lint the Markdown, render PDF/HTML/PPTX/PNG, and catch overflowing slides.

    slide-deck new deck-pricing.md --title "Pricing that sells itself"
    slide-deck lint deck-pricing.md            # words per slide, bullets, alt text, notes
    slide-deck render deck-pricing.md          # PDF + HTML + PNG previews + overflow check
    slide-deck render deck-pricing.md --pptx   # also PowerPoint (slides as images)

Runs a pinned Marp CLI through npx with this skill's themes (`octo` by default) and a local
Chrome, Edge, Chromium, or Firefox. The overflow check renders small PNGs and looks for ink in
the theme's bottom margin, where clipped text ends up. Stdlib only, Python 3.9+.
"""

import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

MARP = "@marp-team/marp-cli@4.5.1"
THEMES = Path(__file__).resolve().parent.parent / "assets"
DIRECTIVES = {
    "theme",
    "paginate",
    "header",
    "footer",
    "class",
    "backgroundcolor",
    "backgroundimage",
    "backgroundposition",
    "backgroundrepeat",
    "backgroundsize",
    "color",
    "headingdivider",
    "size",
    "style",
    "math",
    "title",
    "description",
    "author",
    "image",
    "keywords",
    "url",
    "lang",
    "marp",
    "transition",
}

STARTER = """---
marp: true
theme: octo
paginate: true
title: {title}
# Brand color: uncomment and set
# style: section {{ --octo-accent: #2563eb; }}
---

<!-- _class: lead -->
<!-- _paginate: skip -->

# {title}

Speaker or team · Date

<!-- Open with the stakes: why this matters to this room now. -->

---

# State the claim as a full sentence

- Evidence point one
- Evidence point two
- Evidence point three

<!-- Speaker notes carry the narration the slide leaves out. -->

---

<!-- _class: stat -->

## 47%

# of churned accounts leave in month two

Source: billing data, Jan–Sep

<!-- One number, one message. -->

---

<!-- _class: divider -->

# Next section

---

# Approve the two-week pilot by Friday

What we need from this room, by when, and what it costs.

<!-- The last slide stays up during Q&A: make it the ask, not "Thank you". -->
"""


def warn(msg):
    print(f"slide-deck: warning: {msg}", file=sys.stderr)


def die(msg):
    sys.exit(f"slide-deck: {msg}")


# ---------------------------------------------------------------- parsing


def split_deck(text):
    """Front matter dict + list of (index, slide_text). Slides split on --- outside code fences."""
    lines = text.splitlines()
    front = {}
    i = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                for ln in lines[1:j]:
                    m = re.match(r"^\s*([A-Za-z_]+)\s*:\s*(.*)$", ln)
                    if m and not ln.lstrip().startswith("#"):
                        front[m.group(1).lower()] = m.group(2).strip()
                i = j + 1
                break
    slides, cur, fence = [], [], False
    for ln in lines[i:]:
        if re.match(r"^\s*(```|~~~)", ln):
            fence = not fence
        if not fence and ln.strip() == "---":
            slides.append("\n".join(cur))
            cur = []
        else:
            cur.append(ln)
    slides.append("\n".join(cur))
    return front, [(n + 1, s) for n, s in enumerate(slides) if s.strip()]


def comments(slide):
    return re.findall(r"<!--(.*?)-->", slide, re.S)


def is_directive(comment):
    body = comment.strip()
    m = re.match(r"^_?([A-Za-z]+)\s*:", body)
    return bool(m) and m.group(1).lower() in DIRECTIVES or body.lower() in ("fit",)


def slide_class(slide, deck_class):
    for c in comments(slide):
        m = re.match(r"^\s*_?class\s*:\s*(.+?)\s*$", c)
        if m:
            return m.group(1)
    return deck_class


def analyze(slide):
    notes = [c.strip() for c in comments(slide) if not is_directive(c) and c.strip()]
    body = re.sub(r"<!--.*?-->", "", slide, flags=re.S)
    body = re.sub(r"(```|~~~).*?\1", "", body, flags=re.S)
    title = None
    words = 0
    bullets = 0
    images = re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", body)
    table_rows = 0
    for ln in body.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m and title is None and len(m.group(1)) <= 2:
            title = m.group(2).strip()
            continue
        if re.match(r"^([-*+]|\d+[.)])\s+", s):
            bullets += 1
        if s.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", s):
            table_rows += 1
        s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
        s = re.sub(r"<[^>]+>", "", s)
        words += len(re.findall(r"[\w'’%$€£.,-]+", s))
    return dict(title=title, words=words, bullets=bullets, images=images, notes=notes, table_rows=table_rows)


def cmd_lint(args, quiet=False):
    path = Path(args.deck)
    if not path.exists():
        die(f"{path} not found")
    front, slides = split_deck(path.read_text(encoding="utf-8"))
    problems = 0

    def say(msg):
        if not quiet:
            print(msg)

    def flag(n, msg):
        nonlocal problems
        problems += 1
        say(f"  slide {n}: {msg}")

    if front.get("marp", "").lower() != "true":
        say("  front matter: add `marp: true`")
        problems += 1
    if "theme" not in front:
        say("  front matter: no `theme:` (the octo theme ships with this tool)")
    size = front.get("size", "16:9")
    if size not in ("16:9", ""):
        say(f"  front matter: size {size}; 16:9 fits projectors, video calls, and PDF readers best")
    word_cap = 90 if args.mode == "read" else 40
    deck_class = front.get("class", "")
    content = 0
    for n, s in slides:
        a = analyze(s)
        cls = slide_class(s, deck_class)
        structural = any(c in cls.split() for c in ("lead", "divider"))
        if not structural:
            content += 1
        if a["title"] is None and not structural and a["images"] == []:
            flag(n, "no heading; a content slide needs a title that states its point")
        elif a["title"] and not structural and "stat" not in cls:
            tw = len(a["title"].split())
            if tw <= 3 and not re.search(r"\d", a["title"]):
                flag(n, f"title \"{a['title']}\" is a topic label; write the claim as a sentence")
            if tw > 14:
                flag(n, f"title is {tw} words; keep the claim under ~12")
        if a["words"] > word_cap:
            flag(n, f"{a['words']} words on the slide ({args.mode} deck cap ~{word_cap}); move detail to notes or split")
        if a["bullets"] > 6:
            flag(n, f"{a['bullets']} bullets; split the slide or build it up")
        if a["table_rows"] > 7:
            flag(n, f"{a['table_rows']} table rows; show the rows that make the point, the rest in an appendix")
        for alt, src in a["images"]:
            words = alt.split()
            if "bg" in words:
                continue  # background images are decorative to screen readers
            text = [w for w in words if not re.match(r"^(\w+:\S*|contain|cover|fit|auto|left|right|vertical)$", w)]
            if not text:
                flag(n, f"image {src} has no alt text")
        if args.mode == "talk" and not structural and not a["notes"]:
            flag(n, "no speaker notes; put the narration in an HTML comment")
    if not quiet:
        print(f"slide-deck: {len(slides)} slides ({content} content), {problems} issue(s) in {path}")
    return problems


# ---------------------------------------------------------------- rendering


def find_browser():
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    cands = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge"):
        p = shutil.which(name)
        if p:
            cands.append(p)
    caches = [
        (Path.home() / ".cache/puppeteer", ("chrome-headless-shell/*/*/chrome-headless-shell", "chrome/*/*/chrome")),
        (Path.home() / ".cache/ms-playwright", ("chromium-*/chrome-*/chrome",)),
        (Path.home() / "Library/Caches/ms-playwright", ("chromium-*/chrome-mac*/*.app/Contents/MacOS/*",)),
        (Path(os.environ.get("LOCALAPPDATA", "/nonexistent")) / "ms-playwright", ("chromium-*/chrome-win*/chrome.exe",)),
    ]
    for base, pats in caches:
        if base.is_dir():
            for pat in pats:
                cands += [str(p) for p in sorted(base.glob(pat), reverse=True)]
    cands += ["/Applications/Firefox.app/Contents/MacOS/firefox"]
    if shutil.which("firefox"):
        cands.append(shutil.which("firefox"))
    for c in cands:
        if c and Path(c).exists() and os.access(c, os.X_OK):
            return c
    return None


def marp(deck, extra, browser):
    npx = shutil.which("npx")
    if not npx:
        die("npx not found; install Node.js 18+")
    cmd = [npx, "-y", MARP, str(deck), "--allow-local-files", "--theme-set", str(THEMES), "--no-config-file"]
    if browser:
        cmd += ["--browser-path", browser]
        if "firefox" in browser.lower():
            cmd += ["--browser", "firefox"]
    cmd += extra
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path(deck).resolve().parent))
    if r.returncode != 0:
        tail = "\n".join(line for line in r.stderr.splitlines() if "npm warn" not in line)[-1200:]
        die(f"marp failed:\n{tail}")
    return r


def read_png(path):
    """Decode an 8-bit RGB/RGBA PNG into (width, height, channels, rows)."""
    data = Path(path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    pos, idat, w = 8, b"", None
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        kind = data[pos + 4 : pos + 8]
        chunk = data[pos + 8 : pos + 8 + length]
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
            if depth != 8 or ctype not in (2, 6) or interlace:
                raise ValueError("unsupported PNG format")
            ch = 3 if ctype == 2 else 4
        elif kind == b"IDAT":
            idat += chunk
        pos += 12 + length
    raw = zlib.decompress(idat)
    stride = w * ch
    rows, prev = [], bytearray(stride)
    i = 0
    for _ in range(h):
        ftype = raw[i]
        line = bytearray(raw[i + 1 : i + 1 + stride])
        i += 1 + stride
        if ftype == 1:
            for x in range(ch, stride):
                line[x] = (line[x] + line[x - ch]) & 255
        elif ftype == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif ftype == 3:
            for x in range(stride):
                left = line[x - ch] if x >= ch else 0
                line[x] = (line[x] + ((left + prev[x]) >> 1)) & 255
        elif ftype == 4:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                b = prev[x]
                c = prev[x - ch] if x >= ch else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[x] = (line[x] + pred) & 255
        rows.append(line)
        prev = line
    return w, h, ch, rows


def overflow_slides(pngs):
    """Slides with ink in the octo theme's bottom margin band, above the footer/page number."""
    bad = []
    for n, png in pngs:
        try:
            w, h, ch, rows = read_png(png)
        except (ValueError, zlib.error, struct.error):
            continue
        # octo: 80 px bottom padding at 1280x720; footer and page number sit in the last ~55 px.
        y0, y1 = int(h * (720 - 78) / 720), int(h * (720 - 60) / 720)
        x0, x1 = int(w * 80 / 1280), int(w * (1280 - 80) / 1280)
        ref = rows[y0][int(w * 20 / 1280) * ch : int(w * 20 / 1280) * ch + 3]
        hits = total = 0
        for y in range(y0, y1):
            row = rows[y]
            for x in range(x0, x1):
                o = x * ch
                total += 1
                if abs(row[o] - ref[0]) + abs(row[o + 1] - ref[1]) + abs(row[o + 2] - ref[2]) > 90:
                    hits += 1
        if total and hits / total > 0.004:
            bad.append(n)
    return bad


def cmd_render(args):
    deck = Path(args.deck).resolve()
    if not deck.exists():
        die(f"{deck} not found")
    text = deck.read_text(encoding="utf-8")
    front, slides = split_deck(text)
    issues = cmd_lint(argparse.Namespace(deck=str(deck), mode=args.mode), quiet=True)
    if issues:
        warn(f"{issues} lint issue(s); run `slide-deck lint {deck.name}` for details")
    browser = find_browser()
    if not browser:
        die(
            "no Chrome, Edge, Chromium, or Firefox found for PDF/PNG export; install one, "
            "or set CHROME_PATH (`npx playwright@1.64.1 install chromium`)"
        )
    out_dir = Path(args.out_dir).resolve() if args.out_dir else deck.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = deck.stem
    made = []
    if not args.no_pdf:
        marp(deck, ["--pdf", "--pdf-outlines", "-o", str(out_dir / f"{stem}.pdf")], browser)
        made.append(f"{stem}.pdf")
    if args.html:
        marp(deck, ["--html", "-o", str(out_dir / f"{stem}.html")], browser)
        made.append(f"{stem}.html")
    if args.pptx or args.pptx_editable:
        extra = ["--pptx", "-o", str(out_dir / f"{stem}.pptx")]
        if args.pptx_editable:
            extra.append("--pptx-editable")
        marp(deck, extra, browser)
        made.append(f"{stem}.pptx" + (" (editable, experimental)" if args.pptx_editable else " (slides as images)"))
    if args.notes:
        marp(deck, ["--notes", "-o", str(out_dir / f"{stem}-notes.txt")], browser)
        made.append(f"{stem}-notes.txt")
    if args.png:
        png_dir = out_dir / f"{stem}-png"
        png_dir.mkdir(exist_ok=True)
        marp(deck, ["--images", "png", "-o", str(png_dir / f"{stem}.png")], browser)
        made.append(f"{png_dir.name}/")

    theme = front.get("theme", "default")
    if theme == "octo" and not args.no_check:
        with tempfile.TemporaryDirectory(prefix="deck-") as td:
            marp(deck, ["--images", "png", "--image-scale", "0.25", "-o", str(Path(td) / "s.png")], browser)
            pngs = sorted(Path(td).glob("s.*.png"))
            bad = overflow_slides([(int(p.stem.split(".")[-1]), p) for p in pngs])
        if bad:
            warn(
                "content runs into the bottom margin (likely clipped) on slide(s) "
                + ", ".join(map(str, bad))
                + ": cut words, split the slide, or shrink an image"
            )
    elif not args.no_check:
        warn(f"overflow check needs `theme: octo` (deck uses {theme}); check the PNGs by eye")
    print(f"slide-deck: {len(slides)} slides -> " + ", ".join(made) + f" in {out_dir}", file=sys.stderr)


def cmd_new(args):
    path = Path(args.deck)
    if path.exists() and not args.force:
        die(f"{path} exists (use --force to overwrite)")
    path.write_text(STARTER.format(title=args.title), encoding="utf-8")
    print(f"slide-deck: wrote {path}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    n = sub.add_parser("new", help="write a starter deck with the octo theme")
    n.add_argument("deck")
    n.add_argument("--title", default="Title that states the point")
    n.add_argument("--force", action="store_true")
    n.set_defaults(fn=cmd_new)

    li = sub.add_parser("lint", help="check words, bullets, titles, alt text, and notes per slide")
    li.add_argument("deck")
    li.add_argument("--mode", choices=["talk", "read"], default="talk", help="talk deck or send-ahead read deck")
    li.set_defaults(fn=lambda a: sys.exit(1 if cmd_lint(a) else 0))

    r = sub.add_parser("render", help="export PDF (default), HTML, PPTX, notes, PNGs; check overflow")
    r.add_argument("deck")
    r.add_argument("--out-dir", help="output directory (default: next to the deck)")
    r.add_argument("--no-pdf", action="store_true")
    r.add_argument("--html", action="store_true", help="self-contained HTML deck")
    r.add_argument("--pptx", action="store_true", help="PowerPoint with each slide as an image (exact look)")
    r.add_argument(
        "--pptx-editable", action="store_true", help="experimental editable PPTX (needs LibreOffice; lower fidelity)"
    )
    r.add_argument("--notes", action="store_true", help="speaker notes as a text file")
    r.add_argument("--png", action="store_true", help="full-size PNG per slide for review")
    r.add_argument("--mode", choices=["talk", "read"], default="talk")
    r.add_argument("--no-check", action="store_true", help="skip the overflow check")
    r.set_defaults(fn=cmd_render)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""GitHub social preview card (1280x640 PNG) in a repository's own brand.

Lays out a wordmark, an open-source badge, a one-line tagline, an optional subline, install
command and URL, and an optional logo, then renders with Typst using only the fonts you point it
at, so the same inputs give the same PNG on every machine:

    social-preview -o card.png --name acme --tagline "Two-way sync between Postgres and spreadsheets" \\
        --accent "#0969da" --badge "Open source · Go · MIT" --logo assets/logo.svg \\
        --install "go install github.com/acme/acme@latest" --url github.com/acme/acme --preview card-preview.png

Colors not given are derived from --accent and --bg. Warnings flag low contrast, long text, and
numbers that go stale (stars, versions, percentages). Fails on a missing font family, a wrong
output size, or a file over GitHub's 1 MB limit. Stdlib only, Python 3.9+; needs typst 0.13+.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WIDTH, HEIGHT = 1280, 640
PPI = 72  # the template is laid out in points, 1 pt = 1 px at 72 ppi
PREVIEW_WIDTH = 480  # about the width X, Slack, and LinkedIn show the card in a feed
GITHUB_MAX_BYTES = 1_000_000
TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "card.typ"
FONTS_DIR = Path(os.environ.get("OCTOMIND_FONTS_DIR", Path.home() / ".local/share/octomind/fonts"))
LOGO_TYPES = {".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp"}
TAGLINE_MAX_CHARS = 60
SUBLINE_MAX_CHARS = 48
INSTALL_MAX_CHARS = 44
TEXT_CONTRAST = 4.5  # WCAG AA for body-size text
LARGE_CONTRAST = 3.0  # WCAG AA for large or bold text (wordmark, footer URL)
STALE = re.compile(
    r"\b\d[\d.,]*\s*k?\+?\s*(stars?|downloads?|users?|installs?)\b|\bv?\d+\.\d+\.\d+\b|\d+(\.\d+)?\s*%|★",
    re.IGNORECASE,
)


def warn(msg):
    print(f"social-preview: warning: {msg}", file=sys.stderr)


def die(msg):
    sys.exit(f"social-preview: {msg}")


# ---------------------------------------------------------------- color


def parse_hex(value):
    m = re.fullmatch(r"#?([0-9a-fA-F]{6})", value.strip())
    if not m:
        die(f"color must be #rrggbb, got {value!r}")
    h = m.group(1)
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return "#" + "".join(f"{round(c):02x}" for c in rgb)


def mix(a, b, t):
    """t=0 gives a, t=1 gives b."""
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def luminance(rgb):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


BLACK, WHITE = (0, 0, 0), (255, 255, 255)
TERMINAL_BG, TERMINAL_FG = (27, 27, 38), (240, 240, 245)


def palette(args):
    bg = parse_hex(args.bg)
    fg = parse_hex(args.fg)
    accent = parse_hex(args.accent)
    dark = luminance(bg) < 0.5
    toward_text = WHITE if dark else BLACK
    colors = {
        "bg": bg,
        "fg": fg,
        "accent": accent,
        "accent2": parse_hex(args.accent_2) if args.accent_2 else mix(accent, BLACK, 0.25),
        "highlight": parse_hex(args.highlight) if args.highlight else mix(accent, toward_text, 0.3),
        "muted": parse_hex(args.muted) if args.muted else mix(fg, bg, 0.45),
        # A terminal stays dark on either background, so its ink can't follow --fg.
        "pane": mix(bg, BLACK, 0.5) if dark else TERMINAL_BG,
        "pane-fg": fg if dark else TERMINAL_FG,
        "pop": parse_hex(args.pop) if args.pop else mix(accent, WHITE, 0.3),
    }
    checks = [
        ("--fg on --bg (tagline)", "fg", TEXT_CONTRAST),
        ("highlight on --bg (badge, subline)", "highlight", TEXT_CONTRAST),
        ("--accent on --bg (wordmark)", "accent", LARGE_CONTRAST),
    ]
    if args.url:
        checks.append(("muted on --bg (URL)", "muted", LARGE_CONTRAST))
    for label, key, need in checks:
        ratio = contrast(colors[key], bg)
        if ratio < need:
            warn(f"{label} contrast {ratio:.2f}:1 is below {need}:1; pick a lighter/darker shade")
    return {k: to_hex(v) for k, v in colors.items()}


# ---------------------------------------------------------------- render


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        die(f"{path} is not a PNG")
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def typst_compile(typst, root, font_paths, inputs, out, ppi):
    cmd = [typst, "compile", "--root", str(root), "--ignore-system-fonts", "--ppi", str(ppi)]
    for p in font_paths:
        cmd += ["--font-path", str(p)]
    for k, v in inputs.items():
        cmd += ["--input", f"{k}={v}"]
    cmd += [str(root / TEMPLATE.name), str(out)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        die(f"typst failed:\n{proc.stderr.strip()}")
    if "unknown font family" in proc.stderr:
        listing = " ".join(f"--font-path {p}" for p in font_paths)
        die(
            f"a font family is not installed:\n{proc.stderr.strip()}\n"
            f"List what is available: typst fonts --ignore-system-fonts {listing}"
        )
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)


def check_text(args):
    for flag, value in (("--name", args.name), ("--tagline", args.tagline)):
        if not value.strip():
            die(f"{flag} must be non-empty")
    if len(args.tagline) > TAGLINE_MAX_CHARS:
        warn(f"tagline is {len(args.tagline)} chars; above {TAGLINE_MAX_CHARS} it shrinks toward feed-unreadable sizes")
    if args.subline and len(args.subline) > SUBLINE_MAX_CHARS:
        warn(f"subline is {len(args.subline)} chars; keep it under {SUBLINE_MAX_CHARS}")
    if args.install and len(args.install) > INSTALL_MAX_CHARS:
        warn(f"install command is {len(args.install)} chars; above {INSTALL_MAX_CHARS} it runs under the logo")
    for flag, value in (
        ("--tagline", args.tagline),
        ("--subline", args.subline),
        ("--badge", args.badge),
    ):
        if value and STALE.search(value):
            warn(f"{flag} {value!r} carries a count, version, or percentage that will go stale on the card")


def main():
    ap = argparse.ArgumentParser(
        prog="social-preview",
        description="Render a 1280x640 GitHub social preview card in a repository's brand.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Upload: repository Settings > General > Social preview > Edit > Upload an image.",
    )
    ap.add_argument("-o", "--output", required=True, help="output PNG path")
    ap.add_argument("--name", required=True, help="project name as the wordmark (exact casing)")
    ap.add_argument("--tagline", required=True, help="one line: what it is (fitted to two lines)")
    ap.add_argument("--subline", default="", help="optional 3-part value line, e.g. 'One binary · Any model'")
    ap.add_argument("--badge", default="", help="open-source facts, e.g. 'Open source · Rust · MIT'")
    ap.add_argument("--install", default="", help="install command shown in a terminal pane, without '$'")
    ap.add_argument("--url", default="", help="footer URL, e.g. github.com/org/repo")
    ap.add_argument("--logo", help="logo or mark: SVG preferred; PNG/JPG/GIF/WebP accepted")
    ap.add_argument("--pixelated", action="store_true", help="scale a raster logo without smoothing (pixel art)")
    ap.add_argument("--accent", required=True, help="primary brand color #rrggbb")
    ap.add_argument("--accent-2", help="gradient end of the edge bars (default: accent darkened)")
    ap.add_argument("--highlight", help="badge and subline color (default: accent lightened toward the text)")
    ap.add_argument("--pop", help="color of the '$' prompt (default: highlight)")
    ap.add_argument("--muted", help="URL color (default: fg mixed into bg)")
    ap.add_argument("--bg", default="#0d0d12", help="background #rrggbb (default: near-black)")
    ap.add_argument("--fg", default="#f5f5f7", help="tagline color #rrggbb")
    ap.add_argument("--font", default="Inter", help="sans family for tagline and subline (default: Inter)")
    ap.add_argument("--mono", default="JetBrains Mono", help="mono family for badge, install, URL")
    ap.add_argument("--wordmark", choices=["mono", "sans"], default="mono", help="wordmark face (default: mono)")
    ap.add_argument(
        "--font-path",
        action="append",
        default=[],
        help=f"extra font directory, e.g. the repo's bundled fonts (repeatable; {FONTS_DIR} is always searched)",
    )
    ap.add_argument("--preview", help=f"also write a {PREVIEW_WIDTH}px-wide feed-size PNG here")
    args = ap.parse_args()

    typst = shutil.which("typst")
    if not typst:
        die("typst not found on PATH; install it (the social-preview capability does)")
    out = Path(args.output)
    if out.suffix.lower() != ".png":
        die("--output must end in .png (GitHub, X, Slack, and LinkedIn don't render SVG previews)")
    font_paths = [Path(p).resolve() for p in args.font_path]
    for p in font_paths:
        if not p.is_dir():
            die(f"--font-path {p} is not a directory")
    if FONTS_DIR.is_dir():
        font_paths.append(FONTS_DIR)
    logo_path = None
    if args.logo:
        logo_path = Path(args.logo).resolve()
        if not logo_path.is_file():
            die(f"--logo {logo_path} not found")
        if logo_path.suffix.lower() not in LOGO_TYPES:
            die(f"--logo must be one of {', '.join(sorted(LOGO_TYPES))}")

    check_text(args)
    out.parent.mkdir(parents=True, exist_ok=True)
    # Typst reads files only inside --root; a scratch root holding just the template and the logo
    # keeps the rest of the filesystem out of its reach.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        shutil.copy(TEMPLATE, root)
        logo = ""
        if logo_path:
            logo = "logo" + logo_path.suffix.lower()
            shutil.copy(logo_path, root / logo)
        inputs = {
            "name": args.name,
            "tagline": args.tagline,
            "subline": args.subline,
            "badge": args.badge,
            "install": args.install,
            "url": args.url,
            "logo": logo,
            "logo-scaling": "pixelated" if args.pixelated else "smooth",
            "font": args.font,
            "mono": args.mono,
            "wordmark": args.wordmark,
            **palette(args),
        }

        typst_compile(typst, root, font_paths, inputs, out.resolve(), PPI)
        size = png_size(out)
        if size != (WIDTH, HEIGHT):
            die(f"rendered {size[0]}x{size[1]}, expected {WIDTH}x{HEIGHT}")
        nbytes = out.stat().st_size
        if nbytes > GITHUB_MAX_BYTES:
            die(f"{out} is {nbytes} bytes; GitHub rejects social previews over 1 MB (simplify the logo or texture)")

        if args.preview:
            preview = Path(args.preview)
            preview.parent.mkdir(parents=True, exist_ok=True)
            typst_compile(typst, root, font_paths, inputs, preview.resolve(), PPI * PREVIEW_WIDTH / WIDTH)

    print(f"social-preview: {out} {WIDTH}x{HEIGHT}, {nbytes // 1024} KB" + (f", preview {args.preview}" if args.preview else ""))


if __name__ == "__main__":
    main()

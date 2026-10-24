#!/usr/bin/env python3
"""Video thumbnails and cover images: background + optional cut-out subject + fitted text.

Renders with ffmpeg and libass, so the text is real typography (measured, line-balanced,
outlined or boxed) instead of an image model's guess at letters:

    video-thumbnail render frame.jpg -o thumb.jpg --text "I quit my job" --highlight quit \\
        --subject me-cutout.png --layout left --preview thumb-preview.png

    video-thumbnail frames talk.mp4 -o frames/ --count 12   # candidate stills + contact sheet

The background is an image or a video (one frame, --at seconds). Text size is fitted to the
layout box by measuring each candidate line with libass itself. The preview shows the result at
feed sizes on dark and light UI, with the YouTube duration badge drawn in. Warnings flag long
text, title repetition, the timestamp corner, the 3:4 grid crop of vertical covers, low
contrast, missing fonts and oversized files. Stdlib only, Python 3.9+.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FORMATS = {
    "youtube": (1920, 1080),
    "youtube-4k": (3840, 2160),
    "hd": (1920, 1080),
    "vertical": (1080, 1920),
    "portrait": (1080, 1350),
    "square": (1080, 1080),
}
ALIASES = {"shorts": "vertical", "reels": "vertical", "tiktok": "vertical", "linkedin": "hd", "x": "hd"}

# Text box per layout as (x0, y0, x1, y1) fractions of the frame, plus vertical anchoring.
# Landscape boxes keep the bottom-right corner free for the duration badge; vertical boxes stay
# inside the centered 3:4 crop that profile grids show.
BOXES_LANDSCAPE = {
    "left": ((0.055, 0.09, 0.56, 0.86), "middle"),
    "right": ((0.44, 0.09, 0.945, 0.74), "middle"),
    "top": ((0.06, 0.06, 0.94, 0.42), "top"),
    "bottom": ((0.06, 0.56, 0.78, 0.92), "bottom"),
    "center": ((0.08, 0.16, 0.92, 0.80), "middle"),
}
BOXES_VERTICAL = {
    "left": ((0.07, 0.16, 0.80, 0.48), "top"),
    "right": ((0.20, 0.16, 0.93, 0.48), "top"),
    "top": ((0.07, 0.16, 0.93, 0.44), "top"),
    "bottom": ((0.07, 0.54, 0.93, 0.80), "bottom"),
    "center": ((0.07, 0.32, 0.93, 0.68), "middle"),
}

# Style defaults. outline/shadow/pad are fractions of the font size.
STYLES = {
    # Heavy caps, thick black outline, hard drop shadow, highlight words in the accent color.
    "bold": dict(
        font="Poppins Black",
        case="upper",
        color="#FFFFFF",
        accent="#FFE600",
        outline_color="#000000",
        outline=0.075,
        shadow=0.055,
        darken=0.45,
        leading=0.12,
    ),
    # News / explainer look: each line on its own solid box.
    "box": dict(
        font="Poppins ExtraBold",
        case="asis",
        color="#0A0A0A",
        accent="#E11D48",
        outline_color="#FFFFFF",
        pad=0.16,
        darken=0.0,
        leading=0.10,
    ),
    # Premium / B2B: sentence case on a darkened side, no outline.
    "clean": dict(
        font="Poppins ExtraBold",
        case="asis",
        color="#FFFFFF",
        accent="#FFD54A",
        outline_color="#000000",
        outline=0.0,
        shadow=0.035,
        darken=0.72,
        leading=0.16,
    ),
}

STOP = set(
    "a an the and or but of to in on for with my your our is are was be this that it i you we "
    "how why what when do does did not no vs".split()
)


def warn(msg):
    print(f"video-thumbnail: warning: {msg}", file=sys.stderr)


def die(msg):
    sys.exit(f"video-thumbnail: {msg}")


# ---------------------------------------------------------------- tools


def libass_ffmpeg():
    """First ffmpeg with the libass `ass` filter: PATH, then Homebrew's keg-only ffmpeg-full."""
    for cand in (
        shutil.which("ffmpeg"),
        "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg",
        "/usr/local/opt/ffmpeg-full/bin/ffmpeg",
    ):
        if cand and Path(cand).exists():
            out = subprocess.run([cand, "-hide_banner", "-filters"], capture_output=True, text=True).stdout
            if re.search(r"^\s*\S+\s+ass\s", out, re.M):
                return cand
    return None


def ffprobe_for(ff):
    side = Path(ff).with_name("ffprobe")
    return str(side) if side.exists() else shutil.which("ffprobe")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        tail = "\n".join(r.stderr.strip().splitlines()[-6:])
        die(f"ffmpeg failed:\n{tail}")
    return r


def probe(ffprobe, path):
    out = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,pix_fmt,nb_frames:format=duration,format_name",
            "-of",
            "json",
            path,
        ],
        capture_output=True,
        text=True,
    )
    if out.returncode != 0:
        die(f"cannot read {path}: {out.stderr.strip()[-200:]}")
    d = json.loads(out.stdout)
    st = (d.get("streams") or [{}])[0]
    fmt = d.get("format", {})
    dur = float(fmt.get("duration") or 0)
    still = fmt.get("format_name", "").endswith("_pipe") or fmt.get("format_name") in ("image2", "png_pipe")
    return dict(
        w=st.get("width"),
        h=st.get("height"),
        pix_fmt=st.get("pix_fmt", ""),
        duration=dur,
        video=not still and dur > 0.5,
    )


def default_fontsdir():
    env = os.environ.get("OCTOMIND_FONTS_DIR")
    for cand in (env, str(Path.home() / ".local/share/octomind/fonts")):
        if cand and Path(cand).is_dir():
            return cand
    return None


def font_available(font, fontsdir):
    key = re.sub(r"[\s_-]", "", font).lower()
    if fontsdir and Path(fontsdir).is_dir():
        for f in Path(fontsdir).iterdir():
            if f.suffix.lower() in (".ttf", ".otf", ".ttc") and key in re.sub(r"[\s_-]", "", f.stem).lower():
                return True
    if shutil.which("fc-list"):
        fams = subprocess.run(["fc-list", ":", "family", "fullname"], capture_output=True, text=True).stdout
        return key in re.sub(r"[\s_-]", "", fams).lower()
    return False


def ass_color(hexcol, alpha=0):
    h = hexcol.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        die(f"bad color {hexcol!r}; use #RRGGBB")
    return f"&H{alpha:02X}{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def inline_color(hexcol):
    h = hexcol.lstrip("#")
    return f"&H{h[4:6]}{h[2:4]}{h[0:2]}&".upper()


def luminance(hexcol):
    h = hexcol.lstrip("#")
    return rel_lum(*(int(h[i : i + 2], 16) for i in (0, 2, 4)))


def rel_lum(r, g, b):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(l1, l2):
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def clean_text(s):
    return re.sub(r"[{}\\]", "", s).strip()


# ---------------------------------------------------------------- measuring

STYLE_FORMAT = (
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
    "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
    "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"
)


def ass_header(W, H, styles):
    return [
        "[Script Info]",
        "; generated by video-thumbnails/scripts/thumbnail.py",
        "ScriptType: v4.00+",
        f"PlayResX: {W}",
        f"PlayResY: {H}",
        "WrapStyle: 2",
        "ScaledBorderAndShadow: yes",
        # Frames are full-range RGB: no TV-range remap, so #FFFFFF stays 255.
        "YCbCr Matrix: None",
        "",
        "[V4+ Styles]",
        STYLE_FORMAT,
        *styles,
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]


def ass_time(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def measure(ff, tmp, font, strings, R=100):
    """Ink extents of each string at font size R, measured by rendering with libass.

    Each string is drawn white on black in its own frame; the frames come back as raw gray
    pixels and the bounding box of everything brighter than the background is the extent.
    Returns {string: (x_off, y_off, width, height)} in px at size R, relative to the anchor.
    """
    strings = list(dict.fromkeys(strings))
    longest = max(len(s) for s in strings)
    CW, CH, AX, AY = int(longest * R * 1.1) + 300, int(R * 3), 100, int(R * 0.8)
    CW += CW % 2
    styles = [
        f"Style: M,{font},{R},&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1"
    ]
    lines = ass_header(CW, CH, styles)
    for i, s in enumerate(strings, 1):
        lines.append(
            f"Dialogue: 0,{ass_time(i * 0.1 - 0.02)},{ass_time(i * 0.1 + 0.05)},M,,0,0,0,,"
            f"{{\\an7\\pos({AX},{AY})}}{s}"
        )
    name = "measure.ass"
    (tmp / name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    n = len(strings) + 1
    fd = ":fontsdir=fonts" if (tmp / "fonts").exists() else ""
    r = subprocess.run(
        [
            ff,
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"color=c=black:s={CW}x{CH}:r=10:d={n * 0.1 + 0.05:.2f}",
            "-vf",
            f"ass={name}{fd},format=gray",
            "-frames:v",
            str(n),
            "-f",
            "rawvideo",
            "-",
        ],
        capture_output=True,
        cwd=tmp,
    )
    size = CW * CH
    if r.returncode != 0 or len(r.stdout) < size * n:
        die(f"text measurement failed: {r.stderr.decode(errors='replace').strip()[-300:]}")
    ink = bytes(0 if v < 60 else 1 for v in range(256))
    out = {}
    for i, s in enumerate(strings, 1):
        frame = r.stdout[i * size : (i + 1) * size].translate(ink)
        rows = [y for y in range(CH) if frame.find(1, y * CW, (y + 1) * CW) != -1]
        if not rows:
            die(f"text measurement failed for {s!r}: nothing drawn (font missing glyphs?)")
        x1 = min(frame.find(1, y * CW, (y + 1) * CW) - y * CW for y in rows)
        x2 = max(frame.rfind(1, y * CW, (y + 1) * CW) - y * CW for y in rows)
        y1, y2 = rows[0], rows[-1]
        out[s] = (x1 - AX, y1 - AY, x2 - x1 + 1, y2 - y1 + 1)
    return out


def partitions(words, k):
    n = len(words)
    if k == 1:
        yield [words]
        return
    for i in range(1, n - k + 2):
        for rest in partitions(words[i:], k - 1):
            yield [words[:i]] + rest


def line_metrics(st, meas, R):
    """Cap top below the anchor and the visual line height, as fractions of the font size.

    Caps-only text is as tall as an H; mixed case runs from the top of H to the bottom of g.
    Lines are stacked on these, so baselines stay evenly spaced whatever the letters are.
    """
    cap_top = meas["H"][1] / R
    vis = (meas["H"][3] if st["case"] == "upper" else meas["Hg"][3]) / R
    return cap_top, vis


def fit(words, box_w, box_h, meas, st, style, R, max_lines, fs_max, fs_min):
    """Pick the line split that allows the largest font size inside the box."""
    _, vis = line_metrics(st, meas, R)
    best = None
    for k in range(1, min(max_lines, len(words)) + 1):
        for part in partitions(words, k):
            lines = [" ".join(p) for p in part]
            ink = max(meas[ln][2] for ln in lines) / R
            if style == "box":
                wf = ink + 2 * st["pad"]
                hf = k * (vis + 1.5 * st["pad"]) + (k - 1) * st["leading"]
            else:
                o, sh = st["outline"], st["shadow"]
                wf = ink + 2 * o + sh
                hf = k * vis + (k - 1) * st["leading"] + 2 * o + sh
            fs = min(box_w / wf, box_h / hf, fs_max)
            widths = [meas[ln][2] for ln in lines]
            balance = min(widths) / max(widths) if k > 1 else 1.0
            # A line that ends on "I", "the", "my"... reads as a broken phrase.
            dangling = any(re.sub(r"[^\w]", "", p[-1]).lower() in STOP for p in part[:-1])
            score = fs * (1 - 0.05 * (k - 1)) * (0.85 + 0.15 * balance) * (0.85 if dangling else 1.0)
            if best is None or score > best[0]:
                best = (score, fs, lines)
    _, fs, lines = best
    if fs < fs_min:
        warn(f"text only fits at {fs:.0f}px; cut words so it reads at feed size")
    return lines, fs


def rounded_rect(w, h, r):
    w, h, r = int(round(w)), int(round(h)), int(round(r))
    return (
        f"m {r} 0 l {w - r} 0 b {w} 0 {w} 0 {w} {r} l {w} {h - r} b {w} {h} {w} {h} {w - r} {h} "
        f"l {r} {h} b 0 {h} 0 {h} 0 {h - r} l 0 {r} b 0 0 0 0 {r} 0"
    )


# ---------------------------------------------------------------- rendering


def styled_line(line, highlights, st):
    out = []
    for w in line.split(" "):
        key = re.sub(r"[^\w]", "", w).lower()
        if key and key in highlights:
            out.append(f"{{\\c{inline_color(st['accent'])}}}{w}{{\\c{inline_color(st['color'])}}}")
        else:
            out.append(w)
    return " ".join(out)


def gradient_expr(layout, strength):
    a = f"{strength:.3f}*255"
    if layout == "left":
        return f"{a}*clip((0.80*W-X)/(0.45*W),0,1)"
    if layout == "right":
        return f"{a}*clip((X-0.20*W)/(0.45*W),0,1)"
    if layout == "top":
        return f"{a}*clip((0.66*H-Y)/(0.46*H),0,1)"
    if layout == "bottom":
        return f"{a}*clip((Y-0.34*H)/(0.46*H),0,1)"
    return f"{a}*0.6"


def region_luma(ff, tmp, img, x, y, w, h):
    r = subprocess.run(
        [
            ff,
            "-v",
            "error",
            "-i",
            str(img),
            "-vf",
            f"crop={max(2, int(w))}:{max(2, int(h))}:{int(x)}:{int(y)},scale=1:1:flags=area,format=rgb24",
            "-f",
            "rawvideo",
            "-",
        ],
        capture_output=True,
        cwd=tmp,
    )
    if r.returncode != 0 or len(r.stdout) < 3:
        return None
    return rel_lum(*r.stdout[:3])


def jpeg_out(ff, src, out, max_bytes):
    for q in (2, 3, 4, 5, 6, 8, 10, 13):
        run([ff, "-v", "error", "-y", "-i", str(src), "-q:v", str(q), "-pix_fmt", "yuvj420p", str(out)])
        if not max_bytes or out.stat().st_size <= max_bytes:
            return q
    warn(f"{out} is still {out.stat().st_size} bytes at the lowest quality tried")
    return q


def preview(ff, img, out, W, H):
    """Thumbnail at feed sizes on dark and light UI, duration badge drawn bottom-right."""
    vertical = H > W
    if vertical:
        # Full 9:16 at 180 wide plus the centered 3:4 grid crop at 150 wide.
        g = (
            "[0:v]split=4[a][b][c][d];"
            "[a]scale=180:-2[a1];[b]crop=iw:iw*4/3,scale=150:-2[b1];"
            "[c]scale=180:-2[c1];[d]crop=iw:iw*4/3,scale=150:-2[d1];"
            "color=c=0x0F0F0F:s=402x368[dk];color=c=0xFFFFFF:s=402x368[lt];"
            "[dk][a1]overlay=24:24[dk1];[dk1][b1]overlay=228:24[dk2];"
            "[lt][c1]overlay=24:24[lt1];[lt1][d1]overlay=228:24[lt2];"
            "[dk2][lt2]hstack[out]"
        )
    else:
        badge = "drawbox=x=iw*0.84:y=ih*0.80:w=iw*0.13:h=ih*0.14:color=black@0.82:t=fill"
        g = (
            "[0:v]split=4[a][b][c][d];"
            f"[a]scale=360:-2,{badge}[a1];[b]scale=168:-2,{badge}[b1];"
            f"[c]scale=360:-2,{badge}[c1];[d]scale=168:-2,{badge}[d1];"
            "color=c=0x0F0F0F:s=600x250[dk];color=c=0xFFFFFF:s=600x250[lt];"
            "[dk][a1]overlay=24:24[dk1];[dk1][b1]overlay=408:24[dk2];"
            "[lt][c1]overlay=24:24[lt1];[lt1][d1]overlay=408:24[lt2];"
            "[dk2][lt2]vstack[out]"
        )
    run(
        [
            ff,
            "-v",
            "error",
            "-y",
            "-i",
            str(img),
            "-filter_complex",
            g,
            "-map",
            "[out]",
            "-frames:v",
            "1",
            str(out),
        ]
    )


def cmd_render(args):
    ff = libass_ffmpeg()
    if not ff:
        die(
            "no ffmpeg with libass found (needed for the `ass` filter). macOS: brew install ffmpeg-full; "
            "Debian/Ubuntu/Fedora/Arch: the distro ffmpeg package includes it."
        )
    ffprobe = ffprobe_for(ff)
    if not ffprobe:
        die("ffprobe not found next to ffmpeg or on PATH")
    fmt = ALIASES.get(args.format, args.format)
    W, H = FORMATS[fmt]
    vertical = H > W
    st = dict(STYLES[args.style])
    for k in ("color", "accent", "case", "font", "darken"):
        v = getattr(args, k)
        if v is not None:
            st[k] = v
    if args.box_color:
        st["outline_color"] = args.box_color
    fontsdir = args.fontsdir or default_fontsdir()
    if not font_available(st["font"], fontsdir):
        warn(f"font '{st['font']}' not found in fonts dir or fontconfig; libass will substitute a fallback")

    text = clean_text(args.text)
    if not text:
        die("--text is empty")
    if st["case"] == "upper":
        text = text.upper()
    words = text.split()
    highlights = set()
    for h in args.highlight or []:
        highlights.update(re.sub(r"[^\w]", "", w).lower() for w in h.split())
    limit = 6 if vertical else 5
    if len(words) > limit:
        warn(
            f"{len(words)} words of overlay text; {limit} or fewer read at feed size — the title carries the rest"
        )
    if args.title:
        tw = {w for w in re.findall(r"\w+", args.title.lower()) if w not in STOP}
        ow = [w for w in re.findall(r"\w+", text.lower()) if w not in STOP]
        if ow and sum(w in tw for w in ow) / len(ow) >= 0.6:
            warn("overlay text mostly repeats the title; make it add something the title doesn't say")

    bg = probe(ffprobe, args.background)
    subject = None
    if args.subject:
        subject = probe(ffprobe, args.subject)
        alpha_fmts = ("rgba", "bgra", "argb", "abgr", "ya8", "ya16", "yuva", "gbrap", "pal8", "rgba64")
        if not subject["pix_fmt"].startswith(alpha_fmts):
            warn(f"--subject {args.subject} has no alpha channel ({subject['pix_fmt']}); use a cut-out PNG")

    boxes = BOXES_VERTICAL if vertical else BOXES_LANDSCAPE
    (fx0, fy0, fx1, fy1), anchor = boxes[args.layout]
    if not vertical and not fmt.startswith("youtube"):
        # No duration badge outside YouTube: bottom and right boxes may use the full width/height.
        fx1 = 0.94 if args.layout == "bottom" else fx1
        fy1 = 0.86 if args.layout == "right" else fy1
    bx0, by0, bx1, by1 = fx0 * W, fy0 * H, fx1 * W, fy1 * H
    box_w, box_h = bx1 - bx0, by1 - by0

    R = 100
    with tempfile.TemporaryDirectory(prefix="vthumb-") as td:
        tmp = Path(td)
        if fontsdir:
            os.symlink(os.path.abspath(fontsdir), tmp / "fonts")
        cands = {"H", "Hg"}
        for k in range(1, min(args.lines, len(words)) + 1):
            for part in partitions(words, k):
                cands.update(" ".join(p) for p in part)
        meas = measure(ff, tmp, st["font"], sorted(cands), R=R)
        fs_max = H * (0.13 if vertical else 0.30)
        fs_min = H * (0.040 if vertical else 0.085)
        lines, fs = fit(words, box_w, box_h, meas, st, args.style, R, args.lines, fs_max, fs_min)
        fs = int(fs)

        # Placement from measured extents: every line sits on the same cap/descender grid, and
        # boxes hug the letters instead of the font's tall line box.
        k = len(lines)
        box = args.style == "box"
        cap_top, vis = line_metrics(st, meas, R)
        vis_px, gap = vis * fs, st["leading"] * fs
        pad_h = st.get("pad", 0) * fs if box else 0
        pad_v = pad_h * 0.75
        o_px = 0 if box else st["outline"] * fs
        sh_px = 0 if box else st["shadow"] * fs
        row_h = vis_px + 2 * pad_v
        block_h = k * row_h + (k - 1) * gap + 2 * o_px + sh_px
        if anchor == "top":
            top = by0
        elif anchor == "bottom":
            top = by1 - block_h
        else:
            top = by0 + (box_h - block_h) / 2
        cx = (bx0 + bx1) / 2
        events = []
        block = [W, H, 0, 0]  # x0, y0, x1, y1 of the text block
        for i, ln in enumerate(lines):
            ink_x, ink_w = meas[ln][0] / R * fs, meas[ln][2] / R * fs
            cw = ink_w + 2 * pad_h
            if args.layout == "left":
                x0 = bx0 + o_px
            elif args.layout == "right":
                x0 = bx1 - o_px - sh_px - cw
            else:
                x0 = cx - cw / 2
            row_top = top + o_px + i * (row_h + gap)
            if box:
                r = min(row_h * 0.12, pad_h * 0.5)
                events.append(
                    f"Dialogue: 0,{ass_time(0)},{ass_time(10)},B,,0,0,0,,"
                    f"{{\\an7\\pos({x0:.1f},{row_top:.1f})\\p1}}{rounded_rect(cw, row_h, r)}{{\\p0}}"
                )
            tx, ty = x0 + pad_h - ink_x, row_top + pad_v - cap_top * fs
            events.append(
                f"Dialogue: 1,{ass_time(0)},{ass_time(10)},T,,0,0,0,,"
                f"{{\\an7\\pos({tx:.1f},{ty:.1f})}}{styled_line(ln, highlights, st)}"
            )
            block = [
                min(block[0], x0 - o_px),
                top,
                max(block[2], x0 + cw + o_px + sh_px),
                top + block_h,
            ]

        outline, shadow = (0, 0) if box else (round(o_px, 1), round(sh_px, 1))
        styles = [
            f"Style: T,{st['font']},{fs},{ass_color(st['color'])},{ass_color(st['color'])},"
            f"{ass_color(st['outline_color'])},{ass_color('#000000', 0x30)},0,0,0,0,100,100,"
            f"{args.spacing},0,1,{outline},{shadow},7,0,0,0,1",
            f"Style: B,{st['font']},{fs},{ass_color(st['outline_color'])},{ass_color(st['outline_color'])},"
            f"{ass_color(st['outline_color'])},{ass_color('#000000', 0xFF)},0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        ]
        (tmp / "text.ass").write_text("\n".join(ass_header(W, H, styles) + events) + "\n", encoding="utf-8")

        # Stage 1: background (+ grade, gradient, subject). Stage 2: text.
        inputs = []
        if bg["video"]:
            at = args.at if args.at is not None else bg["duration"] * 0.33
            inputs += ["-ss", f"{at:.3f}", "-i", os.path.abspath(args.background)]
        else:
            inputs += ["-i", os.path.abspath(args.background)]
        g = [
            f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={W}:{H}:(iw-{W})*{args.crop_x}:(ih-{H})*{args.crop_y},setsar=1"
            + (",eq=contrast=1.06:saturation=1.18,unsharp=5:5:0.45" if args.grade == "pop" else "")
            + ",format=rgba[bg0]"
        ]
        last = "bg0"
        if st["darken"] > 0:
            g.append(
                f"color=c=black:s={W}x{H}:d=1,format=rgba,"
                f"geq=r=0:g=0:b=0:a='{gradient_expr(args.layout, st['darken'])}'[grad]"
            )
            g.append(f"[{last}][grad]overlay=0:0:format=auto[bg1]")
            last = "bg1"
        if subject:
            inputs += ["-i", os.path.abspath(args.subject)]
            scale = args.subject_scale if args.subject_scale is not None else (0.62 if vertical else 0.92)
            sh_ = int(H * scale) // 2 * 2
            sw_ = max(2, int(subject["w"] * sh_ / subject["h"]) // 2 * 2)
            P = max(args.stroke, 0) + 4
            if vertical or args.layout in ("top", "bottom", "center"):
                sx = (W - sw_) / 2
            elif args.layout == "left":
                sx = W - sw_ - W * 0.02
            else:
                sx = W * 0.02
            if args.subject_x is not None:
                sx = args.subject_x * W - sw_ / 2
            sy = H - sh_ + H * 0.02
            x, y = int(sx - P), int(sy - P)
            g.append(
                f"[1:v]format=rgba,scale={sw_}:{sh_}:flags=lanczos,"
                f"pad=iw+{2 * P}:ih+{2 * P}:{P}:{P}:color=black@0[sp]"
            )
            if args.stroke > 0:
                sig = max(args.stroke / 1.86, 0.5)
                g.append("[sp]split=3[sa][sb][sc]")
                g.append(
                    f"[sb]alphaextract,gblur=sigma={sig:.2f},lut=y='if(gt(val,8),255,0)',gblur=sigma=0.7[m]"
                )
                g.append(f"[sc]alphaextract,gblur=sigma={max(H * 0.012, 2):.1f},lut=y='val*0.55'[shm]")
                g.append(f"color=c={args.stroke_color}:s={sw_ + 2 * P}x{sh_ + 2 * P}:d=1,format=rgba[scol]")
                g.append(f"color=c=black:s={sw_ + 2 * P}x{sh_ + 2 * P}:d=1,format=rgba[shcol]")
                g.append("[scol][m]alphamerge[ol]")
                g.append("[shcol][shm]alphamerge[shd]")
                off = int(H * 0.008)
                g.append(f"[{last}][shd]overlay={x + off}:{y + off}:format=auto[bg2]")
                g.append(f"[bg2][ol]overlay={x}:{y}:format=auto[bg3]")
                g.append(f"[bg3][sa]overlay={x}:{y}:format=auto[bg4]")
            else:
                g.append(f"[{last}][sp]overlay={x}:{y}:format=auto[bg4]")
            last = "bg4"
        g.append(f"[{last}]format=rgb24[out]")
        stage1 = tmp / "stage1.png"
        run(
            [
                ff,
                "-v",
                "error",
                "-y",
                *inputs,
                "-filter_complex",
                ";".join(g),
                "-map",
                "[out]",
                "-frames:v",
                "1",
                str(stage1),
            ],
            cwd=tmp,
        )

        # Contrast under the text block (outline and boxes carry their own contrast).
        if args.style == "clean":
            lum = region_luma(ff, tmp, stage1, block[0], block[1], block[2] - block[0], block[3] - block[1])
            if lum is not None:
                c = contrast(lum, luminance(st["color"]))
                if c < 4.5:
                    warn(
                        f"text-to-background contrast ~{c:.1f}:1 under the text; raise --darken or use --style bold"
                    )

        fd = ":fontsdir=fonts" if fontsdir else ""
        final = tmp / "final.png"
        run(
            [
                ff,
                "-v",
                "error",
                "-y",
                "-i",
                str(stage1),
                "-vf",
                f"ass=text.ass{fd}",
                "-frames:v",
                "1",
                str(final),
            ],
            cwd=tmp,
        )

        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        # YouTube: 2 MB is the mobile-upload cap (desktop takes 50 MB); 4K output targets desktop.
        caps = {"youtube": 2_000_000, "youtube-4k": 50_000_000}
        max_bytes = args.max_bytes if args.max_bytes is not None else caps.get(fmt, 0)
        if out.suffix.lower() in (".jpg", ".jpeg"):
            q = jpeg_out(ff, final, out, max_bytes)
        else:
            shutil.copyfile(final, out)
            q = None
            if max_bytes and out.stat().st_size > max_bytes:
                warn(f"{out} is {out.stat().st_size} bytes (limit {max_bytes}); write .jpg instead")
        if args.keep_ass:
            shutil.copyfile(tmp / "text.ass", out.with_suffix(".ass"))
        if args.preview:
            preview(ff, out, Path(args.preview), W, H)

    # Placement checks on the final geometry.
    if fmt.startswith("youtube"):
        if block[2] > W * 0.82 and block[3] > H * 0.78:
            warn("text block reaches the bottom-right corner, where YouTube draws the duration badge")
    if vertical and (block[1] < H * 0.125 or block[3] > H * 0.875):
        warn(
            "text block leaves the centered 3:4 area that profile grids show; use --layout top/center/bottom"
        )
    small_w = 124 if vertical else 168
    ink_px = vis_px * small_w / W
    if ink_px < 8:
        warn(f"text is ~{ink_px:.0f}px tall at {small_w}px-wide feed size; cut words or enlarge")
    qn = f", jpeg q{q}" if q else ""
    print(
        f"video-thumbnail: {W}x{H} {fmt}, {args.style}/{args.layout}, {len(lines)} line(s) at {fs}px"
        f"{qn}, {out.stat().st_size // 1024} KB -> {out}"
        + (f" (+ preview {args.preview})" if args.preview else ""),
        file=sys.stderr,
    )
    print("lines: " + " | ".join(lines))


def cmd_frames(args):
    ff = libass_ffmpeg() or shutil.which("ffmpeg")
    if not ff:
        die("ffmpeg not found")
    ffprobe = ffprobe_for(ff)
    info = probe(ffprobe, args.video)
    if not info["video"]:
        die(f"{args.video} is not a video")
    d = info["duration"]
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    n = max(1, args.count)
    seg = d * 0.9 / n
    shots = []
    for i in range(n):
        start = d * 0.05 + i * seg
        # thumbnail= picks the most representative frame of the window (skips flashes and blends);
        # showinfo reports its timestamp. PNG keeps the still lossless for use as a background.
        dst = outdir / f"frame-{i + 1:02d}.png"
        r = run(
            [
                ff,
                "-hide_banner",
                "-y",
                "-copyts",
                "-ss",
                f"{start:.2f}",
                "-t",
                f"{max(seg, 0.5):.2f}",
                "-i",
                args.video,
                "-vf",
                "fps=4,thumbnail=n=40,showinfo",
                "-frames:v",
                "1",
                str(dst),
            ]
        )
        m = re.search(r"pts_time:([\d.]+)", r.stderr)
        shots.append((dst, float(m.group(1)) if m else start))
    cols = 4 if n > 6 else 2 if n == 4 else max(1, min(n, 3))
    rows = -(-n // cols)
    sheet = outdir / "sheet.jpg"
    run(
        [
            ff,
            "-v",
            "error",
            "-y",
            "-framerate",
            "1",
            "-i",
            str(outdir / "frame-%02d.png"),
            "-vf",
            f"scale=480:-2,pad=iw+8:ih+8:4:4:color=white,tile={cols}x{rows}",
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(sheet),
        ]
    )
    for i, (p, t) in enumerate(shots, 1):
        print(f"{i:02d}  at {t:8.2f}s  {p}")
    print(f"sheet: {sheet} ({cols}x{rows}, numbered left to right, top to bottom)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("render", help="render a thumbnail or cover")
    r.add_argument("background", help="background image, or a video (one frame at --at)")
    r.add_argument("-o", "--out", required=True, help="output .jpg (YouTube) or .png")
    r.add_argument("--text", required=True, help="overlay text, ideally 2-5 words")
    r.add_argument("--highlight", action="append", help="word(s) to color with the accent (repeatable)")
    r.add_argument("--format", default="youtube", choices=sorted(set(FORMATS) | set(ALIASES)))
    r.add_argument("--layout", default="left", choices=["left", "right", "top", "bottom", "center"])
    r.add_argument("--style", default="bold", choices=sorted(STYLES))
    r.add_argument("--subject", help="cut-out PNG with alpha (person or product), placed opposite the text")
    r.add_argument(
        "--subject-scale",
        type=float,
        help="subject height as a fraction of the frame (default 0.92; 0.62 vertical)",
    )
    r.add_argument("--subject-x", type=float, help="subject center as a fraction of the width")
    r.add_argument("--stroke", type=int, default=0, help="sticker outline around the subject, px")
    r.add_argument("--stroke-color", default="white")
    r.add_argument("--at", type=float, help="seconds into a video background (default: a third in)")
    r.add_argument(
        "--crop-x", type=float, default=0.5, help="horizontal crop anchor 0-1 when the aspect differs"
    )
    r.add_argument("--crop-y", type=float, default=0.5, help="vertical crop anchor 0-1")
    r.add_argument("--darken", type=float, help="gradient strength behind the text, 0-1 (default: style)")
    r.add_argument("--grade", default="pop", choices=["pop", "none"], help="contrast/saturation/sharpen pass")
    r.add_argument("--color", help="text #RRGGBB")
    r.add_argument("--accent", help="highlight #RRGGBB")
    r.add_argument("--box-color", help="outline (bold) or box (box style) #RRGGBB")
    r.add_argument("--case", choices=["upper", "asis"])
    r.add_argument("--font", help="font family (default: style)")
    r.add_argument("--fontsdir", help="directory with font files (default: ~/.local/share/octomind/fonts)")
    r.add_argument("--spacing", type=float, default=0, help="letter spacing px")
    r.add_argument("--lines", type=int, default=3, choices=[1, 2, 3], help="maximum text lines")
    r.add_argument("--title", help="the video title, to flag overlay text that just repeats it")
    r.add_argument("--preview", help="write a feed-size preview PNG (dark + light UI)")
    r.add_argument("--max-bytes", type=int, help="file size cap (default: 2 MB youtube, 50 MB youtube-4k)")
    r.add_argument("--keep-ass", action="store_true", help="keep the text layer as .ass next to the output")
    r.set_defaults(fn=cmd_render)

    f = sub.add_parser("frames", help="export candidate stills from a video plus a contact sheet")
    f.add_argument("video")
    f.add_argument("-o", "--out", required=True, help="output directory")
    f.add_argument("--count", type=int, default=12)
    f.set_defaults(fn=cmd_frames)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

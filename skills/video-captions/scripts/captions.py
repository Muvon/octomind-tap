#!/usr/bin/env python3
"""Word-timed social captions: word-timing JSON -> styled ASS for ffmpeg's libass.

Reads word timings from whisper-ctranslate2 / faster-whisper / openai-whisper /
WhisperX JSON, OpenAI verbose_json, whisper.cpp -ojf, AssemblyAI, Deepgram,
ElevenLabs Scribe or TTS alignment, Remotion Caption[] JSON, or (approximate)
SRT/VTT. Groups words into short pages and writes an ASS subtitle file with an
animated active-word highlight, ready to burn with:

    ffmpeg -i in.mp4 -vf "ass=captions.ass:fontsdir=fonts" ... out.mp4

Optional sidecars: --srt (platform upload / accessibility) and --remotion
(Caption[] JSON for @remotion/captions). Stdlib only, Python 3.9+.
"""

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

FILLERS = {"um", "uh", "uhm", "umm", "erm", "er", "hmm", "mm", "ah"}

# Per-preset defaults. size/outline/shadow are fractions of the shorter frame
# side, so the same preset reads the same at 1080x1920 and 1920x1080.
PRESETS = {
    # TikTok / Reels "pop": 1-3 words, active word recolored and scaled up.
    "pop": dict(
        size=0.095,
        max_words=3,
        line_chars=14,
        lines=2,
        case="upper",
        punct="strip",
        color="#FFFFFF",
        highlight="#FFE600",
        outline_color="#000000",
        outline=0.085,
        shadow=0.030,
        border_style=1,
        scale=112,
    ),
    # Karaoke fill: page stays up, spoken words switch to the highlight color.
    "karaoke": dict(
        size=0.085,
        max_words=5,
        line_chars=16,
        lines=2,
        case="upper",
        punct="strip",
        color="#FFFFFF",
        highlight="#39FF14",
        outline_color="#000000",
        outline=0.085,
        shadow=0.030,
        border_style=1,
        scale=100,
    ),
    # One big word at a time with a scale-in.
    "word": dict(
        size=0.115,
        max_words=1,
        line_chars=12,
        lines=1,
        case="upper",
        punct="strip",
        color="#FFFFFF",
        highlight="#FFFFFF",
        outline_color="#000000",
        outline=0.090,
        shadow=0.035,
        border_style=1,
        scale=100,
    ),
    # TikTok-native text box behind each line, active word recolored.
    "box": dict(
        size=0.065,
        max_words=4,
        line_chars=18,
        lines=2,
        case="asis",
        punct="keep",
        color="#000000",
        highlight="#FE2C55",
        outline_color="#FFFFFF",
        outline=0.22,
        shadow=0.0,
        border_style=3,
        scale=100,
    ),
    # Accessible sentence captions on a translucent box (explainers, 16:9).
    "clean": dict(
        size=0.050,
        max_words=14,
        line_chars=42,
        lines=2,
        case="asis",
        punct="keep",
        color="#FFFFFF",
        highlight="#FFFFFF",
        outline_color="#000000",
        outline=0.18,
        shadow=0.0,
        border_style=3,
        scale=100,
        box_alpha=0x50,
    ),
}


@dataclass
class Word:
    text: str
    start: float
    end: float


def warn(msg):
    print(f"captions: {msg}", file=sys.stderr)


# ---------------------------------------------------------------- loading


def _words_from_items(items, units):
    scale = 0.001 if units == "ms" else 1.0
    out = []
    for it in items:
        if it.get("type") not in (None, "word"):  # ElevenLabs spacing / audio_event
            continue
        text = next((it[k] for k in ("punctuated_word", "word", "text") if it.get(k)), "")
        s, e = it.get("start"), it.get("end")
        out.append(Word(str(text), None if s is None else s * scale, None if e is None else e * scale))
    return out


def _detect_units(data, items, forced):
    if forced != "auto":
        return forced
    if isinstance(data, dict) and "audio_duration" in data:  # AssemblyAI transcript
        return "ms"
    ends = [it.get("end") for it in items if isinstance(it.get("end"), (int, float))]
    if ends and all(isinstance(v, int) for v in ends) and max(ends) > 50:
        return "ms"
    return "s"


def _join_tokens(tokens):
    """Merge subword tokens (leading space starts a new word) into words."""
    words = []
    for text, s, e in tokens:
        if not text or text.startswith("[_") or text.startswith("<|"):
            continue
        if text[0].isspace() or not words:
            words.append(Word(text.strip(), s, e))
        else:
            words[-1].text += text
            words[-1].end = e
    return words


def _from_alignment(al):
    words, cur = [], None
    for c, s, e in zip(
        al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    ):
        if c.isspace():
            cur = None
            continue
        if cur is None:
            cur = Word(c, s, e)
            words.append(cur)
        else:
            cur.text += c
            cur.end = e
    return words


_TS = re.compile(r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{3})")


def _ts(s):
    m = _TS.search(s)
    h, mi, se, ms = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + se + ms / 1000


def _interpolate(cues):
    warn(
        "segment-level input: word timing is interpolated by length and only approximate; "
        "prefer a word-timestamp transcript"
    )
    words = []
    for text, s, e in cues:
        toks = re.sub(r"<[^>]+>", "", text).split()
        if not toks:
            continue
        weights = [len(t) + 1 for t in toks]
        total, t = sum(weights), s
        for tok, w in zip(toks, weights):
            d = (e - s) * w / total
            words.append(Word(tok, t, t + d))
            t += d
    return words


def _parse_subs(text):
    cues = []
    for block in re.split(r"\n\s*\n", text.replace("\r", "")):
        lines = [ln for ln in block.strip().split("\n") if ln.strip()]
        for i, ln in enumerate(lines):
            if "-->" in ln:
                a, b = ln.split("-->", 1)
                cues.append((" ".join(lines[i + 1 :]), _ts(a), _ts(b)))
                break
    return cues


def load_words(path, units):
    raw = Path(path).read_text(encoding="utf-8")
    if Path(path).suffix.lower() in (".srt", ".vtt"):
        return _interpolate(_parse_subs(raw))
    data = json.loads(raw)
    if isinstance(data, list):  # Remotion Caption[] or a bare words array
        if data and "startMs" in data[0]:
            return _join_tokens([(c["text"], c["startMs"] / 1000, c["endMs"] / 1000) for c in data])
        return _words_from_items(data, _detect_units(data, data, units))
    for key in ("alignment", "normalized_alignment"):  # ElevenLabs TTS with-timestamps
        if isinstance(data.get(key), dict) and "characters" in data[key]:
            return _from_alignment(data[key])
    if "transcription" in data:  # whisper.cpp --output-json-full
        toks = []
        for seg in data["transcription"]:
            for tok in seg.get("tokens", []):
                off = tok.get("offsets") or {}
                toks.append((tok.get("text", ""), off.get("from", 0) / 1000, off.get("to", 0) / 1000))
        return _join_tokens(toks)
    if "results" in data:  # Deepgram
        items = data["results"]["channels"][0]["alternatives"][0].get("words", [])
        return _words_from_items(items, "s")
    if data.get("words"):  # OpenAI verbose_json, AssemblyAI, ElevenLabs Scribe
        return _words_from_items(data["words"], _detect_units(data, data["words"], units))
    if "segments" in data:  # faster-whisper / whisper-ctranslate2 / openai-whisper / WhisperX
        items = [w for seg in data["segments"] for w in (seg.get("words") or [])]
        if items:
            return _words_from_items(items, "s")
        return _interpolate([(s["text"], s["start"], s["end"]) for s in data["segments"]])
    sys.exit(
        "captions: unrecognised JSON shape (expected words / segments[].words / "
        "transcription / alignment / Caption[])"
    )


# ---------------------------------------------------------------- cleanup


def clean(words, args):
    reps = []
    for r in args.replace:
        if "=" not in r:
            sys.exit(f"captions: --replace needs FROM=TO, got {r!r}")
        frm, to = r.split("=", 1)
        reps.append((re.compile(rf"(?<!\w){re.escape(frm)}(?!\w)", re.I), to))

    out = []
    for w in words:
        text = re.sub(r"[{}\\]", "", w.text).strip()
        if not text:
            continue
        if args.drop_fillers and re.sub(r"[^\w']", "", text).lower() in FILLERS:
            continue
        if re.fullmatch(r"[^\w]+", text) and out:  # bare punctuation token
            out[-1].text += text
            continue
        for pat, to in reps:
            text = pat.sub(to, text)
        out.append(Word(text, w.start, w.end))

    # Fill missing timings (WhisperX leaves numerals unaligned) from neighbours.
    for i, w in enumerate(out):
        if w.start is None:
            w.start = out[i - 1].end if i and out[i - 1].end is not None else 0.0
        if w.end is None:
            nxt = next((x.start for x in out[i + 1 :] if x.start is not None), None)
            w.end = nxt if nxt is not None and nxt > w.start else w.start + 0.25

    prev = None
    for w in out:
        w.start += args.offset
        w.end += args.offset
        if prev is not None:
            w.start = max(w.start, prev.start + 0.01)
            if prev.end > w.start:
                prev.end = w.start
        if w.end - w.start < 0.06:
            w.end = w.start + 0.06
        prev = w
    return out


# ---------------------------------------------------------------- paging


def paginate(words, max_words, max_chars, max_gap, max_dur):
    pages, cur = [], []
    for w in words:
        if cur:
            chars = len(" ".join(x.text for x in cur)) + 1 + len(w.text)
            if (
                len(cur) >= max_words
                or chars > max_chars
                or w.start - cur[-1].end > max_gap
                or w.end - cur[0].start > max_dur
                or re.search(r"[.!?…]$", cur[-1].text)
                or (len(cur) >= 2 and cur[-1].text.endswith(","))
            ):
                pages.append(cur)
                cur = []
        cur.append(w)
    if cur:
        pages.append(cur)
    return pages


def split_lines(tokens, line_chars, lines):
    if lines < 2 or len(tokens) < 2 or len(" ".join(tokens)) <= line_chars:
        return [list(range(len(tokens)))]
    # Most balanced split; on a tie keep more words on the top line.
    k = min(
        range(1, len(tokens)),
        key=lambda k: (max(len(" ".join(tokens[:k])), len(" ".join(tokens[k:]))), -k),
    )
    return [list(range(k)), list(range(k, len(tokens)))]


def wrap_text(text, width):
    out, line = [], ""
    for tok in text.split():
        if line and len(line) + 1 + len(tok) > width:
            out.append(line)
            line = tok
        else:
            line = f"{line} {tok}".strip()
    if line:
        out.append(line)
    return "\\N".join(out)


# ---------------------------------------------------------------- ASS


def ass_color(hexcol, alpha=0):
    h = hexcol.lstrip("#")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        sys.exit(f"captions: colors are #RRGGBB, got {hexcol!r}")
    return f"&H{alpha:02X}{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def inline_color(hexcol):
    h = hexcol.lstrip("#")
    return f"&H{h[4:6]}{h[2:4]}{h[0:2]}&".upper()


def ass_time(t):
    cs = max(0, int(round(t * 100)))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def display(text, p):
    if p["punct"] == "strip":  # bold styles drop trailing , . ; : but keep ? !
        text = re.sub(r"[,.;:…]+$", "", text) or text
    case = p["case"]
    return text.upper() if case == "upper" else text.lower() if case == "lower" else text


def build_events(pages, p, args, x, y):
    events = []
    hl = inline_color(p["highlight"])
    pos = f"\\an5\\pos({x},{y})"
    for pi, page in enumerate(pages):
        nxt = pages[pi + 1][0].start if pi + 1 < len(pages) else None
        end = page[-1].end + args.hold
        if nxt is not None and nxt - page[-1].end <= args.max_gap:
            end = nxt  # bridge short pauses so the caption block doesn't flicker
        elif nxt is not None:
            end = min(end, nxt)
        tokens = [display(w.text, p) for w in page]
        rows = split_lines(tokens, p["line_chars"], p["lines"])

        if args.preset == "karaoke":
            parts = []
            for idxs in rows:
                seg = []
                for i in idxs:
                    until = page[i + 1].start if i + 1 < len(page) else end
                    seg.append(f"{{\\k{max(1, round((until - page[i].start) * 100))}}}{tokens[i]}")
                parts.append(" ".join(seg))
            events.append((page[0].start, end, f"{{{pos}}}" + "\\N".join(parts)))
            continue

        if args.preset == "clean":
            text = "\\N".join(" ".join(tokens[i] for i in idxs) for idxs in rows)
            events.append((page[0].start, end, f"{{{pos}\\fad(80,60)}}{text}"))
            continue

        for i, w in enumerate(page):
            w_end = page[i + 1].start if i + 1 < len(page) else end
            if args.preset == "word":
                events.append(
                    (w.start, w_end, f"{{{pos}\\fscx72\\fscy72\\t(0,90,\\fscx100\\fscy100)}}{tokens[i]}")
                )
                continue
            sc = p["scale"]
            grow = (
                f"\\fscx100\\fscy100\\t(0,70,\\fscx{sc + 6}\\fscy{sc + 6})\\t(70,140,\\fscx{sc}\\fscy{sc})"
                if sc != 100
                else ""
            )
            intro = "\\fscx92\\fscy92\\t(0,80,\\fscx100\\fscy100)" if i == 0 else ""
            parts = []
            for idxs in rows:
                seg = []
                for j in idxs:
                    seg.append(f"{{\\c{hl}{grow}}}{tokens[j]}{{\\r}}" if j == i else tokens[j])
                parts.append(" ".join(seg))
            events.append((w.start, w_end, f"{{{pos}{intro}}}" + "\\N".join(parts)))
    return events


def write_ass(path, events, p, args, W, H, hook):
    short = min(W, H)
    size = args.size or round(short * p["size"])
    outline = round(size * p["outline"], 1)
    shadow = round(size * p["shadow"], 1)
    if args.preset == "karaoke":  # \k fills from Secondary to Primary
        primary, secondary = ass_color(p["highlight"]), ass_color(p["color"])
    else:
        primary, secondary = ass_color(p["color"]), ass_color(p["highlight"])
    box_alpha = p.get("box_alpha", 0)
    outline_col = ass_color(p["outline_color"], box_alpha if p["border_style"] == 3 else 0)
    back = ass_color("#000000", 0x80)
    bold = -1 if args.bold else 0
    hook_size = round(short * 0.058)
    lines = [
        "[Script Info]",
        "; generated by video-captions/scripts/captions.py",
        "ScriptType: v4.00+",
        f"PlayResX: {W}",
        f"PlayResY: {H}",
        "WrapStyle: 2",
        "ScaledBorderAndShadow: yes",
        "YCbCr Matrix: TV.709",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Caption,{args.font},{size},{primary},{secondary},{outline_col},{back},{bold},0,0,0,"
        f"100,100,{args.spacing},0,{p['border_style']},{outline},{shadow},5,40,40,0,1",
        f"Style: Hook,{args.hook_font or args.font},{hook_size},{ass_color('#000000')},{ass_color('#000000')},"
        f"{ass_color('#FFFFFF')},{ass_color('#000000', 0xFF)},{bold},0,0,0,100,100,0,0,3,"
        f"{round(hook_size * 0.3, 1)},0,5,40,40,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    if hook:
        text, until, hy = hook
        lines.append(
            f"Dialogue: 1,{ass_time(0)},{ass_time(until)},Hook,,0,0,0,,"
            f"{{\\an5\\pos({W // 2},{hy})\\fad(120,150)}}{text}"
        )
    for s, e, text in events:
        if e - s < 0.02:
            continue
        lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Caption,,0,0,0,,{text}")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return size


# ---------------------------------------------------------------- sidecars


def srt_time(t):
    ms = max(0, int(round(t * 1000)))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(path, words, max_gap):
    # Sentence-sized cues for platform upload, independent of the burned paging.
    cues = paginate(words, 14, 84, max_gap, 6.0)
    out = []
    for i, cue in enumerate(cues, 1):
        text = wrap_text(" ".join(w.text for w in cue), 42).replace("\\N", "\n")
        out.append(f"{i}\n{srt_time(cue[0].start)} --> {srt_time(cue[-1].end)}\n{text}\n")
    Path(path).write_text("\n".join(out), encoding="utf-8")


def write_remotion(path, words):
    caps = [
        {
            "text": (" " if i else "") + w.text,
            "startMs": round(w.start * 1000),
            "endMs": round(w.end * 1000),
            "timestampMs": round((w.start + w.end) * 500),
            "confidence": None,
        }
        for i, w in enumerate(words)
    ]
    Path(path).write_text(json.dumps(caps, indent=1), encoding="utf-8")


# ---------------------------------------------------------------- checks


def probe_size(video):
    if not shutil.which("ffprobe"):
        sys.exit("captions: --video needs ffprobe on PATH; pass --res WxH instead")
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height:stream_side_data=rotation",
            "-of",
            "json",
            video,
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    st = json.loads(out)["streams"][0]
    w, h = st["width"], st["height"]
    rot = next(
        (abs(int(sd.get("rotation", 0))) for sd in st.get("side_data_list", []) if "rotation" in sd), 0
    )
    return (h, w) if rot in (90, 270) else (w, h)


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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words", help="word-timing JSON (or .srt/.vtt, approximate)")
    ap.add_argument("-o", "--out", required=True, help="output .ass path")
    ap.add_argument("--preset", choices=sorted(PRESETS), default="pop")
    size_src = ap.add_mutually_exclusive_group(required=True)
    size_src.add_argument("--res", help="frame size WxH, e.g. 1080x1920")
    size_src.add_argument("--video", help="probe frame size from this video with ffprobe (and burn into it)")
    ap.add_argument("--font", default="Poppins Black", help="font family (default: Poppins Black)")
    ap.add_argument("--fontsdir", help="directory with the font files (also pass it to ffmpeg)")
    ap.add_argument("--bold", action="store_true", help="faux-bold; only for fonts without a heavy cut")
    ap.add_argument("--size", type=int, help="font size in px (default: preset, scaled to frame)")
    ap.add_argument("--spacing", type=float, default=0, help="letter spacing px")
    ap.add_argument("--color", help="text #RRGGBB")
    ap.add_argument("--highlight", help="active-word #RRGGBB")
    ap.add_argument("--outline-color", help="outline / box #RRGGBB")
    ap.add_argument("--case", choices=["upper", "lower", "asis"])
    ap.add_argument("--punct", choices=["strip", "keep"], help="trailing , . ; : on screen (default: preset)")
    ap.add_argument("--y", type=float, help="caption block center as a fraction of height")
    ap.add_argument("--max-words", type=int)
    ap.add_argument("--line-chars", type=int)
    ap.add_argument("--lines", type=int, choices=[1, 2])
    ap.add_argument("--max-gap", type=float, default=0.6, help="pause (s) that starts a new page")
    ap.add_argument("--max-page", type=float, default=2.5, help="max seconds one page stays up")
    ap.add_argument("--hold", type=float, default=0.25, help="seconds a page lingers after its last word")
    ap.add_argument("--offset", type=float, default=0.0, help="shift all timings (s), e.g. VO starts at 0.4s")
    ap.add_argument(
        "--replace",
        action="append",
        default=[],
        metavar="FROM=TO",
        help="fix a single-word spelling, e.g. octamind=Octomind (repeatable)",
    )
    ap.add_argument("--drop-fillers", action="store_true", help="drop um/uh/erm from the captions")
    ap.add_argument("--hook", help="on-screen hook text shown in a top box from 0s")
    ap.add_argument("--hook-end", type=float, default=3.0, help="seconds the hook box stays up")
    ap.add_argument("--hook-font", help="font for the hook box (default: --font)")
    ap.add_argument("--srt", help="also write a sentence-level SRT sidecar")
    ap.add_argument("--remotion", help="also write Remotion Caption[] JSON")
    ap.add_argument("--burn", metavar="OUT.mp4", help="burn the captions into --video with a libass ffmpeg")
    ap.add_argument(
        "--units", choices=["auto", "s", "ms"], default="auto", help="timestamp units of a words array"
    )
    args = ap.parse_args()
    if args.burn and not args.video:
        sys.exit("captions: --burn needs --video as the input")

    p = dict(PRESETS[args.preset])
    for k in ("color", "highlight", "outline_color", "case", "punct", "max_words", "line_chars", "lines"):
        v = getattr(args, k)
        if v is not None:
            p[k] = v

    if args.video:
        W, H = probe_size(args.video)
    else:
        m = re.fullmatch(r"(\d+)[xX:](\d+)", args.res)
        if not m:
            sys.exit("captions: --res is WxH, e.g. 1080x1920")
        W, H = int(m.group(1)), int(m.group(2))
    vertical = H > W

    words = clean(load_words(args.words, args.units), args)
    if not words:
        sys.exit("captions: no words with timings found")
    pages = paginate(words, p["max_words"], p["line_chars"] * p["lines"], args.max_gap, args.max_page)

    # 9:16: block center just below a talking head's chin and above the Reels bottom band.
    default_y = {"clean": 0.62 if vertical else 0.86}.get(args.preset, 0.58 if vertical else 0.80)
    y = round(H * (args.y if args.y is not None else default_y))
    x = W // 2
    hook = None
    if args.hook:
        hook_text = wrap_text(args.hook.strip(), 22 if vertical else 40)
        hook = (re.sub(r"[{}]", "", hook_text), args.hook_end, round(H * (0.20 if vertical else 0.14)))

    events = build_events(pages, p, args, x, y)
    size = write_ass(args.out, events, p, args, W, H, hook)
    if args.srt:
        write_srt(args.srt, words, args.max_gap)
    if args.remotion:
        write_remotion(args.remotion, words)

    # Safe-zone sanity: Meta Reels keeps the top 14% and bottom 35% clear.
    block = size * 1.25 * p["lines"]
    if vertical and (y + block / 2 > H * 0.65 or y - block / 2 < H * 0.14):
        warn(f"caption block at y={y} reaches into the 9:16 UI bands (top 14% / bottom 35%); try --y 0.5-0.6")
    if not font_available(args.font, args.fontsdir):
        warn(
            f"font '{args.font}' not found in --fontsdir or fontconfig; libass will substitute a fallback. "
            "Download the font file into the fonts directory first."
        )
    dur = words[-1].end - words[0].start
    print(
        f"captions: {len(words)} words, {len(pages)} pages, {dur:.1f}s, {W}x{H}, preset {args.preset} -> {args.out}",
        file=sys.stderr,
    )
    ff = libass_ffmpeg()
    if not ff:
        warn(
            "no ffmpeg with libass found (needed for the `ass` filter). macOS: brew install ffmpeg-full; "
            "Debian/Ubuntu/Fedora/Arch: the distro ffmpeg package includes it."
        )
        if args.burn:
            sys.exit(1)
        return
    fd = f":fontsdir={args.fontsdir}" if args.fontsdir else ""
    cmd = [
        ff,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        args.video or "IN.mp4",
        "-vf",
        f"ass={args.out}{fd}",
    ]
    cmd += ["-c:v", "libx264", "-crf", "18", "-preset", "slow", "-pix_fmt", "yuv420p"]
    cmd += ["-c:a", "copy", "-movflags", "+faststart", args.burn or "OUT.mp4"]
    if not args.burn:
        print("captions: burn with  " + " ".join(shlex.quote(c) for c in cmd), file=sys.stderr)
        return
    subprocess.run(cmd, check=True)
    print(f"captions: burned -> {args.burn}", file=sys.stderr)


if __name__ == "__main__":
    main()

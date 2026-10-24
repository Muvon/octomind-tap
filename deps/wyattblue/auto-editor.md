# wyattblue/auto-editor

auto-editor — a command-line editor that detects silence (or motion) and cuts it out, the first pass when editing talking-head, podcast, or creator footage into a tight short. It renders the trimmed file directly or exports a timeline for Premiere, DaVinci Resolve, Final Cut Pro, Shotcut, or Kdenlive so a human editor can take over. Installed from Homebrew on macOS, otherwise from the pinned GitHub release binary (the PyPI package is no longer published).

## Key Commands

| Command | Description |
|---------|-------------|
| `auto-editor raw.mp4 --margin 0.15s -o cut.mp4` | Cut silences, keeping 0.15 s of air around speech |
| `auto-editor raw.mp4 --edit audio:threshold=0.06 -o cut.mp4` | Raise the loudness threshold for noisy rooms (default 0.04) |
| `auto-editor raw.mp4 --cut 3.2sec,3.6sec --cut 7.1sec,7.4sec -o cut.mp4` | Also remove listed ranges (filler words, flubbed takes); one `--cut` per range |
| `auto-editor raw.mp4 --export v1 -o cut.json` | Write the keep/cut chunks as JSON instead of rendering |
| `auto-editor raw.mp4 --export resolve -o cut.fcpxml` | Hand the cut timeline to DaVinci Resolve |

## Common Usage

```bash
# Silence cut for a creator talking-head clip; re-encode at high quality
auto-editor raw.mp4 --margin 0.15s -c:v libx264 -crf 18 -o cut.mp4

# Inspect what would be removed first: chunks are [start_frame, end_frame, speed], speed 99999 = cut
auto-editor raw.mp4 --margin 0.15s --export v1 -o cut.json
```

Transcribe after the final cut, not before: caption timings must match the cut file. When filler words are removed by time range, transcribe the raw file once to find them, cut, then transcribe the cut file for captions.

## Links

- [Homepage](https://auto-editor.com)
- [Options reference](https://auto-editor.com/ref/options)
- [Releases](https://github.com/WyattBlue/auto-editor/releases)

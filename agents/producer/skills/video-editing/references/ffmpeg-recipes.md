# ffmpeg recipes for short-form editing

Each command below was run end to end on ffmpeg 9.0 before being written here. Paths are relative to `./video-out/<slug>/`. Intermediates use `-crf 16 -preset veryfast` to limit generation loss; the final encode follows the `video-spec-sheet` presets. `drawtext` and `ass` need an ffmpeg built with freetype and libass (macOS: Homebrew `ffmpeg-full`, at `$(brew --prefix)/opt/ffmpeg-full/bin/ffmpeg` when stock ffmpeg is first on PATH).

## Probe

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate:stream_side_data=rotation -of json raw/clip.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 raw/clip.mp4
ffmpeg -i raw/clip.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12     # loudness and true peak
```

## Voice cleanup (phone or room audio)

```bash
ffmpeg -i raw/clip.mp4 -vn -af "highpass=f=80,afftdn=nf=-25,acompressor=threshold=-18dB:ratio=3:attack=5:release=120" work/voice.wav
```

For heavy noise or echo, ElevenLabs `isolate_audio` (voice capability) does better; it costs credits, so run it on the final selects only.

## Reframe 16:9 → 9:16

Face-centred crop; replace `FX` with the face's x pixel in the source (read it off an extracted frame):

```bash
ffmpeg -i work/cut.mp4 -vf "crop=ih*9/16:ih:clip(FX-ih*9/32\,0\,iw-ih*9/16):0,scale=1080:1920:flags=lanczos,setsar=1" \
  -c:v libx264 -crf 16 -preset veryfast -c:a copy work/v916.mp4
```

Blurred fill, for screen recordings or wide shots that must stay whole:

```bash
ffmpeg -i work/cut.mp4 -filter_complex "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:2[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1" \
  -c:v libx264 -crf 16 -preset veryfast -c:a copy work/v916.mp4
```

Two speakers side by side in one 16:9 shot (podcast, interview): stack the left half over the right half, no face tracking needed. Put captions on the seam with `--y 0.5`:

```bash
ffmpeg -i work/cut.mp4 -filter_complex "[0:v]split[l][r];\
[l]crop=iw/2:iw/2*8/9:0:(ih-iw/2*8/9)/2,scale=1080:960,setsar=1[t];\
[r]crop=iw/2:iw/2*8/9:iw/2:(ih-iw/2*8/9)/2,scale=1080:960,setsar=1[b];[t][b]vstack[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 16 -preset veryfast -c:a copy work/v916.mp4
```

## Punch-in zooms on emphasis words

Hard 115% punch-ins between word timestamps (here 1.0–2.0 s and 3.0–3.6 s). Add one `between(t,a,b)` per range:

```bash
ffmpeg -i work/v916.mp4 -vf "scale=w='iw*if(between(t,1,2)+between(t,3,3.6),1.15,1)':h=-2:eval=frame,crop=1080:1920" \
  -c:v libx264 -crf 16 -preset veryfast -c:a copy work/zoom.mp4
```

Hard punch-ins read as edited; slow `zoompan` push-ins on faces jitter. Build smooth camera moves in Remotion instead.

## B-roll cutaway over A-roll, SFX on entry, music ducked under voice

B-roll from 1.2 s to 2.4 s with the speaker's audio continuing, a whoosh 50 ms before the cut, music compressed by the voice:

```bash
ffmpeg -i work/zoom.mp4 -i broll/product.mp4 -i music/track.mp3 -i sfx/whoosh.wav -filter_complex "\
[1:v]trim=0:1.2,setpts=PTS-STARTPTS+1.2/TB,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[br];\
[0:v][br]overlay=enable='between(t,1.2,2.4)':eof_action=pass[v];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vo][sc];\
[2:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.35[mu];\
[mu][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];\
[3:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=1150:all=1,volume=0.6[sfx];\
[vo][duck][sfx]amix=inputs=3:duration=first:normalize=0[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset veryfast -c:a aac -b:a 192k work/mix.mp4
```

More cutaways: one `trim`/`setpts` branch and one chained `overlay=enable=...` per clip. Drop the `[2:a]` branch and the `duck` input for UGC that runs without music.

## Loudness: two-pass to -14 LUFS, -1 dBTP

```bash
M=$(ffmpeg -hide_banner -i work/mix.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 \
  | sed -n '/^{/,/^}/p' | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -i work/mix.mp4 -af "loudnorm=I=-14:TP=-1:LRA=11:$M:linear=true,aresample=48000" -c:v copy -c:a aac -b:a 192k work/norm.mp4
```

## Text card and progress bar

```bash
ffmpeg -i work/norm.mp4 -vf "drawtext=fontfile=fonts/Poppins-Black.ttf:text='3 CAPTION RULES':fontsize=96:fontcolor=white:borderw=8:bordercolor=black:x=(w-tw)/2:y=h*0.2-th/2:enable='between(t,0,1.5)',drawbox=x=0:y=0:w='iw*t/DURATION':h=10:color=white@0.9:t=fill" \
  -c:v libx264 -crf 16 -preset veryfast -c:a copy work/titled.mp4
```

Replace `DURATION` with the clip length in seconds. Word-timed captions and the hook box come from the `video-captions` script, not `drawtext`.

## Hook swap on a winning ad (mixed sources)

New 2 s hook clip, then the winner's body from 1.3 s; the `concat` filter normalises size, frame rate and audio format:

```bash
ffmpeg -i hooks/hook-B.mp4 -i cuts/winner.mp4 -filter_complex "\
[0:v]scale=1080:1920,setsar=1,fps=30[h];[0:a]aformat=sample_rates=48000:channel_layouts=stereo[ha];\
[1:v]trim=start=1.3,setpts=PTS-STARTPTS,scale=1080:1920,setsar=1,fps=30[b];\
[1:a]atrim=start=1.3,asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[ba];\
[h][ha][b][ba]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" \
  -c:v libx264 -crf 16 -preset veryfast -c:a aac -b:a 192k work/winner-hookB.mp4
```

## Cut-downs and covers

```bash
ffmpeg -i cuts/master-9x16.mp4 -vf "crop=1080:1350:0:(ih-1350)/2,setsar=1" -c:v libx264 -crf 18 -c:a copy cuts/feed-4x5.mp4
ffmpeg -i cuts/master-9x16.mp4 -vf "crop=1080:1080:0:(ih-1080)/2,setsar=1" -c:v libx264 -crf 18 -c:a copy cuts/feed-1x1.mp4
ffmpeg -ss 1.2 -i cuts/master-9x16.mp4 -frames:v 1 -q:v 2 meta/cover.jpg
```

Check that captions and the face survive the crop; if not, re-render captions at the cut-down's size with `--video` pointing at the cropped file.

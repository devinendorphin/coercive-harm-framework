# Name, Place, Time — reels

Seventeen vertical Instagram reels recounting the season-by-season close-read of *Something
Was Wrong* (S1–S10). The analysis itself lives on branch `ccr-93dfe246-4ja9f0`
(`research/sww-corpus/`, commit `729dd3e`); these files only re-voice it. `SCRIPT.md` is the
full narration with what appears on screen.

Rendered video is not committed (≈ 300 MB). To rebuild:

```
uv venv -p python3.12 venv && . venv/bin/activate
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install kokoro soundfile "misaki[en]" pillow numpy
python tts.py                                  # build/voice_NN.wav + timing_NN.json
seq -w 1 17 | xargs -P 3 -I{} ./build_one.sh {}  # out/reel_NN.mp4
```

| File | Role |
|---|---|
| `content.py` | the scripts: narration per scene plus the on-screen card |
| `tts.py` | Kokoro narration (voice `af_heart`) with word timestamps for captions |
| `music.py` | procedural soundtrack: minor-key pad, heartbeat pulse, delayed arpeggio |
| `render.py` | frames (Pillow) piped to ffmpeg; cards, cycle ring, bars, word-synced captions |
| `build_one.sh` | music → video → mix (voice ducks the music; loudness −14 LUFS) |

**BOUNDARY.** The reels carry the study's limits: survivor testimony as broadcast (P2), one
curator and so no prevalence rates, shared move-set rather than coordination, and step one
only — no finding about any individual.

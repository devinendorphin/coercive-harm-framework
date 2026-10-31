# Name, Place, Time — reels

Twenty-four vertical Instagram reels recounting the season-by-season close-read of *Something
Was Wrong* (S1–S15). The analysis itself lives on branches `ccr-93dfe246-4ja9f0` (S1–S10,
commit `729dd3e`) and `ccr-89a0fcc4-xfqzcf` (S11–S15, commit `a5611e8`), under
`research/sww-corpus/`; these files only re-voice it. `SCRIPT.md` is the
full narration with what appears on screen.

Rendered video is not committed (≈ 1 GB). To rebuild:

```
uv venv -p python3.12 venv && . venv/bin/activate
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install kokoro soundfile "misaki[en]" pillow numpy
python tts.py      # build/voice_<slug>.wav + timing_<slug>.json
python hold.py     # hold quote cards long enough to read
python -c "from content import REELS; print('\n'.join(r['slug'] for r in REELS))" \
  | xargs -P 3 -I{} ./build_one.sh {}     # out/reel_NN_<slug>.mp4
python gen_script.py                       # SCRIPT.md
```

| File | Role |
|---|---|
| `content.py` | the scripts: narration per scene plus the on-screen card |
| `tts.py` | Kokoro narration (voice `af_heart`) with word timestamps for captions |
| `hold.py` | adds silence after a scene whose quote card needs more reading time than its narration |
| `gen_script.py` | writes `SCRIPT.md` from `content.py` and the timings |
| `music.py` | procedural soundtrack: minor-key pad, heartbeat pulse, delayed arpeggio |
| `render.py` | frames (Pillow) piped to ffmpeg; cards, cycle ring, bars, word-synced captions |
| `build_one.sh` | music → video → mix (voice ducks the music; loudness −14 LUFS) |

**BOUNDARY.** The reels carry the study's limits: survivor testimony as broadcast (P2), one
curator and so no prevalence rates, shared move-set rather than coordination, and step one
only — no finding about any individual.

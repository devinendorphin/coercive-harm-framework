> **RETIRED 2026-11-11.** Endorphin: "And that's where the original series [?were scrapping→we're
> scrapping] that." These reels are not to be posted. They used "allegations, not verdicts" across
> the board, which understates stories backed by convictions and records; the replacement series
> is `../sww-whole-story-reels/`. Kept in the repository as the record (git keeps it either way).

# Name, Place, Time — reels

Thirty-five vertical Instagram reels recounting the season-by-season study of *Something Was
Wrong* (S1–S24). The analysis itself lives on branches `ccr-93dfe246-4ja9f0` (S1–S10,
commit `729dd3e`) and `ccr-89a0fcc4-xfqzcf` (S11–S15, commit `a5611e8`), under
`research/sww-corpus/`. Part two (S16–S24, `content_part2.py`) comes from branch
`ccr-81ec1931-b41u1s` (commit `92925ef`): `research/something-was-wrong-s16.md` and
`research/something-was-wrong-s17-s24.md`. Those seasons were read for institutional
response rather than coded on the cycle, and S17–S19 only in excerpts; the reels say so.
These files only re-voice the research. `SCRIPT.md` is the
full narration with what appears on screen.

Rendered video is not committed (≈ 1.5 GB). To rebuild:

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
| `content.py` | the scripts: narration per scene plus the on-screen card (S1–S15, and the series order) |
| `content_part2.py` | the scripts for Seasons 16–24 and their cross-season findings |
| `tts.py` | Kokoro narration (voice `af_heart`) with word timestamps for captions |
| `hold.py` | adds silence after a scene whose quote card needs more reading time than its narration |
| `gen_script.py` | writes `SCRIPT.md` from `content.py` and the timings |
| `music.py` | procedural soundtrack: minor-key pad, heartbeat pulse, delayed arpeggio |
| `render.py` | frames (Pillow) piped to ffmpeg; cards, cycle ring, bars, word-synced captions |
| `build_one.sh` | music → video → mix (voice ducks the music; loudness −14 LUFS) |

**BOUNDARY.** The reels carry the study's limits: survivor testimony as broadcast (P2), one
curator and so no prevalence rates, shared move-set rather than coordination, and step one
only — no finding about any individual.

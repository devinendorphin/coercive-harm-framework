# Told Whole — reels

A series of vertical reels (about 2–3 minutes each) explaining the whole-story test of
*Something Was Wrong* (`research/sww-corpus/results/whole_story/RESULTS.md`). Made **one reel at a
time** (Endorphin, 2026-11-11): each is reviewed before the next is written. The pipeline is
copied from `../sww-reels/` (Kokoro narration, Pillow frames, ffmpeg); only `content.py` and
the header numbering differ. `SCRIPT.md` is the narration with what appears on screen.

Rendered video is not committed. To rebuild:

```
uv venv -p python3.12 venv && . venv/bin/activate
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install kokoro soundfile "misaki[en]" pillow "numpy>=2" "spacy>=3.8" "thinc>=8.3"
# the spaCy English model, if GitHub downloads are blocked: the wheel on huggingface.co/spacy/en_core_web_sm
python tts.py intro && python hold.py intro && ./build_one.sh intro   # out/reel_01_intro.mp4
python gen_script.py
```

| Reel | Status |
|---|---|
| 01 · Intro (2:00) | drafted 2026-11-11, awaiting Endorphin's review |

**BOUNDARY.** Survivor testimony as broadcast; a podcast's selected stories, not a population
rate; Claude coders were not blind and every result is shown for both model families.

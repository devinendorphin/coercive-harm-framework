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
| 01 · Intro (2:10) | v3 2026-11-11: visual cards (tiles, timeline, readers, gauges, eyes, one dot per person, evidence cards); awaiting review |
| 02 · Same moves (2:47) | v6 2026-11-13: thesis-first overhaul (six moves, one survivor's telling each; one short edges segment; audit detail moved to arc 7); v5 2026-11-13: revised after the symmetric re-read audit (re-read rows, 34 of 43 marks held, three counts too high, all four misfits held, Kaelyn's story belongs with the deceivers); v4 2026-11-13 (Diana scenes carry the friction reading, amendment 6; '72 misfits' corrected to 4 of 72 notes): arc 1 opener; close-read tallies as dot rows (new `dotrows` card), the isolation test's failure, the room hypothesis, 72 misfits; evidence checks in `CHECKS.md`; awaiting review |
| 03 · Every room (2:19) | v1 2026-11-13: arc 2 opener, thesis first; one move (isolate) through six rooms, one survivor's telling each; one edges segment (15 of 56 outside romance, no room difference detectable, cases not a measure); evidence checks in `CHECKS.md`; awaiting review |

**BOUNDARY.** Evidence is graded, not disclaimed: convictions and records are stated as such,
and what rests on a survivor's word alone is attributed to them (about 4 in 10 coded stories; about
6 in 10 are backed by a conviction, a document, a record the show checked or a second witness).
No uncharged person is named. A podcast's selected stories, not a population
rate; Claude coders were not blind and every result is shown for both model families.

## Rules for every reel (Endorphin, 2026-11-11)

- **Evidence wording.** Convictions and court records are stated as what they are. A story that
  rests only on the person's own account is described as **"told solely from the person's own
  account"**, never with "she says" or "allegedly", and **only after checking that it really is**:
  (1) both coders' `evidence_types` for that person; (2) because the two coders agree on "account
  alone" only 81 % of the time (κ 0.60), also (3) the full transcript, for any document, record
  or second witness the coders missed. The check is written down in `CHECKS.md` before the reel is
  built. Calling a corroborated account uncorroborated repeats the lack of care many people in
  this series met.
- **Visual, not numeric.** Each figure is shown as people (one dot per person), as a life on a
  timeline, or as shapes, not as a bare number on a card. Data colours are validated for
  colour-blind viewers on the reel background; every colour is also named in text.
- **One reel at a time,** each reviewed before the next is written.

# Whole-story test: run status (updated 2026-11-08)

Coded files are in `../results/whole_story/coded/` (checked on arrival: valid JSON, every chunk
read to its last line, quotations verified against the transcripts with `tools/check_quotes.py`).

## Done
- Claude neutral pairs (A, B): S1, S2, S3, S4, S5, S6, S14, S16, S17, S18, S24
- Claude single coder so far: S15 B, S19 B
- Codex neutral pairs (CA, CB): S7, S8, S9, S10, S11, S12, S17 (cross-check), S20, S21, S23, S25
- Codex single: S26 CB
- Codex framing pair: S13 CPOS / CNEG

## Still to code
- Claude neutral: S13 A+B, S15 A, S19 A, S22 A+B (in progress in session_01DekSu4xpiRwMGNBweYLj8Z)
- Claude framing pairs (POS, NEG): S2, S4 (in progress); S3, S13, S22, S24 (not started)
- Codex: S26 CA (not on the kit repo)

## Known issues to carry into the analysis
- Some Codex files contradict themselves: `reached_institution` not "no" but outcome
  `never_reached` (e.g. S17 CB 5 records, S21 CB 14). Count per coder; report headlines with and
  without those records. Do not edit coder output.
- People from one season reappear as update stories in another (e.g. S14 survivors coded again in
  S19 B). Decide, before computing, how cross-season repeats are counted; report both ways.
- S24 B: 6 of 199 quotations below the 0.8 match bar, several on coded responses — check by hand.
- Coders differ on what counts as an institution (restaurant staff, a president's remarks) and on
  person-finding (host/listener asides). These show up as disagreement; do not override codes.
- Naming (S-21): some quotations keep a non-victim's first name (e.g. S15 A, an agency owner),
  because the instructions only required replacing perpetrator names. Scrub non-victim names from
  any quotation before it is published in RESULTS.md or elsewhere.
- S22 A kept the perpetrator's name inside quotations taken from news reports, court records or
  statements read on air (its own deviation from the rule). Redact before any publication.
- S22 NEG names people the perpetrator falsely accused (as harmed parties); other S22 coders
  describe them by role. Treat falsely accused people as unnamed in anything published (S-21).
- Isolation of coders is by instruction; several wrote helper scripts outside their folder.

## Rebuilding the transcripts in a new container
`python3 tools/fetch_sww.py /tmp/sww` (about 40 minutes), then `python3 tools/prepare_reading.py
/tmp/sww /tmp/read whole_story` and `python3 tools/corpus.py index /tmp/sww` (expect 387 episodes,
16 unassigned).

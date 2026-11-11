# Whole-story test: run status (updated 2026-11-11) — CODING COMPLETE; ANALYSIS DONE

**Analysis (2026-11-11):** `../results/whole_story/RESULTS.md`. Decisions fixed before computing:
DEVIATIONS D6. Matching: `matching_hand.csv` (546 hand decisions). Repeats:
`cross_season_repeats.csv` (94 records). Post-hoc checks: `tools/whole_story_checks.py`.
Open for Endorphin: whether D3's "Claude-only is the pre-registered result" still applies after
D5 (self-audit lean log 6); the clean-environment Claude recode D5 proposes; whether emergency
medical care counts as protection for the decisive-work prediction (S23). Quotation check done
(16 of about 9,000 below the bar; no verdict changes).

Coded files are in `../results/whole_story/coded/` (checked on arrival: valid JSON, every chunk
read to its last line, quotations verified against the transcripts with `tools/check_quotes.py`).

## Done (all coding complete, 2026-11-11)
- Neutral pairs, every season S1–S26: Claude A/B for S1–S6, S13–S19, S22, S24; Codex CA/CB for
  S7–S12, S20, S21, S23, S25, S26; S17 also coded by Codex CA/CB as the cross-check.
- Framing pairs: Claude POS/NEG for S2, S3, S4, S13, S22, S24; Codex CPOS/CNEG for S13.

## Known issues to carry into the analysis
- **Pinned (Endorphin, 2026-11-11):** the only coder that disclosed the CLAUDE.md exposure (D5) was
  the last one to finish: S24 POS, the one Endorphin paid extra usage to complete. All other Claude
  coders received the same files and none mentioned them. Open question, not yet examined: why this
  one reported it and the others did not.
- **Claude coders were not blinded (deviation D5):** the harness loaded the project CLAUDE.md files
  into every Claude coder's context. Report Claude-coded results as unblinded; Codex coders were
  blinded. See DEVIATIONS.md D5.
- Several coders lost their notes on a container change and re-read from file 1; reading logs say so.
- S04 NEG: 4 of 56 quotations below the 0.8 match bar.
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

# Whole-story test: run status (updated 2026-11-11) — CODING AND ANALYSIS COMPLETE (isolated branch)

Coded files are in `../results/whole_story/coded/`; their contents are unchanged. The completed
[analysis](../results/whole_story/RESULTS.md), [arithmetic](../results/whole_story/ARITHMETIC.md)
and [quotation audit](../results/whole_story/QUOTATION-AUDIT.md) remain on the unmerged
`analysis/whole-story-isolated` branch. All 502 reported endpoints match the actual rebuilt
files; all 207 reading files match original line and word counts. The full wording recheck
found 8,841/8,857 tested quotations, with 11 additional too-short entries; automatic failures
remain flagged and reported with and without exclusions. No coder output was edited.

## Done (all coding complete, 2026-11-11)
- Neutral pairs, every season S1–S26: Claude A/B for S1–S6, S13–S19, S22, S24; Codex CA/CB for
  S7–S12, S20, S21, S23, S25, S26; S17 also coded by Codex CA/CB as the cross-check.
- Framing pairs: Claude POS/NEG for S2, S3, S4, S13, S22, S24; Codex CPOS/CNEG for S13.

## Known issues to carry into the analysis
- **Pinned (Endorphin, 2026-11-11):** the only coder that disclosed the CLAUDE.md exposure (D5) was
  the last one to finish: S24 POS, the one Endorphin paid extra usage to complete. All other Claude
  coders received the same files and none mentioned them. Open question, not yet examined: why this
  one reported it and the others did not.
  **Provenance clarified by Endorphin:** the supervisor relayed that warning in chat;
  Endorphin raised its significance; D5 was then written. The formal record followed his
  intervention. It is not evidence of independently initiated supervisory correction.
  A limited review of the saved outputs does not explain why the warning surfaced only then.

- **Claude coders were not blinded (deviation D5):** the harness loaded the project CLAUDE.md files
  into every Claude coder's context. Report Claude-coded results as unblinded; Codex coders were
  blinded. See DEVIATIONS.md D5.
- Several coders lost their notes on a container change and re-read from file 1; reading logs say so.
- S04 NEG: 4 of 56 quotations remain below the 0.8 bar; manually found in the source, with joined excerpts/redactions. The failures remain in the exclusion analysis.
- Some Codex files contradict themselves: `reached_institution` not "no" but outcome
  `never_reached` (e.g. S17 CB 5 records, S21 CB 14). There are 21 across the input set, listed by file/ID in `flags.csv`; unchanged and excluded analyses are complete. Do not edit coder output.
- People from one season reappear as update stories in another (e.g. S14 survivors coded again in
  S19 B). D6 fixed the rule before calculation: per-season primary plus earliest identifiable story once. Both analyses are complete.
- S24 B: 6 of 199 quotations remain below the 0.8 bar; all checked by hand against the transcripts, with exact passages documented in QUOTATION-AUDIT. They remain flagged in the exclusion analysis.
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

From `research/sww-corpus/`:

```sh
python3 -I tools/rebuild_whole_story_sources.py results/whole_story /tmp/sww-frozen
python3 -I tools/verify_whole_story_sources.py results/whole_story /tmp/sww-frozen /tmp/read
```

This restores the original 387 canonical episodes and 16 unassigned episodes, retaining
four season assignments originally inherited from discarded twins (D8). Use `--frozen-index
results/whole_story/episode_index.txt` when running `prepare_reading.py` or `check_quotes.py`
on this canonical-only collection. Omitting it incorrectly makes those four episodes
unassigned. Full reproduction commands and hashes are in the quotation audit and manifests.
The original `fetch_sww.py` remains available for fetching raw alternate transcriptions;
later publications must not enter this frozen analysis.

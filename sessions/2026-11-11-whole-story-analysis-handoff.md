# Whole-story analysis handoff — 2026-11-11

## Work completed

Endorphin requested the analysis and plain-language write-up of the completed whole-story
coding, without subagents or new coders, with script-computed arithmetic and a disconfirming
check before every reported result. Required instructions, audit, design, plan, D1–D5,
status, synthesis, power critique and earlier results were read.

The attached environment contained only the earlier sww-coding-kit. The analysis repository
was located through the connected GitHub account and cloned at
`/workspace/coercive-harm-framework`; main initially was `ccfabfb`.

Two stages were committed and pushed to main:

- `d03752d`: D6 analysis decisions, fixed before opening person records or computing any
  headline. Primary person–harm-per-season analysis plus earliest-identifiable-story
  sensitivity; unchanged and contradiction-excluded analyses; identity-only matching;
  Claude S17 primary in pooled figures, Codex substitution sensitivity; max of family
  framing bands for pooled decisions, with both shown; D5 labels throughout.
- `b773dac`: `matching_hand.csv`, `repeat_links.csv`, `MATCHING-NOTES.md`. All neutral
  comparisons and the four S17 cross-family comparisons were reviewed using identity-only
  exports; unique full normalised names preserve parenthetical harm labels. Hand matches
  and unmatched dispositions are recorded. No outcome/response codes were consulted when
  making these decisions. Records split by different perpetrators versus combined records,
  group-to-individual records and indistinguishable unnamed children/dancers were retained
  unmatched. Read MATCHING-NOTES for unresolved cross-season identities.

**No headline has been computed. No RESULTS.md has been written.** The analysis script has
not been modified. After identity decisions were committed, a schema inspection listed
allowed field values and inspected example reading logs and others-mentioned numeric types;
this did not compute results. Working identity-export helper scripts are untracked in
`work/` and are not needed to consume the committed CSVs.

## Blocker and Endorphin's response

This running instance blocks `podscripts.co` with proxy HTTP 403. A fresh request outside
its command sandbox also failed. Runtime status identified the attached instance and showed
an enforced policy with no custom allowed domains. Endorphin added the domain to the
published SWW environment and republished it; this running instance still reported the old
policy. There is no available runtime request-changes/restart tool. Endorphin asked how to
change instances and then asked for a prompt for a new one. The next instance should use
the updated published environment and validate access before fetching.

Do not waive transcript checks. STATUS requires hand checks of S24 B and S04 NEG failures.
No transcripts were fetched, no quote checks rerun, and no sample quotation audit performed
here. Do not report verification as completed.

## Next work

1. Read the original required files and D5, D6 and MATCHING-NOTES. Validate the matching
   inputs (IDs, uniqueness, complete unmatched dispositions) without looking at codes to
   revise identities. Validate the newly applied network policy. Rebuild transcripts as
   STATUS describes if needed for flagged and sample passages.
2. Extend `research/sww-corpus/tools/analyze_whole_story.py` for all groups and sensitivity
   variants, all per-season agreement, S17 cross-family comparisons, own-coder and agreed
   figures, intervals, framing, reasons and others-mentioned counts. Existing `norm()`
   removes harm labels; fix it. Existing own-coder W3 unnecessarily filters on reached=yes,
   whereas the plan's W3 eligibility uses protected/partly protected and known worker;
   follow the plan consistently. Include unknown/omitted denominators, not just agreed
   percentages. Never mutate coded files. Record newly necessary choices before results.
3. Run disconfirming tests and read coded quotations for each headline, recording exact
   sample IDs and counts. Write RESULTS beside the earlier results and external data;
   update README, docs 04/08/10, audit lean log and continuity; execute the session-log
   workflow from `.claude/commands/session-log.md`. Commit and push after each stage.

## Limits and tensions

D5 is the weakest load-bearing measurement condition: Claude results are unblinded and
Codex results are blinded. S17 estimates their difference on one season; it does not isolate
exposure from model-family differences. Claude's framing band measures an extra sentence
on top of contamination. Codex's S13 band is only a single-season check.

Matching conservatively sacrifices some paired coverage rather than inventing individual
correspondence. Own-coder figures must retain those records and the person-finding rate must
make the cost visible. No direction of its effect is claimed before arithmetic.

No new substantive objections were raised; OBJ-031 still needs its whole-story update once
results exist. No changes to working agreements were proposed. Endorphin's naming,
no-shortcuts, machine-only and no-subagents instructions remain in force.

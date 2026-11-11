# Deviations from the pre-registration and the analysis plan

*Dated entries only. Each says what changed, why, when (relative to coding), and what was recoded.*

## D1 — 2026-11-01, after the S17 pilot, before the full run

The pilot (two neutral coders on S17) was read by the analyst against the full S17 transcripts,
which the analyst had read in full beforehand. Quotations: 48/48 (A) and 63/63 (B) found in the
transcripts. Changes, each because a coder misread the instructions or the instructions left a
gap the pilot exposed:

1. **Reading in full failed at the last line.** Both coders stopped one line short of the end of
   all four chunk files (they reported last lines 100/97/106/54; the files have 101/98/107/55).
   The chunk files had no final newline, so a line count came out one short, and the missing lines
   hold story content. Fix: chunk files now end with a newline (`prepare_reading.py`), each
   coder's task message lists the exact line count of every file, and the instructions say to read
   until that line number is reached.
2. **A child who was killed was coded "partly protected" by one coder** (A: `partly_protected`;
   B: `not_protected`), because his killer was convicted after his death. The pre-registration
   defines protected as "institutional action stopped the harm or made the person safe"; the
   instructions' clause about harm that had already ended left room for the other reading. Added:
   if the person died from the harm, or the harm went on until something other than an
   institution ended it, a later conviction is not protection of that person. *This change moves
   the coding away from the institution's side; the unclarified wording let a death count as
   partial protection.*
3. **Separate harms by different perpetrators** were handled two ways (A coded one harm and left
   the other in notes; B merged both into one record). Added: one record per such harm.
4. **Perpetrator names inside quotations**: coder A replaced them with `[perpetrator]`, coder B did
   not. Added: replace with `[perpetrator]`, change nothing else (naming rule S-21). The quotation
   check tolerates this.
5. **Writing outside the output folder**: coder A wrote helper scripts in another directory.
   Added: write files only in your own output folder.

Nothing in the predictions, thresholds, outcome categories or analysis rules changed. **S17 is
recoded by two fresh neutral coders with the final instructions**; the pilot codes are kept in
`../results/whole_story/pilot/` and are not used in any result.

## D2 — 2026-11-01, framing draw re-run (no coding affected)

The first run of the seeded draw read the index file's summary line as a 27th "season" (387),
so its population broke the committed rule. It was discarded and re-run once on seasons 1–26
with the same seed. Both outputs are in `../results/whole_story/framing_draw.txt`. No framing
coder had started.

## D3 — 2026-11-02, a second model family for named seasons (before any outside coder starts)

**Why:** the session's usage limit stops a 10-coder batch about every five hours; the full plan
needs 64 coders. Endorphin approved using Codex (a different model family) to share the load.
**What:** Codex codes, as independent single-coder tasks with the identical coder instructions,
format and reading folders (rebuilt by `codex-kit/build_kit.py`; tested byte-identical):
- seasons 7–12: neutral coders `CA` and `CB` (two separate tasks per season);
- season 17: `CA` and `CB` again, beside the Claude coders, to measure agreement between models;
- season 13: framing pair `CPOS` / `CNEG`, to measure Codex's own lean (the pre-registered framing
  test measures only the Claude coders).
**Blinding:** the kit lives in a separate repository (`devinendorphin/sww-coding-kit`, commit
`ee0585e`) that contains no project documents, hypotheses or results; each task is told not to open
other branches or pull requests. As with the Claude coders, isolation is by instruction.
**Analysis changes (fixed now):** every headline is reported three ways: all seasons pooled;
Claude-coded seasons only; and Codex-coded seasons only, each with its own framing band (Claude
band from the six drawn seasons; Codex band from S13). If the pooled and Claude-only verdicts differ,
both are reported and the Claude-only result is the one the pre-registration describes. S17's four
neutral codings give a between-model agreement figure, reported beside the within-model ones.
Seasons coded by Codex are not also coded by Claude neutral coders unless capacity allows; any such
double coding is reported, never used to pick a preferred result.

## D4 — 2026-11-03, Codex also codes S20, S21, S23, S25, S26 (before any of these is coded)

**Why:** the usage limit still stops Claude coders every few hours; Endorphin approved moving more
neutral coding to Codex. **What:** Codex neutral coders `CA` and `CB` (separate tasks) for seasons
20, 21, 23, 25 and 26, with the same kit (`sww-coding-kit`, unchanged since `ee0585e`). Claude keeps
seasons 13 and 22 (neutral A/B) and all six pre-registered framing pairs (S2, S3, S4, S13, S22, S24).
**Consequence, stated now:** the Claude-only result rests on 15 seasons (S1, S2, S3, S4, S5, S6,
S13, S14, S15, S16, S17, S18, S19, S22, S24) and the Codex-only result on 12 (S7, S8, S9, S10, S11, S12,
S17 as cross-check, S20, S21, S23, S25, S26). (Drafting this entry exposed that S13 had no neutral
pair assigned to either model; it is assigned to Claude here, so every season S1–S26 has one.) The three-way reporting
rule of D3 applies unchanged; no season is coded by Claude neutral coders and Codex neutral coders
both, except S17 (the planned cross-check).

## D5 — 2026-11-11, found after coding: Claude coders saw the project's CLAUDE.md files

**What happened:** the S24 POS coder reported that "the CLAUDE.md contents under /home/user were
shown to me automatically by the environment". Claude Code loads the CLAUDE.md files of the working
directories into every subagent's context. Every Claude coder (neutral A/B and framing POS/NEG) ran
in this session's container, where both `coercive-harm-framework/CLAUDE.md` and
`veriticide-general-ledger/CLAUDE.md` sit under `/home/user`. Not every coder reported it, but the
loading is automatic, so **assume all Claude coders were exposed**. Codex coders were not: they
worked in the separate `sww-coding-kit` repository, which has no project instructions.

**What those files say that matters:** the project studies how institutions handle psychological
and coercive harm (`coercive-harm-framework/CLAUDE.md` line 8); "sycophancy to power" is its subject
(line 48); the ledger repo's thesis is "institutional harm laundering" (`veriticide-general-ledger/
CLAUDE.md` line 8). Neither file states W1–W3 or their thresholds, but together they frame
institutions as failing victims. The pre-registration promised coders would "not see ... this
project's documents"; for Claude coders that promise was broken.

**Direction of possible bias:** toward coding institutional failure (the opposite of the earlier
leans recorded in the self-audit, but contamination all the same).

**What the analysis must do:** (1) report the Claude-coded and Codex-coded results separately (D3
already requires it) and state that only the Codex coders were blinded as promised; (2) use the S17
cross-check (two Claude and two Codex coders on the same season) to estimate the difference; (3) note
that the Claude framing band was measured with the same exposure in place, so it measures the
effect of the framing sentence on top of it, not the exposure itself; (4) not present any Claude-only
figure as blinded. **Possible repair, not yet done:** re-code one or more seasons with Claude coders
run in a clean environment (the kit repository, with no project CLAUDE.md) and compare.

## D6 — 2026-11-11, analysis decisions fixed before any headline was computed

*Written after reading the coded files' structure (record counts, field values, which episodes
each record cites) and before matching people or computing any figure. Nothing here changes a
prediction or threshold.*

1. **People who reappear in another season.** Some seasons carry another season's update
   episodes (S15 e10–e11 = S9 updates, S15 e13 = S7; S19 e9–e10 = S14; S21 e18 = S20, S18, S7;
   S23 e20 = S21), and some coders coded people from the same unassigned data episode in several
   seasons. Every such record whose person is already coded in the home season (by either neutral
   coder) is listed by hand in `../results/whole_story/cross_season_repeats.csv`, identified by
   name, role and harm only. Records told only in another season's update whose person the home
   season's coders did not record (e.g. S15 A "Danielle's daughter", S21 "Dani", the newly targeted
   doula, S23 "Daisy") are not repeats. **Both counts are reported:** *per season* (every record as
   coded, the plan's default) and *once* (listed repeats removed before matching). A repeat is
   removed only when its home season is in the set being reported (pooled, Claude-only or
   Codex-only), so no set loses a person it does not otherwise contain. In the *once* count the
   home-season record stands for the person, even where the update knows more; this is stated
   beside the figures.
2. **Records that contradict themselves.** 21 Codex records give `reached_institution` "unclear"
   but outcome `never_reached` (S12 CB 1, S17 CA 1, S17 CB 5, S21 CB 14); no other kind of
   contradiction exists. Coder output is not edited. Reported three ways: *as coded* (the plan:
   "unclear" leaves the record out of every yes/no share); *without them* (the 21 records removed
   before matching); and, for the never-reached share only, *read by their outcome* (counted as
   not reached). W1–W3 need `reached = yes`, so the 21 records cannot enter them as coded.
3. **Person matching** uses only `name`, `role_in_story`, `harm`, `perpetrator_role` and
   `episodes`, never a code. Automatic name matching first, then by hand; every hand match and
   every hand decision that a record has no counterpart goes in `matching_hand.csv` with its
   reason. A `pair` column names the two coders (A-B, CA-CB, or the S17 cross pairs A-CA, A-CB,
   B-CA, B-CB).
4. **S17 in the pooled count.** D4 places S17's Claude pair in the Claude-only set and its Codex
   pair as the cross-check. The pooled figure uses the Claude pair for S17 (one pair per season);
   the pooled figure with the Codex pair instead is reported beside it.
5. **Framing band for the pooled figure.** D3 gives a band to each model's set but none to the
   pooled set. The pooled headline is judged against the wider of the two bands, so a result
   counts as decided only if it is decided under both models' measured lean.
6. **The D5 estimate (unblinded Claude vs blinded Codex) on S17** is: each coder's own figures
   side by side; agreement on people matched across models; and the direction of every
   cross-model disagreement on outcome and on the W2 indicator (which way the Claude coder leans
   relative to the Codex coder). One season and two coders a side cannot separate the exposure
   from the model family; the results will say so.
7. **Each coder's own figures in the three-way report** are pooled by coder label: A and B over
   the Claude seasons, CA and CB over the Codex seasons.

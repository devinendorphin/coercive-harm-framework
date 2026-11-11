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

**Provenance clarification from Endorphin, 2026-11-11:** the final coder disclosed the
exposure to the supervising Claude, which mentioned it in the chat Endorphin could see.
Endorphin then raised the significance of that disclosure and the fact that it came only
from the last coder, whose completion he had funded with extra usage. The supervisor wrote
this deviation note after that intervention. The formal record therefore followed
Endorphin’s intervention; its existence must not be credited as independently initiated
supervisory correction. The warning was already in the chat, but formal recognition and
preservation as a study deviation are a separate step. There is no evidence here establishing
that the supervisor would have made that formal record without Endorphin raising it.
This chronology is Endorphin’s account of the interaction; this checkout does not supply
the original complete exchanges or per-coder delivered-context logs. Why earlier coders did
not disclose the exposure remains unresolved; absence of disclosure does not establish
whether they noticed it.

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

## D6 — 2026-11-11, analysis decisions fixed before computing any headline

These decisions are made after reading the design, plan, status and D5, but before opening
person records or running the analysis. No coder output is changed.

1. **Repeated appearances.** The primary analysis retains a person–harm story once per
   season, as the original season-based plan does. A second analysis counts each identifiable
   person–harm story once across seasons, retaining its earliest season in that reporting
   group. Separate harms by different perpetrators remain separate (D1.3). Cross-season
   identity is determined from names, roles, harm descriptions, perpetrator roles and episode
   references only, before looking at codes; ambiguous identities remain separate and are
   described. A committed `repeat_links.csv` records links and reasons. In agreed analyses,
   the earliest matched appearance is retained before testing agreement or eligibility; a
   later agreed/protected appearance is never selected in preference to an earlier one.
2. **Contradictions.** Flag a record if `outcome = never_reached` while `reached_institution`
   is anything other than `no`, or if `reached_institution = no` while the outcome is anything
   other than `never_reached`. Report the unchanged-code analysis and a sensitivity analysis
   excluding flagged records. For paired figures exclude a pair if either record is flagged;
   for own-coder figures exclude only that coder's flagged records. `unclear` is not silently
   changed to `no` or `yes`. List flags by file and person ID, with no names in the flag report.
3. **Matching.** Use only the plan's identity fields, never outcome or response codes. The
   existing script strips parenthesised harm labels, potentially conflating separate harms;
   preserve those labels. Automatic matching requires a unique, nonempty, normalised full
   name on both sides. Review identity-only exports of all automatic matches and unmatched
   records. Record every manual match, rejected automatic match, and unmatched disposition
   in `matching_hand.csv`, including pair/coder labels and reasons; generate `matching.csv`
   from that audit trail. Apply the same rule to all four Claude–Codex pairings on S17.
4. **Three reporting groups and S17.** All seasons uses Claude A/B for S17, the original
   neutral pair, and the assigned family for every other season (26 seasons). Claude-only
   uses its 15 seasons and is labelled **unblinded** everywhere. Codex-only includes its 12
   seasons, including S17, and is labelled **blinded**. Never double-weight S17 in a pooled
   headline. Also report the pooled sensitivity substituting Codex's S17 pair. For the S17
   cross-check report A–CA, A–CB, B–CA and B–CB agreement and each family's own and agreed
   rates; their difference cannot isolate exposure from model-family differences.
5. **Framing for pooled figures.** D3 requires each family's band but leaves the combined
   band unspecified. Show both family bands beside pooled figures; use the larger available
   band for the pooled decision, avoiding unsupported averaging. An unavailable band means
   the prediction cannot be decided by this method. Calculate differences from exact ratios,
   not rounded display rates. Claude's band measures the extra sentence on top of its
   unblinded exposure; Codex's single-season band is a limited check, not a model-wide bound.
6. **Uncertainty and disconfirmation.** Preserve the plan's prediction-specific agreement
   rules, own-coder rates, central-survivor and fully-protected-only checks, season results
   and Wilson intervals. Intervals describe the coded sample; they do not make this a random
   population sample or account for shared seasons. Before publishing any finding, inspect
   the specified sensitivity analyses and contrary coded quotations. Save a reproducible
   quotation-sample manifest and checked observations. Do not treat a matched quotation as
   proof that its code follows from the passage or that the underlying account is verified.

## D7 — 2026-11-11, reporting details fixed before the first headline calculation

The continuation uses D6 unchanged. The following implementation details are fixed before
running the extended analysis, with no coder output edited:

1. Report W2 and W3 indicator agreement on all matched records with non-missing indicators,
   as the plan's “per field, on matched people” specifies; also report agreement inside each
   prediction's eligible subset, so absence of contact/protection does not inflate the
   assessment of those predictions. Unknown reached status and unknown decisive workers
   are reported as omitted, never treated as negative evidence.
2. In addition to flagging each failed quotation, report a conservative sensitivity excluding
   any person record with a contact, outcome, decisive-work or never-reached quotation that
   fails the script's 80% test (or has fewer than four words). This is broader than excluding
   only a decisive quotation and avoids deciding which failure matters after seeing results.
   A missing outcome quotation also flags the record. For a pair, either coder's flag excludes
   the pair. Other-mentioned quotation failures are reported separately. Unchanged codes
   remain primary, including after a manual quotation check. Framing bands are recalculated
   under the same exclusions, including repeat removal within framing streams.
3. `others_mentioned` entries can overlap each other, named stories and seasons; numbers may
   be strings or ranges. Preserve the exact stated count and report entries and numeric
   subtotals separately by season/coder, never call their sum a count of unique unheard people.
   The repeated-story sensitivity cannot identify or remove overlap in these entries.
4. Select the quotation-audit sample reproducibly: for each prediction and each of the three
   primary reporting groups, take the first eligible agreed positive and negative pair in
   season/ID order, and the first eligible disagreement if present. For never-reaching, take
   the first agreed yes and no pair and the first disagreement. Inspect both coders' relevant
   quotations and transcript context, permitting overlap between groups but reporting unique
   records checked. Also examine every below-bar quotation in S24 B and S04 NEG, and check
   the first quoted example for each never-reached reason before publishing any example.
   This is a deliberately contrary-case check, not a random validity estimate.
5. A further sensitivity excludes records of deceased people coded protected/partly protected,
   preserving the codes and without assuming that protection of an earlier, distinct harm was
   impossible. Schema inspection encountered such a record in S17 CB. This checks D1.2's
   application; it does not recode it or replace the pre-registered analysis.

## D8 — 2026-11-11, transcript reconstruction correction before quotation-excluded results

The continuation retrieves the 387 canonical episode files in the original committed
`episode_index.txt`, preserving the episode selection made before coding rather than adding
later publications or refetching discarded alternate transcriptions. The first reconstruction
revealed that **four selected canonical slugs inherit their season from a discarded twin**:
`data-points-child-abuse` (S17), `sww-live-sacramento` (S1), the John Michael Lander WCN episode
(S20), and the Madison McGhee WCN episode (S22). Applying slug-only assignment to those files
incorrectly put them in the unassigned pool.

This was caught by comparing the rebuilt index before publishing results. The source tools
now accept `--frozen-index` to restore the **original** selections and inherited assignments;
this changes no study unit, coder output, identity decision or prediction. All 68 quotation
checks are rerun with that frozen map, replacing preliminary checks. The 207 rebuilt reading
files exactly match the original committed line counts **and word counts**; all 502 reported
reading endpoints match the rebuilt files. `source_validation.json` records these checks and
all coder-file hashes; `transcript_manifest.json` records the canonical sources and hashes.

The original quotation matching heuristic and D7's conservative exclusion rule are unchanged.
A below-bar quotation found verbatim by hand remains flagged in that sensitivity; manual
verification does not silently turn its automatic score into a pass.

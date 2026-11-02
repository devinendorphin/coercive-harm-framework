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

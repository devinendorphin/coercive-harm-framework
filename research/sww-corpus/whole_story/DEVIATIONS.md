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

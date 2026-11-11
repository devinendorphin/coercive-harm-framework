# Prompt for the next session: the whole-story test

*Paste everything below the line into a fresh session that has the
`devinendorphin/coercive-harm-framework` repository attached.*

---

This session runs the self-audit's main repair: the **whole-story test** of how institutions
treated the people in *Something Was Wrong*. Everything you need is in the repo on branch
**`ccr-c49788dd-8fejpj`**. If that branch has not been merged to `main` yet, fetch it and
bring it into your working branch before you start (`git fetch origin ccr-c49788dd-8fejpj`,
then merge it).

**Read these first, in this order, and follow them:**
1. `CLAUDE.md` and `sessions/LATEST.md`, especially standing notes **S-21, S-22 and S-23**.
2. `research/sww-corpus/SELF-AUDIT-2026-11-01.md`: how the last analysis reproduced the
   silencing it studies. Every shortcut in its table is banned in this session.
3. `research/sww-corpus/preregistration-whole-story.md`: the design. It was committed before
   any coding. **Do not change it after coding starts**; if you must, log a dated deviation
   and recode what it affects.

**The rules for this session:**
- **No shortcuts.** Every season is read from its full transcripts, one whole story at a
  time. Summaries, earlier notes, keyword counts and the existing close-read files may help
  you *find* things; they never substitute for reading. If something can't be read in full,
  say so plainly; don't code around it.
- **Machines score, not humans** (Endorphin's decision, S-22). You are authorised to run
  **subagent coders**: two neutral coders per season, plus the framing-test pairs on 6
  randomly chosen seasons, exactly as the pre-registration says. Coders get only their
  season's transcript chunks, the list of unassigned episodes, and the coding instructions.
  They must not see the repo, earlier results, close-read files, or each other's work.
- **Count the people who were never heard**: everyone in a story who never reached an
  institution, with the reasons the story gives.
- **Grade evidence by what backs it up, not by who wrote it.** An institution's own record
  gets no automatic advantage over the person's account.
- **Lean check.** If you notice your own work leaning toward the institution's side (a
  faster write-up, a softer word, a caveat dropped), stop and record it in the self-audit
  file. That has happened at least twice in this project.
- **Plain language** in everything you report to Endorphin. Say the thing, not the label
  ("whether institutions protected the people who came to them", not "C2").
- Naming follows S-21: survivors keep the show's names; only the convicted, public records
  and institutions are named.
- Commit and push after each stage. The container is temporary.

**Steps:**
1. **Rebuild the transcripts** outside the repo (they are not committed):
   `python3 research/sww-corpus/tools/fetch_sww.py /tmp/sww` — one request every 1.5 s with
   back-off, so expect about an hour; run it in the background. When it finishes, run
   `python3 research/sww-corpus/tools/corpus.py index /tmp/sww` and check you get about 387
   episodes, with the 16 unassigned ones listed. If the site has changed and the numbers
   differ, stop and report before coding.
2. **Write the coding instructions and the output format** (one JSON file per season: one
   record per person harmed, with every field in the pre-registration, and the verbatim quote
   behind each coded response). Commit them **before the pilot**.
3. **Pilot on season 17** with the two neutral coders (`corpus.py dump /tmp/sww 17 /tmp/read`).
   Read their output against the transcripts yourself. Fix the instructions only if the coders
   misunderstood them; log any change as a deviation; recode S17 with the final instructions.
4. **Full run**: every season S1–S26 (all seasons the site has), two neutral coders each, in
   background batches. Then the framing test on 6 seasons chosen by a seeded random draw that
   you record before drawing.
5. **Analyse**: agreement between coders per field; the three predictions (W1–W3) on people
   both neutral coders coded the same way, each coder's own result beside it; the framing
   band; the share who never reached an institution and why. Write
   `research/sww-corpus/results/whole_story/RESULTS.md` in plain language, with the earlier
   results (`results/power_vector/RESULTS.md`, `EXTERNAL_DATA.md`) set beside it, not replaced.
6. **Update** the docs that cite the institutions result (`README.md`, docs 04, 08 and 10),
   the self-audit, and `sessions/LATEST.md`; then run `/session-log`.

**Before you report any result, run a disconfirming test on it**: ask what would show it is
wrong, look for that, and say what you found.

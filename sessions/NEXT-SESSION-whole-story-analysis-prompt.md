# Prompt for the analysis session: the whole-story test

*Paste everything below the line into a fresh session that has the
`devinendorphin/coercive-harm-framework` repository attached. Use it only after
`research/sww-corpus/whole_story/STATUS.md` shows coding complete (or lists exactly what is
still missing).*

---

This session analyses the **whole-story test** of how institutions treated the people in
*Something Was Wrong*. The coding is done; your job is the analysis and the write-up. Work on the
branch that holds `research/sww-corpus/results/whole_story/coded/` (currently
`ccr-0935b17a-u165ie`); merge it into your working branch first if it is not on `main`.

**Read these first, in this order, and follow them:**
1. `CLAUDE.md` and `sessions/LATEST.md`, especially standing notes **S-21, S-22 and S-23**.
2. `research/sww-corpus/SELF-AUDIT-2026-11-01.md`, including its lean log. Every shortcut in its
   table is banned.
3. `research/sww-corpus/preregistration-whole-story.md` (the design and the three predictions
   W1–W3), then `whole_story/ANALYSIS-PLAN.md` (how each prediction is computed),
   `whole_story/DEVIATIONS.md` (D1–D4: what changed and why) and `whole_story/STATUS.md` (what is
   coded, and the known issues you must handle).

**What you have:** one JSON file per season per coder in `results/whole_story/coded/`. Claude
neutral coders are `A`/`B`; Codex neutral coders `CA`/`CB`; framing coders `POS`/`NEG` (Claude)
and `CPOS`/`CNEG` (Codex, season 13). Scripts: `tools/analyze_whole_story.py` (written before any
output existed; it reads only `A`/`B` and `POS`/`NEG`, so extend it for the D3/D4 three-way
reporting: all seasons, Claude-only, Codex-only), `tools/check_quotes.py`. The transcripts are not
in the repo; rebuild them only if you need to check a passage (`STATUS.md` says how, about 40
minutes).

**Read deviation D5 first.** Claude coders were shown the project's CLAUDE.md files by the harness
and so were not blinded; Codex coders were. Every Claude-coded figure must be labelled unblinded,
the S17 cross-check used to estimate the difference, and no Claude-only figure presented as blind.

**Decisions to make and commit BEFORE computing any headline** (log each as a dated entry in
`DEVIATIONS.md` if the plan does not already fix it):
- People who reappear across seasons (e.g. S14 survivors coded again in S19 update episodes):
  count once or per season? Report both.
- Records where `reached_institution` contradicts the outcome (several Codex files): report the
  headlines with and without them; never edit coder output.
- Person matching between the two coders of a season uses names, roles and harm descriptions only,
  never the codes; write every hand match to `matching_hand.csv` with its reason.

**Then:**
1. Agreement between the two coders of each season, per field, as the plan lists it; plus the
   person-finding rate. Report Claude pairs, Codex pairs and the S17 Claude-vs-Codex cross-check.
2. W1, W2, W3 on people both coders coded the same way, with each coder's own figure beside it, as
   `ANALYSIS-PLAN.md` says, three ways per D3/D4.
3. The framing band: Claude's from its six framing pairs (S2, S3, S4, S13, S22, S24), Codex's from
   S13. Any headline whose distance from its threshold is smaller than the band is **not decided by
   this method**.
4. The people who were never heard: the share who never reached an institution, with the reasons
   the coders recorded, and the `others_mentioned` counts.
5. **Before you report any result, run a disconfirming test on it**: say what would show it is
   wrong, look for that, and say what you found. Read a sample of the coded records against their
   quotations for each headline, and say how many you checked.
6. Write `research/sww-corpus/results/whole_story/RESULTS.md` in **plain language** ("whether
   institutions protected the people who came to them", not "W1"). Set the earlier results
   (`results/power_vector/RESULTS.md`, `EXTERNAL_DATA.md`) beside it, not replaced. Follow the
   naming rules (S-21): survivors keep the show's names; only the convicted, public records and
   institutions are named; scrub any non-victim or uncharged person's name from quotations you
   publish (`STATUS.md` lists files where coders left some in).
7. Update the documents that cite the institutions result (`README.md`, docs 04, 08 and 10), the
   self-audit (lean log: record anything you notice leaning toward the institution's side), and
   `sessions/LATEST.md`; then run `/session-log`.

**Rules:** no shortcuts; grade evidence by what backs it up, not by who wrote it; plain language in
everything you report to Endorphin; commit and push after each stage (the container is temporary).

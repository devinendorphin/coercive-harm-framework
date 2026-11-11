# Prompt for the analysis session: the whole-story test

*Paste everything below the line into a fresh session that has the
`devinendorphin/coercive-harm-framework` repository attached. Use it only after
`research/sww-corpus/whole_story/STATUS.md` shows coding complete (or lists exactly what is
still missing).*

---

This session continues the existing Codex analysis of the **whole-story test** of how
institutions treated the people in *Something Was Wrong*. The coding is done; your job is the
analysis and the write-up. This is a continuation of this branch's work, not a fresh independent
replication.

**Branch isolation comes first.** Another Claude session is independently doing this task and
is paused under a rate limit. Endorphin requires this work to remain on the **unmerged branch
`analysis/whole-story-isolated`**, so that Claude does not receive it when resuming.

- Use a separate checkout or worktree of `devinendorphin/coercive-harm-framework`; preserve
  existing work. Fetch and check out `analysis/whole-story-isolated` before reading its handoff
  or analysis files. Do not switch or modify another session's working directory.
- Commit and push every stage **only to `analysis/whole-story-isolated`**. Do not push to
  `main`, merge this branch, rewrite `main` or incorporate another analyst's branch. Merging
  requires a new explicit instruction from Endorphin.
- `main` was restored to the original coding-complete commit `ccfabfb`. The decisions and
  matching work below are on this unmerged branch, **not on main**. Do not repeat the earlier
  handoff's instruction to pull them from main.
- Verify access to `podscripts.co` in the updated published SWW environment. The previous
  running instance retained an older policy and returned HTTP 403. Do not waive quotation
  checks if access is still blocked; report the specific blocker and continue independent work.

**Progress to preserve:** `d03752d` fixed D6 analysis decisions before calculation;
`b773dac` recorded identity-only matches and cross-season repeats; `cbc18c8` recorded the
initial handoff. Those commits belong to this branch. **No headline has been calculated, no
whole-story RESULTS.md has been written, the analysis script is unchanged, and no transcript
or quotation checks were performed in that session.**

**Read these first, in this order, and follow them:**
1. `CLAUDE.md` and `sessions/LATEST.md`, especially standing notes **S-21, S-22 and S-23**.
2. `research/sww-corpus/SELF-AUDIT-2026-11-01.md`, including its lean log. Every shortcut in its
   table is banned.
3. `research/sww-corpus/preregistration-whole-story.md` (the design and the three predictions
   W1–W3), then `whole_story/ANALYSIS-PLAN.md` (how each prediction is computed),
   `whole_story/DEVIATIONS.md` (D1–D6: changes, blinding breach and fixed analysis decisions),
   and `whole_story/STATUS.md` (what is coded and the known issues you must handle).
4. `sessions/2026-11-11-whole-story-analysis-handoff.md` and
   `research/sww-corpus/results/whole_story/MATCHING-NOTES.md`. Validate the committed
   `matching_hand.csv` and `repeat_links.csv` for IDs, uniqueness and coverage. Preserve the
   identity-only rule; never revise identity matches to obtain a preferred result. Record
   every additional manual match and unmatched disposition in `matching_hand.csv` with its
   reason, using only the plan's permitted identity fields.

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

**Decisions already fixed before any headline calculation:** follow D6. Report both
person–harm stories per season and identifiable stories counted once across seasons, retaining
the earliest appearance before testing eligibility or agreement. Show unchanged records and
analyses excluding reached/outcome contradictions; never edit coder output. The committed
matching records were made using identity fields, never codes. Read MATCHING-NOTES for
unresolved cases and keep separate harms separate.

Report all seasons, Claude-only and Codex-only. Pooled results use Claude A/B for S17 once;
also show substitution of Codex's S17 pair. Codex-only includes its S17 pair. Show all four
S17 Claude–Codex comparisons. These differences cannot isolate model-family effects from
CLAUDE.md exposure. Show both framing bands beside pooled figures and use the larger for
the pooled decision, as D6 fixes. Any additional necessary choice must be committed as a
dated deviation **on this branch before computing the affected result**.

Scripts live under `research/sww-corpus/tools/`; shorter paths below are relative to
`research/sww-corpus/`. The existing analysis script strips parenthetical harm labels in
name matching: preserve them. Its own-coder W3 calculation also unnecessarily restricts
eligibility to reached=yes; follow the plan's protection/known-worker eligibility consistently.

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

**How to work (to keep usage down):**
- **Do the analysis yourself, in this session. Do not start subagents** or any other agents. The
  coding is finished; nothing in this step needs more coders.
- **Let scripts do the arithmetic.** Counts, rates, agreement figures, intervals and the framing
  band come from `tools/analyze_whole_story.py` (extended as needed) run over the coded files. Do
  not tally by reading files. Read coded records yourself only to check them: the person matching,
  the samples for each disconfirming test, and the quotations you publish.

**Rules:** keep every commit and push on the unmerged `analysis/whole-story-isolated` branch;
no shortcuts; grade evidence by what backs it up, not by who wrote it; plain language in
everything you report to Endorphin; commit and push after each stage (the container is temporary).

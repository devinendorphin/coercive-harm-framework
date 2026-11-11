# Session 2026-11-11 — whole-story test: analysis and write-up

Branch `ccr-f78b372d-8qdcn9` (from `main` at the 2026-11-11 merge of the coding). Run from
`sessions/NEXT-SESSION-whole-story-analysis-prompt.md`. No subagents; every number from a script.

## What was done

1. **Decisions fixed before any figure** (DEVIATIONS **D6**, committed `a6f0cf9`, extended
   during matching as D6.8, still before computing): people retold in another season counted
   both per season and once (`cross_season_repeats.csv`, 94 records); the 21 self-contradictory
   Codex records reported as coded / removed / read by outcome; S17's Claude pair used in the
   pooled figure (Codex pair reported beside); the pooled band = the wider of the two models'
   bands; the S17 cross-check method.
2. **Person matching by hand** for all 26 seasons and the four S17 cross pairs, from names,
   roles, harm descriptions and episodes only (546 decisions with reasons, `matching_hand.csv`).
3. **`tools/analyze_whole_story.py` extended** (committed before its first run): three-way
   reporting, variants, S17 cross-check, quotation flags. **`tools/whole_story_checks.py`**
   (post hoc, labelled): robustness figures, leave-one-season-out, seeded samples.
4. **Results** (`research/sww-corpus/results/whole_story/RESULTS.md`, plain language):
   - Protected: **21 %** of people who reached an institution (Claude 28 %, Codex 16 %).
     Prediction holds every way it is counted.
   - Disbelief / blame / condition-as-dismissal / self-protection: **31 %**, on the 30 % line,
     not decided pooled; Claude 26 % (refuted by the rule, unstable, unblinded); Codex 35 %
     (holds, stable). **50 % for central survivors.**
   - Decisive work by the person or their network: **43 %**, not decided; Codex's "refuted"
     rests on S23 (63 % without it).
   - Never reached: about **three in ten** had no institutional contact in the story; the plan's
     rule shows 3 % for Codex because Codex coded those people "unclear".
   - S17 cross-check: the unblinded Claude coders coded outcomes more favourably to institutions
     than the blind Codex coders (18 vs 4 disagreements in that direction).
5. **Disconfirming tests**: 92 draws of matched people (184 coder records) read against their
   quotations; findings per headline in RESULTS.
6. **Docs annotated beside the earlier 63 % result** (not replacing it): corpus README, doc 04
   item 4, doc 08 OBJ-031 (second test paragraph; status line), doc 10 Finding B.
7. **Self-audit lean log 4–7**; STATUS updated.
8. **Quotation check** (transcripts rebuilt in-session, about 3 hours): 16 of about 9,000
   quotations below the 80 % bar; no verdict changes; all 10 published quotations found verbatim.

## Endorphin's input this session (from the session prompt, close to their words)

- "Do the analysis yourself, in this session. Do not start subagents… Let scripts do the
  arithmetic… Read coded records yourself only to check them."
- "Every shortcut in [the self-audit's] table is banned." "Grade evidence by what backs it up,
  not by who wrote it." "Plain language in everything you report."
- Pinned earlier (STATUS): only the last, extra-paid coder (S24 POS) disclosed the CLAUDE.md
  exposure. Still unexamined.

## Tensions left open

- **Which W2 figure is "the verdict".** D3 says the Claude-only figure is the pre-registered
  one; D5 says Claude coders were not blind as the pre-registration promised. My position: report
  all three, call it split, let neither stand alone (lean log 6). Endorphin has not ruled.
- **Does emergency medical care count as protection for W3?** S23's hospital rescues decide the
  Codex W3 figure. The pre-registration did not say. Open.
- **Was the earlier power-vector test also unblinded?** Those coders were Claude subagents in the
  same container; probably shown the CLAUDE.md files. Not checked.

## Objections

No new objection. OBJ-031 got its second-test paragraph and an updated status line in doc 08.

## Proposed CLAUDE.md edit (not applied; awaiting approval)

Add to the working agreements: *"Blind coders never run as subagents in this container: the
harness loads every CLAUDE.md under the working directories into each subagent. Run them from a
repository with no project instructions (as the Codex kit did), and check what the harness
shows them, not only what they open."* Reason: D5.

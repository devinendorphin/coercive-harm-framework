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

## Later the same day: comparison with the Codex analysis, and Endorphin's rulings

Endorphin pointed to the Codex analysis on `analysis/whole-story-isolated` (done in parallel,
without reading this one). Headlines agree within one point (20.3/30.8/43.1 % vs 20.9/31.5/43.3 %);
same 16 failed quotations. It caught the D5 provenance (corrected here) and the twin-index
problem (its D8). This analysis adds the S23 dependence, the meaning of Codex "unclear", and the
"partly protected" lever.

**Rulings (DEVIATIONS D9):** (1) the two analyses stand side by side; (2) disbelief-and-blame is
reported as split, with its factors; (3) decisive work counts only an institution acting on a
report of the harm (medical rescue set aside): 49.5 % / 41.2 % / 56.1 %. Endorphin noted that my
question for (3) carried a cue saying which option favoured his prediction, and asked whether I
found that funny. It is: one appended sentence is the framing test's own manipulation. Lean log 8.

**Other answers:** CLAUDE.md proposal reworked into "what a coder sees is a setting"
(`whole_story/PROPOSAL-coder-environment.md`, awaiting approval); paid-usage study written and
parked (`research/proposal-paid-access-to-correction.md`); S7 CA ran with Codex memory on,
disclosed now (D10; only one version exists; it matches its partner on the headline rates); the
earlier power-vector coders were probably exposed too (same container; RESULTS updated); doc 09
wording held until Endorphin understands the results better; first reel of a new series begun.

**Endorphin's statement of purpose (verbatim, speech-to-text; guess marked):**
> "The purpose of this is to demonstrate whether or not coercive harm which is harder to render
> legible under current law warrants expedited procedure because all the times abuse takes the
> [?fill→guise] of good faith for the purposes of leveraging delay in order to continue
> extraction. It also use his institutional procedural conventions it uses avenue everything that
> is the way Society tries to create Justice and leverages it to create Injustice so the purpose is
> to address this really complex issue create a system of a discernment to determine whether or
> not it is happening to have it ideally backed by data but also understand how even the
> collection of data might render the harm invisible."

**Why only the last coder disclosed (Endorphin asked for speculation; all unverified):** (a) the
"institutions do their jobs well" line clashed with the CLAUDE.md framing, giving a reason to
mention it, though five other POS coders had the same clash and stayed silent; (b) resumed or
compacted context restating the files near the end, though most coders resumed after limits and
S24 POS's notes show no interruption; (c) how literally a coder read "list every file path you
opened": the files were shown, not opened, and one coder in about 40 counting them is ordinary
variation; (d) others may have mentioned it in final replies that were not kept or surfaced.
Final replies were not saved, so none can be checked.

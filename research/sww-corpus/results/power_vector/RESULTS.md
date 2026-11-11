# Power-vector follow-up: results (2026-11-01)

*Pre-registered in `../../preregistration-power-vector.md` (design, then operational
decisions and two logged deviations, all committed before any code was seen). Coders were
fresh model instances given only `packet.json` (Part 1) or `sample.json` (Part 2); each was
told to read nothing else and reported that it had not. The analyst had seen `results/`.
Inputs, codes and raw outputs are in this folder.*

## Verdicts (pre-registered rule; nothing below replaces them)

| Prediction | Test | Result | Verdict |
|---|---|---|---|
| **P1** impunity (omnipotence rate) higher in `DOWN-INST` seasons | one-sided permutation, 10,000 shuffles | difference −0.047; p = 0.57 (7 vs 19 seasons) | **Refuted** |
| **P2** institutional-failure rate higher in `DOWN-INST` seasons | same | difference −0.108; p = 0.51 | **Refuted** |
| **P3** core function profile does not differ by power position | R2 with power codes | R² = 0.159; p = 0.47 | **Not refuted** |
| **C2 (Part 2)** neutralizing responses outnumber appropriate ones; refuted if appropriate ≥ 40 % of response segments | two coders, 200 segments, verdict on agreed segments | κ = 0.83 (91.5 % agreement). Agreed response segments: **31 appropriate, 18 neutralizing (63 % appropriate)** | **Refuted in this corpus** |

Each coder's own verdict, beside it: coder A (told the hypothesis) 33 of 51, 65 %; coder B
(not told) 32 of 54, 59 %. Both refute. The coder who knew the hypothesis found *more*
appropriate responses than the one who did not.

## Reported beside the verdicts

- **Residual duplicates (deviation 2).** Dropping segments 48 and 97: 30 of 47, 64 %.
- **Analyst's reading of the agreed "appropriate" segments.** The analyst read the other 30
  (97 is one of the dropped duplicates). Most are plain institutional action (a verdict, a
  detective's daily contact, a DA who believed her, a facility that removed a staff member, a
  counsellor's mandated report). Three are weak (14 medical care, 156 a defendant appearing,
  165 expert testimony). Dropping them: 28 of 46, 61 %. Coder A named seven "generous" calls
  of its own; recoding all seven, coder A still has 48 %.
- **Precision audit (standing rule).** Omnipotence lexicon 10/20 (50 %); institutional-failure
  lexicon 5/20 (25 %, 35 % counting two unclear windows). See `precision_audit.md`. P1 and P2
  stand as refuted; a weak instrument is also a reason a real difference could be missed, and
  that is said here rather than used to soften the verdict.
- **Part 1 coding was thin for 7 of 26 seasons** (5, 6, 8, 13, 14, 19, 25), per the coder's
  own notes. Seasons 25–26 have no frozen rates, so P1–P3 ran on the seasons that do.

## Added after review: the outside-world data (`EXTERNAL_DATA.md`)

The first write-up left out the population figures read on the show's expert and Data
Points episodes. They change the conclusion, not the verdict: most harm never reaches an
institution (about 69 % of sexual assaults and 71 % of stalking go unreported), and most of
what does drops out before an outcome (about 1 in 6 reported sexual assaults leads to an
arrest, fewer than 1 in 10 to a felony conviction). **"Appropriate in 63 %" describes the
responses the podcast shows, which over-represent cases that got far enough to have an
outcome.** The outside data support the *inaction* part of the institutional claim at
population scale; they do not show whether the drop-out is disbelief and blame or the limits
of proof and victims' own choices.

## What the result says, and its bound

- **C2, as worded, does not hold in this corpus.** When a segment that mentions an
  institution describes that institution responding to harm, the response is appropriate
  more often than not. The pre-registered bound runs in the other direction from what one
  might expect: a survivor podcast is selected *for* institutional failure, and appropriate
  responses still made up most response segments.
- **What survives is narrower.** The neutralizing moves exist and are nameable: 18 agreed
  segments, mostly inaction (14), with disbelief, reversal and reputation protection rare (1,
  1, 2) and pathologizing absent. That is a present-and-nameable result, not a dominance
  result. Any text in the framework that says or implies institutions *mostly* neutralize
  must be corrected to this.
- **Why the first study's lexicon read differently.** It counted failure words near
  institution words; its precision is 25 %, and it never counted appropriate responses at
  all. The hand-coded test is the better instrument and it replaces the lexicon's impression.
- **Power position did not predict impunity or failure rates.** P1 and P2 were the
  cross-scale claim's sharpest form (the move-set is worse where formal authority is held);
  neither held. P3 (the same function profile across power positions) was not refuted, which
  is compatible with "one mechanism across scale" but is a null, not a demonstration.
- **Step one, still.** None of this is a finding about any institution in particular, and the
  appropriate responses are counter-evidence that the case files must cite with the same
  weight as the failures.

## Files

`packet.json`, `part1_codes.csv`, `part1_output.json`; `sample.json`, `coderA.csv`,
`coderB.csv`, `part2_output.json`; `audit_sample.json`, `precision_audit.md`.

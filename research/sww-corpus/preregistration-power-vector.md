# Pre-registration: power-vector and hand-coded C2 follow-up to the *Something Was Wrong* corpus test

*Written 2026-10-04 after the sycophancy-to-power audit (README, A3, A4 and A7). **Not yet
run.** The analyst who wrote this has seen the season-level rates, so the analyst may not
do the coding below. The coders must be blind to `results/`.*

## Why

The first study coded relationship type, not power, and tested C2 with an instrument
narrower than the claim. Doc 02 holds that behaviour without the power vector is "not
sufficient." Doc 10, Finding B, holds that the framework enforces down-scale while
claiming cross-scale. This follow-up tests the claim the first study under-tested.

## Part 1: perpetrator power position (season level)

**Coder:** Endorphin, or a model instance given **only** show notes and each season's first
two episode descriptions. It must not see `results/`.

**Codes:**
- `DOWN-INST`: the perpetrator holds formal authority or custody granted by an institution
  (cult leader, pastor, program staff, military chain of command, employer, clinician);
- `DOWN-DOM`: parent or guardian over child;
- `INTIMATE`: partner. Recorded separately, not merged into lateral, because the power in
  intimate partnerships is often structural but informal;
- `LATERAL`: friend, sibling, peer, community member;
- `MIXED`.

**Predictions, with refutation in brackets:**
- **P1.** Impunity rate (omnipotence lexicon) is higher in `DOWN-INST` seasons than in all
  others. [Refuted if not higher, permutation p ≥ 0.05.]
- **P2.** Institutional-failure rate is higher in `DOWN-INST` seasons. [Same test.]
- **P3.** The core function profile does *not* differ by power position (the R2 test,
  repeated with power codes). [Refuted if p < 0.05.]

## Part 2: hand-coded C2 (segment level)

**Sample:** 200 segments drawn at random from **all** episodes, *including* the update,
Q&A and WCN episodes. A segment is eligible if it contains an institution word: police,
court, judge, prosecutor, church leadership, school, university, Title IX, HR, military
command, program staff, CPS, or a medical provider.

**Coders:** two. Coder B is told only the category definitions, not the hypothesis.
Agreement is reported as Cohen's κ.

**Categories** (one per segment):
- **inaction or failure**;
- **disbelief**;
- **reversal**: the victim is blamed, punished or counter-accused;
- **pathologizing**: the victim's condition becomes the reason to disbelieve;
- **reputation protection**: concealment, transfer, settlement with silence;
- **appropriate response**: believed, investigated, protected, charged;
- **not a response** (mention only);
- **unclear**.

**Prediction:** among segments that describe a response, the neutralizing categories
(inaction, disbelief, reversal, pathologizing, reputation protection) outnumber
appropriate response.

**Refutation:** C2 is refuted *in this corpus* if appropriate responses are ≥ 40 % of
response segments.

**Bound stated in advance:** a survivor podcast is selected for institutional failure, so
a pass shows that the move-set is present and nameable. It does not give a rate.
Appropriate responses are **counter-evidence** and are reported in full.

## Verdict rule

The standing rule in `preregistration.md` applies: one verdict rule and one
precision-audit rule for every prediction.

## Operational decisions fixed before coding (2026-11-01)

*Written and committed before any coding, with `power_vector.py`. The analyst has seen
`results/`; the coders are fresh model instances given only what is listed here.*

- **Part 1 coder:** a model instance given **only** the publisher's notes for the first two
  narrative episodes of each season (`power_vector.py packet`) and the code definitions above.
  It is not shown `results/`, `settings.csv`, the README or any close-read file.
- **Part 2 segments:** a 3-sentence window centred on a transcript sentence that matches the
  institution list (the pre-registered list, plus counsellors, social workers, caseworkers,
  DHS, therapists, psychiatrists, nurses, hospital and "staff", which were implied by "program
  staff", "CPS" and "a medical provider"). Candidates come from **all** episodes, including
  update, Q&A and WCN episodes. Windows that overlap a drawn window are skipped. Seed 20261101.
- **Part 2 coders:** two fresh instances. **Coder A** is told the hypothesis; **coder B** gets
  only the category definitions. Neither sees the other's codes.
- **Disagreements:** the verdict is computed on segments both coders placed in the same
  category. Each coder's own verdict is reported beside it, under the one-rule standing note.
- **Tests:** P1 and P2 use a one-sided permutation test (10,000 shuffles) of the mean rate,
  `DOWN-INST` against all other coded seasons. P3 repeats `analyze.py`'s R2 statistic with
  power codes. Rates come from the frozen `results/season_rates.csv`. The transcripts were
  re-fetched for Part 2 only.
- **Precision audit (standing rule):** the omnipotence lexicon (P1) and the
  institutional-failure lexicon (P2) each get the same 20-hit reading audit that isolation,
  reversal and institutional failure received in the first study. Omnipotence was never audited.

## Deviations (logged before the packet or the sample was drawn)

- **2026-11-01, de-duplication.** The fetched corpus holds two machine transcriptions of 262
  of its 417 episodes. `episodes()` as first committed iterated every file, so the Part 1
  packet could show one episode twice where it should show two, and Part 2 would give
  double-transcribed episodes twice the chance of being drawn and could draw one passage
  twice. `episodes()` now keeps one transcription per episode (key: the slug without its
  `sN-eM-` prefix; the longer text is kept), the rule the close-read already used. This
  implements "the first two narrative episodes" and "200 segments drawn at random from all
  episodes" as written; no definition, category, threshold or test changed. Nothing had been
  drawn or coded when it was made.
- **2026-11-01, residual duplicates (found after drawing, before any Part 2 code was seen).**
  The de-duplication key missed two listing patterns: 17 episodes (all S24) listed a second
  time with a `-2` suffix, and WCN episodes listed both with and without a season prefix. The
  drawn sample therefore gives those episodes double weight and contains two near-duplicate
  pairs (segments 30/48 and 60/97). **The sample is kept as drawn** (redrawing after coders
  had started would be a second draw). The pre-registered verdict is computed on all 200; a
  sensitivity result that drops segments 48 and 97 is reported beside it, never in its place.

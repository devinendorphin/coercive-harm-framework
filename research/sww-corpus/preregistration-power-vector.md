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

# *Something Was Wrong* corpus — a test of the low-variance / "fractal" claim

*Compiled 2026-10-04 at Endorphin's direction. Cross-filed: the ledger-side entry is
`veriticide-general-ledger/docs/sww-corpus-low-variance-test-2026-10-04.md`. Design was
pre-registered and pushed before analysis (`preregistration.md`, commit `e0bdc7b`).
Deviations are logged in the pre-registration and below.*

## The claim, and the test

Endorphin (primed): the podcast "should help establish how low variance these tactics are
across various strata of society … like a fractal." Two claims were separated:

- **C1 — low variance across settings.** The coercive *function* profile is about the same
  whatever the setting.
- **C2 — self-similarity ("fractal").** The institutions a survivor turns to reproduce the
  perpetrator's neutralizing moves.

Five refutation criteria (R1–R5) were fixed in advance. Details are in `preregistration.md`.

## Corpus

| | |
|---|---|
| Source | podscripts.co machine transcripts (no speaker labels). Transcripts are **not** committed (copyright) |
| Pages fetched | 634 episode pages, seasons 1–26 (2019 – Sep 2026); 9 have no transcript |
| Unique episodes | **382** after title de-duplication. The site lists many episodes twice, as separate transcriptions |
| Narrative seasons | 26. S25 has only its first episode on the site. S17's setting could not be coded and is excluded from R2 |
| Control | *The Moth*, 61 episodes with transcripts, about 335k words, same site and pipeline |

**Settings coded from show notes before any rates were seen** (`settings.csv`): intimate
partner (13 seasons) · family (3) · group/institutional (8: Jonestown, a religious group,
a workplace, military sexual assault, the troubled-teen industry, a university, a midwifery
practice) · other non-intimate (2: friendship betrayal, a community rental scam).

## Results

Rates are per 10k words. Ratio = median season rate ÷ control mean.

| Function | Ratio | Elevated in % of seasons, **pre-registered** (vs single-episode p90) | Elevated, **post-hoc** (vs length-matched p90) |
|---|---|---|---|
| **Frame vocabulary** (gaslight, narcissist, love bomb, red flag…) | **11.8×** | — | 100 % |
| Reversal (DARVO-type) | 6.9× | 81 % *(control p90 = 0, so this means "present at all")* | 81 % |
| Isolation | 3.4× | **27 %** | 77 % |
| Threats / stalking | 2.3× | 38 % | 81 % |
| Perception / reality control | 2.2× | **46 %** | 77 % |
| Omnipotence / impunity | 1.9× | 85 % *(control p90 = 0)* | 35 % |
| Institutional failure | 1.7× | 69 % *(control p90 = 0)* | **35 %** |
| Economic control | 1.2× | 31 % | 85 % *(shows the post-hoc bias; see below)* |
| Degradation | 1.1× | 0 % | 46 % |
| Micro-regulation | 0.8× | 4 % | 31 % |
| Intermittent reward | 0.8× | 0 % | 23 % |

**The two baselines are biased in opposite directions.**
- The pre-registered baseline compares long pooled seasons with *short single* Moth
  episodes, whose rates are noisier. Its 90th percentile is set too high, which biases the
  test **against** the claim.
- The post-hoc baseline resamples one small control corpus, so its 90th percentile is set
  too narrow, which biases the test **toward** the claim. Economic control gives it away:
  a 1.2× ratio still counts as "elevated" in 85 % of seasons.
- The ratio column is the most trustworthy summary. The pre-registered column is the one
  that counts as the test.

### Verdict against each criterion

| Criterion | Pre-registered result | Reading |
|---|---|---|
| **R1** core functions elevated in ≥ 75 % of seasons | **FAILED for isolation (27 %) and perception (46 %)**. Reversal passed (81 %), but only against a zero baseline | The flaw was spotted after a smoke test on partial data, so the post-hoc pass (77/77/81 %) is labeled post-hoc and is not substituted. The ratios (3.4×, 2.2×, 6.9×) show these functions are clearly over-represented. Whether they reach "nearly every case" is not shown |
| **R2** settings cluster the profiles | **Not refuted**: coarse R² 0.15 vs a chance level of 0.125, p = 0.21. Fine 9-way coding: p = 0.31. With title de-dupe: p = 0.15 | No detectable setting effect. **This is weak evidence**: n = 25, with unbalanced groups (13 intimate-partner seasons) |
| **R3** profiles more alike than control pseudo-seasons | **Passed**: mean pairwise ρ 0.39 vs a null mean of 0.23 (95th percentile 0.32), p = 0.004. With de-dupe: 0.41 vs 0.14, p = 0.001 | The seasons share a function profile beyond what English produces |
| **R4** convergence survives in the low-frame-vocabulary half | **Passed**: low-label half ρ 0.36 (de-dupe 0.34), above the null 95th percentile. High-label half 0.40 (0.49) | Convergence is not *only* the show's vocabulary. It is stronger where the vocabulary is denser, which is consistent with partial frame imposition |
| **R5** (C2) institutional failure elevated in ≥ 50 % of seasons | Passed as written (69 %), but **only against a zero baseline**. Length-matched: 35 %. Reading samples: the indicator's precision is about half | **C2 is not established by this test** |

## What this does to the claims

**C1, low variance across settings: `[SUPPORTED]`, qualified.** Across seasons spanning
intimate partners, families, a cult, a religious group, a workplace, the military, the
troubled-teen industry, a university, a midwifery practice, a friendship and a community
scam:
- no setting effect on the function profile was detected;
- the seasons share a profile more than ordinary narratives do;
- reversal, isolation, threats and perception control are the over-represented core.

This is consistent with Biderman's and Herman's cross-setting convergence (see
`coercion-continuity-across-scale.md`). It does **not** reach "nearly every case shows the
core functions." That pre-registered criterion failed for two of the three core functions.

**C2, fractal self-similarity: `[HYPOTHESIS]`. Not established here.** The corpus
contains clear instances:
- a pastor "so dismissive of it" (S1);
- "the police didn't do anything" (S10);
- an assault not reported because "the offender's father was a police officer, and I
  thought no one would believe me" (S11);
- a death ruled homicide where "no charges were ultimately filed" (S24);
- institutions that "would rather the victim be ignored … than have their reputation be
  tarnished" (S19).

But a crude institution-plus-failure co-occurrence measure cannot separate these from
noise. A real test needs hand-coded segments, and a coder blind to the hypothesis.

**"Strata of society" was not tested.** Show notes allow coding of **setting**, not class,
income, race or education. The settings do run from the Playboy Mansion (S15) to military
and firefighter families (S3, S21), but nothing here measures variance across class.

**The loudest signal is the frame.** Frame vocabulary is 11.8× the control rate, a larger
ratio than any behaviour. The corpus is narrated, heavily, in therapy-culture and
coercive-control vocabulary. R4 shows the convergence is not *only* that, but frame
saturation is the main reason this corpus cannot carry more than `[SUPPORTED]`.

## Limits no statistic here removes

1. **Curation.** One host selects stories that fit the show. Selection alone can produce
   convergence.
2. **Narration through a learned frame.** See above.
3. **No speaker separation.** Host narration, survivor speech and expert segments are
   pooled.
4. **The lexicon is crude.** Negation, quotation and commentary all count. Reward,
   degradation and micro-regulation could not be separated from ordinary speech. That is a
   null for the instrument, not a finding about the behaviour.
5. **Small control corpus** (61 episodes).
6. **Expert episodes only partly excluded.** The slug filter catches `with-dr` and
   `data-points`, but not `featuring`/`ft.` episodes inside seasons (e.g. S3 E10, S5 E15,
   S6 E3). These add frame vocabulary and some generic tactic terms.

## Role in the framework

- **doc 04, Finding 4** (`foreseeability-and-risk-assessment.md`): the corpus stays
  **illustrative, not a dataset**. This test moves it from "assumed convergent" to
  "measured convergent at function level, with the named limits." It is still not a base
  rate.
- **doc 02, cluster coherence (OBJ-001):** partial corpus-level support for co-occurrence
  of isolation, perception control, reversal and threats. It is not a validated instrument.
- **Next test, if wanted:** hand-code ~200 segments for C2 (institutional reproduction of
  DARVO, minimization and disbelief), with a second coder blind to the hypothesis.

## Files

`preregistration.md` (design and deviations) · `analyze.py` (frozen pre-registered
analysis) · `posthoc.py` (labeled post-hoc checks) · `settings.csv` (setting codes and their
basis) · `results/` (`results.json`, `season_rates.csv`, `posthoc_length_matched.csv`,
`robustness_title_dedupe.json`, `r2_fine_settings.json`).

## Sources

- Transcripts: https://podscripts.co/podcasts/something-was-wrong/ (634 pages, fetched
  2026-10-04)
- Control: https://podscripts.co/podcasts/the-moth/
- Show: https://somethingwaswrong.com (Tiffany Reese / Broken Cycle Media)

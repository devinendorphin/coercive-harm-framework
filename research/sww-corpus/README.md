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
| **R5** (C2) institutional failure elevated in ≥ 50 % of seasons | **Passed** (69 %), against a zero baseline, the same caveat as reversal in R1. Post-hoc length-matched: 35 %, reported beside the result and not in place of it. Precision on a reading sample is about half, close to isolation's (about 55 %) | *Corrected in the power audit below.* The first version let the post-hoc failure override this pre-registered pass, the opposite of how R1 was handled. C2 was **not adequately tested**: the instrument was narrower than the claim, and the episodes richest in institutional aftermath were filtered out |

## What this does to the claims

**C1, low variance across settings: `[SUPPORTED]`, qualified.** Across seasons spanning
intimate partners, families, a cult, a religious group, a workplace, the military, the
troubled-teen industry, a university, a midwifery practice, a friendship and a community
scam:
- no setting effect on the function profile was detected;
- the seasons share a profile more than ordinary narratives do;
- reversal, isolation, threats and perception control are the over-represented core.
- *(Added in the power audit.)* On a 20-hit reading sample, the isolation lexicon's
  precision is about 55 %, mostly "so isolating" and "isolated incident." That is the same
  noise level used against C2. Reversal's precision is about 80 %.

This is consistent with Biderman's and Herman's cross-setting convergence (see
`coercion-continuity-across-scale.md`). It does **not** reach "nearly every case shows the
core functions." That pre-registered criterion failed for two of the three core functions.

**C2, fractal self-similarity: not adequately tested by this corpus study.** *(Corrected
in the power audit. The first version said "not established here," which put an
instrument failure onto the claim.)* Its evidential status in the framework rests on the
literature: institutional betrayal (Smith & Freyd 2014) and the custody inversion of abuse
claims (Meier et al. 2020), both catalogued as E4 and E5 in the ledger's
coercive-control foundation file. That gives `[SUPPORTED]`. The corpus contains clear
instances:
- a pastor "so dismissive of it" (S1);
- "the police didn't do anything" (S10);
- an assault not reported because "the offender's father was a police officer, and I
  thought no one would believe me" (S11);
- a death ruled homicide where "no charges were ultimately filed" (S24);
- institutions that "would rather the victim be ignored … than have their reputation be
  tarnished" (S19).

Some instances name institutions, attributed as the show and its cited sources report
them (step one: allegations and official records, not findings):
- **Trails Carolina** (S24): a 12-year-old died within 24 hours of arrival in Feb 2024.
  The medical examiner listed the death as homicide. The district attorney filed no
  charges.
- **Asheville Academy** (S24 show notes, citing Spectrum News and Asheville News): fined
  $45,000 after a state child-safety investigation. It gave up its license after two
  suicides in May 2025.
- **Utah Valley University and the University of Utah** (S25): according to a student's
  lawsuit as reported, both schools failed to act on her 2019 rape report.

The first version named none of these. It wrote "the troubled-teen industry" and "a
university."

A real test needs hand-coded segments, including institutional *reversal* and
pathologizing, not only "failure" words, and a coder blind to the hypothesis.

**"Strata of society" was not tested.** Show notes allow coding of **setting**, not class,
income, race or education. The settings do run from the Playboy Mansion (S15) to military
and firefighter families (S3, S21), but nothing here measures variance across class.

**Frame vocabulary is 11.8× the control rate.** *(Corrected in the power audit. The first
version called this "the loudest signal" and "the main reason" for the ceiling. That was
the "coached witness" discount.)* What the count measures is that survivors, the host and
experts have **names** for what happened. Acquiring names for an unnamed harm is the remedy
for hermeneutical injustice, not evidence of fabrication. The pre-registered test of
whether the frame *produces* the convergence is R4, and R4 passed. The ceiling on this
corpus is **curation**: one selection process, which bounds base-rate claims.

## Sycophancy-to-power audit (2026-10-04, operator request)

*Lens: `docs/10-power-critique.md`. Question: where did this study put the heavier burden on
the claim that implicates power? The claim that does is C2: institutions such as police,
courts, churches, universities, the military and the troubled-teen industry reproduce the
perpetrator's moves. C1 implicates individual perpetrators.*

| # | What the first version did | Why it favoured power | Status |
|---|---|---|---|
| A1 | **Asymmetric verdict rule.** R1's pre-registered *failure* stood, and its post-hoc pass was "not substituted." R5's pre-registered *pass* was overridden by its post-hoc failure. Reversal (interpersonal) was counted as passing against a zero baseline. Institutional failure was counted as failing with the same zero baseline | Each choice of rule went against the claim at hand. The institutional claim got the rule that failed it | **Corrected.** One rule for every criterion: the pre-registered result is the verdict, and the post-hoc result is reported beside it |
| A2 | **Asymmetric scrutiny.** Only the institutional indicator was audited for precision (about half), and that audit was used to discount C2. Isolation was never audited | Audited now: isolation precision is about 55 %, the same noise level. The scrutiny went to the claim about institutions | **Corrected.** Both precisions reported; reversal about 80 % |
| A3 | **The exclusion filter removed the aftermath.** Update, Q&A and WCN episodes were excluded as "non-narrative." Post-hoc check: in those episodes institutional failure is about 25 % denser (0.45 vs 0.36 per 10k words) and impunity about 2× denser (0.95 vs 0.48) than in the narrative episodes kept. Reversal is lower (0.33 vs 0.49) | The filter was chosen without asking what C2 needs, and it removed the material where police, courts and institutions respond | **Recorded.** The C2 test was underpowered by design. The next test includes those episodes |
| A4 | **Instrument narrower than the claim.** C2 was measured only as "institution + failure word." Institutional *reversal* got counted as interpersonal: "The church had convinced him that he was the problem" (S4) scores as reversal, not as institutional. Institutional pathologizing was not measured at all | The claim was "institutions reproduce the moves." The measure covered one move, and the verdict ("not established") landed on the claim | **Corrected.** C2 marked "not adequately tested." Its framework status rests on the literature (E4, E5): `[SUPPORTED]` |
| A5 | **Headline asymmetry.** In chat: "The 'fractal' part did not come through." C1, with a *failed* pre-registered criterion, was headlined "supported, with conditions" | A headline-level disconfirmation of the institutional claim, from an instrument failure | **Corrected** here and in the reply to the operator |
| A6 | **Generic institutions.** "The troubled-teen industry," "a university," "the military." The show and its sources name Trails Carolina, Asheville Academy, Chrysalis (later sold to Embark Behavioral Health), and Utah Valley University and the University of Utah | The same error the ledger's foundation file recorded the day before ("generic state examples avoid naming the powerful"). Individual survivors' words were quoted, but no institution was named | **Corrected** (named, attributed, step one) |
| A7 | **No power-vector coding.** Settings were coded by relationship type, and 13 of 25 seasons were intimate-partner. The perpetrator's power position was never coded: cult leader, pastor, a celebrity's mansion, military command, a program with custody of children, a peer | This repeats doc 10 **Finding B**: enforcing down-scale while claiming cross-scale. Doc 02 says behaviour without the power vector is "not sufficient." The operator's "strata" question is a power question; I converted it to "setting," then reported strata as untested | **Next test pre-registered** (`preregistration-power-vector.md`). I have seen the season rates, so a blind coder must code power |
| A8 | **Frame vocabulary as "the loudest signal."** Survivors' use of names for what happened (gaslighting, DARVO, love bombing) was made the main reason for the ceiling, after R4 had already passed | This is structurally the "coached witness" discount: the Yale–New Haven "coached by her mother" move in the ledger's survivor comparator, and E3. Acquired concepts are the remedy for hermeneutical injustice (Fricker 2007, gen.) | **Corrected.** The ceiling is curation |

**Pattern.** Every error ran the same way: the burden fell on the claim about institutions.
The ledger's foundation file recorded this exact failure ("the highest burden fell on the
scale that implicates states") **one day earlier**, and it recurred anyway. A note did
not hold. That is why the ledger made developer-symmetry a script, and the same applies
here. **Standing rule, added to `preregistration.md`:** a multi-criterion test declares
one verdict rule and one precision-audit rule, and applies both to every criterion
before any verdict is written.

## Limits no statistic here removes

1. **Curation.** One host selects stories that fit the show. Selection alone can produce
   convergence.
2. **Shared vocabulary** may smooth surface descriptions. R4 tested whether it drives
   the convergence, and it does not.
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
- **Next test, if wanted:** see `preregistration-power-vector.md`. Perpetrator power
  position is coded by a coder blind to the rates, and C2 segments are hand-coded,
  update and aftermath episodes included.

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

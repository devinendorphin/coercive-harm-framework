# Pre-registration — *Something Was Wrong* corpus test of the low-variance / "fractal" claim

*Written and committed 2026-10-04 **before** any tactic counts were computed. Transcripts
were being downloaded at the time of writing; none had been analysed. The commit timestamp
of this file is the evidence of ordering.*

## The claim under test (Endorphin, 2026-10-04, primed)

> "…that should help establish how low variance these tactics are across various strata of
> society. As to be like a fractal."

Two separable claims:

- **C1 — low variance across strata.** The coercive *function* profile (not the surface
  behaviours) is roughly the same whatever the setting: intimate partner, family,
  friendship, religious community, professional/workplace, group/cult/MLM, institution.
- **C2 — self-similarity ("fractal").** The same moves recur one scale up: the institutions
  a survivor turns to (police, courts, church leadership, HR, schools) reproduce the
  neutralizing moves of the individual perpetrator (disbelief, reversal, minimization).

## Corpus

- *Something Was Wrong* (Tiffany Reese / Broken Cycle Media, 2018–2026), all episode
  transcripts available on podscripts.co (machine transcripts; no speaker labels).
- **Narrative-season subset:** episodes whose slug/title contains none of
  `q-a, qa, update, bts, wcn, presents, data-points, bonus, trailer, answering, with-dr,
  black-lives-matter, announcement`. Grouped by season number; one season ≈ one case.
- **Control corpus:** *The Moth* (first-person true stories, broad social range, not
  abuse-focused), ~80 most recent episodes from the same site, same transcription pipeline.
- Transcripts stay outside the repo (copyright). Only the analysis script, derived counts,
  and short quotations are committed.

## Measures (lexicon fixed here; not to be tuned after results)

Ten **behaviour-level** function indicators, mapped to Biderman / Duluth / Freyd
(regexes in `analyze.py`, frozen with this file): isolation · perception/reality control ·
economic control & debility · threats & intimidation · intermittent reward ·
omnipotence/impunity · degradation · micro-regulation & surveillance · reversal (DARVO-type)
· institutional failure (an institution word and a failure word in the same transcript
segment).

One **label-level** frame indicator (the show's and the therapy culture's vocabulary):
gaslight*, love bomb*, DARVO, narcissis*, coercive control, trauma bond*, flying monkey*,
grooming, red flag*, sociopath*, psychopath*, manipulat*.

Rates are per 10,000 words. A function is **elevated** in a season when its rate exceeds
the 90th percentile of the control episodes' rates for that function.

## Refutation criteria (stated in advance)

- **R1 (core invariance).** If isolation, perception control, or reversal is *not*
  elevated in ≥ 75 % of narrative seasons, C1 fails for that function.
- **R2 (strata clustering).** Seasons are coded by setting from show notes and content
  warnings, *before* rates are inspected. A permutation test (10,000 shuffles) on the
  between-setting share of profile variance (z-scored log rates). If p < 0.05 **and**
  R² ≥ 0.25, C1 is refuted at the function level. *A null here is weak evidence only:
  ~20–25 seasons gives low power.*
- **R3 (lexicon artefact).** Mean pairwise Spearman correlation of season function
  profiles (rates divided by control mean) is compared with the same statistic on
  control pseudo-seasons (random Moth episodes pooled to matching word counts, 1,000
  draws). If SWW profiles are not more similar to each other than control pseudo-seasons
  are, the apparent convergence is a property of English, not of coercion.
- **R4 (frame circularity).** Seasons are split at the median label-term rate. If the
  R1/R3 convergence holds only in the high-label half, the convergence is plausibly the
  show's frame imposed on the stories, not the stories.
- **R5 (C2 — institutional self-similarity).** If institutional failure is elevated in
  fewer than half of narrative seasons, C2 fails in this corpus.

## Known threats that no statistic here removes

1. **Curation.** One host selects stories that fit the show. Convergence is partly
   manufactured by selection. Nothing in this design can rule that out; it bounds every
   finding.
2. **Narration through a learned frame.** Survivors who have listened to the show describe
   their experience in its vocabulary. R4 tests this only partially.
3. **No speaker separation.** Host narration, survivor speech, and expert segments are
   pooled.
4. **Strata are thin.** "Strata of society" in the class sense (income, race, education)
   is mostly not recoverable from show notes. What can be coded is *setting*. The test
   is of setting-variance, and the write-up must say so.
5. **Lexicon counts are crude.** Negation, quotation, and host commentary all count.

## Deviations logged before results (2026-10-04, same session, still blind to all rates)

- **D1 — duplicate pages.** The source site lists many episodes under two slugs
  (`s1-e1-…` and `s1-ep1-…`). Episodes are de-duplicated by text hash. Rates are
  unaffected by exact duplication; episode counts would not be.
- **D2 — the R² threshold was wrong as written.** With ~9 fine setting categories over
  ~25 seasons, the chance-level R² is about (k−1)/(n−1) ≈ 0.33, so "R² ≥ 0.25" would fire
  on noise. Corrected rule: settings are collapsed to **four coarse strata** (intimate ·
  family · group/institutional — religious group, workplace, professional, institution ·
  other non-intimate — friendship, community scam), chosen now from `settings.csv`; the
  test is the permutation p-value, and the write-up reports observed R² **against the
  permutation-null mean**, not against a fixed bar. The fine 9-way coding is also run and
  reported.
- **D3 — S17 excluded from R2** (setting not determinable from notes; transcript opening
  empty). It stays in R1/R3/R4.

## Deviations and additions after results were seen (2026-10-04) — labeled post-hoc

- **D4 — near-duplicate transcriptions.** The duplicate pages are *different* machine
  transcriptions under *different* episode numbers (e.g. `s1-e14-we-all-dodged-a-bullet`
  vs `s1-ep13-…`), so the D1 hash de-dupe missed them. A robustness re-run de-duplicated
  by title (382 unique episodes) and gave the same verdicts (`results/robustness_title_dedupe.json`).
  The primary results are left as pre-registered.
- **D5 — baseline asymmetry.** "Elevated" compares pooled seasons with single short
  control episodes, which biases the test against the claim. The asymmetry was noticed on a
  smoke test of partial data, *after* seeing partial numbers. The length-matched
  comparison in `posthoc.py` is therefore post-hoc and is reported beside the
  pre-registered result, never in place of it. It has the opposite bias.
- **D6 — 88 pages were rate-limited** on the first pass and returned empty; they were
  re-fetched before the full analysis. Nine pages have no transcript on the source.

## Standing rule (added 2026-10-04 after the sycophancy-to-power audit)

Every criterion gets the same verdict rule: **the pre-registered result is the verdict,
and post-hoc results are reported beside it, never in its place.** Every indicator used in
a verdict gets the same precision audit (a random 20-hit reading sample). Both rules are
applied before any verdict is written. The first write-up broke both, each time against
C2, the claim that implicates institutions (README, audit A1–A2).

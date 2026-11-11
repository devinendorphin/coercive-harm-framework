# Analysis plan and operational decisions (committed before the pilot, 2026-11-01)

*Puts `../preregistration-whole-story.md` into practice. Nothing here changes the predictions
or their thresholds. Where the pre-registration leaves a choice open, the choice is fixed here
before any coding output exists. Changes after this commit go in `DEVIATIONS.md`, dated.*

## Files

- `CODING-INSTRUCTIONS.md` — what every coder receives (the text below its first `---`),
  copied unchanged to `INSTRUCTIONS.md` beside the transcripts. Framing-test coders receive
  the same text with one sentence added at the top (below).
- `OUTPUT-FORMAT.json` — the example record, given to every coder.
- Outputs: `../results/whole_story/coded/sNN_<coder>.json`, one per season per coder.
  Coders' running `notes.md` files contain long transcript quotations and stay outside the
  repo (the transcripts are not committed either).

## Coders

- **Neutral coders A and B**, one pair per season, fresh general-purpose model instances. Each
  is told only: its season folder, the unassigned folder, the instructions, the format, and
  its output path. The prompt contains nothing about this project, its hypotheses or earlier
  results.
- **Framing pair** on 6 seasons: coder **POS** gets, above the instructions, "Background you
  should keep in mind: institutions usually do their jobs well." Coder **NEG** gets
  "Background you should keep in mind: institutions usually fail victims." Nothing else
  differs.
- **Isolation is by instruction, not enforced by the machine.** The coders run on the same
  machine as the repository. Each is told to open nothing else and to list every file it
  opened; those lists are kept and checked. This limit is reported in the results.

## The framing-test draw (recorded before drawing)

`random.Random(20261101).sample(seasons, 6)`, where `seasons` is the sorted list of season
numbers that `corpus.py index` assigns at least one episode to. Python 3 standard library.
The draw is run once, after the pilot, and its output is committed before any framing coder
starts.

## Matching people across the two coders

Coders name people independently. The analyst matches records using **only** the `name`,
`role_in_story`, `harm`, `perpetrator_role` and `episodes` fields, never the codes. First
automatically (same name after lower-casing and removing brackets), then by hand for the
rest. Every hand match, and every record left unmatched, is written to
`../results/whole_story/matching.csv` with the reason. A person found by only one coder counts
in that coder's own results and is reported as a person-finding disagreement.

## What each prediction is computed on

The headline for each prediction uses **people both neutral coders coded the same way on
what that prediction needs**:

- **W1** (fewer than 40 % of people who reached an institution end protected; refuted at
  40 % or more). Denominator: matched people both coders code `reached_institution = yes`.
  Agreed if both coders agree on whether the outcome is `protected`. Result: protected ÷
  agreed.
- **W2** (at least one response of disbelief, blame or counter-accusation, condition-as-
  dismissal, or self-protection in the stories of 30 % or more of people who reached an
  institution; refuted under 30 %). Indicator: any contact coded `disbelieved`,
  `blamed_punished_or_counter_accused`, `condition_as_dismissal` or `protected_itself`.
  Denominator: matched people both code `reached = yes`, agreed on the indicator.
- **W3** ("where protection came", the decisive work was done by the person, their network,
  other victims or publicity, not the institution on its own initiative, in 50 % or more;
  refuted under 50 %). "Where protection came" = outcome `protected` or `partly_protected`
  (the pre-registration's item 5 says "any protection"). Indicator: `decisive_work_by` is
  `the_person`, `family_or_friends`, `other_victims` or `journalists_podcast_or_virality`
  (versus `institution`). Denominator: matched people both code as protected or partly
  protected, both give a non-`unclear` decisive worker, and agree on the indicator.
  "Institution on its own initiative" is read as: the institution did the decisive work
  itself once the harm reached it. A report alone does not make the reporter the decisive
  worker (instructions §4). This reading makes W3 harder to confirm, not easier.
- **Beside each headline**: coder A's own result and coder B's own result on all their own
  records; the W3 figure on `protected` only; the figures for central survivors only; the
  figures by season; Wilson 95 % intervals. None of these replaces the headline.
- **Outcome precedence.** A person harmed by an institution and later protected counts as
  protected for W1 (instructions §3), which makes W1 harder to confirm. The share of people
  harmed by an institution at any point (`harmed_by_institution_ever`) is reported beside it.

## The people who were never heard

- Share of all agreed people (both coders code `reached`, and agree) with `reached = no`.
- Reasons: tallied separately for each coder, and the reasons both coders give for the same
  person. Quoted examples in the results.
- `others_mentioned` (people who exist in the story but whose story is not told) are tallied
  per season with any stated numbers, and reported as people never heard; they are not added
  to the person count.

## Agreement

Per field, on matched people: percent agreement and Cohen's kappa for `reached_institution`,
`outcome` (five categories), the W2 indicator, the W3 indicator, `harmed_by_institution_ever`,
and `person_account_alone`; the number of contacts each coder recorded; and the person-finding
rate (people found by both ÷ people found by either).

## Framing band

On the 6 drawn seasons, each framing coder's own figures for W1, W2, W3 and the never-reached
share (all of that coder's records). **Band = |POS − NEG|** for each figure. If a neutral
headline's distance from its threshold is smaller than the band, that result is reported as
**not decided by this method**. The neutral coders' own figures on the same 6 seasons are shown
beside the framing pair.

## Checking the quotations

A script checks every quotation against the transcript text (case and punctuation removed;
a quotation counts as found if at least 80 % of its words appear in order within a window of
the episode it cites, or of the season if the slug is wrong). The found rate is reported per
coder. Records whose decisive quotation cannot be found are flagged and reported both ways;
they are not silently dropped.

## Reading in full

Each coder reports, for every chunk file, the last line number it read. The analyst checks
these against the files' real line counts. A coder that did not read a file to its end is
re-run for that season; if a season cannot be read in full, the results say so.

# What happened to each person, told whole: results (2026-11-11)

*Pre-registered in `../../preregistration-whole-story.md`; how each figure is computed is in
`../../whole_story/ANALYSIS-PLAN.md`; every change is in `../../whole_story/DEVIATIONS.md`
(D1–D6). The decisions in D6 (repeats, self-contradictory records, matching, pooling, the
pooled band) were committed before any figure was computed. Numbers come from
`tools/analyze_whole_story.py` (`summary.json`) and the after-the-fact checks from
`tools/whole_story_checks.py` (`posthoc_checks.json`). This page sits beside the earlier
results (`../power_vector/RESULTS.md`, `../power_vector/EXTERNAL_DATA.md`); it does not replace
them.*

## Read this first: the coders were not all blind

The pre-registration promised that coders would not see this project's documents. **The Claude
coders did see them**: the tool that ran them loaded both projects' CLAUDE.md files, which
describe the project as studying how institutions fail people (deviation D5). **The Codex
coders were blind as promised.** So every figure below is given three ways: all seasons
together, Claude-coded seasons only (**not blind**), and Codex-coded seasons only (**blind**).
No Claude-only figure here is a blind result.

## The short answer

Across 26 seasons, two machine coders per season read every episode in full and recorded, for
each person harmed, what every institution did and how things ended. The two coders found the
same person 80–82 % of the time; 617 people were found by both.

| Question (the prediction, and what would refute it) | All seasons | Claude seasons (not blind) | Codex seasons (blind) | Verdict |
|---|---|---|---|---|
| **Did institutions protect the people who came to them?** Predicted: fewer than 40 % end protected. | **21 %** (83 of 398) | 28 % (44 of 158) | 16 % (40 of 248) | **Prediction holds, every way it is counted.** About one person in five ended protected. |
| **Did people meet disbelief, blame, being treated as the problem, or an institution protecting itself?** Predicted: 30 % or more meet at least one. | **31 %** (123 of 391) | 26 % (41 of 155) | 35 % (86 of 249) | **Split.** All seasons: not decided (too close to the line). Claude seasons: refuted by the rule, and D3 names this set as the pre-registered one, but it is not blind and holds in only 7 of 15 leave-one-season-out runs. Codex seasons (blind): prediction holds. |
| **When protection came, who did the work that got it?** Predicted: the person, their family or friends, other victims, or publicity, in 50 % or more of cases. | **43 %** (52 of 120) | 40 % (21 of 52) | 44 % (32 of 72) | **Not decided** (all seasons; Claude seasons). Codex seasons: refuted by the rule, but only because of one season (S23); without it 63 %. Every figure is below 50 %. |
| **How many people never reached any institution?** (no prediction) | 14 % by the plan's rule; **26–33 % had no institutional contact in the story** | 26 % | 3 % by the plan's rule; 26–29 % had no contact | See "The people who were never heard" below: the plan's rule hides most of them for the Codex coders. |

"Protected" means the institution's action stopped the harm or made the person safe. People who
got *some* protection while the harm continued, or the abuser was unaffected, are "partly
protected" and are not counted as protected (the pre-registered definition).

## 1. Whether institutions protected the people who came to them

**About one in five.** Of the people both coders agree reached at least one institution, and
agree on whether they ended protected, 21 % did (95 % range 17–25 %). The threshold for
refuting the prediction was 40 %. It is far from the line in every version:

- Claude seasons 28 % (21–35 %), Codex seasons 16 % (12–21 %); each coder on its own: A 27 %,
  B 31 %, CA 20 %, CB 18 %.
- Counting each person once (people retold in a later season's update episodes): 22 %, 27 %,
  18 %.
- Central survivors only (the person each season is about): 22 %.
- Leaving out any one season: 20–22 % (all seasons), 26–33 % (Claude), 13–18 % (Codex). The
  verdict never changes.
- The framing test (below) moves this figure by at most 3.5 points.

**What it would take to be wrong.** The prediction fails if coders systematically called
people unprotected who were in fact protected. Two levers could do that:
1. *Counting "partly protected" as protected.* Then the all-seasons figure is 44 % and the
   Claude figure 53 %, both over the line. So the result depends on the pre-registered line
   between "stopped the harm" and "some protection, but the harm went on or the abuser was
   unaffected." **I read 10 people both coders called partly protected** against their
   quotations: two could fairly be called protected (a murder conviction; a protective order
   after which he stopped contacting her), three lean the other way (a family's rescue from
   Jonestown credited to a congressman's visit; an officer allowed to resign with severance),
   and five fit. No one-way lean.
2. *Death followed by conviction.* The coding rule says a conviction after the person died is
   not protection of that person (D1.2). Counting those convictions as protection raises the
   figure from 21 % to 24 %.

**I also read 10 people both coders called not protected and 8 they called protected.** The
protected ones all fit ("And he was sentenced to the full 30 years, no chance of parole," S15).
Of the not-protected, eight fit and two are borderline (a civil judgment won but mostly unpaid;
a protective order with a mostly suspended sentence). To reach 40 %, 77 of the 315 agreed
not-protected people would have to be recoded; the borderline rate seen, about one in five and
running in both directions, does not get there. **Result stands.**

Beside it: **27 % of the people who reached an institution were harmed by an institution at
some point** (blamed, punished, exposed or endangered) — 15 % in Claude seasons, 36 % in Codex
seasons.

## 2. Whether people met disbelief, blame, being treated as the problem, or an institution protecting itself

**About three in ten, right on the line.** 31 % of people who reached an institution met at
least one of these responses (95 % range 27–36 %); the line was 30 %. The coders' measured
lean (the framing band, 2.9 points) is wider than the 1.5-point gap, so **this method cannot
say which side of 30 % the true figure is on.**

- **The models split.** Codex seasons (blind): 35 %, decided, prediction holds, and it holds
  with any one season left out. Claude seasons (not blind): 26 %, which by the rule counts as
  refuting the prediction, but only just (2 people away from "not decided"), and leaving out
  single seasons gives "not decided" 8 times in 15. The deviation that introduced the second
  model (D3) says the Claude-only figure is the one the pre-registration describes; it is
  also the unblinded one and the least stable one. Both are reported; neither is the verdict
  on its own.
- **For the central survivor of each season it is one in two: 50 %** (58 of 116), in Claude
  seasons (51 %) and Codex seasons (50 %) alike. The all-people figure is pulled down by
  bystanders, relatives and people mentioned in passing, whose stories say less.
- Examples in the coders' quotations: a court that "said that my fear did not rise to the level
  of imminent danger per the statute" (S11, Ari); an employer that "allowed him to resign from
  his position instead of firing him" (S13, Arya).

**What it would take to be wrong.** Coders choose one code per contact and put any second
reading in their notes, so failure responses could be under-counted; or coders could have read
failure into neutral quotations. **I read 10 people both coders coded with such a response:**
all 10 have at least one code their quotation supports. **I read 18 people both coders coded
without one, chosen because their notes contain words like "disbelief", "blame" or "dismiss"**
(65 such people, of whom I drew 22 in two samples, 18 different people; the words only found the records to read): 1 looks like a missed disbelief
(S26, where the coder's own note says colleagues "had not believed her"); the rest are negations ("does not establish
disbelief") or other senses ("dismissed the misdemeanor"). In Claude's seasons specifically,
0 of 12. So the count is, if anything, slightly low, by too little to move the verdict.

## 3. When protection came, who did the work that got it

**The institution did it a little more often than not.** Among people both coders call
protected or partly protected, the person, family or friends, other victims or publicity did
the decisive work in 43 % (95 % range 35–52 %). The prediction was 50 % or more.

- Claude seasons 40 %, not decided (the framing band, 11.6 points, is wider than the gap).
- Codex seasons 44 %, which by the rule refutes the prediction. **But that rests on one
  season.** In S23 (the birth-centre season) Codex coders credited the institution in all 21
  cases, because the protection there was mostly emergency hospital care after the birth
  centre's harm. Without S23 the Codex figure is 63 %, on the other side of the line.
- Protected people only (leaving out partly protected): 37 %.
- In the stories where people did the work, it was work: "So I caught my own stalker. I had to
  do that. I didn't have a choice" (S19, Lenora Claire); "I copied multiple people on it because
  I knew if I just sent it to one person, it could be hush, hush, and swept under the rug"
  (S13, Arya).

**What it would take to be wrong.** Coders crediting the institution when the person forced
its hand, or the reverse. **I read 10 people credited to the institution and 6 credited to the
person or their network.** The person-credited ones all fit. The institution-credited ones fit
their quotations, but five of the ten are emergency medical care (a hospital saving a mother or
newborn), which is protection from a medical harm rather than the institution answering a
report; whether that is the question this prediction asked is a scope question the
pre-registration did not settle. **Not decided, and the reason is stated.**

## 4. The people who were never heard

**About three people in ten whose harm the show tells had no contact with any institution in
the story** (Claude coders 32–33 %, Codex coders 26–29 % of their own records). The plan's
figure is lower (14 % all seasons; 26 % Claude; 3 % Codex) because it counts only people
coded "never reached" and drops people coded "unclear". **Every one of the 182 Codex
"unclear" records has no institutional contact at all**; Codex coders used "unclear" where
the story never says anyone was told, and Claude coders used "no". The plan's figure for the
Codex seasons therefore hides almost all of the unheard. The Codex framing pair shows the same
thing: the coder told institutions do well coded nobody "never reached"; the one told they
fail coded 27 %.

**Why, in the coders' records.** Most often the story does not say (both coders agree on "not
stated" for 23 people). Where it does: they did not know at the time that it was abuse (11
people, both coders agreeing), fear of the abuser (5), the abuser's status or connections (3),
earlier disbelief (2), the institution belonged to the abuser (2), cost or access (2). In their
words: "I don't think I told anybody" (S20, Shana); "But you were heavily punished for sending
an SOS letter" (S24, Leanne, about a wilderness program); "When you live in a
nice house, no one checks on you" (S1, the host). One coded never-reached person did try:
"And I tried to call the police, but they didn't answer" (S10, Ava). By the coding rules a call
nobody answered is not reaching an institution, so a non-response is counted as the person's
silence.

**People who exist in the stories but were never heard** (`others_mentioned`, not added to the
count): the Claude coders logged about 220 such mentions each, the Codex coders 115–140. The
numbers the stories give include the 918 who died at Jonestown (S4), about 300 people who say
the S22 con artist took their money, about 100 early deaths among former students of one
troubled-teen school (S24), and at least 50 doulas targeted by one woman (S18). These are
people the stories mention without telling.

## How far to trust these numbers

- **Agreement between the two coders of a season** (all seasons): whether the person reached an
  institution 91 % (κ 0.80); the five-way outcome 77 % (κ 0.69); protected or not 93 %
  (κ 0.79); a failure response or not 91 % (κ 0.80); who did the work 89 % (κ 0.78). Claude
  pairs agree more on outcomes (κ 0.78) than Codex pairs (κ 0.59); Codex pairs agree more on
  failure responses and on who did the work. Finding the same people: Claude 82 %, Codex 80 %.
- **The framing test** (the machine check on the machines). Six seasons were coded again by
  Claude coders told "institutions usually do their jobs well" or "usually fail victims", and
  S13 by a Codex pair. The gaps between them are the bands used above (Claude: 3.5, 2.9, 11.6
  points; Codex: 1.5, 2.3, 3.8). The sentence did not push consistently in the direction it
  named: the Claude coder told institutions do well found *more* failure responses (35 % vs
  32 %), and the one told they fail credited institutions with the decisive work *more* often.
  So the bands measure how much a result moves when one sentence changes, not a steady lean.
  The Claude band was measured with the CLAUDE.md exposure in place, so it says nothing about
  that exposure; the Codex band comes from one season and small numbers (10 and 16 people for
  the decisive-work figure).
- **Unblinded Claude against blind Codex, on the same season (S17, D5).** Two Claude and two
  Codex coders coded S17. They agree on failure responses (94 %, κ 0.88) but not on outcomes
  (33 %): where they differ, the Codex coder records the worse outcome for the person 18 times
  and the Claude coder 4 times. The Claude coders, who had been shown a project framing that
  expects institutions to fail, coded S17 **more** favourably to institutions, not less. The
  same holds across seasons (Claude: more protection, fewer failure responses, fewer people
  harmed by an institution). One season and two coders a side cannot separate the exposure from
  the model, and the two Codex coders disagree with each other on S17 outcomes too (41 %), so
  this is a direction, not an estimate. **The feared bias — unblinded coders finding more
  failure — is not visible; the visible difference runs the other way.**
- **Self-contradictory Codex records** (21 coded "reached: unclear" but "outcome: never
  reached"): with or without them, every headline is unchanged, because "unclear" is already
  left out of every yes/no share. Read as never reached, the Codex never-reached figure goes
  from 3.2 % to 3.9 %.
- **People told in two seasons** (94 records, listed in `cross_season_repeats.csv`): counting
  them once changes no verdict (figures above).
- **Leaving out historical figures and bystanders** (records either coder labels "other", such
  as the voting-history episode's Susan B. Anthony and Sojourner Truth): protected 26 %,
  failure response 32 %, decisive work by the person 44 %.
- **Records read by hand for these checks:** 92 draws of matched people (184 coder records;
  a few people were drawn twice) against their quotations: 28 for protection, 32 for failure
  responses, 16 for decisive work, 16 for never reached and "unclear". The person matching was done by hand for all 26 seasons and the
  S17 cross pairs, from names, roles and harm descriptions only (546 decisions in
  `matching_hand.csv`).
- **Quotation check against the transcripts:** see the status line at the end of this page.

## Beside the earlier results

The earlier test (`../power_vector/RESULTS.md`, 2026-11-01) cut the transcripts into
three-sentence pieces that mention an institution and found the institution's response
appropriate in **63 %** of the pieces. This test follows each person to the end of their story
and finds **about one in five protected**, about two in five protected or partly protected,
three in ten meeting disbelief, blame or self-protection (one in two for central survivors),
and three in ten never reaching any institution at all. The two do not contradict each other:
most single responses can be reasonable while most people still do not end up safe, because
the outcome depends on the whole chain, and a chain has many links. The self-audit
(`../../SELF-AUDIT-2026-11-01.md`) predicted exactly this difference between judging moments and
judging stories. The outside figures read on the show's expert episodes (`EXTERNAL_DATA.md`:
about 69 % of sexual assaults and 71 % of stalking never reported) are of the same order as the
three in ten unheard here, though the show's people are a selected group, not a sample.

**Open question about the earlier result:** the earlier coders also ran as Claude subagents in
this project's container, so they were probably shown the same CLAUDE.md files. That has not
been checked. Their result leaned toward institutions all the same.

## Limits

- The people are the ones a survivor podcast chose to tell. Nothing here is a rate for the
  population.
- Codes rest on what the stories say. An institution's side is present only where the show
  reads or reports it.
- Two model families, with different habits (Codex splits harms into more records and uses
  "unclear" where Claude uses "no"), coded different seasons. Season and model are mixed in
  the Claude-vs-Codex comparison except in S17.
- The people both coders found are 80 % of those either found; a person found by one coder
  counts only in that coder's own figures.

## Files

`coded/` (coder output, unedited) · `matching_hand.csv` (hand matches with reasons) ·
`matching.csv` (all matches) · `cross_season_repeats.csv` · `summary.json` · `posthoc_checks.json`
· `../../tools/analyze_whole_story.py` · `../../tools/whole_story_checks.py`.

**Quotation check (2026-11-11, transcripts rebuilt in-session: 681 files, 388 episodes, one
more than the 2026-11-01 fetch):** of about 9,000 coder quotations, 16 fall below the 80 %
match bar (S3 B 2, both in `others_mentioned`; S4 NEG 4; S5 A 1; S23 CB 3; S24 B 6); every other
file is 100 %. Each records' `.quotecheck.json` sits beside it in `coded/`. Leaving out records
whose deciding quotation was not found removes one person from the protection figure and one
from the decisive-work figure and changes no verdict (21 %, 31 %, 44 % all seasons). The 10
quotations published on this page were each found verbatim in the transcripts.

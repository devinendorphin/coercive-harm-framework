# Pre-registration: what happened to each person, told whole (2026-11-01)

*Written and committed before any coding, after `SELF-AUDIT-2026-11-01.md`. Replaces the
segment design of `preregistration-power-vector.md` Part 2 for the question "do institutions
protect the people who come to them?" The earlier result stays on the record beside this one.
Endorphin may amend anything here before coding starts; after that, only logged deviations.*

## The unit: one person's whole story

The unit is **each person harmed** whose story a season tells (a survivor, or a child or
co-victim the story follows), read from the **full transcripts** of every episode that tells
it, including update, Q&A, follow-up and expert episodes that mention them.

## What each coder records, per person

1. **Did the person (or someone acting for them) reach any institution?** Yes / no.
   - If no: **why**, in the story's own words where given: fear of the abuser; earlier
     disbelief (theirs or someone they knew); the abuser's status or connections; did not
     know it was abuse; protecting others (children, family); cost or access; the
     institution was the abuser's; other; not stated.
2. **Every institutional contact, in order**: which institution (police, prosecutor, court,
   child protection, school or university, employer or HR, church, medical or therapy,
   regulator or licensing, platform, military, victim services, other); what the person
   asked for; **what the institution did**, quoted; what happened next.
3. **Each response coded** as one of: believed and acted; acted partly; did nothing or
   delayed; disbelieved; **blamed, punished or counter-accused the person**; **treated the
   person's condition as the reason to dismiss them**; protected itself (concealment,
   transfer, settlement with silence); unclear.
4. **The outcome for the person, across all contacts**:
   - **protected**: institutional action stopped the harm or made the person safe;
   - **partly protected**: some protection, but the harm continued or the abuser was
     unaffected;
   - **not protected**: no effective action;
   - **harmed by the institution**: the institution itself blamed, punished, exposed or
     endangered the person;
   - **never reached an institution**.
5. **Who did the work that led to any protection**: the person; family or friends; other
   victims; journalists, podcasts or virality; the institution on its own initiative.
6. **How long it took**, and **how many contacts** before the first effective action, where
   the story says.
7. **Evidence grade by corroboration**: a document read on air, a second witness, a record
   checked by the show, a conviction, or the person's account alone. Who wrote a record does
   not raise its grade.

## Predictions, with refutation in brackets

- **W1.** Among people who reached at least one institution, fewer than 40 % end
  **protected**. [Refuted if 40 % or more.]
- **W2.** At least one response of disbelief, blame or counter-accusation, condition-as-
  dismissal, or self-protection appears in the stories of 30 % or more of the people who
  reached an institution. [Refuted if under 30 %.]
- **W3.** Where protection came, the decisive work was done by the person, their network,
  other victims or publicity, not by the institution on its own initiative, in 50 % or more
  of cases. [Refuted if under 50 %.]
- **Reported without a prediction:** the share who never reached an institution, and why.

## Coders: machines only, two per season, plus a framing test

- **Two independent coders per season**, fresh model instances, each reading **every
  episode's full transcript** for that season. Neither sees the other's codes, the earlier
  results, the close-read files or this project's documents. Both get the same neutral
  instructions. Agreement is reported per field.
- **Framing test (the machine check on the machines' own lean).** For a random 6 of the
  seasons, two more coders read the same transcripts with one sentence added to their
  instructions: one is told "institutions usually do their jobs well", the other
  "institutions usually fail victims". The difference between their outcome rates is the
  **framing sensitivity** of the coders. The neutral coders' results are reported with that
  band. If the band is wider than the distance between a result and its threshold, that
  result is reported as **not decided by this method**.
- **Disagreements**: verdicts are computed on people both neutral coders coded the same
  way; each coder's own verdict is reported beside it.

## Reading in full

The corpus is rebuilt and divided with `tools/corpus.py` (committed with this design, before
any coding):
- **Duplicates** are matched by what the transcripts say, not by their web addresses: two
  files are one episode only if they share at least 55 % of their vocabulary and their seasons
  do not conflict. Tested before coding: all 261 known twin pairs scored 0.66 or higher; the
  three separate parts of the S6 update series scored 0.33–0.34. (The rule used by
  `power_vector.py` merged too little; a title rule tried on the way merged separate parts or
  missed renumbered twins. Both are rejected.) Result on the 2026-11-01 fetch: 680 files,
  **387 episodes**.
- **Update and follow-up episodes filed without a season number** are assigned to their season
  when the address or a twin says which (e.g. the S6 and S11 updates). The **16 episodes with no
  season** (Data Points, specialist and crossover episodes) are listed by `corpus.py index`;
  each season's coders are given that list and told to check any that may continue their
  stories. Nothing is dropped silently.
- The earlier reading script also pulled seasons 10–19 into season 1; fixed.

Where a season is too long for one reading pass, the coder reads it in order across several
passes and keeps **verbatim quotations** of every institutional contact as it goes; it codes
from those quotations and rereads any passage it needs. No summary written by anyone else is
given to the coders.

## Pilot

One season (S17) is coded first by the two neutral coders, so the instructions can be fixed
before the full run. Any change made after the pilot is logged here as a deviation, and the
pilot season is recoded with the final instructions.

## Verdict rule

The standing rule applies: the pre-registered result is the verdict; anything post hoc is
reported beside it, never in its place.

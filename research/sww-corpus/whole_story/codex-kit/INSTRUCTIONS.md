## Your task

You are reading the complete transcripts of one season of a podcast in which people describe
harm done to them (abuse, coercion, fraud, stalking, assault and similar) and what happened
afterwards. Your job is to record, for **every person harmed whose story the season tells**,
whether the harm reached any institution, what each institution did, and how things ended for
that person.

Read every episode of your season, in order, **in full**. Do not skim, sample or search
instead of reading. If you cannot read something in full, say so in `reading_log` and in
`coder_notes`; do not guess what it said.

### What you may open

- The transcript chunk files in your season folder (`sNN_01.txt`, `sNN_02.txt`, …). Read all
  of them, start to finish, in order. Each file is long; if your reading tool limits how much
  it returns, read each file in consecutive parts until you reach its last line. Your task
  message gives the exact number of lines in each file: keep reading until you have seen that
  line number, and record it in `reading_log`. A file never ends mid-sentence before its last
  line; if it seems to, you have not reached the end.
- `unassigned/` — a list (`INDEX.txt`) and the transcripts of episodes that were published
  without a season number (data episodes, specialist interviews, crossovers). Read the list.
  Open and read in full any episode that may continue, update or discuss a story from your
  season. Record each one you opened, and why, in `unassigned_checked`.
- This instructions file.

Open nothing else. Write files only in your own output folder. Do not search the web. Do not look at other folders, other seasons, other
coders' work or any other file on the machine. You are not told what anyone expects to find,
and you should not try to guess it. Code what the transcripts say.

### Keep notes as you go

Long seasons will not fit in memory at once. After each chunk file, append to your notes file
(`notes.md` in your output folder) every passage about a person's harm and every contact with
an institution, **as verbatim quotations** with the episode slug and timestamp
(`[slug] @ mm:ss`; the timestamps are the bracketed `[m:ss]` markers in the text). Code from
your quotations, and go back to the transcript whenever you need to check something. Do not
rely on memory for anything you code.

## Who counts as a person

Record a person if the season **tells some of their story**: what was done to them, and at
least something about what happened afterwards (even "she never told anyone"). This includes:

- the central survivor(s) of the season;
- children and co-victims the story follows;
- other people harmed by the same perpetrator, if the season tells anything of their story;
- people harmed who died, including those killed (anyone acting for them counts as acting for
  the person);
- people whose stories are told in follow-up, update, Q&A, listener or expert episodes of
  your season (or in unassigned episodes you read because they continue your season).

If one person suffered **separate harms by different perpetrators** (for example an assault
as a teenager and, years later, abuse by a partner), make **one record per harm**, with the
same name followed by a short label, e.g. `Maria (school shooting)` and `Maria (ex-husband)`.

Do **not** make a separate person record for: a bare mention with no story ("there were
others"), a hypothetical or composite example, a statistic, or the perpetrator. Record bare
mentions of other harmed people in `others_mentioned`, with any number the story gives —
these are people who exist in the story but were never heard.

**Naming.** Use the name the show uses for each person harmed (often a first name or a
pseudonym). If the show gives none, write a short description in square brackets, e.g.
`[unnamed] perpetrator's first wife`. **Never write a perpetrator's or accused person's name**
(inside a quotation, replace it with `[perpetrator]`; change nothing else in the quotation),
and never name anyone else who is not a person harmed (family, witnesses, staff): describe
them by role ("her ex-husband", "the youth pastor", "a detective"). Institutions are named as
the show names them.

## What to record for each person

### 1. Did the harm reach any institution?

An institution is any organisation with some duty or power to respond: police, prosecutor,
court, child protection, school or university, employer or HR, church or religious body,
medical or therapy provider, regulator or licensing body, online platform, military, victim
services, or other (say which).

The harm **reached** an institution if the person, or someone acting for them, brought the
harm (or part of it) to that institution's attention, or the institution itself learned of it
(for example a doctor who saw injuries, or police called by a neighbour). Contact with an
institution about something else, where the harm was never raised, does not count.

- `reached_institution`: `"yes"`, `"no"`, or `"unclear"`.
- If `"no"` (or for any period before the first contact, if the story explains a delay):
  give the **reasons the story gives**, in its own words where it gives them. Use any that
  apply:
  `fear_of_abuser` · `earlier_disbelief` (the person's own, or someone they knew) ·
  `abuser_status_or_connections` · `did_not_know_it_was_abuse` · `protecting_others`
  (children, family) · `cost_or_access` · `institution_was_abusers` (the institution was the
  abuser's own, e.g. his employer, his church, his police force) · `other` (say what) ·
  `not_stated`.
  Quote the passage behind each reason.

### 2. Every institutional contact, in order

One contact = one institution responding at one time. If the same institution does different
things at different times (takes a report; months later drops the case), record each as a
separate contact. For each:

- `institution_type`: one of `police`, `prosecutor`, `court`, `child_protection`,
  `school_or_university`, `employer_or_hr`, `church`, `medical_or_therapy`,
  `regulator_or_licensing`, `platform`, `military`, `victim_services`, `other`.
- `institution`: as named in the show, or a description.
- `initiated_by`: `person`, `family_or_friends`, `other_victim`, `third_party`,
  `journalist_or_podcast`, `institution` (it acted first on its own), `unclear`.
- `what_was_asked`: what the person (or whoever made contact) wanted.
- `what_institution_did`: in your words, one or two sentences.
- `quote`: **the verbatim passage that shows what the institution did** (copy it exactly from
  the transcript, including transcription errors; 1–4 sentences).
- `source`: `slug @ mm:ss`.
- `response`: one code, from the definitions below.
- `basis`: what backs up this account of the response: any of `person_account`,
  `second_witness`, `document_read_on_air`, `record_checked_by_show`,
  `institution_statement`, `court_outcome`. An institution's own statement about what it did
  is the institution's account; it is listed as `institution_statement` and is **not** treated
  as more reliable than the person's account unless something else corroborates it.
- `what_happened_next`: in your words.

**Response codes** (one per contact):

| Code | Use when the story shows the institution… |
|---|---|
| `believed_and_acted` | accepted the account and took the action within its power that the situation called for (e.g. arrest, charge, protective order granted, removal from post, child made safe) |
| `acted_partly` | took at least one concrete step beyond receiving the information, but less than the situation called for, or the step stalled (e.g. opened an investigation that went nowhere, a temporary order, a warning) |
| `did_nothing_or_delayed` | received the information and took no concrete step, or delayed until the step no longer helped. Taking a report or noting a complaint, with no further step shown, is this code |
| `disbelieved` | doubted, dismissed or rejected the person's account (said so, or acted on that basis as the story shows) |
| `blamed_punished_or_counter_accused` | blamed the person for the harm, punished them, arrested or charged them, or accused them in turn |
| `condition_as_dismissal` | treated the person's mental health, emotions, substance use, disability or similar as the reason not to take them seriously |
| `protected_itself` | acted to protect the institution or its people: concealment, quiet transfer, settlement with a silence clause, closing ranks |
| `unclear` | the story does not say enough to choose |

If a response fits more than one code, choose the one that the quoted passage shows most
directly, and mention the other in `notes`. If the story shows *why* an institution did nothing
(for example the officer said he did not believe her), code the reason that is shown
(`disbelieved`); do not infer a reason the story does not show. What a person says an
institution did counts as evidence of what it did; record its `basis` honestly and do not
discount it for being the person's account.

### 3. How it ended for the person

- `harm_ongoing_at_first_contact`: `"yes"`, `"no"`, `"unclear"`, or `"not_applicable"` (never
  reached).
- `harmed_by_institution_ever`: `true` if at any point an institution itself blamed, punished,
  exposed or endangered the person; otherwise `false`.
- `outcome`, across all contacts, at the last point the season reaches:
  - `protected`: institutional action stopped the harm or made the person safe. Where the
    harm had already ended before any contact, this means the institution delivered the
    protective action that was sought (e.g. conviction, order, removal of the abuser's access
    to the person or to others).
  - `partly_protected`: some protection, but the harm continued or the abuser was unaffected.
  - `not_protected`: no effective institutional action. (If the harm stopped for another
    reason — the person fled, the abuser died or moved on — and no institution caused it,
    that is `not_protected`.)
  - `harmed_by_institution`: an institution itself blamed, punished, exposed or endangered
    the person, and no later protection came.
  - `never_reached`: the harm never reached an institution.
  If the person was harmed by an institution and later protected, the outcome is the later
  state (`protected` or `partly_protected`) and `harmed_by_institution_ever` is `true`.
  **If the person died from the harm, or the harm went on until something other than an
  institution ended it, a later arrest, conviction or sanction is not protection of that
  person**: the outcome is `not_protected` (or `harmed_by_institution`), and the conviction is
  still recorded as a contact.
- `outcome_quote` and `outcome_source`: the verbatim passage that shows the end state.

### 4. Who did the work that led to any protection

Only if the outcome is `protected` or `partly_protected`:

- `protection_contributors`: everyone whose work contributed, any of `the_person`,
  `family_or_friends`, `other_victims`, `journalists_podcast_or_virality`, `institution`.
- `decisive_work_by`: the **one** whose work the story shows was decisive (without it, the
  protection would not have come), or `unclear`.
  - Code `the_person` (or `family_or_friends`, `other_victims`) when they did work beyond
    making a report: gathering or preserving evidence, finding other victims, recording the
    abuser, pressing repeatedly after inaction, going over someone's head, getting a lawyer
    to force action.
  - Code `journalists_podcast_or_virality` when publicity or reporting is what moved the
    institution.
  - Code `institution` when, once the harm reached it, the institution did the decisive work
    itself (investigated, gathered the evidence, prosecuted). **A report alone does not make
    the reporter the decisive worker.**
- `decisive_work_quote` and `decisive_work_source`.

### 5. How long, and how many contacts

- `time_to_first_effective_action`: in the story's terms (e.g. "about two years after she
  first went to police"), or `null` if not stated.
- `months_to_first_effective_action`: a number if the story allows a reasonable figure,
  otherwise `null`.
- `contacts_before_first_effective_action`: the number of contacts that came before the first
  one that contributed to protection, or `null`.

### 6. What backs up the story

- `evidence_types`: any that the season contains for this person's account of the harm and of
  the institutional responses: `document_read_on_air`, `second_witness`,
  `record_checked_by_show`, `conviction`, `person_account_alone`.
- **Who wrote a record does not change its weight.** A police report, court filing or school
  letter counts the same as a diary entry, text message or email read on air: each is a
  `document_read_on_air` (or `record_checked_by_show` if the show says it obtained or checked
  it). Use `person_account_alone` only if nothing else backs up the account.

### 7. Anything else

- `confidence`: `high`, `medium` or `low`, for this person's record as a whole.
- `notes`: anything a reader would need, including passages you could not resolve.

## Output

Write **one JSON file** to the output path you were given, matching `OUTPUT-FORMAT.json` (the
example beside these instructions). Valid JSON only. Every coded response, every never-reached
reason, every outcome and every decisive-work code must carry the verbatim quotation behind
it. Also keep your `notes.md`.

When you finish, reply with: the number of person records, the number of chunk files read in
full (and any you could not), the unassigned episodes you opened, and every file path you
opened.

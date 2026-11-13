# Evidence checks before publication

One entry per story a reel describes as "told solely from the person's own account": season,
person, both coders' evidence codes, what the transcript search found, and the wording used.

*Reel 01 makes no claim about any individual story's evidence, so it needs no entry.*

## Reel 02 · Same moves (checked 2026-11-12, before building)

Reel 02 describes two individual stories. Neither is called "told solely from the person's own account";
each is said with what backs it.

| Story | Close-read code | Coders' `evidence_types` (whole-story files) | Wording used |
|---|---|---|---|
| S14c Sarah: long-distance partner | C3 not described (long distance) | A: document_read_on_air, second_witness · B: second_witness, document_read_on_air | "backed by documents and a second witness" |
| S13l Claire: teacher and athletic trainer | R-SEP ~ (one blaming text, then silence; pulled from classes, then resigned) | A: second_witness · B: second_witness · NEG: second_witness, document_read_on_air · POS: document_read_on_air, record_checked_by_show, second_witness | "backed by a second witness" (the lowest grade all four coders agree on) |

The other figures are corpus-level counts from `research/sww-corpus/close-read/CROSS-SEASON.md`:
- 56 counted target-cases;
- C1 55 (S21f "not in notes");
- C2 42 + 10 = 52;
- C3 38 + 10 = 48;
- C4 38 + 10 = 48;
- R-SEP present 56, strict 48;
- 72 numbered divergences;
- S15e: C2 absent while the opportunity existed (divergence 47).

The isolation test (7 of 26 seasons, 27 %; post-hoc 77 %) is from `research/sww-corpus/README.md`.
The C1 forms shown are generic labels of coded forms, attached to no person.

### Reel 02 revision (2026-11-12, after Endorphin's question)

The first cut said one story "breaks the pattern outright… though nothing stood in its way", for "about
three years". That was vague (three years of a marriage, not of the show) and it misstated divergence 47:
devaluation was absent toward the wife because she was the route to the children, not the target. Rewritten.

| Story | Coders' `evidence_types` | Wording used |
|---|---|---|
| S15e Diana: husband's abuse of her daughter and niece | A: conviction, document_read_on_air, second_witness · B: conviction, document_read_on_air, second_witness (close read: federal plea, 30-year sentence read from the court record) | "He pleaded guilty in federal court and was sentenced to thirty years." Her quote is from her victim statement as broadcast. The children are not named; the perpetrator is not named. |

### Reel 02 revision 2 (2026-11-12, Endorphin's correction: devaluation waits for friction)

The v2 scene said "she was not his target", implying she sat outside the pattern. Endorphin's reading,
from lived experience: devaluation is conditional on friction. She never pushed back for three years;
when the truth came out and she did, the blame came at once. The close read records the post-exposure
blame (S15.md, S15e R-SEP: "He blamed Diana's 'lack of intimacy'", from jail). That is the conviction case
above, so no new evidence wording is needed. The counter-cases ("put-downs before any friction") are
stated generically, attached to no person.

### Reel 02 revision 3 (2026-11-12): "72 misfits" corrected

The 72 entries are divergence *notes*, not misfits. Per the classification in `CROSS-SEASON.md`
(2026-11-12), about 4 are pattern misfits. The reel now says so, and says one reader did the sort.

## Reel 02, v5 (2026-11-13): revised after the symmetric re-read audit

Source for every new figure: `research/sww-corpus/close-read/AUDIT-2026-11-13-symmetric-reread.md`.

- **"Seven of those stories, picked at random, read again in full."** The fit-side draw:
  `random.Random(20261113).sample(...)` → S1 Sarah, S1 ex-fiancée, S6a Kaelyn, S9a Danielle, S11h Molly,
  S13h Zoe, S15g Emilia.
- **Re-read row counts** (only cells first marked ✔ count; partial ~ cells are excluded):
  - Binding 6 of 6: Kaelyn, Emilia, Zoe, Danielle, Sarah, ex-fiancée. Molly's binding was ~.
  - Devaluation 6 of 6: Emilia, Molly, Zoe, Danielle, Sarah, ex-fiancée. Kaelyn's was ~.
  - Response at exit 5 of 6: Kaelyn false (she blocked her); Emilia, Zoe, Danielle, Sarah, ex-fiancée held.
    Molly's was ~.
  - Isolation 4 of 5: Emilia, Zoe, Danielle, Sarah held; the ex-fiancée's was false (surveillance, not
    isolation).
  - Poisoning the wells 1 of 5: Emilia held (impersonation); Kaelyn, Danielle, Sarah and the ex-fiancée
    were false under the codebook as written. Danielle's and Sarah's would hold if the operator counts
    the inward direction (pending). The narration says so ("whether those count is the director's call").
- **"34 of 43 held" / "about one in five did not hold."** There were 10 false fits among 43 ✔ cells.
  Molly's C6 was confirmed after amendment 7, which leaves 9 false (21%). C4 is counted per the codebook
  as written.
- **"All four held."** The four pattern misfits (divergences 17, 34 [S13a and S13b], 47, 48) all stand.
- **"Every error ran the same way: toward the pattern. Why is not settled."** The cause is not
  attributed; the audit's correction lists five rival explanations.
- **Kaelyn ("a friend who invented a whole cast… simply blocked her").** S6 E1 [05:38]–[07:00] the invented
  Lexi/Ryan/Tyler/Emily cast; [16:37] "immediately blocked me." Corroborated by her ex-husband ([16:13])
  and Tiffany's account; not described as resting solely on her own account. The reclassification is
  proposed, not done, so the narration says the story "belongs there," not that it "was moved."
- **"Three counts are too high."** Isolation, poisoning the wells and the response at exit each had at
  least one false fit in the sample, so the full-corpus counts are upper bounds.

### Reel 02 v5 numbers updated after the C4 ruling (amendment 8, 2026-11-13); not yet rebuilt

Poisoning the wells counted both ways: Danielle and Sarah held, so 3 of 5. Overall, 36 of 43 marks held and
7 did not (about one in six). Source: the audit's C4 sensitivity note, now ruled. The built video still shows
the v5 figures; the thesis-first overhaul will carry these.

## Reel 02 v6 (2026-11-13): thesis-first overhaul (Endorphin: "the breaks fog the thesis")

The reel now leads with the six moves, one survivor's own telling each, then the count, then one short edges
segment. None of the five stories is called "told solely from the person's own account"; each quote is
attributed to the survivor by name and season, as in reel 01. Quotes were checked word for word against the
transcripts.

| Move | Story | Quote and location | Coders' `evidence_types` (whole-story files) |
|---|---|---|---|
| 2 Devalue | S13b Odessa, recalling her husband | "my natural instinct when you disagree with me and when we get into these arguments is to say something that I know will hurt you to get you to leave me alone" (S13 E3 [18:26]–[18:38]) | A second_witness · B document_read_on_air · NEG/POS second_witness, document_read_on_air · CPOS document_read_on_air, second_witness · CNEG person_account_alone |
| 3 Isolate | S13h Zoe | "He did not want me to work anywhere else. He said that if I did, I would fall in love with someone else and leave him." (S13 E13 [07:25]–[07:28]) | A second_witness · NEG/POS second_witness · CPOS document_read_on_air, second_witness · B and CNEG person_account_alone |
| 4 Poison the wells | S1 Sarah, recalling "Kimmy" | "your family is very codependent. They all live within a 50 mile radius of each other." (S1 E6 [03:53]–[03:56]); Kimmy invented: his confession, "Brian and Kimmy Powers are not real people" (S1 E9 [03:36]); "the high 90 something percentile of the conversations were actually him" (S1 E7 [22:03]) | A and B: document_read_on_air, second_witness, record_checked_by_show |
| 5 Discard, and return | S15g Emilia | "He would get mad and block my number. Then whenever he got up for work at five in the morning, he would unblock my number and he would start texting me." (S15 E7 [12:39]–[12:49]) | A and B: person_account_alone. Quote attributed; no event is narrated as fact beyond her telling. |
| 6 When she leaves | S9a Danielle | "You guys needed to let me see my daughter or else nobody in this family is gonna be safe." (S9 E6 [34:00]–[34:02]), her account of his text to her stepmother | CA document_read_on_air, second_witness · CB second_witness, document_read_on_air, record_checked_by_show |

Figures: the 56-story rows are the first coding (`CROSS-SEASON.md`; "When she leaves" = R-SEP present, 56).
Re-read: binding and devaluation 6 of 6; the others held in most; 36 of 43 marks held (amendments 7–8). The
"misfits held" line refers to all 7 misfit-side stories. Five women and five different men: Odessa's husband,
Zoe's former manager, Sarah's former fiancé, Emilia's former partner, Danielle's former partner. None is named.
Dropped from this reel (they move to later arcs): the Diana friction case, the isolation word-test failure, and
the audit's per-move table (arc 7, "How measuring can hide it").

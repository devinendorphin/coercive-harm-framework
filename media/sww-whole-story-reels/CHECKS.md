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

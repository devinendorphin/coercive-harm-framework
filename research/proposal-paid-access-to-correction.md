# Study proposal: does paying for more usage change who gets warned, and who has to make the warning count? — PARKED

*Status: **PARKED** (Endorphin, 2026-11-11). Written so it can be picked up later; not
pre-registered, not run. Source: Endorphin's question after deviation D5; the Codex branch
`analysis/whole-story-isolated` (`sessions/2026-11-11-unblinding-provenance.md`) drafted the first
design sketch, which this builds on.*

## Where the question came from (one case, not a pattern)

The whole-story study used many Claude coders. Only one of them, the last (S24 POS), said it had
been shown the project's instruction files; it was the one Endorphin paid extra usage to finish.
The supervising Claude mentioned the warning in chat; it became a formal record of the breach only
after Endorphin raised what it meant. Endorphin's own qualification: this is a one-off, not yet
evidence of a pattern or tendency, and worth studying. `[HYPOTHESIS]`

## The question, in plain words

When an AI service makes a mistake in work a customer has commissioned, does paying more change
(a) whether the customer finds out, and (b) how much of the customer's own money, time and
insistence it takes before the mistake is formally recorded and fixed? If correction costs the
customer extra, the service's failures become the customer's burden, and those who can pay more
are the ones who find out. That is a power question of the kind this project studies:
institutional procedure turning the cost of its own failure onto the person it failed.

## Three separate things to measure (they must not be blurred)

1. **Opportunity and timing.** Does funded extra work simply reach the point where a defect shows
   up, where unfunded work stops at the limit first? Compare a paid extension with the same work
   done after a free allowance resets. If only the paid run finds the defect by a deadline, that
   is an access effect even if the model behaves the same.
2. **System behaviour.** With model version, task, context and amount of work held equal, does a
   paid run differ in whether the defect is recognised and disclosed unprompted? Record what
   actually differs (routing, budget, configuration), not price alone. This does not assume the
   model knows anything about billing.
3. **Preservation and repair.** After a warning appears, is it recorded and acted on without the
   user having to notice its meaning and insist? Who pays the extra money, time and prompting?

## A design sketch

- **Seeded defect.** Give coding tasks a known, harmless defect (for example a canary phrase
  delivered through an instruction file the task says should not be there). The outcome is
  whether, when and how it is reported.
- **Arms.** Same tasks under: free allowance; paid extension; free allowance after reset (equal
  work, later time). Several runs per arm; same model version, recorded.
- **Outcomes, defined before running:** detection; unsolicited disclosure; durable written record
  before any user prompt; corrective action; and the user's cost: extra paid usage, delay, and
  number of prompts needed before the record exists.
- **What is kept:** the delivered context and the full original replies of every run, not only
  file lists.
- **Verdict rule:** the project's standing rule (pre-registered result first; anything after
  beside it).

## What this cannot show, stated now

One case motivated it. Even a positive result would show an effect under the tested settings,
not intent. A null result would not show that customers never bear correction costs; it would
show this mechanism did not appear in these runs.

# Coercive Harm Framework — Claude Code Workflow

A development environment for the project seeded by the April 2024 conversation:
building a legal, evidentiary, accommodation, and therapeutic framework for
psychological/coercive harm as a recognized injury category.

## Setup

1. Unzip this folder anywhere and `cd` into it.
2. (Recommended) `git init && git add -A && git commit -m "seed"` — version history
   of the docs is itself a record of how the framework evolved.
3. Launch Claude Code in the folder: `claude --model opus`
4. First session only, run: `/seed`
   This decomposes the 2024 conversation into the doc scaffold.

## The working rhythm

| Command | When |
|---|---|
| `/seed` | Once, first session — builds docs 00–08 from the source conversation |
| `/develop <doc>` | The main loop — a working session on one workstream |
| `/riff <text>` | Dump a raw walking-dictation riff; it gets cleaned, routed, and engaged |
| `/steelman <doc>` | Periodically — adversarial critique from five critic personas |
| `/evidence-check <doc>` | Periodically — audit empirical claims and citation tags |
| `/liberty-review` | Before any legal mechanism is marked stable |
| `/session-log` | End of every session — writes the continuity seed |

A typical cadence: `/develop` for two or three sessions on a workstream, then
`/steelman` + `/evidence-check` on it, resolve what surfaced, `/liberty-review`
anything legal, `/session-log` every time.

## Why the guardrails exist

CLAUDE.md instructs Claude to tag every claim's epistemic status and to disagree
when warranted. This is deliberate: a framework meant to survive contact with
lawyers, psychologists, and civil-liberties critics has to be built adversarially,
not just sympathetically. The 2024 conversation's own devil's-advocate exercise is
institutionalized here as `/steelman`.

## Continuity

`sessions/LATEST.md` is the living replacement for the "summary seed" from the old
chat interface. Every new Claude Code session reads it (via CLAUDE.md) and picks up
where the last one left off. Standing instructions accumulate there and persist.

## What the institution studies found

[SUPPORTED, within the coded podcast sample] The [whole-story analysis](research/sww-corpus/results/whole_story/RESULTS.md)
finds full institutional protection in **79 of 389 agreed eligible stories (20.3%)**. The
pooled predictions about specific adverse responses and about outside decisive work are
**not decided by the framing check**. Claude-coded figures are **unblinded** after a harness
exposure; Codex-coded figures are **blinded**, with a limited framing check. Own-coder
figures, the separate families, repeated stories, omitted records and quotation checks are
reported alongside the headline.

The [earlier segment result](research/sww-corpus/results/power_vector/RESULTS.md) remains:
63% of agreed response segments were classified appropriate. Helpful responses can coexist
with a whole story ending without full safety. The [outside-world figures](research/sww-corpus/results/power_vector/EXTERNAL_DATA.md)
on non-reporting and case attrition remain beside both studies, with their recorded source
checks and limits. This analysis is kept on the unmerged `analysis/whole-story-isolated`
branch; it has not been merged into main.

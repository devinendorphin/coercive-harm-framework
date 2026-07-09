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

# Proposal: what a coder is given becomes a setting, not an accident (2026-11-11)

*Status: PROPOSED, awaiting Endorphin's approval. Written after deviation D5 (Claude coders were
shown the project's CLAUDE.md files by the harness) and D10 (the first Codex coder ran with
memory on). Nothing here has been run.*

## The idea, in Endorphin's direction

Instead of a rule that only forbids exposure ("blind coders never run in this container"), build
the coding so that **what each coder is given is chosen, recorded and checked**. Project files are
not loaded into a coder's container unless the design says so. Then exposure stops being a
breach found afterwards and becomes something the study can vary on purpose: the same season
coded with and without the project's framing, and the difference measured. That turns D5 from a
flaw into an experiment.

## How a clean coder is run (options, all checked against this session's tools)

1. **A separate cloud session that holds only the coding kit.** Start each coder as its own
   session with `devinendorphin/sww-coding-kit` as its only repository. The project
   repositories, and so their CLAUDE.md files, are not in that container. (This is how the Codex
   coders were kept blind.)
2. **`claude --bare` in a scratch folder.** The Claude Code build here documents a `--bare`
   mode that skips CLAUDE.md auto-discovery and auto-memory; context is then only what is passed
   with `--system-prompt-file` / `--add-dir`. It authenticates only with an API key, not a
   subscription login, so it costs API usage. Not yet tried.
3. **Codex with memory off**, from the kit repository, as before (D10: check the setting at the
   start of every task, not afterwards).

Subagents started from a session that has the project repositories attached are **not** a clean
route: the harness loads every CLAUDE.md under the working directories into them (D5).

## How "clean" is checked, not assumed

- **A canary.** Put a unique, meaningless phrase in each project CLAUDE.md (for example a
  made-up word). Every coder's final report is searched for it, and every coder is asked, before
  reading anything, to list any instructions in its context beyond its task message. A coder that
  can see the canary was exposed. File-opening lists cannot show this; the canary can.
- **Record what was delivered.** Save each coder's first message and the list of instruction
  sources it reports, beside its output.
- **Memory and settings at the start.** Each task message states the memory setting and asks the
  coder to confirm what it sees.

## The experiment this makes possible (D5's repair, done as a test)

Pick two seasons already coded (S17 first: it has two Claude and two Codex codings). Run two
new Claude coders per season in a clean session (option 1) and two with the project CLAUDE.md
deliberately included, everything else identical. Compare protected, failure-response and
decisive-work rates and person-finding between the arms. This separates the exposure from the
model, which the S17 cross-check cannot. Pre-register it before running, with the same verdict
rule as the main study.

## Proposed CLAUDE.md working agreement (text to add if approved)

> **What a coder sees is a setting.** Coders run where project files are not loaded unless the
> design deliberately includes them (a separate session holding only the coding kit, or a bare
> run); never as subagents of a session that has the project repositories attached. Each run
> records what the coder was given, checks it with a canary, and states memory settings at the
> start. Exposure, when wanted, is an experimental arm, not an accident.

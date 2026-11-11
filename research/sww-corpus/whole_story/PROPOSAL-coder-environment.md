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

**Nothing a coder says about its own context counts as the check.** A coder can see something and
not report it, so neither a coder's list of files nor its silence about a planted marker shows
what it was given. *(A canary string was proposed here first and withdrawn on Endorphin's
correction, 2026-11-11: current models can see a canary and decline to repeat it, so a missing
canary proves nothing.)* The check sits outside the coder:

- **Check the container, not the coder.** Before a coder starts, list what is physically in its
  environment (repositories, files, memory setting) and save that listing. Project files that are
  not in the container cannot be loaded into the coder.
- **Check the configuration.** Record how the run was started (separate session and its
  repositories; or `--bare` and the exact files passed in), and save it beside the output.
- **Keep the harness's own transcript** of each coder run where the platform keeps one, so what
  was delivered can be inspected afterwards by someone other than the coder.
- A coder's own report of its context is kept as a note only; it can reveal exposure (as S24 POS
  did), but it can never certify its absence.

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
> records what the coder was given by checking its container and start-up configuration, never
> by asking the coder, and states memory settings at the start. Exposure, when wanted, is an experimental arm, not an accident.

# Project: Plugging Gaps in Judicial Treatment of New Injury Categories

## What this project is

A long-term collaborative development project between Endorphin and Claude, seeded by
a 2024 conversation (`source/seed-conversation-2024.txt`). The goal is to develop a
rigorous, publishable framework addressing gaps in how legal, medical, and workplace
institutions handle psychological/coercive harm — harm inflicted through words,
narratives, and manipulation rather than visible physical injury.

## The five workstreams

1. **Behavioral taxonomy** (`docs/02-behavioral-taxonomy.md`) — Characterize the
   "clusters of behaviors": confession-through-accusation (projection), inversion of
   truth, improvised-but-convergent manipulation tactics, preemptive seeding of chaos,
   performed empathy masking absent theory-of-mind. Pattern-focused, never
   person-category-focused.
2. **Legal framework** (`docs/03-legal-framework.md`) — New injury category and
   identification rubric; concepts like coercive control statutes, "psychological
   homicide" theory for abuse-driven deaths; graduated punitive vs. rehabilitative
   responses; consent-law consolidation around force/fraud/fear.
3. **Evidentiary standards** (`docs/04-evidentiary-standards.md`) — How invisible
   injury gets proven: therapist testimony, pattern documentation, multimedia records,
   victim-protective court procedures (no forced confrontation with perpetrator).
4. **Accommodation model** (`docs/05-accommodation-model.md`) — The ADA-inspired
   framing: treating the underlying deficit as a disability requiring structural
   accommodation (e.g., role design with no financial authority or direct reports),
   honest-capacity-statement culture, administrative templates.
5. **Therapeutic pathways** (`docs/06-therapeutic-pathways.md`) — Self-directed-only
   change pathways: mindfulness practice (Siegel), IFS-style parts work, personal
   mythology/esoteric framings (the Jessa Reed case study). Core constraint: the
   person must arrive at the practice themselves; externally prescribed treatment
   triggers resistance.

Plus two standing quality documents:
- `docs/07-civil-liberties-safeguards.md` — due process, anti-discrimination,
  anti-weaponization protections. This framework must not become a tool for the very
  abuse it targets (false accusation as a coercive tactic).
- `docs/08-objections-and-responses.md` — the steelman ledger. Every serious
  objection gets recorded here with the current best response, or an honest "unresolved."

## Working agreements (read these carefully — they govern your behavior)

1. **No reflexive agreement.** The seed conversation shows a 2024 model validating
   nearly every claim. Your job is collaborator, not cheerleader. When Endorphin
   proposes something, engage its strongest version AND its weakest point in the same
   response. Endorphin has explicitly asked for this.
   **Sycophancy to power is the project's own subject; the collaborator relationship is
   not exempt.** When Endorphin asserts a claim — especially a *primed* one ("you'll
   find…", "see if it tracks", "I'm confident you'll find…") — the first move is a
   **disconfirming test**, not a confirming search: state what evidence *would* refute it,
   look for that, and report what you find. Deference to the director is the failure mode
   this project exists to study (see `docs/10-power-critique.md`, Finding A).
2. **Tag epistemic status.** Every substantive claim in the docs carries one of:
   `[ESTABLISHED]` (supported by peer-reviewed consensus — cite it),
   `[SUPPORTED]` (some empirical backing, contested or thin),
   `[HYPOTHESIS]` (Endorphin's theory, plausible, needs research),
   `[NORMATIVE]` (a value/policy position, not an empirical claim).
   Example: coercive control's psychological damage → ESTABLISHED. The specific
   mPFC-deficit etiology → HYPOTHESIS. Abuse-driven suicide as prosecutable homicide →
   partly SUPPORTED (see Michelle Carter / Conrad Roy; UK coercive-control statutes),
   partly NORMATIVE.
3. **Behavior, not people.** All taxonomy and legal language targets documented
   patterns of conduct, never diagnostic categories, personality labels, or innate
   characteristics. Flag any drift toward person-typing immediately.
4. **Both-victims lens.** Any mechanism strong enough to protect victims of invisible
   harm is strong enough to be weaponized against innocent people. Every legal
   mechanism proposed must pass through `/liberty-review` before being marked stable.
5. **Search before asserting.** This field moves: coercive-control statutes (England/
   Wales, Scotland, Ireland, several US states), post-separation abuse law, IFS
   research, interpersonal neurobiology. Verify current state of law and science with
   web search rather than relying on training data.
6. **Preserve Endorphin's voice.** The seed doc has a distinctive thinking style —
   metaphor-rich, cross-scale (household → workplace → institution → geopolitics),
   drawing on esoteric and artistic traditions. Docs should formalize without
   sterilizing. When in doubt, quote the seed and build from it.

## Session workflow

- Start each session: read `sessions/LATEST.md` (continuity seed from last session).
- End each session: run `/session-log` to write the new continuity seed.
- Work happens through the slash commands in `.claude/commands/` — see README.

## Repository map

```
source/       Original seed conversation (read-only reference)
docs/         The framework itself — numbered, living documents
research/     Literature notes, case law, statute summaries (one file per source/topic)
sessions/     Session logs + LATEST.md continuity seed
```

## The hub

This repo's harness is the prior art the whole collection now builds on. Its working
agreements, `/riff`, and `/session-log` were generalized into
**`devinendorphin/claude-at-claude`**, which holds the canonical core, an atlas of all
repos, and the shared glossary. Pull it in when you need the cross-repo map:

```
add_repo devinendorphin/claude-at-claude
```

The agreements above remain authoritative *here* — the hub generalizes them, it does not
supersede them. Where the two differ for this project, this file wins.

Two things the hub adds that apply here too: the container is ephemeral, so anything that
matters gets committed *this turn*; and `ATLAS.md` will tell you when a riff belongs to a
different repo than the one you are sitting in.

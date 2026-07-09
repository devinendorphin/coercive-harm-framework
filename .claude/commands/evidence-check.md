---
description: Audit a doc's empirical claims — verify tags, hunt citations, flag drift
---

Target: $ARGUMENTS (a doc, or "all").

1. Extract every empirical claim in the target and its current epistemic-status tag
   ([ESTABLISHED] / [SUPPORTED] / [HYPOTHESIS] / [NORMATIVE] per CLAUDE.md).

2. For each claim tagged ESTABLISHED or SUPPORTED: verify a citation exists in
   `research/`. If not, web-search for current peer-reviewed support. If support is
   found, add the citation to research/ and the doc. If support is weaker than the
   tag, downgrade the tag and say so explicitly.

3. For each HYPOTHESIS: check whether new research would upgrade it. Note especially:
   - mPFC / theory-of-mind / moral-cognition literature (the seed's central
     neurological hypothesis)
   - neurobiology of sustained emotional trauma as physical injury
   - mindfulness-driven structural brain change timelines
   - IFS outcome studies
   - coercive-control statute outcomes since enactment (does the law work in practice?)

4. Flag **tag drift**: any place where a HYPOTHESIS is being written about in the
   confident register of established fact. Quote the offending sentence and propose
   corrected language. This is the failure mode most likely to discredit the whole
   framework with expert readers, so be strict.

5. Output a scorecard: claims checked, tags confirmed, upgraded, downgraded,
   uncited-and-unfindable (candidates for removal or explicit hedging).

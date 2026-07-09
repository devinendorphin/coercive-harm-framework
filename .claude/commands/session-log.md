---
description: End-of-session — write the log and regenerate the continuity seed
---

This replaces the "summary seed" ritual from the 2024 conversation, but as a
persistent file instead of a pasted attachment.

1. Write `sessions/YYYY-MM-DD-<short-slug>.md` containing:
   - What was worked on and what changed (docs touched, decisions made)
   - Endorphin's key riffs/insights this session, in language close to their own —
     these are primary source material, not just meeting minutes
   - Disagreements or tensions left open between Endorphin and Claude (record both
     positions honestly)
   - New objections raised → confirm they landed in docs/08

2. Overwrite `sessions/LATEST.md` with:
   - Project state in ~10 lines (per workstream: stable / active / stub)
   - Top 3 priorities for next session, with reasoning
   - Any standing instruction Endorphin gave that future sessions must remember
     (append to a "Standing notes" section that persists across regenerations —
     never delete existing standing notes without explicit instruction)

3. If any CLAUDE.md working agreement proved wrong or incomplete this session,
   propose the specific edit and apply it upon approval.

Session focus/notes from Endorphin: $ARGUMENTS

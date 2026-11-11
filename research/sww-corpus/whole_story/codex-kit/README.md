# Coding kit for a second model family (prepared 2026-11-02; NOT yet in use)

Everything an outside coder (e.g. Codex) needs to code one season exactly as the Claude coders
did, and nothing else: the coder-facing instructions and format (identical copies), a manifest of
which episode goes in which season, and `build_kit.py`, which downloads only that season plus the
16 unassigned episodes and rebuilds the reading folder. Tested 2026-11-02: rebuilt S09, S13 and the
unassigned folder byte-identical to the Claude coders' folders.

**Blinding:** this folder must be copied into a separate, otherwise empty repository before an
outside coder uses it. Pointed at `coercive-harm-framework` itself, the coder would see the
project's hypotheses, earlier results and close-read files.

**If used, it is deviation D3** (coders from a second model family for named seasons), to be logged
in `../DEVIATIONS.md` with the seasons, before any outside coder starts.

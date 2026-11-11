# Reel scripts for "Told Whole": the whole-story test of Something Was Wrong, S1–S26
# (coercive-harm-framework, research/sww-corpus/results/whole_story/RESULTS.md, branch
# ccr-f78b372d-8qdcn9). Made one reel at a time (Endorphin, 2026-11-11). Every figure is from
# RESULTS.md; survivors keep the show's names; no perpetrator or uncharged person is named.
# Testimony as broadcast: allegations, not verdicts.
#
# Card kinds (shared renderer, see ../sww-reels/content.py): title, head, quote, stat, list, bars.

SERIES = "TOLD · WHOLE"
SUB = "What institutions did for the people of Something Was Wrong, Seasons 1–26"
STAGES = []   # the renderer imports it; this series has no cycle ring

REELS = [
  {"slug": "intro", "id": "01", "kicker": "INTRO", "accent": "#ff4d5e", "scenes": [
    {"say": "Something Was Wrong is a podcast where people tell what was done to them, and what happened after. Twenty-six seasons. This series asks one question of all of them.",
     "card": {"t": "title", "big": "26 seasons.\nOne question.", "small": "Something Was Wrong · Seasons 1–26"}},
    {"say": "When someone who was harmed went to an institution, the police, a court, a school, an employer, a church, a hospital, did it protect them?",
     "card": {"t": "list", "head": "Did it protect them?", "items": ["Police and courts", "Schools and employers", "Churches", "Hospitals and therapists"]}},
    {"say": "An earlier pass asked this one moment at a time. It cut the episodes into short pieces and judged each response alone. Judged that way, most responses looked reasonable.",
     "card": {"t": "stat", "num": "63%", "label": "of single responses looked appropriate, judged one moment at a time"}},
    {"say": "But nobody lives one moment at a time. A detective calls back. Months later, the case is dropped. Cut into pieces, that phone call counts as protection.",
     "card": {"t": "head", "head": "A person is not\na moment.", "body": "The call back. Then the dropped case."}},
    {"say": "So this time, every person's story was followed whole. From the harm, through every institution they reached, in order, to how it ended for them.",
     "card": {"t": "list", "head": "Followed whole", "items": ["Every episode, read in full", "Every institution, in order", "How it ended for the person"]}},
    {"say": "The reading was done by A.I. coders, two per season, working apart. Not people. The project's director gave the reason.",
     "card": {"t": "head", "head": "Two coders per season.\nWorking apart.", "body": "Machine readers, by design."}},
    {"say": "In his words: the human institution and the human individual are both highly vulnerable to the bad faith aspects of language.",
     "card": {"t": "quote", "q": "The human institution and the human individual are both highly vulnerable to the bad faith aspects of language.", "by": "Endorphin, project director"}},
    {"say": "Before any result came in, three predictions were written down, each with the line that would prove it wrong.",
     "card": {"t": "list", "head": "Written down first", "items": ["Fewer than 4 in 10 end up protected", "3 in 10 or more meet disbelief, blame or self-protection", "When protection comes, the person or their people did the decisive work, at least half the time"]}},
    {"say": "And the study broke one of its own promises. The coders were meant to be blind to what the project expected. One family of A.I. coders, Claude, was shown the project's own files. Only the other, Codex, was truly blind. So every result in this series is shown both ways.",
     "card": {"t": "head", "head": "A promise\nbroken.", "body": "Claude coders: not blind · Codex coders: blind · every result shown both ways"}},
    {"say": "Here is the first answer, and the clearest. Of the people who reached an institution, about one in five ended up protected. Under both families of coders, it stayed under one in three.",
     "card": {"t": "stat", "num": "1 in 5", "label": "of people who reached an institution ended up protected"}},
    {"say": "The rest, and what it does and doesn't mean, comes one piece at a time. Everything here is survivors' testimony, as broadcast. Allegations, not verdicts.",
     "card": {"t": "title", "big": "One piece\nat a time.", "small": "testimony as broadcast · allegations, not verdicts"}},
  ]},
]

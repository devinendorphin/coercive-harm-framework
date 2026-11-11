# Reel scripts for "Told Whole": the whole-story test of Something Was Wrong, S1–S26
# (coercive-harm-framework, research/sww-corpus/results/whole_story/RESULTS.md, branch
# ccr-f78b372d-8qdcn9). Made one reel at a time (Endorphin, 2026-11-11). Every figure is from
# RESULTS.md; survivors keep the show's names; no perpetrator or uncharged person is named.
# Evidence is graded, not disclaimed (Endorphin, 2026-11-11): convictions and records are stated as
# such; what rests on a survivor's word alone is attributed to them. No uncharged person is named.
#
# Card kinds (shared renderer, see ../sww-reels/content.py): title, head, quote, stat, list, bars.

SERIES = "TOLD · WHOLE"
SUB = "What institutions did for the people of Something Was Wrong, Seasons 1–26"
STAGES = []   # the renderer imports it; this series has no cycle ring

REELS = [
  {"slug": "intro", "id": "01", "kicker": "INTRO", "accent": "#ff4d5e", "scenes": [
    {"say": "Something Was Wrong is a podcast where people tell what was done to them, and what happened after. Twenty-six seasons. This series asks one question of all of them.",
     "card": {"t": "tiles", "n": 26, "cols": 6, "label": "26 seasons · one question"}},
    {"say": "When someone who was harmed went to an institution, the police, a court, a school, an employer, a church, a hospital, did it protect them?",
     "card": {"t": "chips", "head": "Did it protect them?", "items": ["Police", "Courts", "Schools", "Employers", "Churches", "Hospitals", "Therapists"]}},
    {"say": "An earlier pass asked this one moment at a time. It cut the episodes into short pieces and judged each response alone. Judged that way, most responses looked reasonable.",
     "card": {"t": "pieces", "n": 100, "k": 63, "num": "63%", "label": "of single responses looked appropriate, judged one piece at a time"}},
    {"say": "But nobody lives one moment at a time. A detective calls back. Months later, the case is dropped. Cut into pieces, that phone call counts as protection.",
     "card": {"t": "timeline", "nodes": [{"label": "The harm"}, {"label": "They report it to police"},
              {"label": "A detective calls back", "state": "good", "tag": "cut into pieces: counts as protection"},
              {"label": "Months later, the case is dropped", "state": "bad"}, {"label": "How it ended: not protected", "state": "end"}]}},
    {"say": "So this time, every person's story was followed whole. From the harm, through every institution they reached, in order, to how it ended for them.",
     "card": {"t": "timeline", "nodes": [{"label": "The harm"}, {"label": "The police"}, {"label": "A court"}, {"label": "An employer"},
              {"label": "How it ended for the person", "state": "end", "tag": "followed to the last episode"}]}},
    {"say": "The reading was done by A.I. coders, two per season, working apart. Not people. The project's director gave the reason.",
     "card": {"t": "readers", "a": "Coder 1", "b": "Coder 2", "note": "Every episode read in full, by two machine coders working apart."}},
    {"say": "In his words: the human institution and the human individual are both highly vulnerable to the bad faith aspects of language.",
     "card": {"t": "quote", "q": "The human institution and the human individual are both highly vulnerable to the bad faith aspects of language.", "by": "Endorphin, project director"}},
    {"say": "Before any result came in, three predictions were written down, each with the line that would prove it wrong.",
     "card": {"t": "gauges", "head": "Written down first", "items": [
              {"label": "Fewer than 4 in 10 end up protected", "value": 0.40, "side": "below", "line": "LINE: 40%"},
              {"label": "3 in 10 or more meet disbelief, blame or self-protection", "value": 0.30, "side": "above", "line": "LINE: 30%"},
              {"label": "When protection comes, the person or their people did the decisive work at least half the time", "value": 0.50, "side": "above", "line": "LINE: 50%"}]}},
    {"say": "And the study broke one of its own promises. The coders were meant to be blind to what the project expected. One family of A.I. coders, Claude, was shown the project's own files. Only the other, Codex, was truly blind. So every result in this series is shown both ways.",
     "card": {"t": "eyes", "left": ["Claude", "shown the project's files"], "right": ["Codex", "blind, as promised"], "foot": "Every result in this series is shown both ways."}},
    {"say": "Here is the first answer, and the clearest. Each dot is a person who reached an institution. These are the ones who ended up protected. About one in five. Under both families of coders, it stayed under one in three.",
     "card": {"t": "dots", "n": 398, "k": 83, "cols": 25, "num": "1 in 5", "label": "ended up protected: 83 of 398 people (Claude coders 28% · Codex coders 16%)", "hi": "protected", "lo": "not protected, or only partly"}},
    {"say": "Some of these stories ended in convictions and court records. Some are backed by documents or a second witness. And when a story is told solely from the person's own account, this series will say so, but only after checking that it really is.",
     "card": {"t": "grades", "items": [["Convictions and court records", "stated as what they are", "court"],
              ["Documents, checked records, second witnesses", "said with what backs them", "doc"],
              ["The person's own account alone", "said only after checking that nothing else backs it", "voice"]]}},
    {"say": "The rest comes one piece at a time.",
     "card": {"t": "title", "big": "One piece\nat a time.", "small": "Told Whole · Something Was Wrong, Seasons 1–26"}},
  ]},
]

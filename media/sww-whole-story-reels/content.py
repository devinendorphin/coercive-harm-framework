# Reel scripts for "Told Whole": the whole-story test of Something Was Wrong, S1–S26
# (coercive-harm-framework, research/sww-corpus/results/whole_story/RESULTS.md, branch
# ccr-f78b372d-8qdcn9). Made one reel at a time (Endorphin, 2026-11-11). Every figure is from
# RESULTS.md; survivors keep the show's names; no perpetrator or uncharged person is named.
# Evidence is graded, not disclaimed (Endorphin, 2026-11-11): convictions and records are stated as
# such; what rests on a survivor's word alone is attributed to them. No uncharged person is named.
#
# Card kinds (shared renderer, see ../sww-reels/content.py): title, head, quote, stat, list, bars;
# visual cards in cards_visual.py: tiles, chips, pieces, timeline, readers, gauges, eyes, dots, grades, dotrows.
# Reel 02 draws on the close read (research/sww-corpus/close-read/CODEBOOK.md, CROSS-SEASON.md) and the
# word-count test (research/sww-corpus/README.md), not on RESULTS.md.

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
  {"slug": "same-moves", "id": "02", "kicker": "SAME MOVES", "accent": "#ff4d5e", "scenes": [
    {"say": "The first claim behind this series is about the people who did the harm. Different people, different places, different years. The claim is that they make the same moves.",
     "card": {"t": "title", "big": "Same moves.", "small": "Arc 1 · as far as the room allows"}},
    {"say": "The moves were written down before the reading began, in the project director's own words.",
     "card": {"t": "quote", "q": "It is a cycle: the effusive love bombing, to devaluation, to isolation and poisoning the wells between the people that are part of their care system, and then discard, and then potentially returning again.", "by": "Endorphin, project director"}},
    {"say": "Then the seasons were read in order, one to twenty-four, by a single A.I. reader. That reader knew the prediction. So it had one standing order: write down every story that does not fit. Never smooth it over.",
     "card": {"t": "head", "head": "Write down every misfit.", "body": "Seasons 1–24 read in order by one A.I. reader that knew the prediction."}},
    {"say": "Fifty-six stories were coded move by move. Binding. Devaluation. Isolation. Poisoning the wells. And what happened when the person left, or the truth came out.",
     "card": {"t": "timeline", "nodes": [{"label": "Binding: obligation, dependency, access"}, {"label": "Devaluation"}, {"label": "Isolation"},
              {"label": "Poisoning the wells: a false account to the people around them"}, {"label": "When they leave, or it comes out", "state": "end"}]}},
    {"say": "The first move rarely looks like a move. It binds. And it took whatever shape fit the person. A whirlwind romance. A friend in need. A boss's favour. A place to live, offered in a housing crisis. A mentor at work. A group that felt like family. Praise for a mother, aimed at her children.",
     "card": {"t": "chips", "head": "One move, many shapes", "items": ["A whirlwind romance", "A friend in need", "A boss's favour", "Housing in a crisis", "A mentor at work", "A group like family", "Praise for a mother"]}},
    {"say": "The shapes differ. What each one does is the same. Counted by what it did, not how it looked, each move turned up again and again, as first coded. Each dot is one story.",
     "card": {"t": "dotrows", "n": 56, "head": "56 stories, as first coded", "rows": [["Binding", 55], ["Devaluation", 52], ["Isolation", 48], ["Poisoning the wells", 48]],
              "foot": "Blue: the move is in the story. Binding's one gap: not in the reading notes. Seasons 16–24 were coded from notes, a weaker basis."}},
    {"say": "And when someone left, or the truth came out, the first coding found a response in every one of the fifty-six. Pursuit, threats, reversal, a smear.",
     "card": {"t": "dots", "n": 56, "k": 56, "cols": 14, "num": "56 of 56", "label": "met a response, as first coded", "hi": "a response", "lo": "none"}},
    {"say": "Then seven of those stories, picked at random, were read again in full, with a rule written down first: a mark stays only if the transcript shows what the move does, not just something that looks like it. Binding and devaluation held every time. The response at exit held in five of six. Isolation held in four of five. Poisoning the wells held in one of five.",
     "card": {"t": "dotrows", "n": 12, "head": "7 stories read again in full", "rows": [["Binding", 6, 6], ["Devaluation", 6, 6], ["Response at exit", 5, 6], ["Isolation", 4, 5], ["Poisoning the wells", 1, 5]],
              "foot": "Blue: the mark held. Grey: it did not. Each dot is one story where the move was first marked."}},
    {"say": "Most of the poisoning marks that failed were stories told to the person about the people around her, not stories told to her people about her. Whether those count is the director's call, and it has not been made. Either way, three of the first counts are too high: isolation, poisoning the wells, and the response at exit. By how much is not known until every story is read again.",
     "card": {"t": "head", "head": "Three counts are too high.", "body": "Isolation, poisoning the wells and the response at exit, by amounts not yet known. Binding and devaluation held."}},
    {"say": "Now, where it breaks. Binding alone tells you nothing. Some deceivers bound people, and simply ran when they were caught. The re-read found one more story that belongs there: a friend who invented a whole cast of people, and when she was caught, simply blocked her. The pattern is the combination, not any one move.",
     "card": {"t": "head", "head": "No single move is the pattern.", "body": "Some deceivers bound people and simply ran when caught. What marks the pattern is the moves together, and the response when someone leaves."}},
    {"say": "Isolation was the weakest move. A word-count test, written down in advance, found isolation talk three times as common as in a comparison podcast. But it was clearly raised in only about one season in four. By its own rule, the test failed.",
     "card": {"t": "dots", "n": 26, "k": 7, "cols": 13, "num": "1 in 4", "label": "seasons where isolation talk clearly stood out, by the test written in advance (7 of 26)", "hi": "stood out", "lo": "did not",
              "after": "A fairer comparison, chosen afterwards, gives about 3 in 4. It came after, so the failure stands."}},
    {"say": "The project director's answer: look at the room. One relationship was long distance, backed by documents and a second witness. You can't cut someone off from people you never meet. In another story, backed by a second witness, the school pulled a teacher from his classes. He sent one message, then nothing. The room left no way in.",
     "card": {"t": "timeline", "nodes": [{"label": "A long-distance relationship", "tag": "documents + a second witness"},
              {"label": "No isolation coded: no room to do it"},
              {"label": "A teacher pulled from his classes", "tag": "a second witness"},
              {"label": "One message, then nothing", "state": "end"}]}},
    {"say": "That is a hypothesis, not a finding. To test it, a separate reader would have to code what each room allowed, before looking at the moves.",
     "card": {"t": "head", "head": "As far as the room allows.", "body": "A hypothesis until a separate reader codes each room's openings first."}},
    {"say": "And one story did not fit the prediction as written. For about three years of their marriage, a man gave his wife constant praise, and she can name no put-downs. Her daughter and her niece were his targets, and the praise was how he reached them. He pleaded guilty in federal court and was sentenced to thirty years. In her words:",
     "card": {"t": "quote", "q": "For a predator to successfully groom a child, they first have to groom the parent.", "by": "Diana, Season 15"}},
    {"say": "It was written down as a misfit. The project director reads it differently: devaluation waits for friction. For three years she never pushed back. When the truth came out and she did, the blame came at once. He put what he did down to her lack of intimacy.",
     "card": {"t": "timeline", "nodes": [{"label": "Three years: praise, and no friction"},
              {"label": "The truth comes out; she pushes back"},
              {"label": "The blame comes at once", "tag": "her \u201clack of intimacy\u201d", "state": "end"}]}},
    {"say": "That is a reading to test, not a finding. Some stories do not fit it either: the put-downs start before any friction at all.",
     "card": {"t": "head", "head": "Does devaluation wait for friction?", "body": "A reading to test, with counter-cases: in some stories the put-downs start before any friction at all."}},
    {"say": "Seventy-two notes were written down along the way. Most are about institutions, evidence and method, or are new shapes of the same moves. Sorted against the misfit rules, about four are stories where a move was missing or different while the chance was there. When they were read again in full, all four held.",
     "card": {"t": "dots", "n": 72, "k": 4, "cols": 12, "num": "4 of 72", "label": "notes are true misfits", "hi": "true misfit", "lo": "other notes",
              "after": "Read again in full: all four held."}},
    {"say": "The marks in the stories that fit did worse. About one in five did not hold. Every error ran the same way: toward the pattern. Why is not settled. The re-reader was the same kind of A.I. as the first, and not blind. A blind reader still has to check it.",
     "card": {"t": "dots", "n": 43, "k": 34, "cols": 11, "num": "34 of 43", "label": "marks in the fitting stories held", "hi": "held", "lo": "did not hold (9)",
              "after": "Every error ran toward the pattern. Same kind of reader, not blind."}},
    {"say": "Same moves, as far as the room allows, and as far as the re-reading holds. That is the claim. These are its edges.",
     "card": {"t": "title", "big": "Same moves.\nAs far as the\nroom allows.", "small": "Told Whole · Seasons 1–24"}},
  ]},
]

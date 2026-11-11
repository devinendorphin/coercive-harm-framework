"""Check every quotation in the whole-story coder files against the transcripts.

  python3 -I check_quotes.py <sww_json_dir> <coded_json> [<coded_json> ...]

A quotation is FOUND if >= 80 % of its words appear in order inside one window of the episode
the source cites (case and punctuation removed); if the cited slug is wrong or missing, the
whole season plus the unassigned episodes are searched and the hit is marked 'other-episode'.
Prints one summary line per file and writes <coded_json>.quotecheck.json beside it.
"""
import json, os, re, sys
from difflib import SequenceMatcher
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus

def toks(s): return re.findall(r"[a-z0-9']+", (s or "").lower())

src = sys.argv[1]
eps = corpus.episodes(src)
by_slug = {}
for e in eps:
    t = toks(e["text"])
    for s in [e["slug"]] + e["twins"]:
        by_slug[s] = (e, t)
grams = {}
for e in eps:
    t = toks(e["text"]); g = {}
    for i in range(len(t) - 2): g.setdefault((t[i], t[i+1], t[i+2]), []).append(i)
    grams[e["slug"]] = (t, g)

def score(q, slug):
    t, g = grams[slug]
    cand = {}
    for i in range(len(q) - 2):
        for p in g.get((q[i], q[i+1], q[i+2]), [])[:50]:
            start = max(0, p - i); cand[start // 10] = start
    best = 0.0
    for start in list(cand.values())[:200]:
        w = t[max(0, start - 5): start + int(len(q) * 1.5) + 10]
        m = sum(b.size for b in SequenceMatcher(None, q, w, autojunk=False).get_matching_blocks())
        best = max(best, m / len(q))
        if best >= 0.999: break
    return best

def quotes(d):
    for p in d.get("persons", []):
        pid = p.get("person_id")
        for c in p.get("contacts") or []:
            yield pid, f"contact{c.get('n')}", c.get("quote"), c.get("source")
        nr = p.get("never_reached") or {}
        for q in nr.get("quotes") or []:
            yield pid, "never_reached", q.get("quote"), q.get("source")
        yield pid, "outcome", p.get("outcome_quote"), p.get("outcome_source")
        if p.get("decisive_work_quote"):
            yield pid, "decisive", p.get("decisive_work_quote"), p.get("decisive_work_source")
    for i, o in enumerate(d.get("others_mentioned") or []):
        yield f"other{i}", "others_mentioned", o.get("quote"), o.get("source")

for fn in sys.argv[2:]:
    d = json.load(open(fn))
    season = d.get("season")
    pool = [e["slug"] for e in eps if e["season"] in (season, None)]
    rows, n, found, other = [], 0, 0, 0
    for pid, field, q, srcref in quotes(d):
        qt = toks(q)
        if len(qt) < 4: rows.append([pid, field, "too-short", None]); continue
        n += 1
        slug = (srcref or "").split("@")[0].strip().strip("[]")
        s = 0.0; where = "cited"
        if slug in by_slug:
            s = score(qt, by_slug[slug][0]["slug"])
        if s < 0.8:
            best = max(((score(qt, sl), sl) for sl in pool), default=(0, None))
            if best[0] > s: s, where = best[0], "other-episode"
        ok = s >= 0.8
        found += ok; other += ok and where == "other-episode"
        rows.append([pid, field, round(s, 3), where])
    json.dump(rows, open(fn + ".quotecheck.json", "w"))
    print(f"{os.path.basename(fn)}: {found}/{n} quotations found ({other} in a different episode than cited)")

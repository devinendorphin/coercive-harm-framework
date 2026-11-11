"""Shared corpus rules for the whole-story test (preregistration-whole-story.md).

  python3 -I corpus.py index <sww_json_dir>                 # every episode -> season (or UNASSIGNED)
  python3 -I corpus.py dump  <sww_json_dir> <season> <out>  # one season, in order, ~18k-word chunks

De-duplication: the site lists most episodes twice, as two different machine transcriptions
under different slugs and slightly different titles. Two files are the same episode only if
their vocabularies overlap (Jaccard of distinct words longer than five letters >= 0.55) and
their seasons do not conflict. Tested 2026-11-01: 261 known twin pairs all scored >= 0.66
(median 0.85); the three separate parts of the S6 update series scored 0.33-0.34. The longer
text is kept, and a season carried by either twin is kept. Slug and title rules alone failed
both ways (they merged separate parts, or missed renumbered twins), so they are not used.
Season assignment: the slug's own "sN" prefix; otherwise an explicit "season-N", "sww-sN" or
"-sN-" inside the slug (update and WCN episodes). Episodes with no season (Data Points,
some specialist episodes) are UNASSIGNED and listed by `index` so a coder can decide whether
a story is told there; they are never silently dropped.
"""
import glob, json, re, sys, os

def key(slug):
    k = re.sub(r"^s\d+-e?p?\d+(-\d+)?-", "", slug)
    k = re.sub(r"^s\d+-", "", k)
    k = re.sub(r"^\d+-(?=wcn)", "", k)
    return re.sub(r"-2$", "", k)

def season_of(slug):
    m = re.match(r"s(\d+)(?!\d)", slug)
    if m: return int(m.group(1))
    m = re.search(r"season-(\d+)|sww-s(\d+)\b|-s(\d+)-|-s(\d+)$", slug)
    return int(next(g for g in m.groups() if g)) if m else None

def vocab(e):
    return set(w for w in re.findall(r"[a-z']+", e.get("text", "").lower()) if len(w) > 5)

def episodes(src, threshold=0.55):
    files = [json.load(open(f)) for f in sorted(glob.glob(f"{src}/*.json"))]
    for e in files: e["_v"] = vocab(e); e["_s"] = season_of(e["slug"])
    parent = list(range(len(files)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            si, sj = files[i]["_s"], files[j]["_s"]
            if si and sj and si != sj: continue
            vi, vj = files[i]["_v"], files[j]["_v"]
            if vi and vj and len(vi & vj) / len(vi | vj) >= threshold:
                parent[find(i)] = find(j)
    groups = {}
    for i, e in enumerate(files): groups.setdefault(find(i), []).append(e)
    out = []
    for g in groups.values():
        e = max(g, key=lambda x: len(x.get("text", "")))
        e["season"] = next((x["_s"] for x in g if x["_s"]), None)
        e["twins"] = sorted(x["slug"] for x in g if x is not e)
        out.append(e)
    return out

def frozen_episodes(src, index_file):
    """Read the original canonical selections and season assignments from a saved index.

    A canonical slug can lack its season while a discarded twin supplied it. Rebuilding
    from canonical files alone must retain the committed assignment, not rerun slug-only
    assignment without those twins. Full transcript text is read; no summaries are used.
    """
    out, seen = [], set()
    with open(index_file) as f:
        lines = f.read().splitlines()
    for line in lines:
        fields = line.split()
        if len(fields) != 3:
            continue
        season, _, slug = fields
        assert slug not in seen, slug
        seen.add(slug)
        with open(os.path.join(src, slug + '.json')) as f:
            e = json.load(f)
        assert e['slug'] == slug and e['text'], slug
        e['season'] = None if season == 'UNASSIGNED' else int(season)
        e['twins'] = []
        out.append(e)
    return out

def epnum(slug):
    m = re.match(r"s\d+(?!\d)-?e?p?(\d+)", slug)
    return int(m.group(1)) if m else 999

def index(src):
    rows = sorted((e["season"] or 0, epnum(e["slug"]), e["slug"]) for e in episodes(src))
    for s, n, slug in rows: print(s if s else "UNASSIGNED", n, slug)
    print(len(rows), "unique episodes;", sum(1 for r in rows if not r[0]), "unassigned")

def dump(src, season, out, episodes_override=None):
    os.makedirs(out, exist_ok=True)
    source_eps = episodes(src) if episodes_override is None else episodes_override
    eps = sorted(((epnum(e["slug"]), e["slug"], e) for e in source_eps if e["season"] == season),
                 key=lambda x: (x[0], x[1]))
    chunk, words, k = [], 0, 1
    def flush():
        nonlocal chunk, words, k
        if chunk:
            with open(f"{out}/s{season:02d}_{k:02d}.txt", "w") as f:
                f.write("\n".join(chunk))
            k += 1; chunk, words = [], 0
    for n, slug, e in eps:
        notes = re.sub(r"\s+", " ", e.get("notes", ""))[:1500]
        chunk.append(f"\n##### {e['title']}  [{slug}]\nNOTES: {notes}\n")
        para, last = [], -999
        for sec, t in e["segments"]:
            if sec - last >= 60:
                if para: chunk.append(" ".join(para)); para = []
                para.append(f"[{sec//60}:{sec%60:02d}]"); last = sec
            para.append(t); words += len(t.split())
            if words > 18000 and len(para) > 1 and sec - last >= 55:
                chunk.append(" ".join(para)); para = []; flush()
                para.append(f"[{sec//60}:{sec%60:02d}] (cont. {slug})"); last = sec
        if para: chunk.append(" ".join(para))
    flush()
    print(season, len(eps), "episodes:", [s for _, s, _ in eps])

if __name__ == "__main__":
    cmd, *a = sys.argv[1:]
    index(a[0]) if cmd == "index" else dump(a[0], int(a[1]), a[2])

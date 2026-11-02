"""Rebuild one season's reading folder exactly as the other coders received it.

  python3 -I build_kit.py fetch <season> <json_dir>          # download only this season + unassigned
  python3 -I build_kit.py build <season> <json_dir> <read_dir>

Same chunking as tools/corpus.py dump (18k-word chunks, one paragraph per minute), same
unassigned folder, and a final check that every file's line count matches manifest.json.
"""
import html, json, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(f"{HERE}/manifest.json"))

def get(url):
    for i in range(8):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace")
            time.sleep(1.5); return r
        except Exception:
            time.sleep(min(300, 15 * 2 ** i))
    raise RuntimeError(url)

def fetch(season, out):
    os.makedirs(out, exist_ok=True)
    for slug in M["seasons"][str(season)] + M["unassigned"]:
        fn = f"{out}/{slug}.json"
        if os.path.exists(fn): continue
        h = get(f"https://podscripts.co/podcasts/something-was-wrong/{slug}")
        m = re.search(r"window\.__EPISODE__ = (\{.*?\});?\s*</script>", h, re.S); meta = {}
        if m:
            try: meta = json.loads(m.group(1)).get("episode", {})
            except Exception: pass
        segs = [(int(s), html.unescape(re.sub(r"<[^>]+>", "", t)).strip())
                for s, t in re.findall(r'class="psb-ep__sentence"[^>]*data-seconds="(\d+)"[^>]*>(.*?)</span>', h, re.S)]
        title = meta.get("title") or html.unescape((re.search(r"<title>(.*?)</title>", h) or [None, slug])[1])
        json.dump({"slug": slug, "title": title, "notes": meta.get("description", ""), "segments": segs,
                   "text": " ".join(t for _, t in segs)}, open(fn, "w"))
        print("fetched", slug, flush=True)

def paras(e):
    out, para, last = [], [], -999
    for sec, t in e["segments"]:
        if sec - last >= 60:
            if para: out.append(" ".join(para)); para = []
            para.append(f"[{sec//60}:{sec%60:02d}]"); last = sec
        para.append(t)
    if para: out.append(" ".join(para))
    return out

def build(season, src, out):
    d = f"{out}/s{season:02d}"; os.makedirs(d, exist_ok=True)
    chunk, words, k = [], 0, 1
    def flush():
        nonlocal chunk, words, k
        if chunk:
            open(f"{d}/s{season:02d}_{k:02d}.txt", "w").write("\n".join(chunk) + "\n"); k += 1; chunk, words = [], 0
    for slug in M["seasons"][str(season)]:
        e = json.load(open(f"{src}/{slug}.json"))
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
    u = f"{out}/unassigned"; os.makedirs(u, exist_ok=True); idx = []
    for slug in M["unassigned"]:
        e = json.load(open(f"{src}/{slug}.json"))
        lines = [f"##### {e['title']}  [{slug}]", "NOTES: " + re.sub(r"\s+", " ", e.get("notes", ""))[:1500], ""] + paras(e)
        open(f"{u}/{slug}.txt", "w").write("\n".join(lines) + "\n")
        idx.append(f"{slug}.txt\t{e['title']}\t{len(e.get('text','').split())} words\t" + re.sub(r"\s+", " ", e.get("notes", ""))[:400])
    open(f"{u}/INDEX.txt", "w").write("Episodes published without a season number. Open and read in full any that may continue, update "
                                      "or discuss a story from your season.\n\n" + "\n".join(idx) + "\n")
    bad = []
    for rel, n in M["linecounts"].items():
        if rel.startswith(f"s{season:02d}/") or rel.startswith("unassigned/"):
            p = f"{out}/{rel}"
            got = sum(1 for _ in open(p)) if os.path.exists(p) else None
            if got != n: bad.append((rel, n, got))
    print("LINE COUNTS MATCH" if not bad else f"MISMATCH (site may have changed; stop and report): {bad}")

if __name__ == "__main__":
    cmd, s = sys.argv[1], int(sys.argv[2])
    fetch(s, sys.argv[3]) if cmd == "fetch" else build(s, sys.argv[3], sys.argv[4])

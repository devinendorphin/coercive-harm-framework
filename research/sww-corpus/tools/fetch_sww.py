"""Fetch Something Was Wrong transcripts from podscripts.co -> one JSON per episode
{slug,title,notes,text,segments:[[sec,sentence],...]}. Transcripts stay outside the repo."""
import json, os, re, sys, time, html, urllib.request, concurrent.futures as cf
BASE = "https://podscripts.co"
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
def get(url):
    for i in range(8):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8", "replace")
            time.sleep(1.5)
            return r
        except Exception as e:
            time.sleep(min(300, 15 * 2 ** i))
    raise RuntimeError(url)
links = set()
for p in range(1, 40):
    h = get(f"{BASE}/podcasts/something-was-wrong?page={p}")
    new = set(re.findall(r'href="(/podcasts/something-was-wrong/[^"#?]+)"', h))
    if not new - links and p > 1: break
    links |= new
print(len(links), "episode links", flush=True)
def one(path):
    slug = path.rsplit("/", 1)[1]
    fn = f"{OUT}/{slug}.json"
    if os.path.exists(fn): return slug, "cached"
    h = get(BASE + path)
    m = re.search(r"window\.__EPISODE__ = (\{.*?\});?\s*</script>", h, re.S)
    meta = {}
    if m:
        try: meta = json.loads(m.group(1)).get("episode", {})
        except Exception: pass
    segs = [(int(s), html.unescape(re.sub(r"<[^>]+>", "", t)).strip())
            for s, t in re.findall(r'class="psb-ep__sentence"[^>]*data-seconds="(\d+)"[^>]*>(.*?)</span>', h, re.S)]
    title = meta.get("title") or html.unescape((re.search(r"<title>(.*?)</title>", h) or [None, slug])[1])
    d = {"slug": slug, "title": title, "notes": meta.get("description", ""), "segments": segs,
         "text": " ".join(t for _, t in segs)}
    json.dump(d, open(fn, "w"))
    return slug, len(d["text"].split())
with cf.ThreadPoolExecutor(1) as ex:
    for slug, n in ex.map(one, sorted(links)):
        pass
print("done", len(os.listdir(OUT)))

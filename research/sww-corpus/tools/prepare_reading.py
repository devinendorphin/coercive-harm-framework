"""Prepare the coders' reading folders for the whole-story test.

  python3 -I prepare_reading.py <sww_json_dir> <read_dir> <repo_whole_story_dir>

Writes <read_dir>/sNN/ (season chunks, via corpus.dump), <read_dir>/unassigned/ (INDEX.txt plus
one transcript file per unassigned episode, same paragraph format), and copies the coder-facing
part of CODING-INSTRUCTIONS.md (below its first '---' line) to <read_dir>/INSTRUCTIONS.md and
OUTPUT-FORMAT.json beside it. Also writes <read_dir>/linecounts.tsv for the reading-in-full check.
"""
import argparse, os, re, sys, shutil, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('src')
parser.add_argument('out')
parser.add_argument('ws')
parser.add_argument('--frozen-index', help='Retain original canonical selections and inherited season assignments')
args = parser.parse_args()
src, out, ws = args.src, args.out, args.ws
os.makedirs(out, exist_ok=True)
eps = corpus.frozen_episodes(src, args.frozen_index) if args.frozen_index else corpus.episodes(src)
seasons = sorted({e["season"] for e in eps if e["season"]})
for s in seasons:
    corpus.dump(src, s, f"{out}/s{s:02d}", episodes_override=eps if args.frozen_index else None)
for p in glob.glob(f"{out}/s*/*.txt"):  # D1: end every chunk with a newline so line counts agree
    t = open(p).read()
    if not t.endswith("\n"): open(p, "w").write(t + "\n")

ua = sorted((e for e in eps if not e["season"]), key=lambda e: e["slug"])
os.makedirs(f"{out}/unassigned", exist_ok=True)
idx = []
for e in ua:
    lines = [f"##### {e['title']}  [{e['slug']}]", "NOTES: " + re.sub(r"\s+", " ", e.get("notes", ""))[:1500], ""]
    para, last = [], -999
    for sec, t in e["segments"]:
        if sec - last >= 60:
            if para: lines.append(" ".join(para)); para = []
            para.append(f"[{sec//60}:{sec%60:02d}]"); last = sec
        para.append(t)
    if para: lines.append(" ".join(para))
    open(f"{out}/unassigned/{e['slug']}.txt", "w").write("\n".join(lines) + "\n")
    idx.append(f"{e['slug']}.txt\t{e['title']}\t{len(e.get('text','').split())} words\t"
               + re.sub(r"\s+", " ", e.get("notes", ""))[:400])
open(f"{out}/unassigned/INDEX.txt", "w").write(
    "Episodes published without a season number. Open and read in full any that may continue, update "
    "or discuss a story from your season.\n\n" + "\n".join(idx) + "\n")

text = open(f"{ws}/CODING-INSTRUCTIONS.md").read()
coder_text = text.split("\n---\n", 1)[1].lstrip()
open(f"{out}/INSTRUCTIONS.md", "w").write(coder_text)
shutil.copy(f"{ws}/OUTPUT-FORMAT.json", f"{out}/OUTPUT-FORMAT.json")

with open(f"{out}/linecounts.tsv", "w") as f:
    for p in sorted(glob.glob(f"{out}/s*/*.txt")) + sorted(glob.glob(f"{out}/unassigned/*.txt")):
        n = sum(1 for _ in open(p))
        w = len(open(p).read().split())
        f.write(f"{os.path.relpath(p, out)}\t{n}\t{w}\n")
print("seasons", seasons, "| unassigned", len(ua))

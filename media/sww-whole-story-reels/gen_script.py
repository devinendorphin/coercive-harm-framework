"""Write SCRIPT.md: every reel's narration with what appears on screen."""
import json, re
from content import REELS, SERIES, SUB

L = [f"# {SERIES} — reel scripts", "",
     f"*{SUB}. {len(REELS)} vertical reels (1080×1920, 30 fps), Kokoro TTS narration (voice `af_heart`), "
     "procedural soundtrack. Source: `research/sww-corpus/results/whole_story/RESULTS.md` (branch `ccr-f78b372d-8qdcn9`). "
     "Made one reel at a time. Survivors keep the show's names; no perpetrator or uncharged person is named. "
     "Testimony as broadcast: allegations, not verdicts.*", ""]
for r in REELS:
    d = json.load(open(f"build/timing_{r['slug']}.json"))["dur"] + 2.6
    L += [f"## {r['id']} · {r['kicker'].title()}  ({d:.0f} s)", ""]
    for sc in r["scenes"]:
        say = re.sub(r"\[([^\]]+)\]\(/[^)]*/\)", r"\1", sc["say"])
        c = sc["card"]
        on = {"title": lambda: c["big"].replace("\n", " ") + " — " + c["small"],
              "head": lambda: c["head"].replace("\n", " ") + " — " + c["body"],
              "quote": lambda: "“" + c["q"] + "” — " + c["by"], "stat": lambda: c["num"] + " — " + c["label"],
              "list": lambda: c["head"] + ": " + "; ".join(c["items"]),
              "cycle": lambda: f"cycle ring: {c['label']} [{c['marks']}]",
              "bars": lambda: c["head"] + ": " + "; ".join(f"{x[0]} {x[1]}" for x in c["rows"])}[c["t"]]()
        L += [f"- {say}", f"  - *on screen:* {on}"]
    L.append("")
L += ["Cycle-ring marks: y present · p partial · n absent · o not observable · d not described "
      "(stages: love bombing, devalue, isolate, poison the well, discard, return)."]
open("SCRIPT.md", "w").write("\n".join(L) + "\n")
print(round(sum(json.load(open(f"build/timing_{r['slug']}.json"))["dur"] + 2.6 for r in REELS) / 60, 1), "min")

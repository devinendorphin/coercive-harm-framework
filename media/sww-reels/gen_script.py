"""Write SCRIPT.md: every reel's narration with what appears on screen."""
import json, re
from content import REELS, SERIES, SUB

L = [f"# {SERIES} — reel scripts", "",
     f"*{SUB}. {len(REELS)} vertical reels (1080×1920, 30 fps), Kokoro TTS narration (voice `af_heart`), "
     "procedural soundtrack. Sources: the close-read on branches `ccr-93dfe246-4ja9f0` (S1–S10, `729dd3e`) and "
     "`ccr-89a0fcc4-xfqzcf` (S11–S15, `a5611e8`), `research/sww-corpus/`; Seasons 16–24 from `ccr-81ec1931-b41u1s` (`92925ef`), "
     "`research/something-was-wrong-s16.md` and `-s17-s24.md` (S17–S19 read in excerpts only). Survivors keep the show's pseudonyms; "
     "the S14 perpetrator's surname is left out, as in the study. Testimony as broadcast (P2): allegations, not verdicts.*", ""]
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

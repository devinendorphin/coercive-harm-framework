"""Hold quote cards long enough to read when the narration only introduces them.
Inserts silence after such scenes and shifts later timings. Idempotent (marks the JSON)."""
import json, sys
import numpy as np, soundfile as sf
from content import REELS

SR, WPS, BASE = 24000, 3.3, 0.8
for reel in REELS:
    slug = reel["slug"]
    if sys.argv[1:] and slug not in sys.argv[1:]:
        continue
    tm = json.load(open(f"build/timing_{slug}.json"))
    if tm.get("held"):
        continue
    audio, _ = sf.read(f"build/voice_{slug}.wav", dtype="float32")
    shift, pieces, cur = 0.0, [], 0
    for sc, ti in zip(reel["scenes"], tm["scenes"]):
        for w in ti["words"]:
            w["s"] += shift; w["e"] += shift
        ti["start"] += shift; ti["end"] += shift
        c = sc["card"]
        if c["t"] != "quote":
            continue
        need = len(c["q"].split()) / WPS + BASE
        hold = need - (ti["end"] - ti["start"])
        if hold <= 0.3:
            continue
        cut = int(round((ti["end"] - shift) * SR))
        pieces += [audio[cur:cut], np.zeros(int(hold * SR), np.float32)]
        cur = cut
        ti["end"] += hold
        shift += hold
    pieces.append(audio[cur:])
    sf.write(f"build/voice_{slug}.wav", np.concatenate(pieces), SR)
    tm["dur"] += shift; tm["held"] = True
    json.dump(tm, open(f"build/timing_{slug}.json", "w"), indent=1)
    print(slug, f"+{shift:.1f}s")

"""Kokoro narration for each reel: one WAV plus a timing JSON (scene spans and word spans)."""
import json, re, sys, os
import numpy as np, soundfile as sf
from kokoro import KPipeline
from content import REELS

SR = 24000
LEAD, GAP, TAIL = 0.7, 0.45, 0.3
VOICE, SPEED = "af_heart", 1.0

pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
os.makedirs("build", exist_ok=True)
ids = sys.argv[1:] or [r["slug"] for r in REELS]

for reel in REELS:
    if reel["slug"] not in ids:
        continue
    chunks, scenes, t = [np.zeros(int(LEAD * SR), np.float32)], [], LEAD
    for sc in reel["scenes"]:
        start, words = t, []
        for r in pipe(sc["say"], voice=VOICE, speed=SPEED):
            a = r.audio.numpy().astype(np.float32)
            for tk in r.tokens:
                txt = re.sub(r"\[([^\]]+)\]\(/[^)]*/\)", r"\1", tk.text)
                s = t + (tk.start_ts or 0.0)
                e = t + (tk.end_ts or tk.start_ts or 0.0)
                if words and (not re.search(r"\w", txt) or words[-1]["glue"]):
                    words[-1]["w"] += txt
                    words[-1]["e"] = max(words[-1]["e"], e)
                    words[-1]["glue"] = not tk.whitespace
                else:
                    words.append({"w": txt, "s": s, "e": e, "glue": not tk.whitespace})
            chunks.append(a)
            t += len(a) / SR
        for w in words:
            w.pop("glue")
        scenes.append({"start": start, "end": t, "words": words})
        chunks.append(np.zeros(int(GAP * SR), np.float32))
        t += GAP
    chunks.append(np.zeros(int(TAIL * SR), np.float32))
    audio = np.concatenate(chunks)
    sf.write(f"build/voice_{reel['slug']}.wav", audio, SR)
    json.dump({"dur": len(audio) / SR, "scenes": scenes}, open(f"build/timing_{reel['slug']}.json", "w"), indent=1)
    print(reel["slug"], round(len(audio) / SR, 1), "s", flush=True)

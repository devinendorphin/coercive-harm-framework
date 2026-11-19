"""Kokoro narration for each reel: one WAV plus a timing JSON (scene spans and word spans)."""
import json, re, sys, os
import numpy as np, soundfile as sf
from kokoro import KPipeline
from content import REELS

SR = 24000
LEAD, GAP, TAIL = 0.7, 0.45, 0.3
VOICE, SPEED = "af_heart", 1.0

pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")

def room(a):
    """Quoted words: same voice, a subtle room-tone shift (soft low-pass plus two short reflections)."""
    y = np.copy(a); alpha = 0.55
    for i in range(1, len(y)): y[i] = alpha * y[i] + (1 - alpha) * y[i - 1]
    out = 0.9 * y
    for ms, g in ((23, 0.22), (51, 0.12)):
        k = int(SR * ms / 1000); out[k:] += g * y[:-k]
    return (out / max(1e-6, np.abs(out).max()) * np.abs(a).max()).astype(np.float32)

TRIM = False
def synth(text, t, fx=None):
    words, chunks = [], []
    for r in pipe(text, voice=VOICE, speed=SPEED):
        a = r.audio.numpy().astype(np.float32)
        lead = 0.0
        if TRIM:
            loud = np.where(np.abs(a) > 0.012)[0]
            if len(loud):
                i0 = max(0, loud[0] - int(0.04 * SR)); i1 = min(len(a), loud[-1] + int(0.14 * SR))
                lead = i0 / SR; a = a[i0:i1]
        t -= lead
        for tk in r.tokens:
            txt = re.sub(r"\[([^\]]+)\]\(/[^)]*/\)", r"\1", tk.text)
            s = t + (tk.start_ts or 0.0)
            e = t + (tk.end_ts or tk.start_ts or 0.0)
            if words and (not re.search(r"\w", txt) or words[-1]["glue"]):
                words[-1]["w"] += txt; words[-1]["e"] = max(words[-1]["e"], e); words[-1]["glue"] = not tk.whitespace
            else:
                words.append({"w": txt, "s": s, "e": e, "glue": not tk.whitespace})
        chunks.append(fx(a) if fx else a); t += len(a) / SR + lead
    for w in words: w.pop("glue")
    return words, chunks, t
os.makedirs("build", exist_ok=True)
ids = sys.argv[1:] or [r["slug"] for r in REELS]

for reel in REELS:
    if reel["slug"] not in ids:
        continue
    chunks, scenes, t = [np.zeros(int(LEAD * SR), np.float32)], [], LEAD
    TRIM = bool(reel.get("kinetic"))
    gap = 0.42 if reel.get("kinetic") else GAP
    for sc in reel["scenes"]:
        start = t
        words, ch, t = synth(sc["say"], t)
        chunks += ch
        qwords = []
        if sc.get("quote"):
            pq = 0.25 if reel.get("kinetic") else 0.3
            chunks.append(np.zeros(int(pq * SR), np.float32)); t += pq
            qwords, ch, t = synth(sc["quote"], t, room)
            chunks += ch
        scenes.append({"start": start, "end": t, "words": words, "qwords": qwords})
        g = 1.35 if (reel.get("kinetic") and sc.get("quote")) else gap
        chunks.append(np.zeros(int(g * SR), np.float32))
        t += g
    chunks.append(np.zeros(int(TAIL * SR), np.float32))
    audio = np.concatenate(chunks)
    sf.write(f"build/voice_{reel['slug']}.wav", audio, SR)
    json.dump({"dur": len(audio) / SR, "scenes": scenes}, open(f"build/timing_{reel['slug']}.json", "w"), indent=1)
    print(reel["slug"], round(len(audio) / SR, 1), "s", flush=True)

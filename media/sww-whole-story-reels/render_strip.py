"""Filmstrip renderer (1080x1080, 30 fps): python render_strip.py <slug>  ->  build/video_<slug>_strip.mp4

Visual language from the veriticide ledger's "Veriticide Stack" filmstrip, adapted: film edges with sprockets,
a frame per section (coloured panel above, cream caption strip below), a black disc whose nested arcs fill one
institution at a time, ledger cards for spoken quotes, black punchline bars. Narration timing comes from
build/timing_<slug>.json (tts.py); the quoted words reveal as the narrator speaks them.
"""
import json, math, os, re, subprocess, sys, importlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from content import REELS

FMT = os.environ.get("STRIP_FMT", "vertical")
W, H = (1080, 1920) if FMT == "vertical" else (1080, 1080)
FPS = 30
EDGE, INK, CREAM, PAPER = (42, 30, 24), (40, 32, 28), (242, 230, 207), (236, 225, 200)
SHADOW = (34, 24, 20)
DISC = (30, 23, 21)
CAP_INK = (44, 36, 32)
MUTE = (120, 104, 92)
BLUE, ORANGE, AQUA, GREY = (57, 110, 190), (214, 110, 44), (40, 150, 120), (150, 140, 130)
X0, X1, Y0 = 92, 988, 14
YP, Y1 = (1460, 1906) if FMT == "vertical" else (760, 1066)   # panel bottom, frame bottom
CAPF, CAPL, CAPN = (50, 62, 5) if FMT == "vertical" else (37, 46, 4)
SC = 1.32 if FMT == "vertical" else 1.0                          # scale for the taller stage
def z(v): return int(round(v * SC))
DY = 150 if FMT == "vertical" else 0                             # push content down the taller stage
TX = 132                                               # text left

FD = "/usr/share/fonts/opentype/inter/"
FONTS = {"black": FD + "InterDisplay-Black.otf", "xbold": FD + "InterDisplay-ExtraBold.otf", "bold": FD + "Inter-Bold.otf",
         "med": FD + "Inter-Medium.otf", "semi": FD + "Inter-SemiBold.otf",
         "serif": "/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf",
         "serif_i": "/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf",
         "mono": "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf",
         "mono_r": "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"}
_fc = {}
def font(k, s):
    if (k, s) not in _fc: _fc[(k, s)] = ImageFont.truetype(FONTS[k], int(s))
    return _fc[(k, s)]

def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def clamp(x): return min(1.0, max(0.0, x))
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def A(c, a): return tuple(c[:3]) + (int(255 * clamp(a)),)
def tw(f, s): return f.getlength(s)
def wrap(text, f, width):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            c = (line + " " + w).strip()
            if tw(f, c) <= width or not line: line = c
            else: out.append(line); line = w
        out.append(line)
    return out
def fit(text, k, mx, width, mn=40):
    s = mx
    while s > mn and max(tw(font(k, s), l) for l in text.split("\n")) > width: s -= 4
    return s
def norm(w): return re.sub(r"[^\w']", "", w.lower())

# ------------------------------------------------------------------ static layers
def make_edges():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, X0 - 8, H], fill=EDGE + (255,)); d.rectangle([X1 + 8, 0, W, H], fill=EDGE + (255,))
    for y in range(-10, H, 64):
        for x in (22, W - 22 - 30):
            d.rounded_rectangle([x, y + 14, x + 30, y + 50], 6, fill=(226, 214, 190, 255))
    txt = "TOLD WHOLE  ·  SOMETHING WAS WRONG  ·  FILMSTRIP No. 1  ·  " * 4
    f = font("mono_r", 13)
    for xc, ang in ((68, 90), (W - 68, -90)):
        s = Image.new("RGBA", (H + 400, 22), (0, 0, 0, 0)); ImageDraw.Draw(s).text((0, 2), txt, font=f, fill=(170, 150, 120, 255))
        s = s.rotate(ang, expand=True)
        im.paste(s, (int(xc - s.size[0] / 2), -200), s)
    return im

def make_mask():
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([X0, Y0, X1, Y1], 18, fill=255); return m

def vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    return np.clip(1 - 0.28 * np.clip(r - 0.55, 0, None) ** 1.6, 0.6, 1)[..., None]

RNG = np.random.default_rng(5)
GRAIN = [RNG.normal(0, 7, (H // 2, W // 2, 1)).astype(np.float32) for _ in range(6)]

# ------------------------------------------------------------------ text helpers
def sprite(lines, f, fill, lh=1.1):
    asc, desc = f.getmetrics(); step = int(f.size * lh)
    w = int(max(tw(f, l) for l in lines)) + 10
    im = Image.new("RGBA", (w, step * (len(lines) - 1) + asc + desc + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines): d.text((0, i * step), l, font=f, fill=fill)
    return im
def paste(fr, sp, x, y, op=1.0):
    if op <= 0.01: return
    a = sp.getchannel("A")
    if op < 0.99: a = a.point(lambda v: int(v * op))
    fr.paste(sp, (int(x), int(y)), a)
def display(text, size, col=CREAM):
    f = font("black", size); lines = text.split("\n")
    fg = sprite(lines, f, col + (255,), 0.98); sh = sprite(lines, f, SHADOW + (230,), 0.98)
    im = Image.new("RGBA", (fg.size[0] + 10, fg.size[1] + 10), (0, 0, 0, 0))
    im.paste(sh, (7, 7), sh); im.paste(fg, (0, 0), fg); return im

def card(d, x, y, w, h, tab=None, op=1.0):
    d.rectangle([x + 9, y + 9, x + w + 9, y + h + 9], fill=A(SHADOW, 0.55 * op))
    d.rectangle([x, y, x + w, y + h], fill=A(PAPER, op), outline=A(INK, op), width=3)
    if tab:
        f = font("mono", 16); tw_ = tw(f, tab) + 24
        d.rectangle([x + 14, y - 18, x + 14 + tw_, y + 12], fill=A(INK, op))
        d.text((x + 26, y - 13), tab, font=f, fill=A(CREAM, op))

def bars(fr, text, x, y, t, op, size=44):
    f = font("black", size); d = ImageDraw.Draw(fr, "RGBA")
    for i, ln in enumerate(text.split("\n")):
        e = ease((t - 0.18 * i) / 0.3)
        if e <= 0: continue
        w = tw(f, ln) + 30; yy = y + i * int(size * 1.32)
        d.rectangle([x, yy, x + w * e, yy + size * 1.18], fill=A(INK, op))
        if e > 0.6: d.text((x + 15, yy + size * 0.06), ln, font=f, fill=A(CREAM, op * (e - 0.6) / 0.4))

# ------------------------------------------------------------------ the disc
def disc(fr, col, n_arcs, cur, t, op, cx=812, cy=455, R=300, nums=True, a0=-38, a1=34):
    ov = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.ellipse([cx - R + 14, cy - R + 18, cx + R + 14, cy + R + 18], fill=A(SHADOW, 0.45 * op))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A(DISC, op))
    d.arc([cx - R + 30, cy - R + 30, cx + R - 30, cy + R - 30], 200, 232, fill=A((90, 80, 76), op), width=8)
    if n_arcs:
        d.pieslice([cx - R, cy - R, cx + R, cy + R], a0, a1, fill=A(mix(DISC, col, 0.22), op))
        d.line([cx, cy, cx + R * math.cos(math.radians(a0)), cy + R * math.sin(math.radians(a0))], fill=A((120, 110, 100), op), width=3)
        d.line([cx, cy, cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1))], fill=A((120, 110, 100), op), width=3)
        for k in range(n_arcs):
            r = 42 + k * 36
            on = k == cur
            e = ease((t - 0.2 - 0.08 * k) / 0.4)
            colk = col if on else mix(DISC, col, 0.45)
            d.arc([cx - r, cy - r, cx + r, cy + r], a0 + 3, a0 + 3 + (a1 - a0 - 6) * e, fill=A(colk, op), width=7 if on else 5)
    fr.paste(ov, (0, 0), ov)
    if n_arcs and nums:
        d = ImageDraw.Draw(fr, "RGBA"); f = font("bold", 18)
        for k in range(n_arcs):
            r = 42 + k * 36; am = math.radians(a1 + 9)
            x, y = cx + r * math.cos(am), cy + r * math.sin(am)
            if k == cur or k == n_arcs - 1 or n_arcs <= 4 or k == 0:
                d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=A((22, 17, 15), op))
                s = str(k + 1); d.text((x - tw(f, s) / 2, y - 12), s, font=f, fill=A(CREAM, op))

# ------------------------------------------------------------------ main
def main(slug):
    ri = [r["slug"] for r in REELS].index(slug); reel = REELS[ri]
    spec = importlib.import_module("strip_" + reel["id"]).STRIP
    tm = json.load(open(f"build/timing_{slug}.json"))
    END = 3.2; dur = tm["dur"] + END; nfr = int(dur * FPS)
    sc = []
    for k, (s, ti, sp) in enumerate(zip(reel["scenes"], tm["scenes"], spec)):
        v0 = ti["start"] - 0.15
        v1 = tm["scenes"][k + 1]["start"] - 0.15 if k + 1 < len(tm["scenes"]) else tm["dur"]
        loc = lambda ws: [{"w": w["w"], "s": w["s"] - v0, "e": w["e"] - v0} for w in ws]
        sw, qw = loc(ti["words"]), loc(ti.get("qwords", []))
        sents, cur = [], []
        for w in sw:
            cur.append(w)
            if re.search(r"[.?!:]$", w["w"]): sents.append(cur); cur = []
        if cur: sents.append(cur)
        sc.append({"k": k, "s": s, "sp": sp, "v0": v0, "v1": v1, "sw": sw, "qw": qw, "sents": sents,
                   "q0": qw[0]["s"] if qw else None, "q1": qw[-1]["e"] if qw else None})
    edges, mask, vig = make_edges(), make_mask(), vignette()
    pills = spec[0].get("pills") or importlib.import_module("strip_" + reel["id"]).INST

    def at(S, word, default, nth=0):
        n = 0
        for w in S["sw"] + S["qw"]:
            if norm(w["w"]) == word:
                if n == nth: return w["s"]
                n += 1
        return default

    cache = {}
    def title_sp(S):
        key = ("t", S["k"])
        if key not in cache:
            kind = S["sp"]["kind"]
            mx = z(80 if kind in ("chain", "pass", "coders", "quote") else 112)
            wdt = 800 if FMT == "vertical" else (600 if kind in ("inst", "ladder") else 800)
            txt = S["sp"]["title"]; size = fit(txt, "black", mx, wdt, 56)
            cache[key] = display(txt, size)
        return cache[key]

    def quote_block(fr, S, x, y, w, t, op, f=None, lh=None):
        q = S["s"].get("quote", ""); f = f or font("med", 31); lh = lh or 42
        words = q.split(" "); lines = []; line = []
        for wd in words:
            if tw(f, " ".join(line + [wd])) <= w or not line: line.append(wd)
            else: lines.append(line); line = [wd]
        lines.append(line)
        hl = set(); flat = [norm(x) for x in words]
        for p in S["sp"].get("hl", []):
            ps = [norm(x) for x in p.split(" ")]
            for i in range(len(flat) - len(ps) + 1):
                if flat[i:i + len(ps)] == ps: hl.update(range(i, i + len(ps)))
        qw = S["qw"]; n = len(words)
        times = [qw[i]["s"] for i in range(n)] if len(qw) == n else [S["q0"] + (S["q1"] - S["q0"]) * i / n for i in range(n)] if qw else [0.3 + 0.1 * i for i in range(n)]
        d = ImageDraw.Draw(fr, "RGBA"); k = 0
        for li, ln in enumerate(lines):
            xx = x
            for wd in ln:
                a = clamp((t - times[k]) / 0.15) * op
                if a > 0:
                    col = S["sp"]["color"] if k in hl else INK
                    if k in hl: col = mix(col, INK, 0.25)
                    d.text((xx, y + li * lh), wd, font=f, fill=A(col, a))
                xx += tw(f, wd + " "); k += 1
        return len(lines) * lh

    def draw_scene(fr, S, t, op):
        sp, kind = S["sp"], S["sp"]["kind"]
        col = sp["color"]
        if kind == "intro" and t > at(S, "across", 6) - 0.2: col = sp["color2"]
        # panel
        d = ImageDraw.Draw(fr, "RGBA")
        d.rectangle([X0, Y0, X1, YP], fill=col)
        # dashed orbit
        for a in range(0, 360, 9):
            ar = math.radians(a + t * 2)
            x, y = 812 + 470 * math.cos(ar), 455 + 470 * math.sin(ar)
            if X0 < x < X1 and Y0 < y < YP: d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=A(mix(col, INK, 0.45), 0.5 * op))
        getattr(sys.modules[__name__], "k_" + kind)(fr, S, t, op, col, at, title_sp, quote_block)
        # caption strip
        d = ImageDraw.Draw(fr, "RGBA")
        d.rectangle([X0, YP, X1, Y1], fill=PAPER); d.line([X0, YP, X1, YP], fill=INK, width=3)
        lab = (sp.get("section") or sp.get("label") or "").upper()
        if len(lab) > 22: lab = lab[:21] + "…"
        hdr = f"FRAME {S['k'] + 1:02d}  ·  " + lab
        d.text((TX, YP + 22), hdr, font=font("mono_r", 16), fill=MUTE)
        # pills
        f = font("mono", 13); x = X1 - 40
        items = list(reversed(pills)) if kind in ("inst", "ladder") else []
        for j, name in enumerate(items):
            idx = len(pills) - 1 - j; s = name.upper(); w = tw(f, s) + 14; x -= w + 6
            on = kind == "inst" and sp["i"] == idx
            if on: d.rectangle([x, YP + 20, x + w, YP + 44], fill=col, outline=INK, width=2)
            d.text((x + 7, YP + 24), s, font=f, fill=CREAM if on else MUTE)
        # caption text: current sentence, or the attribution while a quote is spoken
        fcap = font("serif", CAPF)
        txt = None
        if S["q0"] is not None and t >= S["q0"] - 0.1:
            txt = "— " + sp.get("by", "") if sp.get("by") else None
        else:
            for sent in S["sents"]:
                if sent[0]["s"] - 0.1 <= t: txt = " ".join(w["w"] for w in sent)
        if txt:
            lines = wrap(txt, fcap, X1 - TX - 50)[:CAPN]
            for i, l in enumerate(lines): d.text((TX, YP + 74 + i * CAPL), l, font=fcap, fill=CAP_INK)

    # ---------------- encoder
    out = f"build/video_{slug}_strip_{FMT}.mp4"
    prev = [float(x) for x in os.environ.get("PREVIEW", "").split(",") if x]
    ff = None if prev else subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "28", "-tune", "grain", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    frames = [int(x * FPS) for x in prev] if prev else range(nfr)
    for n, fi in enumerate(frames):
        t = fi / FPS
        fr = Image.new("RGB", (W, H), EDGE)
        body = Image.new("RGB", (W, H), PAPER)
        if t < tm["dur"]:
            for S in sc:
                if S["v0"] <= t < S["v1"]:
                    op = 1.0
                    draw_scene(body, S, t - S["v0"], op)
        else:
            end_card(body, t - tm["dur"], reel)
        fr.paste(body, (0, 0), mask)
        fr.paste(edges, (0, 0), edges)
        a = np.asarray(fr).astype(np.float32)
        g = GRAIN[fi % len(GRAIN)]; g = np.repeat(np.repeat(g, 2, 0), 2, 1)
        flick = 1 + 0.018 * math.sin(fi * 1.7) + 0.012 * math.sin(fi * 0.37)
        a = (a * flick + g) * vig
        a = a * np.array([1.0, 0.97, 0.9], np.float32) + np.array([6, 3, 0], np.float32)   # warm print
        if (fi // 9) % 23 == 0:                                                          # occasional scratch
            xs = int(300 + 400 * abs(math.sin(fi)))
            a[:, xs:xs + 2] = a[:, xs:xs + 2] * 0.6 + 100
        img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        if prev: img.save(f"build/prev_strip_{slug}_{n}.png")
        else: ff.stdin.write(img.tobytes())
    if ff: ff.stdin.close(); ff.wait()
    print(slug, "strip video", round(dur, 1), flush=True)

def end_card(fr, t, reel):
    d = ImageDraw.Draw(fr, "RGBA")
    d.rectangle([X0, Y0, X1, Y1], fill=PAPER)
    e = ease(t / 0.6)
    d.text((TX, 300 - 20 * (1 - e)), "END OF", font=font("black", 64), fill=A(INK, e))
    d.text((TX, 370 - 20 * (1 - e)), f"FILMSTRIP {reel['id']}", font=font("black", 96), fill=A((205, 72, 46), e))
    e2 = ease((t - 0.4) / 0.5)
    d.text((TX, 510), "TOLD WHOLE  ·  SOMETHING WAS WRONG, SEASONS 1–26", font=font("mono", 18), fill=A(INK, e2))
    f = font("serif", 30)
    for i, l in enumerate(wrap("Analysis: Claude (AI) for Endorphin. Narration: Kokoro TTS (AI voice). Show: Something Was Wrong, Tiffany Reese. Survivors keep the show's names; no uncharged person is named.", f, 760)):
        d.text((TX, 580 + i * 40), l, font=f, fill=A(CAP_INK, e2))
    d.text((TX, 860), "Next: the moves themselves.", font=font("serif_i", 36), fill=A(CAP_INK, ease((t - 0.8) / 0.5)))

# ================================================================== frame kinds
def head(fr, S, t, op, title_sp, label=None, y=50):
    d = ImageDraw.Draw(fr, "RGBA")
    y = z(y)
    if label: d.text((TX, y), label, font=font("xbold", z(40)), fill=A(INK, op * ease(t / 0.4)))
    sp = title_sp(S); e = ease((t - 0.1) / 0.5)
    paste(fr, sp, TX - 4, y + z(52) + 20 * (1 - e), op * e)
    return y + z(52) + sp.size[1]

def k_intro(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]; ta = at(S, "across", 6.0); tc = at(S, "about", 9.0); tg = at(S, "two", 15.0)
    if t < ta - 0.2:
        yb = head(fr, S, t, op, title_sp, None, 40)
        d = ImageDraw.Draw(fr, "RGBA")
        d.text((TX, yb + 6), sp["sub"], font=font("xbold", 30), fill=A(CREAM, op * ease((t - 0.5) / 0.4)))
        e = ease((t - 1.2) / 0.5)
        if e > 0:
            card(d, TX - 10, 470, 560, 170, sp["tab"], op * e)
            for i, l in enumerate(wrap(sp["card"], font("med", 31), 520)):
                d.text((TX + 12, 500 + i * 42), l, font=font("med", 31), fill=A(INK, op * e))
        return
    t2 = t - ta
    d = ImageDraw.Draw(fr, "RGBA")
    n, k, cols = 398, 83, 30
    import random
    rng = random.Random(3); idx = list(range(n)); rng.shuffle(idx); keep = set(idx[:k])
    cell = z(26); gx, gy = TX, z(250)
    for i in range(n):
        r, c = divmod(i, cols)
        x, y = gx + c * cell + 13, gy + r * cell + 13
        ein = clamp((t2 - 0.002 * i) / 0.3)
        if ein <= 0: continue
        if i in keep: cc = mix(CREAM, (255, 236, 150), clamp((t - tc - 0.3) / 0.3))
        else:
            kk = clamp((t - tc - 0.8 * (r / 14)) / 0.3); cc = mix(CREAM, mix(col, INK, 0.55), kk)
        rr = z(8)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=A(cc, op * ein))
    e = ease((t - tc - 0.4) / 0.4)
    if e > 0:
        paste(fr, display("1 IN 5", 104), TX - 4, 60, op * e)
        d.text((TX + 360, 108), "PROTECTED · 83 OF 398", font=font("mono", 20), fill=A(CREAM, op * e))
    else:
        d.text((TX, 120), "398 PEOPLE REACHED AN INSTITUTION", font=font("mono", 22), fill=A(CREAM, op * ease(t2 / 0.4)))
    eg = ease((t - tg) / 0.5)
    if eg > 0:
        GY = 590 if FMT != "vertical" else 1150
        card(d, TX - 10, GY, 820, 150, "TWO FAMILIES OF CODERS, WORKING APART", op * eg)
        bw = 520
        for j, (lab, v) in enumerate((("CLAUDE", 0.28), ("CODEX", 0.16))):
            y = GY + 35 + j * 52
            d.text((TX + 10, y), lab, font=font("mono", 20), fill=A(INK, op * eg))
            d.rectangle([TX + 130, y, TX + 130 + bw, y + 28], fill=A((210, 198, 172), op * eg))
            ev = ease((t - tg - 0.4 - 0.2 * j) / 0.8)
            d.rectangle([TX + 130, y, TX + 130 + bw * v * ev, y + 28], fill=A(BLUE, op * eg))
            d.text((TX + 140 + bw, y - 4), f"{int(v * 100 * ev)}%", font=font("black", 30), fill=A(INK, op * eg))
        lx = TX + 130 + bw / 3
        for yy in range(GY + 15, GY + 125, 14): d.line([lx, yy, lx, yy + 7], fill=A((205, 72, 46), op * eg), width=3)
        d.text((lx + 8, GY + 10), "1 IN 3", font=font("mono", 15), fill=A((205, 72, 46), op * eg))

def k_ladder(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]; times = [at(S, k, 0.6 + 0.5 * i) for i, k in enumerate(sp["keys"])]
    n = sum(1 for x in times if t >= x - 0.1)
    yb = head(fr, S, t, op, title_sp, sp["label"])
    d = ImageDraw.Draw(fr, "RGBA")
    from strip_01 import INST
    for i, name in enumerate(INST):
        e = ease((t - times[i] + 0.15) / 0.3)
        if e <= 0: continue
        y = yb + 20 + DY + i * z(56)
        d.rectangle([TX, y, TX + z(40), y + z(40)], fill=A(INK, op * e))
        d.text((TX + z(13), y + 6), str(i + 1), font=font("bold", z(24)), fill=A(CREAM, op * e))
        d.text((TX + z(56), y + 2), name, font=font("xbold", z(34)), fill=A(CREAM, op * e))

def k_inst(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]; q0 = S["q0"] or 99; q1 = S["q1"] or 99
    yb = head(fr, S, t, op, title_sp, sp["label"])
    d = ImageDraw.Draw(fr, "RGBA")
    CWD = X1 - X0 - 90                                   # card width across the stage
    ed = ease((t - 0.6) / 0.5) * (1 - ease((t - q0 + 0.4) / 0.3))
    if ed > 0:
        for i, l in enumerate(wrap(sp["desc"], font("serif_i", z(38)), CWD)):
            d.text((TX + 6, yb + 14 + i * z(46)), l, font=font("serif_i", z(38)), fill=A(CREAM, op * ed * 0.92))
    mid = (yb + 110 + YP) / 2
    ep = ease((t - 1.0) / 0.4) * (1 - ease((t - q0 + 0.2) / 0.3))
    if ep > 0:
        lines = list(sp["pre"]); ta = at(S, sp.get("add_key", "~"), 99)
        adds = [a for j, a in enumerate(sp.get("adds", [])) if t >= ta + 0.5 * j]
        h = 44 + z(50) * (len(lines) + len(sp.get("adds", []))) + (z(78) if sp.get("status") else 0)
        y0 = mid - h / 2
        card(d, TX - 10, y0, CWD, h, sp["pre_tab"], op * ep)
        y = y0 + 28
        if sp.get("status"):
            ts = at(S, sp["snap_key"], 99); ks = clamp((t - ts) / 0.25)
            bw = CWD - 40
            d.rectangle([TX + 6, y, TX + 6 + bw, y + z(32)], fill=A((210, 198, 172), op * ep))
            d.rectangle([TX + 6, y, TX + 6 + bw * (1 - ease(ks)), y + z(32)], fill=A(BLUE if ks < 1 else col, op * ep))
            d.text((TX + 6, y + z(40)), sp["status"][1] if ks > 0.5 else sp["status"][0], font=font("mono", z(20)),
                   fill=A((205, 72, 46) if ks > 0.5 else BLUE, op * ep))
            y += z(78)
        for l in lines:
            d.text((TX + 8, y), l, font=font("med", z(31)), fill=A(INK, op * ep)); y += z(50)
        for l in adds:
            d.rectangle([TX, y - 4, TX + CWD - 30, y + z(40)], fill=A((236, 190, 180), op * ep))
            d.text((TX + 8, y), l, font=font("semi", z(31)), fill=A((170, 40, 30), op * ep)); y += z(50)
    eq = ease((t - q0 + 0.25) / 0.3) * (1 - ease((t - q1 - 0.3) / 0.3))
    if eq > 0:
        f = font("med", z(34)); lh = z(46)
        nlines = len(wrap(S["s"]["quote"], f, CWD - 50))
        h = nlines * lh + 56; y0 = mid - h / 2
        card(d, TX - 10, y0, CWD, h, sp["tab"], op * eq)
        quote_block(fr, S, TX + 12, y0 + 30, CWD - 50, t, op * eq, f, lh)
    if t > q1 + 0.6:
        nb = len(sp["bar"].split("\n"))
        bars(fr, sp["bar"], TX - 10, mid - nb * z(60) / 2, t - q1 - 0.65, op, z(46))

def k_pieces(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]; yb = head(fr, S, t, op, title_sp, sp["label"])
    d = ImageDraw.Draw(fr, "RGBA")
    import random
    rng = random.Random(7); order = list(range(100)); rng.shuffle(order); rank = {j: i for i, j in enumerate(order)}
    vert = FMT == "vertical"
    cell = z(40); gx, gy = (TX, yb + 330) if vert else (560, 300)
    for i in range(100):
        r, c = divmod(i, 10)
        e = ease((t - 0.01 * i) / 0.5)
        lit = rank[i] < 63 and t > 1.2 + 1.5 * rank[i] / 63
        d.rectangle([gx + c * cell + 3, gy + r * cell + 3, gx + (c + 1) * cell - 3, gy + (r + 1) * cell - 3],
                    fill=A(CREAM if lit else mix(col, INK, 0.5), op * e))
    e = ease((t - 2.0) / 0.5)
    ny = yb + 20 if vert else 330
    paste(fr, display("63%", z(130)), TX - 4, ny, op * e)
    tx_ = TX + z(300) if vert else TX
    ty_ = ny + 30 if vert else 500
    for i, l in enumerate(wrap("of single responses looked appropriate, judged one piece at a time", font("serif_i", z(32)), 420 if vert else 380)):
        d.text((tx_, ty_ + i * z(40)), l, font=font("serif_i", z(32)), fill=A(CREAM, op * e))

def chain_steps(fr, S, t, op, col, at, x, y, gap, dim_except=None):
    d = ImageDraw.Draw(fr, "RGBA")
    kc = {"bad": (205, 72, 46), "person": ORANGE, "help": AQUA, "outcome": BLUE}
    steps = S["sp"]["steps"]; n = len(steps)
    shown = [1.0 if s[3] is None else ease((t - at(S, s[3], 1.0 + i)) / 0.4) for i, s in enumerate(steps)]
    last = max([i for i, e in enumerate(shown) if e > 0] or [0])
    d.line([x + 18, y + 18, x + 18, y + 18 + gap * last], fill=A(INK, op), width=4)
    for i, (lab, tag, kind, key) in enumerate(steps):
        e = shown[i]
        if e <= 0: continue
        a = op * e * (0.25 if (dim_except is not None and i != dim_except) else 1)
        yy = y + i * gap
        d.rectangle([x, yy, x + z(36), yy + z(36)], fill=A(kc[kind], a))
        d.text((x + z(52), yy - 2), lab, font=font("semi", z(27)), fill=A(INK, a))
        d.text((x + z(52), yy + z(31)), tag.upper(), font=font("mono", z(15)), fill=A(kc[kind], a))

def k_chain(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]
    yb = head(fr, S, t, op, title_sp, sp["label"])
    d = ImageDraw.Draw(fr, "RGBA")
    n = len(sp["steps"]); gap = z(62); h = gap * n + 24
    y0 = yb + 34 + DY
    if sp["phase"] == 1:
        card(d, TX - 10, y0, 820, h, "ONE STORY, IN ORDER", op)
        chain_steps(fr, S, t, op, col, at, TX + 8, y0 + 26, gap)
        if S["q0"] is not None:
            eq = ease((t - S["q0"] + 0.25) / 0.3)
            if eq > 0:
                yq = y0 + h + 36
                fq = font("med", z(30)); nq = len(wrap(S["s"]["quote"], fq, 790))
                card(d, TX - 10, yq, 820, nq * z(40) + 34, sp["tab"], op * eq)
                quote_block(fr, S, TX + 10, yq + 20, 790, t, op * eq, fq, z(40))
    else:
        tc = at(S, sp["crop_key"], 2.0); tw_ = at(S, sp["whole_key"], 5.0)
        crop = t >= tc and t < tw_
        card(d, TX - 10, y0, 820, h, "ONE STORY, IN ORDER", op)
        chain_steps(fr, S, t, op, col, at, TX + 8, y0 + 26, gap, dim_except=n - 1 if crop else None)
        if crop: bars(fr, sp["crop"], TX - 10, y0 + h + 30, t - tc, op, z(32))
        if t >= tw_: bars(fr, sp["whole"], TX - 10, y0 + h + 30, t - tw_, op, z(32))

def k_coders(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]; yb = head(fr, S, t, op, title_sp, sp["label"])
    d = ImageDraw.Draw(fr, "RGBA"); tf = at(S, "families", 4.0)
    rates = (2, 1)                                    # of 7 stories end protected: Claude 28 %, Codex 16 %
    for j, lab in enumerate((sp["a"], sp["b"])):
        x0 = TX - 10 + j * 420
        e = ease((t - 0.4 - 0.2 * j) / 0.4)
        card(d, x0, yb + 40 + DY, 390, z(350), lab, op * e)
        for s_ in range(7):
            xs = x0 + 40 + s_ * 52
            for k in range(5):
                y = yb + 92 + DY + k * z(60)
                last = k == 4
                sc_ = clamp((t - tf - 0.15 * s_ - 0.2 * j) / 1.4); reached = sc_ * 4 >= k
                c = (180, 168, 150)
                if reached: c = BLUE
                if last and sc_ >= 1: c = BLUE if s_ < rates[j] else (205, 72, 46)
                d.ellipse([xs - 10, y - 10, xs + 10, y + 10], fill=A(c, op * e))
                if k: d.line([xs, y - z(60) + 10, xs, y - 10], fill=A(BLUE if reached else (180, 168, 150), op * e), width=3)
    eg = ease((t - tf - 2.4) / 0.4)
    if eg > 0:
        d.text((TX, yb + z(350) + 70 + DY), "LAST DOT: HOW IT ENDED  ·  BLUE PROTECTED, RED NOT", font=font("mono", 18), fill=A(CREAM, op * eg))
        d.text((TX, yb + z(350) + 100 + DY), "ENDED PROTECTED: CLAUDE 28%  ·  CODEX 16%", font=font("mono", 18), fill=A(CREAM, op * eg))

def k_quote(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]
    yb = head(fr, S, t, op, title_sp, sp["label"])
    d = ImageDraw.Draw(fr, "RGBA")
    if S["q0"] is not None:
        eq = ease((t - S["q0"] + 0.25) / 0.3)
        if eq > 0:
            f = font("med", z(40)); nl = len(wrap(S["s"]["quote"], f, 760))
            card(d, TX - 10, yb + 50 + DY, 820, nl * z(54) + 60, sp["tab"], op * eq)
            quote_block(fr, S, TX + 14, yb + 80 + DY, 760, t, op * eq, f, z(54))

def k_pass(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]; yb = head(fr, S, t, op, title_sp, sp["label"])
    d = ImageDraw.Draw(fr, "RGBA"); tl = at(S, "line", 3.0)
    yb = yb + DY
    card(d, TX - 10, yb + 30, 820, z(390), "THREE PREDICTIONS, EACH WITH ITS LINE", op)
    bw = 470
    vcol = {"HOLDS": BLUE, "SPLIT": ORANGE, "NOT DECIDED": GREY}
    for i, (lab, line, val, vt, verdict, sub) in enumerate(sp["items"]):
        y = yb + 56 + i * z(122)
        tv = at(S, sp["keys"][i], 6.0 + 2 * i)
        for li, ll in enumerate(wrap(lab, font("semi", z(23)), 780)[:2]):
            d.text((TX + 10, y + li * z(28)), ll, font=font("semi", z(23)), fill=A(INK, op))
        yb_ = y + z(36) + (z(28) if FMT == "vertical" and len(wrap(lab, font("semi", z(23)), 780)) > 1 else 0)
        d.rectangle([TX + 10, yb_, TX + 10 + bw, yb_ + 30], fill=A((214, 202, 176), op))
        el = ease((t - tl - 0.2 * i) / 0.4); lx = TX + 10 + bw * line
        for yy in range(yb_ - 12, yb_ + 44, 10): d.line([lx, yy, lx, yy + 5], fill=A((205, 72, 46), op * el), width=3)
        ev = ease((t - tv) / 0.8)
        if ev > 0:
            d.rectangle([TX + 10, yb_, TX + 10 + bw * val * ev, yb_ + 30], fill=A(vcol[verdict], op))
            d.text((TX + 24 + bw, yb_ - 4), vt, font=font("black", 32), fill=A(INK, op * ev))
            d.text((TX + 10, yb_ + 40), sub.upper() + f"   ·   LINE {int(line * 100)}%", font=font("mono", 14), fill=A(MUTE, op * ev))
        eb = ease((t - tv - 0.8) / 0.25)
        if eb > 0:
            f = font("black", 24); w = tw(f, verdict) + 24; x = TX + 790 - w
            d.rectangle([x, yb_ - 6, x + w, yb_ + 34], fill=A(vcol[verdict], op * eb), outline=A(INK, op * eb), width=2)
            d.text((x + 12, yb_ - 2), verdict, font=f, fill=A(CREAM, op * eb))

def k_close(fr, S, t, op, col, at, title_sp, quote_block):
    sp = S["sp"]; yb = head(fr, S, t, op, title_sp, sp["label"])
    from strip_01 import INST, RED, BLUE as B2, PURPLE, MUSTARD, GREEN, TEAL, ORANGE as O2
    cols = [B2, RED, PURPLE, MUSTARD, GREEN, TEAL, O2]
    d = ImageDraw.Draw(fr, "RGBA"); f = font("xbold", z(34))
    for i, (name, c) in enumerate(zip(INST, cols)):
        e = ease((t - 0.6 - 0.15 * i) / 0.3)
        if e <= 0: continue
        y = yb + 50 + DY + i * z(64)
        d.rectangle([TX, y, TX + z(60) + tw(f, name) + 30, y + z(50)], fill=A(c, op * e), outline=A(INK, op * e), width=3)
        d.text((TX + 14, y + 6), str(i + 1), font=f, fill=A(CREAM, op * e))
        d.text((TX + z(60), y + 6), name, font=f, fill=A(CREAM, op * e))

if __name__ == "__main__":
    main(sys.argv[1])

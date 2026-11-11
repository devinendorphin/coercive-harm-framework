"""Render one reel: python render.py <id>  ->  out/<id>.mp4 (1080x1920, 30 fps)."""
import json, math, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from content import REELS, SERIES, SUB, STAGES

W, H, FPS = 1080, 1920, 30
X0, CW = 72, 864                 # content column (keeps clear of Instagram's right-hand icons)
CARD_CY = 800                    # vertical centre of the card band (≈ 380–1220)
END = 2.6                        # end card after narration
BG = (12, 10, 16)
FG = (243, 238, 232)
MUTED = (154, 147, 160)
DIM = (82, 76, 90)

FD = "/usr/share/fonts/opentype/inter/"
F = {k: FD + v for k, v in {
    "black": "InterDisplay-Black.otf", "xbold": "InterDisplay-ExtraBold.otf", "bold": "InterDisplay-Bold.otf",
    "semi": "Inter-SemiBold.otf", "med": "Inter-Medium.otf", "quote": "InterDisplay-SemiBoldItalic.otf",
    "cap": "Inter-Bold.otf"}.items()}
SYM = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fc = {}
def font(k, size):
    key = (k, int(size))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(F.get(k, k), int(size))
    return _fc[key]

def hexrgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
def ease(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3
def clamp01(x): return min(1.0, max(0.0, x))

def tw(f, s): return f.getlength(s)

def wrap(text, f, width):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            cand = (line + " " + w).strip()
            if tw(f, cand) <= width or not line:
                line = cand
            else:
                out.append(line); line = w
        out.append(line)
    return out

def fit(text, k, maxsize, width, minsize=40):
    s = maxsize
    while s > minsize and max(tw(font(k, s), l) for l in text.split("\n")) > width:
        s -= 4
    return s

def sprite(lines, f, fill, lh=1.12, tracking=0):
    asc, desc = f.getmetrics()
    step = int(f.size * lh)
    wmax = int(max(tw(f, l) + tracking * len(l) for l in lines)) + 8
    im = Image.new("RGBA", (wmax, step * (len(lines) - 1) + asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        if tracking:
            x = 0
            for ch in l:
                d.text((x, i * step), ch, font=f, fill=fill); x += tw(f, ch) + tracking
        else:
            d.text((0, i * step), l, font=f, fill=fill)
    return im

def paste(frame, sp, x, y, op=1.0, scale=1.0):
    if op <= 0.003: return
    if scale != 1.0:
        w0, h0 = sp.size
        sp = sp.resize((max(1, int(w0 * scale)), max(1, int(h0 * scale))), Image.BILINEAR)
        x += (w0 - sp.size[0]) / 2; y += (h0 - sp.size[1]) / 2
    a = sp.getchannel("A")
    if op < 0.997: a = a.point(lambda v: int(v * op))
    frame.paste(sp.convert("RGB"), (int(x), int(y)), a)

# ---------------------------------------------------------------- cards
class Card:
    """Pre-renders sprites for one scene; draw(frame, t_local, dur, op) animates them."""
    def __init__(self, c, acc, words):
        self.c, self.acc, self.k = c, acc, c["t"]
        getattr(self, "init_" + self.k)()

    def stack(self, parts, gap):
        h = sum(p.size[1] for p in parts) + gap * (len(parts) - 1)
        y = CARD_CY - h / 2; ys = []
        for p in parts: ys.append(y); y += p.size[1] + gap
        return ys

    # title
    def init_title(self):
        c = self.c
        s = fit(c["big"], "black", 150, CW)
        self.lines = [sprite([l], font("black", s), FG, 1.0) for l in c["big"].split("\n")]
        self.small = sprite(wrap(c["small"].upper(), font("cap", 30), CW), font("cap", 30), self.acc, 1.3, 3)
        ys = self.stack(self.lines + [self.small], 14)
        self.ys, self.sy = ys[:-1], ys[-1] + 26
    def draw_title(self, fr, t, dur, op):
        for i, (sp, y) in enumerate(zip(self.lines, self.ys)):
            e = ease((t - 0.1 * i) / 0.55)
            paste(fr, sp, X0, y + 60 * (1 - e), op * e)
        e = ease((t - 0.1 * len(self.lines) - 0.15) / 0.5)
        paste(fr, self.small, X0, self.sy + 20 * (1 - e), op * e)

    # head
    def init_head(self):
        c = self.c
        s = fit(c["head"], "xbold", 96, CW - 40, 52)
        f = font("xbold", s)
        self.head = sprite(wrap(c["head"], f, CW - 40), f, FG, 1.08)
        fb = font("med", 44)
        self.body = sprite(wrap(c["body"], fb, CW - 40), fb, MUTED, 1.3)
        self.hy, self.by = self.stack([self.head, self.body], 36)
    def draw_head(self, fr, t, dur, op):
        d = ImageDraw.Draw(fr)
        e = ease(t / 0.5)
        bh = (self.by + self.body.size[1] - self.hy) * e
        if op > 0.01:
            d.rectangle([X0, self.hy + 8, X0 + 9, self.hy + 8 + bh], fill=mix(BG, self.acc, op))
        paste(fr, self.head, X0 + 40, self.hy + 50 * (1 - e), op * e)
        e2 = ease((t - 0.35) / 0.5)
        paste(fr, self.body, X0 + 40, self.by + 30 * (1 - e2), op * e2)

    # quote
    def init_quote(self):
        c = self.c
        q = "“" + c["q"].strip("“”") + "”"
        s = 76 if len(q) < 60 else 64 if len(q) < 100 else 56
        f = font("quote", s)
        self.qwords = [w for w in q.split(" ")]
        self.qlines = wrap(q, f, CW - 20)
        self.qf, self.lh = f, int(s * 1.22)
        self.mark = sprite(["“"], font("black", 240), self.acc, 1.0)
        self.by_ = sprite(["— " + c["by"].upper()], font("cap", 30), self.acc, 1.2, 2)
        qh = self.lh * len(self.qlines)
        top = CARD_CY - (qh + 60 + self.by_.size[1]) / 2
        self.qy, self.byy = top, top + qh + 50
    def draw_quote(self, fr, t, dur, op):
        e = ease(t / 0.5)
        paste(fr, self.mark, X0 - 10, self.qy - 190 + 30 * (1 - e), op * e * 0.9)
        d = ImageDraw.Draw(fr)
        total = sum(len(l.split(" ")) for l in self.qlines)
        reveal = min(dur * 0.55, 0.12 * total + 0.4)
        k = 0
        for i, l in enumerate(self.qlines):
            x = X0
            for w in l.split(" "):
                a = clamp01((t - 0.2 - reveal * k / max(1, total)) / 0.3) * op
                if a > 0:
                    d.text((x, self.qy + i * self.lh), w, font=self.qf, fill=mix(BG, FG, a))
                x += tw(self.qf, w + " "); k += 1
        e2 = ease((t - 0.3 - reveal) / 0.5)
        paste(fr, self.by_, X0, self.byy + 20 * (1 - e2), op * e2)

    # stat
    def init_stat(self):
        c = self.c
        self.num = c["num"]
        self.ns = fit(self.num, "black", 260, CW, 120)
        fl = font("semi", 48)
        self.label = sprite(wrap(c["label"], fl, CW - 40), fl, MUTED, 1.25)
        nh = int(self.ns * 1.05)
        top = CARD_CY - (nh + 30 + self.label.size[1]) / 2
        self.ny, self.ly = top - self.ns * 0.12, top + nh + 30
        m = re.findall(r"\d+", self.num)
        self.count = int(m[0]) if len(m) == 1 and int(m[0]) > 1 else None
    def draw_stat(self, fr, t, dur, op):
        e = ease(t / 0.6)
        s = self.num
        if self.count:
            v = int(round(self.count * ease(t / 1.1)))
            s = re.sub(r"\d+", f"{v:,}" if self.count >= 1000 else str(v), self.num, count=1)
        f = font("black", self.ns)
        d = ImageDraw.Draw(fr)
        d.text((X0, self.ny + 40 * (1 - e)), s, font=f, fill=mix(BG, self.acc, op * e))
        e2 = ease((t - 0.3) / 0.5)
        paste(fr, self.label, X0, self.ly + 30 * (1 - e2), op * e2)

    # list
    def init_list(self):
        c = self.c
        fh = font("xbold", 66)
        self.head = sprite(wrap(c["head"], fh, CW), fh, FG, 1.08)
        fi = font("semi", 48)
        self.items = [sprite(wrap(it, fi, CW - 70), fi, FG, 1.2) for it in c["items"]]
        ys = self.stack([self.head] + self.items, 40)
        self.hy, self.iys = ys[0], ys[1:]
        self.iys = [y + 20 for y in self.iys]
    def draw_list(self, fr, t, dur, op):
        e = ease(t / 0.5)
        paste(fr, self.head, X0, self.hy + 40 * (1 - e), op * e)
        d = ImageDraw.Draw(fr)
        n = len(self.items)
        span = max(0.6, dur * 0.75)
        for i, (sp, y) in enumerate(zip(self.items, self.iys)):
            ti = 0.35 + span * i / n
            e2 = ease((t - ti) / 0.45)
            if e2 <= 0: continue
            x = X0 + 70 - 40 * (1 - e2)
            col = mix(BG, self.acc, op * e2)
            d.rounded_rectangle([X0 + 4, y + 18, X0 + 30, y + 44], 6, fill=col)
            paste(fr, sp, x, y, op * e2)

    # cycle ring
    def init_cycle(self):
        self.cx, self.cy, self.r, self.nr = X0 + CW // 2, CARD_CY - 10, 268, 86
        self.lab = sprite([self.c["label"].upper()], font("cap", 30), self.acc, 1.2, 2)
        self.nodes = []
        for i, (stage, m) in enumerate(zip(STAGES, self.c["marks"])):
            self.nodes.append(self.node(stage, m))
        fl = font(SYM, 22)
        self.legend = sprite(["✓ present   ~ partial   ✕ absent   n/o not observable   n/d not described"], fl, MUTED, 1.2)
    def node(self, stage, m):
        acc, s = self.acc, self.nr * 2 + 40
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        c0, c1 = 20, 20 + self.nr * 2
        if m == "y":
            d.ellipse([c0, c0, c1, c1], fill=acc); tc = BG
        elif m == "p":
            d.ellipse([c0, c0, c1, c1], fill=mix(BG, acc, 0.28), outline=acc, width=5); tc = FG
        elif m == "n":
            d.ellipse([c0, c0, c1, c1], fill=(38, 34, 44), outline=DIM, width=3); tc = DIM
        else:
            for a in range(0, 360, 20):
                d.arc([c0, c0, c1, c1], a, a + 11, fill=MUTED, width=4)
            tc = MUTED
        f = font("cap", 25 if "\n" in stage else 26)
        lines = stage.split("\n"); lh = 30
        y = s / 2 - lh * len(lines) / 2
        for l in lines:
            d.text((s / 2 - tw(f, l) / 2, y), l, font=f, fill=tc); y += lh
        badge = {"y": "✓", "p": "~", "n": "✕", "o": "n/o", "d": "n/d"}[m]
        bf = font(SYM, 26 if len(badge) == 1 else 19)
        bx, by_ = s - 44, 4
        d.ellipse([bx - 4, by_, bx + 40, by_ + 44], fill=FG if m in "yp" else (60, 55, 66))
        d.text((bx + 18 - tw(bf, badge) / 2, by_ + 22 - bf.size * 0.62), badge, font=bf, fill=BG if m in "yp" else FG)
        return im
    def draw_cycle(self, fr, t, dur, op):
        d = ImageDraw.Draw(fr)
        cx, cy, r = self.cx, self.cy, self.r
        stepT = min(0.42, dur * 0.6 / 6)
        p = clamp01((t - 0.15) / (stepT * 6 + 0.2))
        col = mix(BG, mix(DIM, self.acc, 0.55), op)
        if p > 0:
            d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * ease(p), fill=col, width=6)
        for i in range(6):                                     # chevrons between nodes
            a = math.radians(-90 + 60 * i + 30)
            if ease(p) * 360 < 60 * i + 34: continue
            px, py = cx + r * math.cos(a), cy + r * math.sin(a)
            tx, ty = -math.sin(a), math.cos(a)
            nx, ny = math.cos(a), math.sin(a)
            pts = [(px + tx * 14, py + ty * 14), (px - tx * 10 + nx * 14, py - ty * 10 + ny * 14), (px - tx * 10 - nx * 14, py - ty * 10 - ny * 14)]
            d.polygon(pts, fill=col)
        for i, sp in enumerate(self.nodes):
            a = math.radians(-90 + 60 * i)
            e = ease((t - 0.15 - stepT * i) / 0.4)
            if e <= 0: continue
            x = cx + r * math.cos(a) - sp.size[0] / 2
            y = cy + r * math.sin(a) - sp.size[1] / 2
            paste(fr, sp, x, y, op * e, 0.6 + 0.4 * e)
        e = ease((t - 0.2) / 0.5)
        paste(fr, self.lab, cx - self.lab.size[0] / 2, cy - self.lab.size[1] / 2 + 20 * (1 - e), op * e)
        e = ease((t - 0.15 - stepT * 6) / 0.5)
        paste(fr, self.legend, cx - self.legend.size[0] / 2, cy + r + self.nr + 26, op * e)

    # bars
    def init_bars(self):
        c = self.c
        fh = font("xbold", 60)
        self.head = sprite(wrap(c["head"], fh, CW), fh, FG, 1.08)
        self.rows = c["rows"]; self.ref = c["ref"]; self.pct = c.get("pct", False)
        self.lf = font("semi", 40); self.vf = font("black", 50)
        self.rowh = 132
        total = self.head.size[1] + 50 + self.rowh * len(self.rows)
        self.hy = CARD_CY - total / 2
        self.ry = self.hy + self.head.size[1] + 50
    def draw_bars(self, fr, t, dur, op):
        e = ease(t / 0.5)
        paste(fr, self.head, X0, self.hy + 40 * (1 - e), op * e)
        d = ImageDraw.Draw(fr)
        maxw = CW - 170
        for i, row in enumerate(self.rows):
            label, v = row[0], row[1]
            barcol = (96, 90, 104) if row[2:] == ["ref"] else self.acc
            y = self.ry + i * self.rowh
            ei = ease((t - 0.3 - 0.25 * i) / 0.9)
            if ei <= 0: continue
            d.text((X0, y), label, font=self.lf, fill=mix(BG, FG, op * min(1, ei * 2)))
            bw = maxw * (v / self.ref) * ei
            d.rounded_rectangle([X0, y + 54, X0 + max(12, bw), y + 98], 8, fill=mix(BG, barcol, op))
            val = v * ei
            s = (f"{val:.0f}%" if self.pct else (f"{val:.1f}×" if isinstance(v, float) else f"{val:.0f}"))
            d.text((X0 + max(12, bw) + 18, y + 46), s, font=self.vf, fill=mix(BG, FG, op))

    def draw(self, fr, t, dur, op):
        getattr(self, "draw_" + self.k)(fr, t, dur, op)

# ---------------------------------------------------------------- captions
CAPF = None
def cap_pages(words):
    f = font("cap", 50)
    pages, cur, line, lines = [], [], [], 0
    for w in words:
        test = " ".join(x["w"] for x in line + [w])
        if tw(f, test) > CW - 10 and line:
            lines += 1; line = []
            if lines == 2:
                pages.append(cur); cur, lines = [], 0
        line.append(w); cur.append((lines, w))
        if w["w"][-1:] in ".?!:" and lines == 1 and len(cur) > 3:
            pages.append(cur); cur, line, lines = [], [], 0
    if cur: pages.append(cur)
    return pages

def draw_caps(fr, pages, t, acc):
    f = font("cap", 50)
    page = None
    for pg in pages:
        if pg[0][1]["s"] - 0.05 <= t: page = pg
    if page is None or t > page[-1][1]["e"] + 0.6: return
    d = ImageDraw.Draw(fr)
    y0, lh = 1296, 66
    xs = {0: X0, 1: X0}
    for ln, w in page:
        txt = w["w"]
        if t >= w["e"]: col = FG
        elif t >= w["s"] - 0.03: col = acc
        else: col = (110, 104, 116)
        x, y = xs[ln], y0 + ln * lh
        d.text((x + 3, y + 3), txt, font=f, fill=(0, 0, 0))
        d.text((x, y), txt, font=f, fill=col)
        xs[ln] = x + tw(f, txt + " ")

# ---------------------------------------------------------------- background
def make_bg(acc, seed):
    rng = np.random.default_rng(seed)
    lw, lh = 108, 192
    yy, xx = np.mgrid[0:lh, 0:lw].astype(np.float32)
    ph = rng.uniform(0, 6.28, 6)
    deep = np.array([40, 34, 90], np.float32)
    accv = np.array(acc, np.float32)
    base = np.array(BG, np.float32)
    def bg(t):
        img = np.broadcast_to(base, (lh, lw, 3)).copy()
        for k, (col, amp) in enumerate(((accv, 0.20), (deep, 0.55), (accv, 0.10))):
            cx = lw * (0.5 + 0.38 * math.sin(0.07 * t + ph[k]))
            cy = lh * (0.35 + 0.3 * k + 0.12 * math.sin(0.05 * t + ph[k + 3]))
            rad = 46 + 10 * math.sin(0.1 * t + k)
            g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * rad ** 2))[..., None]
            img += g * (col - base) * amp
        return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    return bg

# ---------------------------------------------------------------- main
def main(slug):
    ri = [r["slug"] for r in REELS].index(slug)
    reel = REELS[ri]
    rid = reel["id"]
    acc = hexrgb(reel["accent"])
    tm = json.load(open(f"build/timing_{slug}.json"))
    dur = tm["dur"] + END
    nfr = int(dur * FPS)
    scenes = []
    for sc, ti in zip(reel["scenes"], tm["scenes"]):
        scenes.append({"card": Card(sc["card"], acc, ti["words"]), "s": ti["start"], "e": ti["end"], "pages": cap_pages(ti["words"])})
    for i, s in enumerate(scenes):
        s["vis_end"] = scenes[i + 1]["s"] - 0.05 if i + 1 < len(scenes) else tm["dur"] - 0.1
        s["vis_start"] = s["s"] - 0.15

    bg = make_bg(acc, ri)
    hdr_l = sprite([SERIES], font("cap", 28), FG, 1.2, 4)
    hdr_r = sprite([f"{ri + 1:02d}"], font("cap", 28), MUTED, 1.2, 2)
    kf = font("cap", 30)
    ktxt = reel["kicker"]
    kw = tw(kf, ktxt) + 3 * len(ktxt) + 44
    kick = Image.new("RGBA", (int(kw), 62), (0, 0, 0, 0)); kd = ImageDraw.Draw(kick)
    kd.rounded_rectangle([0, 0, kw - 1, 61], 31, outline=acc, width=3)
    x = 22
    for ch in ktxt: kd.text((x, 13), ch, font=kf, fill=acc); x += tw(kf, ch) + 3
    foot = sprite(["Survivors' accounts and the public record · each piece says which"], font("med", 26), MUTED, 1.2)
    # end card
    nxt = REELS[ri + 1]["kicker"].title() if ri + 1 < len(REELS) else None
    end_big = sprite(SERIES.split(" · "), font("black", 120), FG, 1.02, 2)
    end_sub = sprite(wrap(SUB, font("semi", 40), CW), font("semi", 40), MUTED, 1.25)
    end_nxt = sprite((["NEXT · " + nxt.upper()] if nxt else ["HOTLINE (US) · 1-800-799-7233", "OR TEXT START TO 88788"]), font("cap", 32), acc, 1.2, 3)
    end_cr = sprite(wrap("Analysis: Claude (AI) for Endorphin · narration: Kokoro TTS (AI voice) · show: Something Was Wrong, Tiffany Reese", font("med", 25), CW), font("med", 25), DIM, 1.3)

    import os
    prev = [float(x) for x in os.environ.get("PREVIEW", "").split(",") if x]
    if prev:
        class _S:
            def __init__(s): s.stdin = s; s.i = 0
            def write(s, b): Image.frombytes("RGB", (W, H), b).save(f"build/prev_{slug}_{s.i}.png"); s.i += 1
            def close(s): pass
            def wait(s): pass
        ff = _S()
    else:
      ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-vf", "noise=alls=7:allf=t+u,vignette=PI/6", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                           "-pix_fmt", "yuv420p", f"build/video_{slug}.mp4"], stdin=subprocess.PIPE)
    for fi in (range(nfr) if not prev else [int(x * FPS) for x in prev]):
        t = fi / FPS
        fr = bg(t)
        d = ImageDraw.Draw(fr)
        # header
        d.rectangle([X0, 150, X0 + CW, 155], fill=(50, 46, 56))
        d.rectangle([X0, 150, X0 + CW * min(1, t / tm["dur"]), 155], fill=acc)
        paste(fr, hdr_l, X0, 178); paste(fr, hdr_r, X0 + CW - hdr_r.size[0], 178)
        ek = ease(t / 0.6)
        paste(fr, kick, X0, 240 + 20 * (1 - ek), ek)
        if t < tm["dur"]:
            for s in scenes:
                if s["vis_start"] <= t <= s["vis_end"]:
                    op = clamp01((s["vis_end"] - t) / 0.25)
                    s["card"].draw(fr, t - s["vis_start"], s["vis_end"] - s["vis_start"], op)
                    draw_caps(fr, s["pages"], t, acc)
            paste(fr, foot, X0, 1520, 0.9)
        else:
            te = t - tm["dur"]
            e = ease(te / 0.6)
            paste(fr, end_big, X0, 560 + 50 * (1 - e), e)
            e2 = ease((te - 0.25) / 0.5)
            paste(fr, end_sub, X0, 560 + end_big.size[1] + 40, e2)
            paste(fr, end_nxt, X0, 560 + end_big.size[1] + 70 + end_sub.size[1], ease((te - 0.5) / 0.5))
            paste(fr, end_cr, X0, 1380, ease((te - 0.6) / 0.5))
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()
    print(slug, "video", round(dur, 1), flush=True)

if __name__ == "__main__":
    main(sys.argv[1])

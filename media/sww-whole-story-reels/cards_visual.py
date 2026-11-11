"""Visual card types for the Told Whole reels (2026-11-11): shapes and motion instead of bare numbers.

Installed onto render.Card by install(). Data colours were checked with the dataviz validator on the
reel surface #0c0a10 (dark): protected #3987e5, partly #199e70, person/network #d95926 all pass
lightness, chroma, CVD separation, normal-vision floor and contrast. Every colour is also named in
text on screen, so identity never rests on colour alone. The red accent is chrome, never data.
"""
import math, random
from PIL import Image, ImageDraw

BLUE, AQUA, ORANGE = (57, 135, 229), (25, 158, 112), (217, 89, 38)
GREY, GREY2 = (64, 58, 74), (96, 90, 106)


def install(Card, G):
    font, sprite, paste, wrap, ease, clamp01, mix, tw = (G[k] for k in
        ("font", "sprite", "paste", "wrap", "ease", "clamp01", "mix", "tw"))
    X0, CW, CARD_CY, FG, MUTED, BG = (G[k] for k in ("X0", "CW", "CARD_CY", "FG", "MUTED", "BG"))

    def pop(t, d=0.35):            # 0 -> overshoot -> 1
        x = clamp01(t / d)
        return 0 if x <= 0 else 1 + 0.18 * math.sin(math.pi * x) * (1 - x) * 3 if x < 1 else 1

    def rr(d, box, r, **kw): d.rounded_rectangle([int(v) for v in box], int(r), **kw)

    def A(col, a):                 # colour with real transparency (drawn on an overlay, not blended to a flat colour)
        return tuple(col[:3]) + (int(255 * clamp01(a)),)

    def layered(fn):               # shapes go on a transparent overlay; text is pasted after, on top
        def w(self, fr, t, dur, op):
            ov = Image.new("RGBA", fr.size, (0, 0, 0, 0)); self._d = ImageDraw.Draw(ov); P = []
            self._pp = lambda *a, **k: P.append((a, k))
            fn(self, fr, t, dur, op)
            fr.paste(ov, (0, 0), ov)
            for a, k in P: paste(fr, *a, **k)
        return w

    # ---------------------------------------------------------------- tiles: n numbered tiles pop in
    def init_tiles(self):
        c = self.c; self.n, self.cols = c["n"], c.get("cols", 6)
        self.cell = CW / self.cols; rows = math.ceil(self.n / self.cols)
        self.top = CARD_CY - rows * self.cell / 2 - 40
        self.lab = sprite(wrap(c["label"].upper(), font("cap", 32), CW), font("cap", 32), self.acc, 1.3, 3)
        self.nums = [sprite([str(i + 1)], font("xbold", 46), FG, 1.0) for i in range(self.n)]
        self.ly = self.top + rows * self.cell + 30
    def draw_tiles(self, fr, t, dur, op):
        d = self._d; s = self.cell - 16
        for i in range(self.n):
            k = pop(t - 0.05 * i)
            if k <= 0: continue
            r, cc = divmod(i, self.cols)
            cx, cy = X0 + cc * self.cell + self.cell / 2, self.top + r * self.cell + self.cell / 2
            h = s * k / 2
            col = A((62, 56, 72), op)
            rr(d, [cx - h, cy - h, cx + h, cy + h], 14 * k, fill=col)
            sp = self.nums[i]
            if k > 0.6: self._pp(sp, cx - sp.size[0] / 2, cy - sp.size[1] / 2 - 4, op * clamp01((k - 0.6) / 0.4))
        e = ease((t - 0.05 * self.n - 0.2) / 0.5)
        self._pp(self.lab, X0, self.ly + 20 * (1 - e), op * e)

    # ---------------------------------------------------------------- chips: words as pills, staggered
    def init_chips(self):
        c = self.c
        self.head = sprite(wrap(c["head"], font("xbold", 72), CW), font("xbold", 72), FG, 1.08)
        f = font("semi", 44); self.chips = []; x = 0; y = 0
        for it in c["items"]:
            sp = sprite([it], f, FG, 1.0); w = sp.size[0] + 64
            if x + w > CW: x = 0; y += 112
            self.chips.append((sp, x, y, w)); x += w + 18
        h = self.head.size[1] + 60 + y + 96
        self.hy = CARD_CY - h / 2; self.cy = self.hy + self.head.size[1] + 60
    def draw_chips(self, fr, t, dur, op):
        e = ease(t / 0.5); self._pp(self.head, X0, self.hy + 40 * (1 - e), op * e)
        d = self._d; n = len(self.chips)
        for i, (sp, x, y, w) in enumerate(self.chips):
            k = pop(t - 0.4 - i * min(0.5, dur * 0.6 / n))
            if k <= 0: continue
            cx, cy = X0 + x + w / 2, self.cy + y + 48
            hw, hh = w / 2 * k, 48 * k
            rr(d, [cx - hw, cy - hh, cx + hw, cy + hh], 48 * k, fill=A((34, 30, 42), op), outline=A(self.acc, op), width=3)
            if k > 0.7: self._pp(sp, cx - sp.size[0] / 2, cy - sp.size[1] / 2 - 4, op)

    # ---------------------------------------------------------------- pieces: a story cut into squares
    def init_pieces(self):
        c = self.c; self.n, self.kk, self.cols = c["n"], c["k"], c.get("cols", 10)
        self.num = sprite([c["num"]], font("black", 170), BLUE, 1.0)
        self.lab = sprite(wrap(c["label"], font("semi", 40), CW), font("semi", 40), MUTED, 1.25)
        self.cell = 62; rows = math.ceil(self.n / self.cols)
        self.gx = X0 + (CW - self.cols * self.cell) / 2
        self.top = CARD_CY - (rows * self.cell + 330) / 2 + 330
        rng = random.Random(7); self.jit = [(rng.uniform(-60, 60), rng.uniform(-90, 40)) for _ in range(self.n)]
        self.order = list(range(self.n)); rng.shuffle(self.order); self.rank = {j: i for i, j in enumerate(self.order)}
    def draw_pieces(self, fr, t, dur, op):
        d = self._d
        for i in range(self.n):
            r, cc = divmod(i, self.cols)
            e = ease((t - 0.008 * i) / 0.6)
            jx, jy = self.jit[i]
            x = self.gx + cc * self.cell + jx * (1 - e); y = self.top + r * self.cell + jy * (1 - e)
            lit = self.rank[i] < self.kk and t > 1.0 + 1.6 * self.rank[i] / self.kk
            col = BLUE if lit else GREY
            rr(d, [x + 4, y + 4, x + self.cell - 4, y + self.cell - 4], 8, fill=A(col, op * e))
        e2 = ease((t - 0.9) / 0.5)
        y0 = self.top - 330
        self._pp(self.num, X0, y0 + 20 * (1 - e2), op * e2)
        self._pp(self.lab, X0, y0 + self.num.size[1] + 10, op * e2)

    # ---------------------------------------------------------------- timeline: one life, top to bottom
    def init_timeline(self):
        c = self.c; self.nodes = c["nodes"]; n = len(self.nodes)
        self.gap = min(170, 760 / max(1, n - 1)); self.top = CARD_CY - self.gap * (n - 1) / 2
        f, ft = font("semi", 44), font("cap", 26)
        self.lab = [sprite(wrap(nd["label"], f, CW - 120), f, FG, 1.15) for nd in self.nodes]
        self.tag = [sprite(wrap(nd["tag"].upper(), ft, CW - 120), ft, BLUE if nd.get("state") == "good" else MUTED, 1.2, 2)
                    if nd.get("tag") else None for nd in self.nodes]
    def draw_timeline(self, fr, t, dur, op):
        d = self._d; n = len(self.nodes); span = max(1.0, dur * 0.45); x = X0 + 26
        prog = clamp01(t / span) * (n - 1)
        y1 = self.top + self.gap * prog
        d.line([x, self.top, x, y1], fill=A(GREY2, op), width=6)
        for i, nd in enumerate(self.nodes):
            k = pop(t - span * i / max(1, n - 1))
            if k <= 0: continue
            y = self.top + self.gap * i; st = nd.get("state", "n"); r = 20 * k
            if st == "good": d.ellipse([x - r, y - r, x + r, y + r], fill=A(BLUE, op))
            elif st == "bad": d.ellipse([x - r, y - r, x + r, y + r], fill=A(GREY2, op)); d.line([x - r * .7, y - r * .7, x + r * .7, y + r * .7], fill=A(BG, op), width=5)
            elif st == "end":
                rr(d, [x - r, y - r, x + r, y + r], 6, fill=A(FG, op))
            else: d.ellipse([x - r, y - r, x + r, y + r], outline=A(FG, op), width=5, fill=A(BG, op))
            sp = self.lab[i]; a = op * clamp01(k)
            self._pp(sp, x + 50, y - 30, a)
            if self.tag[i] is not None:
                self._pp(self.tag[i], x + 50, y - 30 + sp.size[1] + 2, a * clamp01((t - span * i / max(1, n - 1) - 0.3) / 0.4))

    # ---------------------------------------------------------------- readers: two coders working apart
    def init_readers(self):
        c = self.c; f = font("cap", 30)
        self.la = sprite([c["a"].upper()], f, self.acc, 1.2, 3); self.lb = sprite([c["b"].upper()], f, self.acc, 1.2, 3)
        self.note = sprite(wrap(c["note"], font("semi", 42), CW), font("semi", 42), MUTED, 1.25)
        rng = random.Random(3); self.wa = [rng.uniform(0.45, 1.0) for _ in range(60)]; self.wb = [rng.uniform(0.45, 1.0) for _ in range(60)]
    def draw_readers(self, fr, t, dur, op):
        d = self._d; colw = (CW - 60) / 2; top, h = CARD_CY - 330, 600
        e = ease(t / 0.5)
        for j, (lab, ws, x0, speed) in enumerate(((self.la, self.wa, X0, 46), (self.lb, self.wb, X0 + colw + 60, 39))):
            self._pp(lab, x0, top - 60, op * e)
            off = (t * speed) % 34
            for i, w in enumerate(ws):
                y = top + i * 34 - off - (t * speed // 34 % 30) * 0
                y = top + ((i * 34 - t * speed) % (len(ws) * 34))
                if y < top or y > top + h - 20: continue
                fade = min(1, (y - top) / 80, (top + h - 20 - y) / 80)
                cur = abs(y - (top + h * 0.55)) < 17
                rr(d, [x0, y, x0 + colw * w, y + 16], 8, fill=A(self.acc if cur else GREY, op * e * clamp01(fade)))
        mx = X0 + colw + 30
        for yy in range(int(top), int(top + h), 28):
            d.line([mx, yy, mx, yy + 14], fill=A(GREY2, op * e), width=3)
        e2 = ease((t - 0.6) / 0.5); self._pp(self.note, X0, top + h + 40, op * e2)

    # ---------------------------------------------------------------- gauges: predictions as lines to cross
    def init_gauges(self):
        c = self.c; self.items = c["items"]
        self.head = sprite(wrap(c["head"], font("xbold", 64), CW), font("xbold", 64), FG, 1.08)
        f = font("semi", 38)
        self.labs = [sprite(wrap(it["label"], f, CW), f, FG, 1.2) for it in self.items]
        self.ticks = [sprite([it["line"]], font("cap", 28), MUTED, 1.2, 2) for it in self.items]
        self.rowh = [sp.size[1] + 120 for sp in self.labs]
        h = self.head.size[1] + 50 + sum(self.rowh); self.top = CARD_CY - h / 2
    def draw_gauges(self, fr, t, dur, op):
        d = self._d; e = ease(t / 0.5)
        self._pp(self.head, X0, self.top + 30 * (1 - e), op * e)
        y = self.top + self.head.size[1] + 50; n = len(self.items)
        for i, it in enumerate(self.items):
            k = ease((t - 0.5 - i * dur * 0.75 / n) / 0.6)
            sp = self.labs[i]; self._pp(sp, X0, y, op * k)
            by = y + sp.size[1] + 22
            rr(d, [X0, by, X0 + CW, by + 26], 13, fill=A((34, 30, 42), op * k))
            v = it["value"]; tx = X0 + CW * v
            side = it["side"]               # "below" or "above": where the prediction says the result lands
            a0, a1 = (X0, tx) if side == "below" else (tx, X0 + CW)
            w = (a1 - a0) * k
            if w > 2: rr(d, [a0, by, a0 + w, by + 26], 13, fill=A(A(self.acc, 0.45), op))
            d.line([tx, by - 14, tx, by + 40], fill=A(FG, op * k), width=5)
            tk = self.ticks[i]; self._pp(tk, min(tx - tk.size[0] / 2, X0 + CW - tk.size[0]), by + 46, op * k)
            y += self.rowh[i]

    # ---------------------------------------------------------------- eyes: one family saw, one was blind
    def init_eyes(self):
        c = self.c; f, f2 = font("xbold", 46), font("cap", 26); hw = CW / 2 - 30
        self.ln = sprite([c["left"][0]], f, FG, 1.1); self.ls = sprite(wrap(c["left"][1].upper(), f2, hw), f2, self.acc, 1.25, 2)
        self.rn = sprite([c["right"][0]], f, FG, 1.1); self.rs = sprite(wrap(c["right"][1].upper(), f2, hw), f2, MUTED, 1.25, 2)
        self.foot = sprite(wrap(c["foot"], font("semi", 42), CW), font("semi", 42), FG, 1.25)
    def draw_eyes(self, fr, t, dur, op):
        d = self._d; cy = CARD_CY - 120; e = ease(t / 0.5)
        for j, cx in enumerate((X0 + CW * 0.25, X0 + CW * 0.75)):
            w, h = 170 * e, 92 * e
            if w < 2: continue
            pts = [(cx + w * math.cos(a), cy + h * math.sin(a) * abs(math.sin(a)) ** 0.2) for a in [i * math.pi / 30 for i in range(61)]]
            d.polygon(pts, fill=A((232, 226, 236), op))
            d.ellipse([cx - 52 * e, cy - 52 * e, cx + 52 * e, cy + 52 * e], fill=A((40, 32, 52), op))
            d.ellipse([cx - 22 * e, cy - 22 * e, cx + 22 * e, cy + 22 * e], fill=A((10, 8, 14), op))
            if j == 1:                      # blindfold slides across the right eye
                b = ease((t - 0.9) / 0.6)
                if b > 0:
                    rr(d, [cx - 210, cy - 108, cx - 210 + 420 * b, cy + 108], 24, fill=A((30, 26, 36), op))
                    d.line([cx - 210, cy - 108, cx - 210 + 420 * b, cy - 108], fill=A(GREY2, op), width=4)
            if j == 0:                      # the files reaching the open eye
                f = clamp01((t - 0.6) / 1.2)
                for q in range(3):
                    g = clamp01(f * 1.3 - q * 0.15)
                    px = cx - 40 + q * 40; py = cy - 330 + 320 * ease(g)
                    if g < 1: rr(d, [px - 22, py - 28, px + 22, py + 28], 5, fill=A(self.acc, op * clamp01((1 - g) * 3)))
        k = ease((t - 0.4) / 0.5)
        for sp, ss, cx in ((self.ln, self.ls, X0 + CW * 0.25), (self.rn, self.rs, X0 + CW * 0.75)):
            self._pp(sp, cx - sp.size[0] / 2, cy + 130, op * k); self._pp(ss, cx - ss.size[0] / 2, cy + 190, op * k)
        e3 = ease((t - 1.6) / 0.5); self._pp(self.foot, X0, cy + 300, op * e3)

    # ---------------------------------------------------------------- dots: one dot per person
    def init_dots(self):
        c = self.c; self.n, self.kk, self.cols = c["n"], c["k"], c.get("cols", 23)
        self.num = sprite([c["num"]], font("black", 150), BLUE, 1.0)
        f = font("semi", 36)
        self.lab = sprite(wrap(c["label"], f, CW - self.num.size[0] - 30), f, MUTED, 1.25)
        self.leg = [sprite([c["hi"]], font("cap", 28), FG, 1.2, 2), sprite([c["lo"]], font("cap", 28), FG, 1.2, 2)]
        self.after = sprite(wrap(c.get("after", ""), font("semi", 36), CW), font("semi", 36), FG, 1.25) if c.get("after") else None
        self.cell = CW / self.cols; rows = math.ceil(self.n / self.cols)
        self.top = CARD_CY - (rows * self.cell + 200) / 2 + 200 - 30
    def draw_dots(self, fr, t, dur, op):
        d = self._d; r = self.cell * 0.36
        fill_start, fill_len = 1.2, min(2.4, dur * 0.35)
        for i in range(self.n):
            row, cc = divmod(i, self.cols)
            a = clamp01((t - 0.003 * i) / 0.3)
            if a <= 0: continue
            cx, cy = X0 + cc * self.cell + self.cell / 2, self.top + row * self.cell + self.cell / 2
            lit = i < self.kk and t > fill_start + fill_len * i / self.kk
            col = BLUE if lit else GREY
            rr_ = r * (1.25 if lit and t < fill_start + fill_len * i / self.kk + 0.15 else 1)
            d.ellipse([cx - rr_, cy - rr_, cx + rr_, cy + rr_], fill=A(col, op * a))
        e = ease((t - fill_start - fill_len) / 0.5); y0 = self.top - 200
        self._pp(self.num, X0, y0 + 20 * (1 - e), op * e)
        self._pp(self.lab, X0 + self.num.size[0] + 30, y0 + 30, op * e)
        ly = self.top + math.ceil(self.n / self.cols) * self.cell + 24; x = X0
        for col, sp in ((BLUE, self.leg[0]), (GREY, self.leg[1])):
            d.ellipse([x, ly + 6, x + 24, ly + 30], fill=A(col, op * e)); self._pp(sp, x + 36, ly + 2, op * e); x += 36 + sp.size[0] + 40
        if self.after is not None:
            e2 = ease((t - dur * 0.7) / 0.5); self._pp(self.after, X0, ly + 60, op * e2)

    # ---------------------------------------------------------------- grades: what backs each story
    def init_grades(self):
        c = self.c; self.items = c["items"]; f, f2 = font("xbold", 46), font("semi", 34)
        self.sp = [(sprite(wrap(it[0], f, CW - 200), f, FG, 1.1), sprite(wrap(it[1], f2, CW - 200), f2, MUTED, 1.2)) for it in self.items]
        self.h = [a.size[1] + b.size[1] + 70 for a, b in self.sp]
        self.top = CARD_CY - (sum(self.h) + 24 * (len(self.h) - 1)) / 2
    def draw_grades(self, fr, t, dur, op):
        d = self._d; y = self.top; n = len(self.items)
        for i, ((a, b), h) in enumerate(zip(self.sp, self.h)):
            k = ease((t - i * dur * 0.6 / n) / 0.5)
            x = X0 + 60 * (1 - k)
            rr(d, [x, y, x + CW, y + h], 22, fill=A((30, 26, 38), op * k))
            ic = self.items[i][2]; cx, cy = x + 70, y + h / 2; col = A(FG, op * k)
            if ic == "court":               # scales
                d.line([cx, cy - 34, cx, cy + 30], fill=col, width=5); d.line([cx - 36, cy - 22, cx + 36, cy - 22], fill=col, width=5)
                for s in (-1, 1): d.arc([cx + s * 36 - 18, cy - 14, cx + s * 36 + 18, cy + 18], 0, 180, fill=col, width=5)
                d.line([cx - 20, cy + 30, cx + 20, cy + 30], fill=col, width=5)
            elif ic == "doc":               # a page with lines
                rr(d, [cx - 26, cy - 34, cx + 26, cy + 34], 5, outline=col, width=5)
                for q in range(3): d.line([cx - 14, cy - 14 + q * 14, cx + 14, cy - 14 + q * 14], fill=col, width=4)
            else:                           # a speech bubble with a check
                d.ellipse([cx - 36, cy - 30, cx + 36, cy + 22], outline=col, width=5)
                d.polygon([(cx - 14, cy + 18), (cx - 26, cy + 38), (cx + 2, cy + 20)], fill=col)
                d.line([cx - 14, cy - 4, cx - 4, cy + 6, cx + 16, cy - 14], fill=A(BLUE, op * k), width=6)
            self._pp(a, x + 140, y + 30, op * k); self._pp(b, x + 140, y + 36 + a.size[1], op * k)
            y += h + 24

    for name, fn in list(locals().items()):
        if name.startswith("init_"):
            setattr(Card, name, fn)
        elif name.startswith("draw_"):
            setattr(Card, name, layered(fn))

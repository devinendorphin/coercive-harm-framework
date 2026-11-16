"""Kinetic artifact cards for Told Whole reels (2026-11-16, reel 01 visual overhaul).

Each institution is drawn as the mechanism it ran (a report stamped, a chart edited, a status bar reset),
and the quoted words reveal in sync with the narrator speaking them. Installed onto render.Card.

Timing: the renderer passes c["_sw"] (setup words) and c["_qw"] (spoken-quote words), each a list of
{"w", "s", "e"} in seconds local to the card's start. Colours follow cards_visual: BLUE = protected or
outcome, ORANGE = the person or their network, the red accent = the institution's act (always labelled
in text, never colour alone).
"""
import math, re
from PIL import Image, ImageDraw

BLUE, ORANGE, AQUA = (57, 135, 229), (217, 89, 38), (25, 158, 112)
PANEL, PANEL2, LINE = (28, 25, 34), (40, 36, 48), (70, 64, 80)
WHITE_DOT = (236, 230, 220)


def install(Card, G):
    font, sprite, paste, wrap, ease, clamp01, mix, tw = (G[k] for k in
        ("font", "sprite", "paste", "wrap", "ease", "clamp01", "mix", "tw"))
    X0, CW, CARD_CY, FG, MUTED, BG, DIM = (G[k] for k in ("X0", "CW", "CARD_CY", "FG", "MUTED", "BG", "DIM"))

    def A(col, a): return tuple(col[:3]) + (int(255 * clamp01(a)),)
    def rr(d, box, r, **kw): d.rounded_rectangle([int(v) for v in box], int(r), **kw)

    # ------------------------------------------------------------ shared timing helpers
    def setup_timing(self):
        c = self.c
        self.sw, self.qw = c.get("_sw", []), c.get("_qw", [])
        self.q0 = self.qw[0]["s"] if self.qw else None
        self.q1 = self.qw[-1]["e"] if self.qw else None
    def at(self, word, default=0.0, which="s", nth=0):       # local time a setup word is spoken
        k = 0
        for w in self.sw + self.qw:
            if re.sub(r"[^\w]", "", w["w"].lower()) == word.lower():
                if k == nth: return w[which]
                k += 1
        return default
    Card.setup_timing, Card.at = setup_timing, at

    def word_times(self, n):
        """reveal time for each of n on-screen quote words, from the spoken quote words."""
        if not self.qw: return [0.3 + 0.12 * i for i in range(n)]
        if len(self.qw) == n: return [w["s"] for w in self.qw]
        return [self.q0 + (self.q1 - self.q0) * i / max(1, n) for i in range(n)]
    Card.word_times = word_times

    def para(self, text, f, width, hl=(), dim=()):
        """layout words; mark words inside highlight / dim phrases."""
        words = text.split(" ")
        lines, line = [], []
        for w in words:
            cand = " ".join(line + [w])
            if tw(f, cand) <= width or not line: line.append(w)
            else: lines.append(line); line = [w]
        lines.append(line)
        flat = [w.lower() for w in words]
        def mark(phr):
            ps = phr.lower().split(" "); out = set()
            for i in range(len(flat) - len(ps) + 1):
                if all(re.sub(r"[^\w']", "", flat[i + j]) == re.sub(r"[^\w']", "", ps[j]) for j in range(len(ps))):
                    out.update(range(i, i + len(ps)))
            return out
        H = set().union(*[mark(p) for p in hl]) if hl else set()
        out, k = [], 0
        for li, ln in enumerate(lines):
            x = 0
            for w in ln:
                out.append((li, x, w, k in H)); x += tw(f, w + " "); k += 1
        return out, len(lines)
    Card.para = para

    def draw_para(self, d, layout, f, lh, x0, y0, t, op, times, hl_col=None, base=FG):
        for i, (li, x, w, hl) in enumerate(layout):
            a = clamp01((t - times[i]) / 0.18) * op
            if a <= 0: continue
            col = (hl_col or self.acc) if hl else base
            d.text((x0 + x, y0 + li * lh), w, font=f, fill=A(col, a))
    Card.draw_para = draw_para

    def stamp(text, col, size=58, angle=-7):
        f = font("black", size)
        w, h = int(tw(f, text)) + 60, int(size * 1.6)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([3, 3, w - 4, h - 4], 10, outline=col + (255,), width=7)
        d.text((30, (h - size * 1.2) / 2), text, font=f, fill=col + (255,))
        return im.rotate(angle, expand=True, resample=Image.BICUBIC)

    def slam(fr, sp, cx, cy, t, op):            # stamp lands: scale 1.6 -> 1, fade in
        if t <= 0: return
        k = clamp01(t / 0.22); s = 1.6 - 0.6 * ease(k)
        paste(fr, sp, cx - sp.size[0] / 2, cy - sp.size[1] / 2, op * k, s)

    def overlay(fr):
        ov = Image.new("RGBA", fr.size, (0, 0, 0, 0)); return ov, ImageDraw.Draw(ov)

    def cap(text, size=26, col=MUTED, track=2):
        return sprite([text.upper()], font("cap", size), col, 1.2, track)

    # ============================================================ 1. dot collapse + coder gauges
    def init_k_dots(self):
        self.setup_timing(); c = self.c
        self.n, self.kk, self.cols = c["n"], c["k"], 28
        self.cell = CW / self.cols
        rows = math.ceil(self.n / self.cols)
        self.gy = 600
        self.rows = rows
        import random
        rng = random.Random(3); idx = list(range(self.n)); rng.shuffle(idx)
        self.keep = set(idx[:self.kk])
        self.title = sprite(["SOMETHING", "WAS WRONG"], font("black", 120), FG, 1.0)
        self.title_s = cap("Seasons 1–26", 34, self.acc, 4)
        self.l_all = cap(f"{self.n} people reached an institution for help", 28, FG)
        self.big = sprite(["1 IN 5"], font("black", 150), BLUE, 1.0)
        self.l_k = cap(f"protected · {self.kk} of {self.n}", 30, BLUE)
        self.t_dots = self.at("across", 2.5)
        self.t_cut = self.at("about", 6.0)
        self.t_g = self.at("two", 12.0)
        self.gauges = [(c["a_label"], c["a"]), (c["b_label"], c["b"])]
        self.ceil = c["ceiling"]
        self.gl = [cap(g[0], 26, FG) for g in self.gauges]
        self.gv = [sprite([f"{int(g[1] * 100)}%"], font("black", 64), BLUE, 1.0) for g in self.gauges]
        self.cl = cap(c["ceiling_label"], 24, self.acc)
    def draw_k_dots(self, fr, t, dur, op):
        ov, d = overlay(fr)
        e0 = ease(t / 0.5) * (1 - ease((t - self.t_dots + 0.3) / 0.4))
        if e0 > 0:
            paste(fr, self.title, X0, 600 + 30 * (1 - e0), op * e0)
            paste(fr, self.title_s, X0, 860, op * e0)
        if t >= self.t_dots - 0.2:
            gshift = 0
            r = self.cell * 0.32
            for i in range(self.n):
                rw, cl = divmod(i, self.cols)
                cx = X0 + cl * self.cell + self.cell / 2
                cy = self.gy + rw * self.cell + self.cell / 2 - gshift
                ein = clamp01((t - self.t_dots - 0.002 * i) / 0.3)
                if ein <= 0: continue
                if i in self.keep:
                    col = mix(WHITE_DOT, BLUE, clamp01((t - self.t_cut - 0.4) / 0.4))
                    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(col, op * ein))
                else:
                    tc = self.t_cut + 0.9 * (rw / self.rows)      # downward cascade
                    k = clamp01((t - tc) / 0.35)
                    col = mix(WHITE_DOT, (60, 30, 40), k)
                    rr_ = r * (1 - 0.35 * k)
                    d.ellipse([cx - rr_, cy - rr_ + 6 * k, cx + rr_, cy + rr_ + 6 * k], fill=A(col, op * ein * (1 - 0.45 * k)))
            fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
            top = self.gy - gshift
            e1 = ease((t - self.t_dots) / 0.4) * (1 - ease((t - self.t_cut) / 0.3))
            paste(fr, self.l_all, X0, top - 80, op * e1)
            e2 = ease((t - self.t_cut - 0.6) / 0.5)
            paste(fr, self.big, X0, top - 215 + 20 * (1 - e2), op * e2)
            paste(fr, self.l_k, X0 + self.big.size[0] + 30, top - 120, op * e2)
            if t > self.t_g:
                gy0 = self.gy + self.rows * self.cell + 70
                eg = ease((t - self.t_g - 0.3) / 0.5)
                bw = CW - 200
                for j, ((lab, v), gl, gv) in enumerate(zip(self.gauges, self.gl, self.gv)):
                    y = gy0 + j * 150
                    paste(fr, gl, X0, y, op * eg)
                    rr(d, [X0, y + 44, X0 + bw, y + 92], 10, fill=A(PANEL2, op * eg))
                    ev = ease((t - self.t_g - 0.5 - 0.25 * j) / 0.9)
                    rr(d, [X0, y + 44, X0 + max(14, bw * v * ev), y + 92], 10, fill=A(BLUE, op * eg))
                    paste(fr, gv, X0 + bw + 24, y + 30, op * ev)
                cx = X0 + bw * self.ceil
                for yy in range(int(gy0 - 24), int(gy0 + 300), 22):
                    d.line([cx, yy, cx, yy + 11], fill=A(self.acc, op * eg), width=4)
                paste(fr, self.cl, cx - self.cl.size[0] / 2, gy0 - 58, op * eg)
        fr.paste(ov, (0, 0), ov)

    # ============================================================ 2. seven-institution ladder
    def init_k_ladder(self):
        self.setup_timing(); c = self.c
        self.items = c["items"]; self.keys = c["keys"]
        f = font("xbold", 54)
        self.sp = [sprite([it], f, FG, 1.0) for it in self.items]
        self.times = [self.at(k, 0.5 + 0.6 * i) for i, k in enumerate(self.keys)]
        self.gap = 104; self.top = CARD_CY - self.gap * (len(self.items) - 1) / 2 - 40
    def draw_k_ladder(self, fr, t, dur, op):
        ov, d = overlay(fr)
        x = X0 + 30
        d.line([x, self.top, x, self.top + self.gap * (len(self.items) - 1) * ease(t / 1.2)], fill=A(LINE, op), width=5)
        for i, (sp, ti) in enumerate(zip(self.sp, self.times)):
            y = self.top + i * self.gap
            e = ease((t - ti + 0.25) / 0.35)
            if e <= 0: continue
            pulse = max(0, 1 - abs(t - ti - 0.2) / 0.45)
            w = sp.size[0] + 70
            rr(d, [x + 40, y - 40, x + 40 + w, y + 40], 40, fill=A(PANEL, op * e),
               outline=A(mix(LINE, self.acc, max(pulse, 0.35)), op * e), width=4 + int(4 * pulse))
            d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=A(mix(LINE, self.acc, max(pulse, 0.5)), op * e))
            fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
            paste(fr, sp, x + 75, y - sp.size[1] / 2 - 4, op * e)
        fr.paste(ov, (0, 0), ov)

    # ============================================================ panel used by the institution artifacts
    def panel(d, box, op, outline=LINE):
        rr(d, box, 22, fill=A(PANEL, op * 0.94), outline=A(outline, op), width=3)

    def qsetup(self, size=46, width=None, hl=(), dim=()):
        f = font("quote", size)
        self.qf, self.qlh = f, int(size * 1.28)
        self.ql, self.qn = self.para(self.c["q"], f, width or CW - 100, hl)
        self.qt = self.word_times(len(self.ql))
    Card.qsetup = qsetup
    def qdraw(self, d, x0, y0, t, op, base=FG):
        self.draw_para(d, self.ql, self.qf, self.qlh, x0, y0, t, op, self.qt, base=base)
    Card.qdraw = qdraw
    def qend(self): return (self.q1 if self.q1 is not None else 3.0)
    Card.qend = qend

    # ============================================================ 3A. police: report, interview clock, stamp
    def init_k_police(self):
        self.setup_timing(); c = self.c
        self.h1 = cap(c["case"], 30, FG, 3)
        self.h2 = cap(c["case_sub"], 24, MUTED, 2)
        self.clock_l = cap("Interview", 22, MUTED)
        self.clock_v = sprite(["2:00:00"], font("black", 44), FG, 1.0)
        self.qsetup(48, CW - 110, hl=c.get("hl", ()))
        self.st = stamp(c["stamp"], self.acc, 50)
        self.t_clock = self.at("interviewed", 2.0)
        self.t_dim = self.at("cried", self.q0 or 4.0)
    def draw_k_police(self, fr, t, dur, op):
        ov, d = overlay(fr)
        top, bot = 440, 1240
        panel(d, [X0, top, X0 + CW, bot], op * ease(t / 0.4))
        d.line([X0 + 40, top + 230, X0 + CW - 40, top + 230], fill=A(LINE, op), width=2)
        cx, cy, R = X0 + 80, top + 175, 30
        ec = clamp01((t - self.t_clock) / 1.6)
        d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=A(LINE, op), width=5)
        if ec > 0:
            d.arc([cx - R, cy - R, cx + R, cy + R], -90, -90 + 360 * ease(ec), fill=A(FG, op), width=6)
        fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
        dimk = 1 - 0.8 * clamp01((t - self.t_dim) / 0.6)
        paste(fr, self.h1, X0 + 40, top + 40, op * dimk)
        paste(fr, self.h2, X0 + 40, top + 88, op * dimk)
        paste(fr, self.clock_l, cx + 50, cy - 34, op * clamp01(ec * 3))
        paste(fr, self.clock_v, cx + 50, cy - 8, op * clamp01(ec * 3))
        self.qdraw(d, X0 + 50, top + 270, t, op)
        fr.paste(ov, (0, 0), ov)
        slam(fr, self.st, X0 + CW / 2, bot - 110, t - self.qend() - 0.15, op)

    # ============================================================ 3B. court: petition, evidence tag, stamp
    def init_k_court(self):
        self.setup_timing(); c = self.c
        self.h1 = cap(c["header"], 28, FG, 3)
        self.tags = [cap(tg, 22, FG, 2) for tg in c["tags"]]
        self.tag_t = [self.at(k, 2.0) for k in c["tag_keys"]]
        self.qsetup(46, CW - 110)
        self.st = stamp(c["stamp"], self.acc, 46)
    def draw_k_court(self, fr, t, dur, op):
        ov, d = overlay(fr)
        top, bot = 440, 1240
        panel(d, [X0, top, X0 + CW, bot], op * ease(t / 0.4))
        d.line([X0 + 40, top + 110, X0 + CW - 40, top + 110], fill=A(LINE, op), width=2)
        y = top + 140
        for sp, ti in zip(self.tags, self.tag_t):
            e = ease((t - ti) / 0.35)
            if e > 0:
                rr(d, [X0 + 40, y, X0 + 40 + sp.size[0] + 40, y + 56], 8, fill=A(PANEL2, op * e), outline=A(ORANGE, op * e), width=3)
            y += 76
        fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
        paste(fr, self.h1, X0 + 40, top + 45, op)
        y = top + 140
        for sp, ti in zip(self.tags, self.tag_t):
            paste(fr, sp, X0 + 60, y + 14, op * ease((t - ti) / 0.35)); y += 76
        self.qdraw(d, X0 + 50, top + 160 + 76 * len(self.tags), t, op)
        fr.paste(ov, (0, 0), ov)
        slam(fr, self.st, X0 + CW / 2, bot - 100, t - self.qend() - 0.15, op)

    # ============================================================ 3C. school: two reports swept under, messages deleted, counter
    def init_k_school(self):
        self.setup_timing(); c = self.c
        self.rows = [cap(r, 26, FG, 2) for r in c["rows"]]
        self.row_t = [self.at(k, 1.0 + i) for i, k in enumerate(c["row_keys"])]
        self.sweep_lab = cap("Swept under the rug", 26, self.acc, 3)
        self.msg = [sprite([m], font("semi", 34), FG, 1.0) for m in c["msgs"]]
        self.del_t = self.at("delete", 4.0)
        self.del_lab = cap("“Delete every single message”", 24, MUTED)
        self.qsetup(46, CW - 110)
        self.cnt_l = sprite(wrap(c["counter"], font("cap", 26), CW - 200), font("cap", 26), FG, 1.2)
        self.cnt = sprite(["0"], font("black", 110), self.acc, 1.0)
        self.t_sweep = self.at("rug", (self.q0 or 4) + 2.5)
    def draw_k_school(self, fr, t, dur, op):
        ov, d = overlay(fr)
        top = 440
        base_y = top + 300
        ks = clamp01((t - self.t_sweep) / 0.7)
        for i, (sp, ti) in enumerate(zip(self.rows, self.row_t)):
            e = ease((t - ti) / 0.35)
            if e <= 0: continue
            y = top + i * 110 + 260 * ease(ks)
            a = op * e * (1 - 0.75 * ks)
            rr(d, [X0, y, X0 + CW, y + 90], 14, fill=A(PANEL2, a), outline=A(LINE, a), width=3)
        d.line([X0, base_y, X0 + CW, base_y], fill=A(self.acc if ks > 0 else LINE, op), width=4)
        if ks > 0:
            d.rectangle([X0, base_y + 4, X0 + CW, base_y + 4 + 250 * ease(ks)], fill=A((8, 6, 10), op * 0.7 * ks))
        # messages being deleted (right column, during setup)
        mx, my = X0 + CW - 360, top + 360
        for j, sp in enumerate(self.msg):
            ein = ease((t - self.del_t + 1.2 - 0.1 * j) / 0.3)
            kdel = clamp01((t - self.del_t - 0.25 * j) / 0.25)
            a = op * ein * (1 - kdel)
            if a <= 0: continue
            rr(d, [mx, my + j * 70, mx + 340, my + j * 70 + 56], 26, fill=A(BLUE, a * 0.85))
        fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
        for i, (sp, ti) in enumerate(zip(self.rows, self.row_t)):
            e = ease((t - ti) / 0.35)
            y = top + i * 110 + 260 * ease(ks)
            paste(fr, sp, X0 + 30, y + 30, op * e * (1 - 0.75 * ks))
        if ks > 0: paste(fr, self.sweep_lab, X0, base_y - 44, op * ks)
        for j, sp in enumerate(self.msg):
            ein = ease((t - self.del_t + 1.2 - 0.1 * j) / 0.3); kdel = clamp01((t - self.del_t - 0.25 * j) / 0.25)
            paste(fr, sp, mx + 24, my + j * 70 + 8, op * ein * (1 - kdel))
        if t > self.del_t - 1.2 and t < (self.q0 or 99):
            paste(fr, self.del_lab, mx, my - 50, op * ease((t - self.del_t + 1.2) / 0.3) * (1 - clamp01((t - (self.q0 or 99) + 0.3) / 0.3)))
        self.qdraw(d, X0 + 10, top + 620, t, op)
        fr.paste(ov, (0, 0), ov)
        ec = ease((t - self.qend() - 0.1) / 0.4)
        if ec > 0:
            paste(fr, self.cnt_l, X0, 1150, op * ec)
            paste(fr, self.cnt, X0 + CW - self.cnt.size[0], 1110, op * ec)

    # ============================================================ 3D. employer: shift grid, arrow up, ricochet back
    def init_k_employer(self):
        self.setup_timing(); c = self.c
        self.days = c["days"]; self.marks = c["marks"]
        self.dl = [cap(dd, 22, MUTED) for dd in self.days]
        self.ml = {k: cap(v, 18, FG, 1) for k, v in {"r": "rage", "p": "physical"}.items()}
        self.box_hi = cap(c["hi"], 26, FG, 2); self.box_lo = cap(c["lo"], 26, FG, 2)
        self.t_days = self.at("day", 1.5)
        self.t_up = self.at("parents", 3.0)
        self.qsetup(54, CW - 60)
    def draw_k_employer(self, fr, t, dur, op):
        ov, d = overlay(fr)
        top = 440; n = len(self.days); cw = CW / n
        for i in range(n):
            e = ease((t - self.t_days - 0.12 * i) / 0.3)
            if e <= 0: continue
            m = self.marks[i]
            col = self.acc if m == "p" else (120, 50, 60) if m == "r" else PANEL2
            rr(d, [X0 + i * cw + 6, top + 40, X0 + (i + 1) * cw - 6, top + 190], 12, fill=A(col, op * e))
        # boxes
        bx_hi = [X0 + CW / 2 - 230, top + 300, X0 + CW / 2 + 230, top + 400]
        bx_lo = [X0 + CW / 2 - 230, top + 620, X0 + CW / 2 + 230, top + 720]
        eb = ease((t - self.t_up + 1.0) / 0.4)
        panel(d, bx_hi, op * eb); panel(d, bx_lo, op * eb, outline=ORANGE)
        ax = X0 + CW / 2
        eu = clamp01((t - self.t_up) / 0.5)
        if eu > 0:
            y1 = bx_lo[1] - (bx_lo[1] - bx_hi[3]) * ease(eu)
            d.line([ax - 60, bx_lo[1], ax - 60, y1], fill=A(ORANGE, op), width=8)
            d.polygon([(ax - 80, y1 + 20), (ax - 40, y1 + 20), (ax - 60, y1 - 6)], fill=A(ORANGE, op))
        er = clamp01((t - (self.q0 or 5) - 0.1) / 0.5)
        if er > 0:
            y2 = bx_hi[3] + (bx_lo[1] - bx_hi[3]) * ease(er)
            d.line([ax + 60, bx_hi[3], ax + 60, y2], fill=A(self.acc, op), width=8)
            d.polygon([(ax + 40, y2 - 20), (ax + 80, y2 - 20), (ax + 60, y2 + 6)], fill=A(self.acc, op))
        fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
        for i in range(n):
            e = ease((t - self.t_days - 0.12 * i) / 0.3)
            paste(fr, self.dl[i], X0 + i * cw + cw / 2 - self.dl[i].size[0] / 2, top + 50, op * e)
            m = self.marks[i]
            if m in self.ml: paste(fr, self.ml[m], X0 + i * cw + cw / 2 - self.ml[m].size[0] / 2, top + 140, op * e)
        paste(fr, self.box_hi, bx_hi[0] + 230 - self.box_hi.size[0] / 2, bx_hi[1] + 34, op * eb)
        paste(fr, self.box_lo, bx_lo[0] + 230 - self.box_lo.size[0] / 2, bx_lo[1] + 34, op * eb)
        self.qdraw(d, X0, top + 790, t, op, base=self.acc)
        fr.paste(ov, (0, 0), ov)

    # ============================================================ 3E. church: ring of members, one leaves, broadcast smear
    def init_k_church(self):
        self.setup_timing(); c = self.c
        self.center = cap(c["center"], 26, FG, 2); self.center2 = cap(c["center_sub"], 20, MUTED, 2)
        self.n = c.get("n", 10)
        self.left_l = cap("Left", 22, ORANGE, 2)
        self.trash = cap("Reputation trashed", 22, self.acc, 2)
        self.t_ring = 0.3
        self.t_leave = self.at("left", (self.q0 or 4) + 3.0)
        self.qsetup(46, CW - 60)
    def draw_k_church(self, fr, t, dur, op):
        ov, d = overlay(fr)
        cx, cy, R = X0 + CW / 2 - 60, 740, 210
        er = ease((t - self.t_ring) / 0.8)
        d.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], fill=A(PANEL2, op * er), outline=A(LINE, op * er), width=4)
        kl = clamp01((t - self.t_leave) / 0.6)
        kb = clamp01((t - self.t_leave - 0.6) / 0.6)
        pts = []
        for i in range(self.n):
            a = 2 * math.pi * i / self.n
            rr_ = R + (120 * ease(kl) if i == 0 else 0)
            x, y = cx + rr_ * math.cos(a), cy + rr_ * math.sin(a)
            pts.append((x, y))
        for i, (x, y) in enumerate(pts):
            if i and kb > 0:
                d.line([cx, cy, cx + (x - cx) * ease(kb), cy + (y - cy) * ease(kb)], fill=A(self.acc, op * 0.8), width=4)
        for i, (x, y) in enumerate(pts):
            e = ease((t - self.t_ring - 0.05 * i) / 0.4)
            col = ORANGE if i == 0 and kl > 0 else (mix(FG, self.acc, kb) if i else FG)
            d.ellipse([x - 26, y - 26, x + 26, y + 26], fill=A(col, op * e))
        fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
        paste(fr, self.center, cx - self.center.size[0] / 2, cy - 30, op * er)
        paste(fr, self.center2, cx - self.center2.size[0] / 2, cy + 10, op * er)
        if kl > 0:
            x, y = pts[0]
            paste(fr, self.left_l, x - self.left_l.size[0] / 2, y + 40, op * kl)
            if kb > 0: paste(fr, self.trash, x - self.trash.size[0] / 2, y + 72, op * kb)
        self.qdraw(d, X0, 1040, t, op)
        fr.paste(ov, (0, 0), ov)

    # ============================================================ 3F. birth centre: chart diff, insertions typed in
    def init_k_chart(self):
        self.setup_timing(); c = self.c
        self.h_a = cap(c["v1"], 24, FG, 2); self.h_b = cap(c["v2"], 24, self.acc, 2)
        fm = font("med", 34)
        self.base = [sprite([ln], fm, FG, 1.0) for ln in c["base"]]
        self.adds = [sprite(wrap(ln, fm, CW - 120), fm, self.acc, 1.15) for ln in c["adds"]]
        self.tag = cap(c["tag"], 22, self.acc, 2)
        self.t_v2 = self.at("month", 3.0)
        self.qsetup(42, CW - 40)
    def draw_k_chart(self, fr, t, dur, op):
        ov, d = overlay(fr)
        top = 440
        panel(d, [X0, top, X0 + CW, top + 520], op * ease(t / 0.4))
        kv = clamp01((t - self.t_v2) / 0.5)
        y = top + 110
        for sp in self.base:
            y += sp.size[1] + 18
        q0 = self.q0 or self.t_v2 + 1
        span = max(1.0, (self.qend() - q0))
        ya = y + 10
        for j, sp in enumerate(self.adds):
            ta = q0 + span * (0.3 + 0.35 * j)
            e = clamp01((t - ta) / 0.5)
            if e > 0:
                d.rectangle([X0 + 30, ya - 6, X0 + CW - 30, ya + sp.size[1] + 4], fill=A((70, 20, 30), op * e * 0.8))
            ya += sp.size[1] + 22
        fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
        paste(fr, self.h_a, X0 + 40, top + 40, op * (1 - kv))
        paste(fr, self.h_b, X0 + 40, top + 40, op * kv)
        y = top + 110
        for sp in self.base:
            paste(fr, sp, X0 + 60, y, op); y += sp.size[1] + 18
        ya = y + 10
        for j, sp in enumerate(self.adds):
            ta = q0 + span * (0.3 + 0.35 * j)
            e = clamp01((t - ta) / 0.5)
            if e > 0:
                d.text((X0 + 36, ya - 2), "+", font=font("black", 40), fill=A(self.acc, op * e))
                paste(fr, sp, X0 + 80, ya, op * e)
            ya += sp.size[1] + 22
        et = ease((t - self.qend() + 0.6) / 0.4)
        paste(fr, self.tag, X0 + 40, top + 470, op * et)
        self.qdraw(d, X0, top + 570, t, op)
        fr.paste(ov, (0, 0), ov)

    # ============================================================ 3G. program: status bar resets, fee meter
    def init_k_program(self):
        self.setup_timing(); c = self.c
        self.h1 = cap(c["header"], 26, FG, 2)
        self.bar_l = cap(c["bar"], 22, MUTED, 2)
        self.full = cap(c["full"], 26, BLUE, 2); self.zero = cap(c["zero"], 26, self.acc, 2)
        self.alert = cap(c["alert"], 22, FG, 2)
        self.fee_l = cap(c["fee"], 24, self.acc, 2)
        self.t_alert = self.at("abused", 2.5)
        self.t_snap = self.at("punished", 4.0)
        self.t_fee = self.at("money", (self.qend() if self.qw else 8) - 1.5)
        self.qsetup(42, CW - 40)
    def draw_k_program(self, fr, t, dur, op):
        ov, d = overlay(fr)
        top = 440
        panel(d, [X0, top, X0 + CW, top + 470], op * ease(t / 0.4))
        bx0, bx1, by = X0 + 40, X0 + CW - 40, top + 160
        rr(d, [bx0, by, bx1, by + 56], 12, fill=A(PANEL2, op))
        ks = clamp01((t - self.t_snap) / 0.25)
        frac = 1 - ease(ks)
        if frac > 0.005:
            rr(d, [bx0, by, bx0 + (bx1 - bx0) * frac, by + 56], 12, fill=A(BLUE if ks == 0 else mix(BLUE, self.acc, ks), op))
        ea = ease((t - self.t_alert) / 0.3)
        if ea > 0:
            rr(d, [X0 + 40, top + 300, X0 + CW - 40, top + 370], 12, fill=A((70, 20, 30), op * ea), outline=A(self.acc, op * ea), width=3)
        fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
        paste(fr, self.h1, X0 + 40, top + 40, op)
        paste(fr, self.bar_l, X0 + 40, by - 50, op)
        paste(fr, self.full if ks < 0.5 else self.zero, bx0, by + 72, op)
        if ea > 0: paste(fr, self.alert, X0 + 64, top + 322, op * ea)
        ef = ease((t - self.t_fee) / 0.4)
        if ef > 0:
            paste(fr, self.fee_l, X0 + 40, top + 410, op * ef)
        self.qdraw(d, X0, top + 530, t, op)
        fr.paste(ov, (0, 0), ov)

    # ============================================================ 4. pieces -> one whole story (chain)
    def init_k_chain(self):
        self.setup_timing(); c = self.c
        self.phase = c["phase"]
        self.steps = c["steps"]
        f = font("semi", 38); ft = font("cap", 22)
        self.sl = [sprite(wrap(s["label"], f, CW - 200), f, FG, 1.15) for s in self.steps]
        self.st = [sprite([s["tag"].upper()], ft, s_col(s), 1.2, 2) for s in self.steps]
        self.step_t = [self.at(s["key"], 1.0 + i) if s.get("key") else -1 for i, s in enumerate(self.steps)]
        fc = font("cap", 24)
        self.crop_l = sprite(wrap(c.get("crop", "").upper(), fc, CW), fc, BLUE, 1.25, 2)
        self.whole_l = sprite(wrap(c.get("whole", "").upper(), fc, CW - 40), fc, ORANGE, 1.25, 2)
        self.t_crop = self.at(c.get("crop_key", "pieces"), 2.0)
        self.t_whole = self.at(c.get("whole_key", "whole"), 5.0, nth=c.get("whole_nth", 0))
        self.gap = 170; self.top = 470
        if c.get("q"): self.qsetup(42, CW - 40)
    def s_col(s):
        return {"bad": (255, 77, 94), "person": ORANGE, "help": AQUA, "outcome": BLUE}[s["kind"]]
    def draw_k_chain(self, fr, t, dur, op):
        ov, d = overlay(fr)
        x = X0 + 40
        shown = []
        for i, s in enumerate(self.steps):
            ti = self.step_t[i]
            e = 1.0 if ti < 0 else ease((t - ti) / 0.45)
            shown.append(e)
        last = max([i for i, e in enumerate(shown) if e > 0] or [0])
        d.line([x, self.top, x, self.top + self.gap * last], fill=A(LINE, op), width=6)
        for i, s in enumerate(self.steps):
            e = shown[i]
            if e <= 0: continue
            y = self.top + i * self.gap
            col = s_col(s)
            sz = 56
            rr(d, [x - sz / 2, y - sz / 2 - 40 * (1 - e), x + sz / 2, y + sz / 2 - 40 * (1 - e)], 10, fill=A(col, op * e))
        if self.phase == 2:
            kc = ease((t - self.t_crop) / 0.4); kw = ease((t - self.t_whole) / 0.5)
            yb = self.top + (len(self.steps) - 1) * self.gap
            if kc > 0 and kw < 1:
                a = op * kc * (1 - kw)
                d.rectangle([X0 - 10, yb - 70, X0 + CW + 10, yb + 80], outline=A(BLUE, a), width=5)
                d.rectangle([X0 - 30, 330, X0 + CW + 30, yb - 70], fill=A((8, 6, 10), a * 0.75))
            if kw > 0:
                d.rectangle([X0 - 10, self.top - 80, X0 + CW + 10, yb + 80], outline=A(ORANGE, op * kw), width=5)
        fr.paste(ov, (0, 0), ov); ov, d = overlay(fr)
        for i, s in enumerate(self.steps):
            e = shown[i]
            if e <= 0: continue
            y = self.top + i * self.gap
            paste(fr, self.sl[i], x + 70, y - 46, op * e)
            paste(fr, self.st[i], x + 70, y - 46 + self.sl[i].size[1] + 6, op * e)
        if self.phase == 2:
            yb = self.top + (len(self.steps) - 1) * self.gap
            kc = ease((t - self.t_crop) / 0.4); kw = ease((t - self.t_whole) / 0.5)
            if kc > 0 and kw < 1: paste(fr, self.crop_l, X0, yb + 100, op * kc * (1 - kw))
            if kw > 0: paste(fr, self.whole_l, X0, yb + 100, op * kw)
        if self.c.get("q"):
            self.qdraw(d, X0, self.top + self.gap * len(self.steps) + 10, t, op, base=AQUA)
        fr.paste(ov, (0, 0), ov)
    G["s_col"] = s_col

    # ============================================================ 5a. two coder families tracing whole stories
    def init_k_coders(self):
        self.setup_timing(); c = self.c
        self.la = cap(c["a"], 26, FG, 3); self.lb = cap(c["b"], 26, FG, 3)
        self.t_c = self.at("families", 3.0)
    def draw_k_coders(self, fr, t, dur, op):
        ov, d = overlay(fr)
        top = 470; colw = CW / 2 - 30
        for j, x0 in enumerate([X0, X0 + CW / 2 + 30]):
            e = ease((t - 0.3) / 0.5)
            for s in range(3):                         # three whole stories per column
                xs = x0 + 50 + s * (colw - 80) / 2
                for k in range(6):
                    y = top + 90 + k * 100
                    d.ellipse([xs - 14, y - 14, xs + 14, y + 14], fill=A(LINE, op * e))
                    if k: d.line([xs, y - 86, xs, y - 14], fill=A(LINE, op * e), width=4)
                # scan
                sc = clamp01((t - self.t_c - 0.3 * s - 0.15 * j) / 1.4)
                if sc > 0:
                    yy = top + 90 + 500 * ease(sc)
                    d.line([xs, top + 90, xs, yy], fill=A(BLUE, op), width=6)
                    d.ellipse([xs - 18, yy - 18, xs + 18, yy + 18], outline=A(BLUE, op), width=5)
        d.line([X0 + CW / 2, top, X0 + CW / 2, top + 640], fill=A(LINE, op), width=2)
        fr.paste(ov, (0, 0), ov)
        paste(fr, self.la, X0, top, op); paste(fr, self.lb, X0 + CW / 2 + 30, top, op)

    # ============================================================ 5b. big spoken quote with emphasis
    def init_k_bigquote(self):
        self.setup_timing(); c = self.c
        self.qsetup(64, CW - 20, hl=c.get("hl", ()))
        self.by_ = cap("— " + c["by"], 26, self.acc, 2)
    def draw_k_bigquote(self, fr, t, dur, op):
        ov, d = overlay(fr)
        self.qdraw(d, X0, 560, t, op)
        fr.paste(ov, (0, 0), ov)
        paste(fr, self.by_, X0, 560 + self.qlh * self.qn + 40, op * ease((t - self.qend()) / 0.4))

    # ============================================================ 5c. predictions: line first, then the measured bar, then the verdict
    def init_k_pass(self):
        self.setup_timing(); c = self.c
        self.items = c["items"]
        f = font("semi", 32)
        self.lab = [sprite(wrap(it["label"], f, CW - 250), f, FG, 1.15) for it in self.items]
        self.badge = [stamp(it["verdict"], it_col(it), 30, -4) for it in self.items]
        self.vals = [sprite([it["value_txt"]], font("black", 46), FG, 1.0) for it in self.items]
        self.subs = [cap(it.get("sub", ""), 20, MUTED, 1) for it in self.items]
        self.lines = [cap(it["line_txt"], 20, self.acc, 1) for it in self.items]
        self.t_line = self.at("line", 3.0)
        self.t_v = [self.at(k, 5.0 + 2 * i) for i, k in enumerate(c["keys"])]
    def it_col(it): return {"holds": BLUE, "split": ORANGE, "open": (154, 147, 160)}[it["kind"]]
    G["it_col"] = it_col
    def draw_k_pass(self, fr, t, dur, op):
        ov, d = overlay(fr)
        top = 450; rowh = 270; bw = CW - 220
        for i, it in enumerate(self.items):
            y = top + i * rowh
            e = ease((t - 0.2 * i) / 0.4)
            ly = y + self.lab[i].size[1] + 20
            rr(d, [X0, ly, X0 + bw, ly + 46], 10, fill=A(PANEL2, op * e))
            el = ease((t - self.t_line - 0.2 * i) / 0.4)
            lx = X0 + bw * it["line"]
            for yy in range(int(ly - 24), int(ly + 70), 16):
                d.line([lx, yy, lx, yy + 8], fill=A(self.acc, op * el), width=4)
            ev = ease((t - self.t_v[i]) / 0.8)
            if ev > 0:
                rr(d, [X0, ly, X0 + max(12, bw * it["value"] * ev), ly + 46], 10, fill=A(it_col(it), op))
        fr.paste(ov, (0, 0), ov)
        for i, it in enumerate(self.items):
            y = top + i * rowh
            e = ease((t - 0.2 * i) / 0.4)
            paste(fr, self.lab[i], X0, y, op * e)
            ly = y + self.lab[i].size[1] + 20
            el = ease((t - self.t_line - 0.2 * i) / 0.4)
            paste(fr, self.lines[i], X0 + bw * it["line"] - self.lines[i].size[0] / 2, ly + 62, op * el)
            ev = ease((t - self.t_v[i]) / 0.8)
            if ev > 0:
                paste(fr, self.vals[i], X0 + bw + 20, ly - 6, op * ev)
                paste(fr, self.subs[i], X0, ly + 92, op * ev)
            slam(fr, self.badge[i], X0 + CW - 110, y + 24, t - self.t_v[i] - 0.8, op)

    # ============================================================ 6. rings out to the title
    def init_k_rings(self):
        self.setup_timing(); c = self.c
        self.rings = [cap(r, 20, FG, 2) for r in c["rings"]]
        self.big = [sprite([l], font("black", 120), FG, 1.0) for l in c["big"].split("\n")]
        self.t_big = self.at(c.get("big_key", "next"), 4.0)
    def draw_k_rings(self, fr, t, dur, op):
        ov, d = overlay(fr)
        cx, cy = X0 + CW / 2, CARD_CY - 40
        n = len(self.rings); fade = 1 - ease((t - self.t_big) / 0.5)
        for i in range(n):
            e = ease((t - 0.35 * i) / 0.6)
            if e <= 0: continue
            R = 60 + i * 62 * e
            d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=A(mix(LINE, self.acc, i / max(1, n - 1)), op * e * fade), width=4)
        fr.paste(ov, (0, 0), ov)
        for i, sp in enumerate(self.rings):
            e = ease((t - 0.35 * i) / 0.6)
            R = 60 + i * 62 * e
            paste(fr, sp, cx - sp.size[0] / 2, cy - R - 26, op * e * fade)
        y = CARD_CY - 140
        for j, sp in enumerate(self.big):
            e = ease((t - self.t_big - 0.12 * j) / 0.5)
            paste(fr, sp, X0, y + 40 * (1 - e), op * e); y += sp.size[1] + 10

    for name, fn in list(locals().items()):
        if name.startswith(("init_k_", "draw_k_")):
            setattr(Card, name, fn)

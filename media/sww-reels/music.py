"""Procedural soundtrack: minor-key pad, heartbeat pulse, sparse delayed arpeggio, air.
Usage: python music.py <seconds> <reel_index> <out.wav>"""
import sys
import numpy as np, soundfile as sf

SR = 48000
dur, idx, out = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = np.random.default_rng(1000 + idx)

BPM = 72
beat = 60 / BPM
bar = 4 * beat
roots = [57, 50, 52, 55, 53, 48]               # A, D, E, G, F, C (MIDI), cycled per reel
root = roots[idx % len(roots)]
# i - VI - III - VII, each chord held two bars
prog = [(0, [0, 3, 7]), (-4, [0, 4, 7]), (3, [0, 4, 7]), (-2, [0, 4, 7])]
if idx % 3 == 1:
    prog = [(0, [0, 3, 7]), (-2, [0, 4, 7]), (-4, [0, 4, 7]), (-5, [0, 3, 7])]   # i - VII - VI - v

n = int(dur * SR)
t = np.arange(n) / SR
L = np.zeros(n); R = np.zeros(n)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
chord_len = 2 * bar

# Pad: additive harmonics with slow timbre LFO, crossfaded chords
lfo = 0.5 + 0.5 * np.sin(2 * np.pi * t / 11.0)
k = 0
while k * chord_len < dur + chord_len:
    off, tri = prog[k % len(prog)]
    c0 = k * chord_len - 1.5
    a, b = max(0, int(c0 * SR)), min(n, int((c0 + chord_len + 3.0) * SR))
    if a < b:
        tt = t[a:b] - c0
        env = np.clip(tt / 1.5, 0, 1) * np.clip((chord_len + 3.0 - tt) / 1.5, 0, 1)
        env = np.sin(env * np.pi / 2) ** 2
        notes = [root + off + i for i in tri] + [root + off - 12, root + off + 12 + tri[1]]
        for j, m in enumerate(notes):
            f = hz(m)
            for h in range(1, 7):
                amp = (1 / h ** 1.6) * (0.55 + 0.45 * lfo[a:b] ** (h / 2))
                det = 1 + (0.0018 * (h % 2) + 0.0009 * j)
                L[a:b] += env * amp * np.sin(2 * np.pi * f * h * tt * det + j)
                R[a:b] += env * amp * np.sin(2 * np.pi * f * h * tt / det + 2 * j)
    k += 1
L *= 0.05; R *= 0.05

# Heartbeat pulse (lub-dub on beat 1 of each bar)
kick = np.zeros(n)
for bstart in np.arange(0, dur, bar):
    for dt, g in ((0.0, 1.0), (0.32, 0.6)):
        a = int((bstart + dt) * SR)
        m = min(n - a, int(0.5 * SR))
        if m <= 0:
            continue
        tt = np.arange(m) / SR
        f = 48 + 40 * np.exp(-tt * 22)
        kick[a:a + m] += g * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
L += 0.22 * kick; R += 0.22 * kick

# Sparse arpeggio, starting after the intro, with ping-pong delay
arp = np.zeros(n)
step = beat / 2
for s_i, s0 in enumerate(np.arange(bar * 2, dur - 2, step)):
    if rng.random() > 0.42:
        continue
    off, tri = prog[int(s0 // chord_len) % len(prog)]
    m = root + off + 12 + tri[rng.integers(0, 3)] + (12 if rng.random() < 0.2 else 0)
    a = int(s0 * SR); ln = min(n - a, int(1.2 * SR))
    tt = np.arange(ln) / SR
    f = hz(m)
    arp[a:a + ln] += (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 4.5) * (1 - np.exp(-tt * 300))
d = int(beat * 0.75 * SR)
aL, aR = arp.copy(), np.zeros(n)
for rep in range(1, 5):
    g = 0.38 ** rep
    tgt = aR if rep % 2 else aL
    tgt[rep * d:] += g * arp[:n - rep * d]
L += 0.045 * aL; R += 0.045 * aR

# Air: smoothed noise
noise = rng.standard_normal((2, n))
for ch in range(2):
    for _ in range(3):
        noise[ch] = np.convolve(noise[ch], np.ones(9) / 9, mode="same")
L += 0.004 * noise[0]; R += 0.004 * noise[1]

fade = np.clip(t / 2.0, 0, 1) * np.clip((dur - t) / 2.5, 0, 1)
mix = np.stack([L, R], 1) * fade[:, None]
mix /= max(1e-9, np.abs(mix).max()) / 0.8
sf.write(out, mix.astype(np.float32), SR)

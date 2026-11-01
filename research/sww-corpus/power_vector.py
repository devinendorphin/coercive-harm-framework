#!/usr/bin/env python3
"""Power-vector follow-up (preregistration-power-vector.md). Written and committed before any
coding. The analyst has seen results/; coders must not.

  python3 power_vector.py packet  <sww_json_dir> <out.json>      # Part 1 coder packet (notes only)
  python3 power_vector.py sample  <sww_json_dir> <out.json>      # Part 2: 200 eligible segments
  python3 power_vector.py part1   <codes.csv>                    # P1, P2, P3 from frozen season_rates.csv
  python3 power_vector.py part2   <coderA.csv> <coderB.csv>      # kappa + C2 verdict

Decisions fixed here, before coding (logged in preregistration-power-vector.md, "Deviations"):
- Part 1 packet = for each season, the publisher notes of its first two narrative episodes
  (episode number order; narrative = the frozen EXCL filter in analyze.py).
- Part 2 segment = a 3-sentence window centred on a transcript sentence that matches INST below.
  Candidate centres are all matching sentences in all episodes, update/Q&A/WCN included;
  windows overlapping an already-drawn window are skipped. Seed 20261101.
- Part 2 verdict uses segments both coders placed in the same category; each coder's own
  verdict is reported beside it. "Response" = any category except "not a response" and "unclear".
- P1/P2: one-sided permutation test (10,000 shuffles) of mean rate, DOWN-INST vs all other
  coded seasons. P3: analyze.py's R2 statistic with power codes in place of settings.
"""
import csv, glob, json, math, random, re, statistics as st, sys
from collections import Counter, defaultdict

HERE = __file__.rsplit("/", 1)[0] or "."
EXCL = re.compile(r"q-a|qa\b|-qa-|update|bts|wcn|presents|data-points|bonus|trailer|answering|with-dr|black-lives-matter|announcement", re.I)
INST = re.compile(r"\b(police|cops?|detectives?|officers?|courts?|judges?|prosecutors?|district attorney|D\.?A\.?|church leader\w*"
                  r"|elders|pastors?|school|principal|universit\w+|title ix|HR|human resources|command(er|ing officer)?|chain of command"
                  r"|staff|counsel(l)?ors?|CPS|child protective|DHS|social workers?|caseworkers?|doctors?|nurses?|hospital|ER\b"
                  r"|therapists?|psychiatrists?)\b")
CATS = ["inaction or failure", "disbelief", "reversal", "pathologizing", "reputation protection",
        "appropriate response", "not a response", "unclear"]
NEUTRALIZING = CATS[:5]
POWER = ["DOWN-INST", "DOWN-DOM", "INTIMATE", "LATERAL", "MIXED"]

def episodes(d):
    for f in sorted(glob.glob(f"{d}/*.json")):
        e = json.load(open(f))
        m = re.match(r"s(\d+)-?ep?(\d+)?", e["slug"])
        yield e, (int(m.group(1)) if m else None), (int(m.group(2)) if m and m.group(2) else None)

def packet(d, out):
    by = defaultdict(list)
    for e, s, n in episodes(d):
        if s and n is not None and not EXCL.search(e["slug"]) and not EXCL.search(e.get("title", "")):
            by[s].append((n, e["title"], re.sub(r"\s+", " ", e.get("notes", "")).strip()))
    pk = {s: [{"title": t, "notes": nt} for _, t, nt in sorted(v)[:2]] for s, v in sorted(by.items())}
    json.dump(pk, open(out, "w"), indent=1)
    print(len(pk), "seasons in packet")

def sample(d, out, n=200, seed=20261101):
    cands = []
    for e, s, _ in episodes(d):
        sents = [t for _, t in e.get("segments", [])] or re.split(r"(?<=[.?!])\s+", e["text"])
        for i, t in enumerate(sents):
            if INST.search(t):
                cands.append((e["slug"], i, sents))
    rng = random.Random(seed); rng.shuffle(cands); taken = defaultdict(set); seg = []
    for slug, i, sents in cands:
        if any(j in taken[slug] for j in (i - 1, i, i + 1)):
            continue
        taken[slug].update((i - 1, i, i + 1))
        seg.append({"id": len(seg) + 1, "episode": slug, "text": " ".join(sents[max(0, i - 1): i + 2])})
        if len(seg) == n:
            break
    json.dump({"n_candidates": len(cands), "seed": seed, "segments": seg}, open(out, "w"), indent=1)
    print(len(cands), "candidate centres;", len(seg), "segments drawn")

def frozen_rates():
    rows = list(csv.DictReader(open(f"{HERE}/results/season_rates.csv")))
    names = [k for k in rows[0] if k not in ("season", "setting", "n_eps", "words", "label")]
    cmean = next(r for r in rows if r["season"] == "control_mean")
    R = {int(r["season"]): {k: float(r[k]) for k in names} for r in rows if r["season"].isdigit()}
    return R, names, {k: float(cmean[k]) for k in names}

def perm_mean(vals, groups, target, rng, n=10000):
    a = [v for v, g in zip(vals, groups) if g == target]; b = [v for v, g in zip(vals, groups) if g != target]
    obs = st.mean(a) - st.mean(b); labs = list(groups); ge = 0
    for _ in range(n):
        rng.shuffle(labs)
        a2 = [v for v, g in zip(vals, labs) if g == target]; b2 = [v for v, g in zip(vals, labs) if g != target]
        ge += (st.mean(a2) - st.mean(b2)) >= obs
    return obs, (ge + 1) / (n + 1), len(a), len(b)

def part1(codes_csv):
    R, names, cmean = frozen_rates()
    code = {int(r["season"]): r["code"].strip() for r in csv.DictReader(open(codes_csv)) if r["code"].strip() in POWER}
    seasons = [s for s in sorted(R) if s in code]
    rng = random.Random(20261101); out = {"n_coded": len(seasons), "codes": Counter(code[s] for s in seasons)}
    for pid, k in (("P1", "omnipotence"), ("P2", "institutional")):
        d, p, na, nb = perm_mean([R[s][k] for s in seasons], [code[s] for s in seasons], "DOWN-INST", rng)
        out[pid] = {"function": k, "diff_DOWN-INST_minus_rest": round(d, 3), "p_one_sided": round(p, 4), "n_DOWN-INST": na, "n_rest": nb,
                    "verdict": "not refuted" if p < 0.05 else "REFUTED (p >= 0.05)"}
    X = {s: [math.log((R[s][k] + 0.5) / (cmean[k] + 0.5)) for k in names] for s in seasons}
    mu = [st.mean(X[s][j] for s in seasons) for j in range(len(names))]
    sd = [st.pstdev([X[s][j] for s in seasons]) or 1 for j in range(len(names))]
    Z = {s: [(X[s][j] - mu[j]) / sd[j] for j in range(len(names))] for s in seasons}
    def r2(lab):
        tot = sum(sum(v * v for v in Z[s]) for s in seasons); g = defaultdict(list)
        for s in seasons: g[lab[s]].append(s)
        w = 0.0
        for grp in g.values():
            c = [st.mean(Z[s][j] for s in grp) for j in range(len(names))]
            w += sum(sum((Z[s][j] - c[j]) ** 2 for j in range(len(names))) for s in grp)
        return 1 - w / tot
    obs = r2(code); labs = [code[s] for s in seasons]; ge = 0
    for _ in range(10000):
        rng.shuffle(labs); ge += r2(dict(zip(seasons, labs))) >= obs
    p = (ge + 1) / 10001
    out["P3"] = {"R2_power": round(obs, 3), "p": round(p, 4), "verdict": "REFUTED (p < 0.05)" if p < 0.05 else "not refuted"}
    print(json.dumps(out, indent=1, default=dict))
    return out

def kappa(a, b):
    n = len(a); po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b); pe = sum(ca[c] * cb[c] for c in set(a) | set(b)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0

def verdict(cats):
    resp = [c for c in cats if c in NEUTRALIZING or c == "appropriate response"]
    app = sum(c == "appropriate response" for c in resp)
    share = app / len(resp) if resp else float("nan")
    return {"n_response": len(resp), "appropriate": app, "neutralizing": len(resp) - app, "appropriate_share": round(share, 3),
            "prediction (neutralizing > appropriate)": len(resp) - app > app,
            "C2 refuted in corpus (appropriate >= 40%)": share >= 0.40, "by_category": Counter(resp)}

def part2(a_csv, b_csv):
    A = {int(r["id"]): r["category"].strip() for r in csv.DictReader(open(a_csv))}
    B = {int(r["id"]): r["category"].strip() for r in csv.DictReader(open(b_csv))}
    ids = sorted(set(A) & set(B)); a = [A[i] for i in ids]; b = [B[i] for i in ids]
    agreed = [x for x, y in zip(a, b) if x == y]
    out = {"n": len(ids), "kappa": round(kappa(a, b), 3), "agreement": round(len(agreed) / len(ids), 3),
           "agreed_segments": verdict(agreed), "coder_A": verdict(a), "coder_B": verdict(b)}
    print(json.dumps(out, indent=1, default=dict))
    return out

if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"packet": packet, "sample": sample, "part1": part1, "part2": part2}[cmd](*args)

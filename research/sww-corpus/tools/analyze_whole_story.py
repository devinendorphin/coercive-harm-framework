"""Whole-story test analysis (follows whole_story/ANALYSIS-PLAN.md and DEVIATIONS.md D3-D6).

  python3 -I analyze_whole_story.py <results/whole_story dir>

History: the first version (commit before any coder output existed) read only coders A/B and
POS/NEG. This version (2026-11-11, written before any headline was computed) keeps every rule of
that version unchanged -- ind(), wilson(), kappa(), own(), the agreed() rules for each prediction,
the band and the decision rule -- and adds what D3-D6 require:
  * three sets: pooled (S17 = Claude pair), Claude-only, Codex-only; plus pooled with S17 = Codex
  * cross-season repeats counted per season (as coded) and once (D6.1; cross_season_repeats.csv)
  * the 21 self-contradictory Codex records as coded / removed / read by outcome (D6.2)
  * matching_hand.csv now has a `pair` column (season,pair,id1,id2,reason) (D6.3)
  * pooled band = the wider of the Claude and Codex bands (D6.5)
  * the S17 Claude-vs-Codex cross-check (D5, D6.6)
  * quotation-check flags, if <coded>.quotecheck.json files exist (plan: "reported both ways")
Writes matching.csv and summary.json; prints the headline table.
"""
import csv, glob, json, math, os, re, sys
from collections import Counter, defaultdict

D = sys.argv[1]
W2_CODES = {"disbelieved", "blamed_punished_or_counter_accused", "condition_as_dismissal", "protected_itself"}
NON_INST = {"the_person", "family_or_friends", "other_victims", "journalists_podcast_or_virality"}
THRESH = {"W1": 0.40, "W2": 0.30, "W3": 0.50}
CLAUDE_S = [1, 2, 3, 4, 5, 6, 13, 14, 15, 16, 17, 18, 19, 22, 24]
CODEX_S = [7, 8, 9, 10, 11, 12, 17, 20, 21, 23, 25, 26]
SETS = {
    "pooled": [(s, "A", "B") for s in CLAUDE_S] + [(s, "CA", "CB") for s in CODEX_S if s != 17],
    "claude": [(s, "A", "B") for s in CLAUDE_S],
    "codex": [(s, "CA", "CB") for s in CODEX_S],
    "pooled_S17codex": [(s, "A", "B") for s in CLAUDE_S if s != 17] + [(s, "CA", "CB") for s in CODEX_S],
}
FRAMING = {"claude": ([2, 3, 4, 13, 22, 24], "POS", "NEG", ("A", "B")),
           "codex": ([13], "CPOS", "CNEG", ("A", "B"))}   # S13 neutral pair is Claude's (D4)
RANK = {"harmed_by_institution": 0, "not_protected": 1, "partly_protected": 2, "protected": 3}

_cache = {}
def load(season, coder):
    fn = f"{D}/coded/s{season:02d}_{coder}.json"
    if fn not in _cache:
        _cache[fn] = json.load(open(fn)) if os.path.exists(fn) else None
    return _cache[fn]

# ---- quotation-check flags (decisive quotation not found) -------------------------------
QFLAG = defaultdict(set)   # (season, coder, pid) -> {"outcome", "decisive", "contactN", ...} not found
QSTATS = {}
for fn in glob.glob(f"{D}/coded/*.quotecheck.json"):
    b = os.path.basename(fn).split(".")[0]; s, c = int(b[1:3]), b[4:]
    rows = json.load(open(fn)); n = f = 0
    for pid, field, score, where in rows:
        if score == "too-short": continue
        n += 1; f += score >= 0.8
        if score < 0.8: QFLAG[(s, c, pid)].add(field)
    QSTATS[b] = {"found": f, "n": n, "rate": round(f / n, 3) if n else None}

def ind(p, read_by_outcome=False):
    r = (p.get("reached_institution") or "").lower()
    out = p.get("outcome")
    if read_by_outcome and r == "unclear" and out == "never_reached":
        r = "no"
    dec = p.get("decisive_work_by")
    return {
        "reached": r,
        "protected": out == "protected",
        "prot_any": out in ("protected", "partly_protected"),
        "w2": any((c.get("response") in W2_CODES) for c in (p.get("contacts") or [])),
        "w3": None if dec in (None, "unclear", "null", "") else dec in NON_INST,
        "w3_raw": dec,
        "harmed_ever": bool(p.get("harmed_by_institution_ever")),
        "alone": "person_account_alone" in (p.get("evidence_types") or []),
        "outcome": out,
        "central": p.get("role_in_story") == "central_survivor",
        "ncontacts": len(p.get("contacts") or []),
        "reasons": (p.get("never_reached") or {}).get("reasons") or [],
        "w2_contacts": [f"contact{c.get('n')}" for c in (p.get("contacts") or []) if c.get("response") in W2_CODES],
    }

def norm(n):
    n = (n or "").lower()
    n = re.sub(r"\[unnamed\]|\(.*?\)|[^a-z ]", " ", n)
    return " ".join(n.split())

def wilson(k, n, z=1.96):
    if not n: return [None, None]
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return [round(c-h, 3), round(c+h, 3)]

def kappa(pairs):
    pairs = [(a, b) for a, b in pairs if a is not None and b is not None]
    n = len(pairs)
    if not n: return None, None, 0
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n*n)
    return round(po, 3), (round((po-pe)/(1-pe), 3) if pe < 1 else None), n

def own(recs):
    """A coder's own figures on all its own records."""
    reached = [i for i in recs if i["reached"] == "yes"]
    prot = [i for i in reached if i["prot_any"] and i["w3"] is not None]
    known = [i for i in recs if i["reached"] in ("yes", "no")]
    f = {
        "people": len(recs),
        "W1": [sum(i["protected"] for i in reached), len(reached)],
        "W2": [sum(i["w2"] for i in reached), len(reached)],
        "W3": [sum(i["w3"] for i in prot), len(prot)],
        "never_reached": [sum(i["reached"] == "no" for i in known), len(known)],
        "harmed_ever": [sum(i["harmed_ever"] for i in reached), len(reached)],
    }
    for k in ("W1", "W2", "W3", "never_reached", "harmed_ever"):
        a, b = f[k]; f[k] = {"k": a, "n": b, "rate": round(a/b, 3) if b else None, "ci95": wilson(a, b)}
    return f

# ---- inputs fixed before computing -------------------------------------------------------
HAND = defaultdict(list)
for r in csv.DictReader(open(f"{D}/matching_hand.csv")):
    HAND[(int(r["season"]), r["pair"])].append(r)
REPEAT = {}
for r in csv.DictReader(open(f"{D}/cross_season_repeats.csv")):
    b = r["file"]; REPEAT[(int(b[1:3]), b[4:], r["person_id"])] = int(r["home_season"])

def contradictory(p):
    r = (p.get("reached_institution") or "").lower(); o = p.get("outcome")
    return (r != "no" and o == "never_reached") or (r == "no" and o != "never_reached")

def records(s, c, set_seasons, repeats, contra):
    d = load(s, c)
    if not d: return {}
    out = {}
    for p in d["persons"]:
        if repeats == "once" and REPEAT.get((s, c, p["person_id"])) in set_seasons: continue
        if contra == "without" and contradictory(p): continue
        out[p["person_id"]] = p
    return out

def match(s, c1, c2, P1, P2, rows=None):
    """Hand matches first (names/roles/harms only), then unique exact names. Never uses codes."""
    pairs, used1, used2 = [], set(), set()
    for r in HAND[(s, f"{c1}-{c2}")]:
        if r["id1"]: used1.add(r["id1"])
        if r["id2"]: used2.add(r["id2"])
        if r["id1"] in P1 and r["id2"] in P2:
            pairs.append((P1[r["id1"]], P2[r["id2"]]))
            if rows is not None: rows.append([s, f"{c1}-{c2}", r["id1"], r["id2"], "hand", r["reason"]])
        elif rows is not None:
            rows.append([s, f"{c1}-{c2}", r["id1"], r["id2"], "hand-unmatched", r["reason"]])
    n1, n2 = defaultdict(list), defaultdict(list)
    for i, p in P1.items():
        if i not in used1: n1[norm(p["name"])].append(i)
    for i, p in P2.items():
        if i not in used2: n2[norm(p["name"])].append(i)
    for n in n1:
        if n and len(n1[n]) == 1 and len(n2.get(n, [])) == 1:
            a, b = n1[n][0], n2[n][0]; used1.add(a); used2.add(b)
            pairs.append((P1[a], P2[b]))
            if rows is not None: rows.append([s, f"{c1}-{c2}", a, b, "auto-name", n])
    if rows is not None:
        for i in P1:
            if i not in used1: rows.append([s, f"{c1}-{c2}", i, "", "unmatched", P1[i]["name"]])
        for i in P2:
            if i not in used2: rows.append([s, f"{c1}-{c2}", "", i, "unmatched", P2[i]["name"]])
    return pairs

def qbad(s, c, p, pred, i):
    """True if the quotation that decides this record for this prediction was not found."""
    f = QFLAG.get((s, c, p["person_id"]), set())
    if not f: return False
    if pred == "W1": return "outcome" in f
    if pred == "W2": return bool(i["w2"]) and all(x in f for x in i["w2_contacts"])
    if pred == "W3": return "decisive" in f
    return False

def agreed(M, pred, subset=lambda ia, ib: True, drop_q=False):
    num = den = dis = 0
    for s, ia, ib, a, b, c1, c2 in M:
        if not subset(ia, ib): continue
        if drop_q and (qbad(s, c1, a, pred[:2], ia) or qbad(s, c2, b, pred[:2], ib)): continue
        if pred == "W1":
            if not (ia["reached"] == ib["reached"] == "yes"): continue
            x, y = ia["protected"], ib["protected"]
        elif pred == "W2":
            if not (ia["reached"] == ib["reached"] == "yes"): continue
            x, y = ia["w2"], ib["w2"]
        elif pred == "W3":
            if not (ia["prot_any"] and ib["prot_any"]): continue
            if ia["w3"] is None or ib["w3"] is None: continue
            x, y = ia["w3"], ib["w3"]
        elif pred == "W3_protected_only":
            if not (ia["outcome"] == ib["outcome"] == "protected"): continue
            if ia["w3"] is None or ib["w3"] is None: continue
            x, y = ia["w3"], ib["w3"]
        elif pred == "never_reached":
            if ia["reached"] not in ("yes", "no") or ib["reached"] not in ("yes", "no"): continue
            x, y = ia["reached"] == "no", ib["reached"] == "no"
        elif pred == "harmed_ever":
            if not (ia["reached"] == ib["reached"] == "yes"): continue
            x, y = ia["harmed_ever"], ib["harmed_ever"]
        if x == y: den += 1; num += x
        else: dis += 1
    return {"k": num, "n": den, "rate": round(num/den, 3) if den else None, "disagreed": dis, "ci95": wilson(num, den)}

PREDS = ("W1", "W2", "W3", "W3_protected_only", "never_reached", "harmed_ever")

def run(setname, repeats="per_season", contra="as_coded", read_by_outcome=False, full=False, rows=None):
    spec = SETS[setname]; set_seasons = {s for s, _, _ in spec}
    M, allrec, finding = [], defaultdict(list), defaultdict(lambda: [0, 0, 0])
    for s, c1, c2 in spec:
        P1 = records(s, c1, set_seasons, repeats, contra); P2 = records(s, c2, set_seasons, repeats, contra)
        for c, P in ((c1, P1), (c2, P2)):
            allrec[c] += [dict(ind(p, read_by_outcome), season=s) for p in P.values()]
        pr = match(s, c1, c2, P1, P2, rows)
        M += [(s, ind(a, read_by_outcome), ind(b, read_by_outcome), a, b, c1, c2) for a, b in pr]
        fam = "claude" if c1 == "A" else "codex"
        finding[fam][0] += len(pr); finding[fam][1] += len(P1); finding[fam][2] += len(P2)
    out = {"seasons": sorted(set_seasons), "matched_people": len(M),
           "people_coded": {c: len(v) for c, v in allrec.items()},
           "headline": {k: agreed(M, k) for k in PREDS}}
    if not full: return out
    out["headline_without_unfound_quotes"] = {k: agreed(M, k, drop_q=True) for k in ("W1", "W2", "W3")}
    out["central_only"] = {k: agreed(M, k, lambda ia, ib: ia["central"] and ib["central"]) for k in ("W1", "W2", "W3", "never_reached")}
    out["coder_own"] = {c: own(v) for c, v in allrec.items()}
    out["by_season"] = {}
    for s in sorted(set_seasons):
        Ms = [m for m in M if m[0] == s]
        out["by_season"][s] = {k: agreed(Ms, k) for k in ("W1", "W2", "W3", "never_reached")}
        out["by_season"][s]["people"] = {c: sum(1 for r in v if r["season"] == s) for c, v in allrec.items()}
        out["by_season"][s]["matched"] = len(Ms)
    out["agreement"] = agreement(M, finding)
    rs = defaultdict(Counter)
    for c, v in allrec.items():
        for r in v:
            if r["reached"] == "no": rs[c].update(r["reasons"])
    for _, ia, ib, _, _, _, _ in M:
        if ia["reached"] == ib["reached"] == "no":
            rs["both"].update(set(ia["reasons"]) & set(ib["reasons"]))
    out["never_reached_reasons"] = {k: dict(v.most_common()) for k, v in rs.items()}
    out["never_reached_people_both"] = sum(1 for _, ia, ib, _, _, _, _ in M if ia["reached"] == ib["reached"] == "no")
    om = {}
    for s, c1, c2 in spec:
        for c in (c1, c2):
            d = load(s, c) or {}
            L = d.get("others_mentioned") or []
            nums = [o.get("count_stated") for o in L if isinstance(o.get("count_stated"), (int, float))]
            om.setdefault(s, {})[c] = {"entries": len(L), "stated_numbers_sum": sum(nums), "entries_with_number": len(nums),
                                       "reached": dict(Counter(o.get("reached_institution") for o in L))}
    out["others_mentioned"] = om
    return out

def agreement(M, finding=None):
    ag = {}
    ag["reached"] = kappa([(ia["reached"], ib["reached"]) for _, ia, ib, *_ in M])
    ag["outcome"] = kappa([(ia["outcome"], ib["outcome"]) for _, ia, ib, *_ in M])
    ag["W1_indicator"] = kappa([(ia["protected"], ib["protected"]) for _, ia, ib, *_ in M if ia["reached"] == ib["reached"] == "yes"])
    ag["W2_indicator"] = kappa([(ia["w2"], ib["w2"]) for _, ia, ib, *_ in M if ia["reached"] == ib["reached"] == "yes"])
    ag["W3_indicator"] = kappa([(ia["w3"], ib["w3"]) for _, ia, ib, *_ in M if ia["prot_any"] and ib["prot_any"]])
    ag["harmed_ever"] = kappa([(ia["harmed_ever"], ib["harmed_ever"]) for _, ia, ib, *_ in M])
    ag["account_alone"] = kappa([(ia["alone"], ib["alone"]) for _, ia, ib, *_ in M])
    res = {k: dict(zip(("pct_agree", "kappa", "n"), v)) for k, v in ag.items()}
    n1 = sum(1 for _ in M)
    res["contacts_per_person_matched"] = {
        "coder1": round(sum(ia["ncontacts"] for _, ia, *_ in M) / max(n1, 1), 2),
        "coder2": round(sum(ib["ncontacts"] for _, _, ib, *_ in M) / max(n1, 1), 2)}
    if finding:
        res["person_finding"] = {f: {"found_by_both": v[0], "coder1_total": v[1], "coder2_total": v[2],
                                     "rate": round(v[0] / (v[1] + v[2] - v[0]), 3) if v[1] + v[2] else None}
                                 for f, v in finding.items()}
    return res

# ---- framing band ---------------------------------------------------------------------------
def framing():
    fr = {}
    for fam, (seasons, pos, neg, neut) in FRAMING.items():
        recs = defaultdict(list)
        for s in seasons:
            for c in (pos, neg) + neut:
                d = load(s, c)
                if d: recs[c] += [ind(p) for p in d["persons"]]
        o = {c: own(recs[c]) for c in recs}
        band = {}
        for k in ("W1", "W2", "W3", "never_reached"):
            a, b = o[pos][k]["rate"], o[neg][k]["rate"]
            band[k] = round(abs(a - b), 3) if a is not None and b is not None else None
        fr[fam] = {"seasons": seasons, "own": o, "band": band}
    fr["pooled"] = {"band": {k: max(fr["claude"]["band"][k], fr["codex"]["band"][k]) for k in fr["claude"]["band"]}}
    return fr

def decide(headline, band):
    dec = {}
    for k, t in THRESH.items():
        h = headline[k]["rate"]
        if h is None or band.get(k) is None: dec[k] = None; continue
        dist = abs(h - t)
        verdict = ("refuted" if (h >= t if k == "W1" else h < t) else "not refuted")
        dec[k] = {"headline": h, "threshold": t, "distance": round(dist, 3), "band": band[k],
                  "verdict": verdict if band[k] <= dist else "not decided by this method"}
    return dec

# ---- S17 cross-check (D5) ---------------------------------------------------------------------
def s17():
    out = {"own": {}}
    for c in ("A", "B", "CA", "CB"):
        out["own"][c] = own([ind(p) for p in load(17, c)["persons"]])
    allM, direction = [], Counter()
    for c1 in ("A", "B"):
        for c2 in ("CA", "CB"):
            P1 = {p["person_id"]: p for p in load(17, c1)["persons"]}
            P2 = {p["person_id"]: p for p in load(17, c2)["persons"]}
            for a, b in match(17, c1, c2, P1, P2):
                ia, ib = ind(a), ind(b)
                allM.append((17, ia, ib, a, b, c1, c2))
                if ia["reached"] == ib["reached"] == "yes":
                    ra, rb = RANK.get(ia["outcome"]), RANK.get(ib["outcome"])
                    if ra is not None and rb is not None:
                        direction["outcome: Claude worse for the person" if ra < rb else
                                  "outcome: Codex worse for the person" if rb < ra else "outcome: same"] += 1
                    if ia["w2"] != ib["w2"]:
                        direction["W2: only Claude finds a failure response" if ia["w2"] else "W2: only Codex finds one"] += 1
                    else:
                        direction["W2: same"] += 1
                if ia["reached"] != ib["reached"]:
                    direction[f"reached: Claude {ia['reached']} / Codex {ib['reached']}"] += 1
    out["cross_agreement"] = agreement(allM)
    out["cross_direction"] = dict(direction)
    out["within"] = {}
    for c1, c2 in (("A", "B"), ("CA", "CB")):
        P1 = {p["person_id"]: p for p in load(17, c1)["persons"]}; P2 = {p["person_id"]: p for p in load(17, c2)["persons"]}
        M = [(17, ind(a), ind(b), a, b, c1, c2) for a, b in match(17, c1, c2, P1, P2)]
        out["within"][f"{c1}-{c2}"] = {"agreement": agreement(M), "headline": {k: agreed(M, k) for k in ("W1", "W2", "W3", "never_reached")}}
    return out

if __name__ == "__main__":
    summary = {"quote_check": QSTATS}
    rows = []
    fr = framing(); summary["framing"] = fr
    for name in SETS:
        summary[name] = run(name, full=True, rows=rows if name in ("pooled", "codex") else None)
        band = fr["pooled" if name.startswith("pooled") else name]["band"]
        summary[name]["decision"] = decide(summary[name]["headline"], band)
        summary[name]["variants"] = {}
        for rep in ("per_season", "once"):
            for con in ("as_coded", "without"):
                v = run(name, rep, con)
                v["decision"] = decide(v["headline"], band)
                summary[name]["variants"][f"{rep}/{con}"] = v
        summary[name]["variants"]["never_reached_read_by_outcome"] = run(name, read_by_outcome=True)["headline"]["never_reached"]
    summary["S17_crosscheck"] = s17()
    seen, uniq = set(), []
    for r in rows:
        k = tuple(map(str, r))
        if k not in seen: seen.add(k); uniq.append(r)
    with open(f"{D}/matching.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["season", "pair", "id1", "id2", "method", "reason_or_name"]); w.writerows(uniq)
    json.dump(summary, open(f"{D}/summary.json", "w"), indent=1)
    for name in SETS:
        print(f"\n== {name}: {summary[name]['matched_people']} matched people")
        for vk, v in summary[name]["variants"].items():
            if not isinstance(v, dict) or "headline" not in v: continue
            print(f"  {vk:22s}", "  ".join(f"{k} {v['headline'][k]['k']}/{v['headline'][k]['n']}={v['headline'][k]['rate']}"
                                         for k in ("W1", "W2", "W3", "never_reached")),
                  "|", {k: (d or {}).get("verdict") for k, d in v["decision"].items()})
    print("\nbands", {k: fr[k]["band"] for k in ("claude", "codex", "pooled")})

"""Whole-story test analysis (follows whole_story/ANALYSIS-PLAN.md).

  python3 -I analyze_whole_story.py <results/whole_story dir>

Reads coded/sNN_{A,B,POS,NEG}.json and matching_hand.csv (season,A_id,B_id,reason; B_id or A_id
may be empty for a record judged to have no counterpart). Writes matching.csv and summary.json.
Written before any coder output existed.
"""
import csv, glob, json, math, os, re, sys
from collections import Counter, defaultdict

D = sys.argv[1]
W2_CODES = {"disbelieved", "blamed_punished_or_counter_accused", "condition_as_dismissal", "protected_itself"}
NON_INST = {"the_person", "family_or_friends", "other_victims", "journalists_podcast_or_virality"}
THRESH = {"W1": 0.40, "W2": 0.30, "W3": 0.50}

def load(season, coder):
    fn = f"{D}/coded/s{season:02d}_{coder}.json"
    return json.load(open(fn)) if os.path.exists(fn) else None

def ind(p):
    r = (p.get("reached_institution") or "").lower()
    out = p.get("outcome")
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
        a, b = f[k]; f[k] = {"k": a, "n": b, "rate": round(a/b, 3) if b else None}
    return f

seasons = sorted({int(re.search(r"s(\d+)_", os.path.basename(p)).group(1)) for p in glob.glob(f"{D}/coded/s*_A.json")})
hand = defaultdict(list)
if os.path.exists(f"{D}/matching_hand.csv"):
    for r in csv.DictReader(open(f"{D}/matching_hand.csv")):
        hand[int(r["season"])].append(r)

matched, match_rows, allrec = [], [], defaultdict(list)
for s in seasons:
    A, B = load(s, "A"), load(s, "B")
    if not (A and B): continue
    pa = {p["person_id"]: p for p in A["persons"]}; pb = {p["person_id"]: p for p in B["persons"]}
    for c, P in (("A", pa), ("B", pb)):
        allrec[c] += [dict(ind(p), season=s) for p in P.values()]
    used_a, used_b = set(), set()
    for r in hand[s]:
        if r["A_id"]: used_a.add(r["A_id"])
        if r["B_id"]: used_b.add(r["B_id"])
        if r["A_id"] and r["B_id"]:
            matched.append((s, pa[r["A_id"]], pb[r["B_id"]])); match_rows.append([s, r["A_id"], r["B_id"], "hand", r["reason"]])
        else:
            match_rows.append([s, r["A_id"], r["B_id"], "hand-unmatched", r["reason"]])
    na = defaultdict(list); nb = defaultdict(list)
    for i, p in pa.items():
        if i not in used_a: na[norm(p["name"])].append(i)
    for i, p in pb.items():
        if i not in used_b: nb[norm(p["name"])].append(i)
    for n in na:
        if n and len(na[n]) == 1 and len(nb.get(n, [])) == 1:
            a, b = na[n][0], nb[n][0]; used_a.add(a); used_b.add(b)
            matched.append((s, pa[a], pb[b])); match_rows.append([s, a, b, "auto-name", n])
    for i in pa:
        if i not in used_a: match_rows.append([s, i, "", "unmatched", pa[i]["name"]])
    for i in pb:
        if i not in used_b: match_rows.append([s, "", i, "unmatched", pb[i]["name"]])

with open(f"{D}/matching.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["season", "A_id", "B_id", "method", "reason_or_name"]); w.writerows(match_rows)

M = [(s, ind(a), ind(b), a, b) for s, a, b in matched]
def agreed(pred, subset=lambda ia, ib: True):
    num = den = dis = 0
    for s, ia, ib, a, b in M:
        if not subset(ia, ib): continue
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

summary = {"seasons": seasons, "matched_people": len(M)}
summary["headline"] = {k: agreed(k) for k in ("W1", "W2", "W3", "W3_protected_only", "never_reached", "harmed_ever")}
summary["central_only"] = {k: agreed(k, lambda ia, ib: ia["central"] and ib["central"]) for k in ("W1", "W2", "W3", "never_reached")}
summary["coder_own"] = {c: own(allrec[c]) for c in ("A", "B")}
summary["by_season"] = {}
for s in seasons:
    Ms = [m for m in M if m[0] == s]
    keep = M; M = Ms
    summary["by_season"][s] = {k: agreed(k) for k in ("W1", "W2", "W3", "never_reached")}
    summary["by_season"][s]["people_A"] = sum(1 for r in allrec["A"] if r["season"] == s)
    summary["by_season"][s]["people_B"] = sum(1 for r in allrec["B"] if r["season"] == s)
    summary["by_season"][s]["matched"] = len(Ms)
    M = keep

ag = {}
ag["reached"] = kappa([(ia["reached"], ib["reached"]) for _, ia, ib, _, _ in M])
ag["outcome"] = kappa([(ia["outcome"], ib["outcome"]) for _, ia, ib, _, _ in M])
ag["W2_indicator"] = kappa([(ia["w2"], ib["w2"]) for _, ia, ib, _, _ in M if ia["reached"] == ib["reached"] == "yes"])
ag["W3_indicator"] = kappa([(ia["w3"], ib["w3"]) for _, ia, ib, _, _ in M if ia["prot_any"] and ib["prot_any"]])
ag["harmed_ever"] = kappa([(ia["harmed_ever"], ib["harmed_ever"]) for _, ia, ib, _, _ in M])
ag["account_alone"] = kappa([(ia["alone"], ib["alone"]) for _, ia, ib, _, _ in M])
na, nb = len(allrec["A"]), len(allrec["B"])
ag["person_finding"] = {"found_by_both": len(M), "A_total": na, "B_total": nb,
                        "rate": round(len(M) / (na + nb - len(M)), 3) if na + nb else None}
ag["contacts_per_person"] = {"A": round(sum(r["ncontacts"] for r in allrec["A"]) / max(na, 1), 2),
                             "B": round(sum(r["ncontacts"] for r in allrec["B"]) / max(nb, 1), 2)}
summary["agreement"] = {k: (dict(zip(("pct_agree", "kappa", "n"), v)) if isinstance(v, tuple) else v) for k, v in ag.items()}

# never-reached reasons
rs = {"A": Counter(), "B": Counter(), "both": Counter()}
for c in ("A", "B"):
    for r in allrec[c]:
        if r["reached"] == "no": rs[c].update(r["reasons"])
for _, ia, ib, _, _ in M:
    if ia["reached"] == ib["reached"] == "no":
        rs["both"].update(set(ia["reasons"]) & set(ib["reasons"]))
summary["never_reached_reasons"] = {k: dict(v.most_common()) for k, v in rs.items()}

# people mentioned but never heard
om = {}
for s in seasons:
    for c in ("A", "B"):
        d = load(s, c)
        if d: om.setdefault(s, {})[c] = [[o.get("description"), o.get("count_stated"), o.get("reached_institution")] for o in d.get("others_mentioned") or []]
summary["others_mentioned"] = om

# framing band
fr = {}
fseasons = [s for s in range(1, 40) if os.path.exists(f"{D}/coded/s{s:02d}_POS.json")]
if fseasons:
    recs = defaultdict(list)
    for s in fseasons:
        for c in ("POS", "NEG", "A", "B"):
            d = load(s, c)
            if d: recs[c] += [ind(p) for p in d["persons"]]
    fr = {"seasons": fseasons, "own": {c: own(recs[c]) for c in recs}}
    band = {}
    for k in ("W1", "W2", "W3", "never_reached"):
        a, b = fr["own"]["POS"][k]["rate"], fr["own"]["NEG"][k]["rate"]
        band[k] = round(abs(a - b), 3) if a is not None and b is not None else None
    fr["band"] = band
    dec = {}
    for k, t in THRESH.items():
        h = summary["headline"][k]["rate"]
        if h is None or band.get(k) is None: dec[k] = None; continue
        dist = abs(h - t)
        verdict = ("refuted" if (h >= t if k == "W1" else h < t) else "not refuted")
        dec[k] = {"headline": h, "threshold": t, "distance": round(dist, 3), "band": band[k],
                  "verdict": verdict if band[k] <= dist else "not decided by this method"}
    fr["decision"] = dec
summary["framing"] = fr
json.dump(summary, open(f"{D}/summary.json", "w"), indent=1)
print(json.dumps({k: summary[k] for k in ("matched_people", "headline", "agreement")}, indent=1))
if fr: print(json.dumps(fr.get("decision"), indent=1), json.dumps(fr.get("band")))

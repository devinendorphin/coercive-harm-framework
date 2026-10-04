#!/usr/bin/env python3
"""Something Was Wrong corpus test of the low-variance / self-similarity claim.

Lexicon and thresholds are frozen by preregistration.md (committed before results).
Usage: python3 analyze.py <sww_json_dir> <control_json_dir> <settings.csv> <out_dir>
Each JSON file: {"slug","title","notes","text"} as written by the fetcher.
"""
import csv, glob, json, math, os, random, re, statistics as st, sys
from collections import defaultdict

F = lambda p: re.compile(p, re.I)
FUNCS = {
    "isolation": F(r"\b(cut (me|her|him|them|us) off|isolat\w*|wouldn'?t let (me|her|him|them) (see|talk|go|leave)"
                   r"|didn'?t want (me|her|him|them) (to see|seeing|talking|hanging|going)|away from (my|her|his|their) (family|friends|parents)"
                   r"|alienat\w* (me|her|him|them) from|no friends|lost (all )?(my|her) friends)"),
    "perception": F(r"\b(lied|lying|liar|made (it|that|this|all of it) up|never happened|you'?re (crazy|insane|imagining|overreacting|too sensitive)"
                    r"|(felt|feel|feeling|going|was) crazy|question(ed|ing)? (my|her|his|their) (own )?(reality|memory|sanity|judgment)"
                    r"|rewr(o|i)te\w* history|fabricat\w*|forged|fake[ds]?\b)"),
    "economic": F(r"\b(debt|credit cards?|bank accounts?|loans?|paychecks?|took (my|her|his|their) (money|car|keys|phone|savings)"
                  r"|stole|stealing|steal\b|financial(ly)?|drained|sleep[- ]deprived|exhausted|depend(ent|ence) on)"),
    "threats": F(r"\b(threat\w*|kill (me|you|her|him|them|myself|himself|herself)|guns?\b|weapons?|scared for my life"
                 r"|afraid (he|she|they) (would|was going)|stalk\w*|follow(ed|ing) (me|her|him|them)|intimidat\w*)"),
    "reward": F(r"\b(gifts?|flowers|apologi\w*|so sweet|charming|swept (me|her) off|promised|showered (me|her))"),
    "omnipotence": F(r"\b(no ?one (would|will|is going to|was going to) believe|nobody (would|will|was going to) believe|untouchable"
                     r"|get away with|got away with|connections|above the law|knew everyone|so powerful)"),
    "degradation": F(r"\b(humiliat\w*|degrad\w*|worthless|stupid|called (me|her|him|them) (a |names)|belittl\w*|insult\w*|ashamed|mock(ed|ing))"),
    "microreg": F(r"\b(control(led|ling)? (what|where|who|how|when|my|her|everything)|track(ed|ing)? (my|her|me|him)"
                  r"|(checked|check|went through|read|reading|monitor\w*) (my|her|his) (phone|texts|messages|email)|passwords?"
                  r"|my location|had to ask (permission|him|her)|permission to)"),
    "reversal": F(r"\b(play(ed|ing|s)? the victim|(i|she|he) was the (abuser|problem|crazy one)|turned it (around|back) on|blamed (me|her|him|them)"
                  r"|it'?s (all )?your fault|(was|is) my fault|accused (me|her|him|them) of|(make|made|making) (me|her) (look|seem|sound) crazy"
                  r"|smear\w*|discredit\w*)"),
}
INST = F(r"\b(police|cops?|detectives?|officers?|courts?|judges?|prosecutors?|district attorney|HR|human resources|elders"
         r"|church leader\w*|pastors?|bishop|school|principal|administration|university|the board|title ix)\b")
FAIL = F(r"(didn'?t (believe|do anything|help|take it seriously|care)|nothing (happened|was done|they could do|we can do)|dismiss\w*"
         r"|ignor\w*|closed the case|no charges|declined to|refused to|laughed (at|it off)|swept (it )?under|covered (it )?up|protected him)")
LABEL = F(r"\b(gaslight\w*|gas lit|love ?bomb\w*|darvo|narcissis\w*|coercive control|trauma bond\w*|flying monkeys?|grooming|groomed"
          r"|red flags?|sociopath\w*|psychopath\w*|manipulat\w*)")
EXCL = re.compile(r"q-a|qa\b|-qa-|update|bts|wcn|presents|data-points|bonus|trailer|answering|with-dr|black-lives-matter|announcement", re.I)
NAMES = list(FUNCS) + ["institutional"]

def segs(text):  # machine transcript has no line breaks; ~sentence windows
    return re.split(r"(?<=[.?!])\s+", text)

def counts(text):
    c = {k: len(r.findall(text)) for k, r in FUNCS.items()}
    s = segs(text); c["institutional"] = sum(1 for i in range(len(s)) if INST.search(" ".join(s[i:i+2])) and FAIL.search(" ".join(s[i:i+2])))
    c["label"] = len(LABEL.findall(text)); c["words"] = len(text.split())
    return c

def rate(c, k): return 1e4 * c[k] / max(c["words"], 1)

def spearman(a, b):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0]*len(v)
        for j, i in enumerate(o): r[i] = j
        return r
    ra, rb = rk(a), rk(b); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x-ma)*(y-mb) for x, y in zip(ra, rb)); den = math.sqrt(sum((x-ma)**2 for x in ra)*sum((y-mb)**2 for y in rb))
    return num/den if den else 0.0

def mean_pairwise(profiles):
    ps = list(profiles); v = [spearman(ps[i], ps[j]) for i in range(len(ps)) for j in range(i+1, len(ps))]
    return st.mean(v) if v else float("nan")

def main(swwdir, ctrldir, settings_csv, out):
    os.makedirs(out, exist_ok=True)
    seasons = defaultdict(lambda: {"text": [], "eps": []})
    for f in sorted(glob.glob(f"{swwdir}/*.json")):
        d = json.load(open(f)); m = re.match(r"s(\d+)-?e?p?\d*", d["slug"])
        if not m or EXCL.search(d["slug"]) or EXCL.search(d.get("title", "")) or len(d["text"].split()) < 500:
            continue
        seasons[int(m.group(1))]["text"].append(d["text"]); seasons[int(m.group(1))]["eps"].append(d["slug"])
    S = {k: counts(" ".join(v["text"])) for k, v in seasons.items()}
    for k in S: S[k]["n_eps"] = len(seasons[k]["eps"])
    ctrl = [counts(json.load(open(f))["text"]) for f in sorted(glob.glob(f"{ctrldir}/*.json"))]
    ctrl = [c for c in ctrl if c["words"] >= 500]
    p90 = {k: sorted(rate(c, k) for c in ctrl)[int(0.9*(len(ctrl)-1))] for k in NAMES}
    cmean = {k: st.mean(rate(c, k) for c in ctrl) for k in NAMES + ["label"]}

    # R1 / R5: elevated share
    elev = {k: sum(rate(S[s], k) > p90[k] for s in S) / len(S) for k in NAMES}

    # Settings coded from notes before inspecting rates
    setting = {int(r["season"]): r["setting"] for r in csv.DictReader(open(settings_csv)) if r["season"].isdigit()}
    coded = [s for s in sorted(S) if s in setting]
    def prof(s): return [math.log((rate(S[s], k) + 0.5) / (cmean[k] + 0.5)) for k in NAMES]
    X = {s: prof(s) for s in coded}
    mu = [st.mean(X[s][j] for s in coded) for j in range(len(NAMES))]
    sd = [st.pstdev([X[s][j] for s in coded]) or 1 for j in range(len(NAMES))]
    Z = {s: [(X[s][j]-mu[j])/sd[j] for j in range(len(NAMES))] for s in coded}
    def r2(labels):
        tot = sum(sum(v*v for v in Z[s]) for s in coded); groups = defaultdict(list)
        for s in coded: groups[labels[s]].append(s)
        within = 0.0
        for g in groups.values():
            c = [st.mean(Z[s][j] for s in g) for j in range(len(NAMES))]
            within += sum(sum((Z[s][j]-c[j])**2 for j in range(len(NAMES))) for s in g)
        return 1 - within/tot
    rng = random.Random(20261004)
    obs = r2(setting); labs = [setting[s] for s in coded]; ge = 0
    for _ in range(10000):
        rng.shuffle(labs); ge += r2(dict(zip(coded, labs))) >= obs
    p_r2 = (ge + 1) / 10001

    # R3: profile similarity vs control pseudo-seasons
    def ratio_prof(c): return [(rate(c, k) + 0.5) / (cmean[k] + 0.5) for k in NAMES]
    sww_sim = mean_pairwise([ratio_prof(S[s]) for s in S])
    target = st.median(S[s]["words"] for s in S); null = []
    for _ in range(1000):
        pseudo = []
        for _ in range(len(S)):
            pool = {k: 0 for k in NAMES + ["label", "words"]}
            while pool["words"] < target:
                c = rng.choice(ctrl)
                for k in pool: pool[k] += c[k]
            pseudo.append(ratio_prof(pool))
        null.append(mean_pairwise(pseudo))
    p_r3 = (sum(n >= sww_sim for n in null) + 1) / 1001

    # R4: split at median label rate
    med = st.median(rate(S[s], "label") for s in S)
    lo = [s for s in S if rate(S[s], "label") <= med]; hi = [s for s in S if rate(S[s], "label") > med]
    half = {}
    for nm, grp in (("low_label", lo), ("high_label", hi)):
        half[nm] = {"seasons": sorted(grp), "profile_similarity": mean_pairwise([ratio_prof(S[s]) for s in grp]),
                    "elevated_share": {k: sum(rate(S[s], k) > p90[k] for s in grp)/len(grp) for k in NAMES}}

    res = {"n_seasons": len(S), "n_control_eps": len(ctrl), "control_p90": p90, "control_mean": cmean,
           "elevated_share": elev, "R2_setting_r2": obs, "R2_p": p_r2, "n_coded": len(coded),
           "settings": {s: setting[s] for s in coded},
           "R3_sww_profile_similarity": sww_sim, "R3_null_mean": st.mean(null), "R3_null_p95": sorted(null)[949], "R3_p": p_r3,
           "R4": half}
    json.dump(res, open(f"{out}/results.json", "w"), indent=1)
    with open(f"{out}/season_rates.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["season", "setting", "n_eps", "words"] + NAMES + ["label"])
        for s in sorted(S):
            w.writerow([s, setting.get(s, ""), S[s]["n_eps"], S[s]["words"]] + [round(rate(S[s], k), 2) for k in NAMES + ["label"]])
        w.writerow(["control_mean", "", len(ctrl), ""] + [round(cmean[k], 2) for k in NAMES + ["label"]])
        w.writerow(["control_p90", "", "", ""] + [round(p90[k], 2) for k in NAMES] + [""])
    print(json.dumps({k: v for k, v in res.items() if k not in ("control_p90", "control_mean", "settings")}, indent=1))

if __name__ == "__main__":
    main(*sys.argv[1:5])

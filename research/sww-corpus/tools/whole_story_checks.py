"""Post-hoc checks and disconfirming-test samples for the whole-story test (2026-11-11).

Everything here is POST HOC: written after the first run of analyze_whole_story.py, to test the
headlines, never to replace them (verdict rule: the pre-registered result is the verdict).

  python3 -I whole_story_checks.py <results/whole_story dir> figures
  python3 -I whole_story_checks.py <results/whole_story dir> sample <name> [n] [seed]

Samples are drawn with a fixed seed from the matched people of the pooled set (per season, as
coded), and print both coders' codes beside the quotations they gave, so a reader can judge
whether each code fits its quotation.
"""
import json, os, random, sys
sys.argv = [sys.argv[0], sys.argv[1]] + sys.argv[2:]
D = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze_whole_story as A

def matched(setname="pooled"):
    spec = A.SETS[setname]; ss = {s for s, _, _ in spec}; M = []
    for s, c1, c2 in spec:
        P1 = A.records(s, c1, ss, "per_season", "as_coded"); P2 = A.records(s, c2, ss, "per_season", "as_coded")
        M += [(s, A.ind(a), A.ind(b), a, b, c1, c2) for a, b in A.match(s, c1, c2, P1, P2)]
    return M

def figures():
    out = {}
    for setname in ("pooled", "claude", "codex"):
        M = matched(setname); o = {}
        # (a) leave out records whose role is "other" in either coder (bystanders, historical figures)
        sub = lambda ia, ib, a, b: a.get("role_in_story") != "other" and b.get("role_in_story") != "other"
        Mo = [m for m in M if sub(*m[1:5])]
        o["without_role_other"] = {k: A.agreed(Mo, k) for k in ("W1", "W2", "W3", "never_reached")}
        # (b) W1 if a person who died, or whose harm was ended by something else, counted as protected
        #     whenever the perpetrator was convicted (the reading D1.2 ruled out)
        def w1alt(m):
            s, ia, ib, a, b, *_ = m
            f = lambda i, p: i["protected"] or (p.get("perpetrator_convicted") == "yes" and i["outcome"] == "not_protected")
            return f(ia, a), f(ib, b)
        num = den = 0
        for m in M:
            if m[1]["reached"] == m[2]["reached"] == "yes":
                x, y = w1alt(m)
                if x == y: den += 1; num += x
        o["W1_if_conviction_counts_as_protection"] = {"k": num, "n": den, "rate": round(num / den, 3) if den else None}
        # (c) W1 with partly_protected counted as protected
        num = den = 0
        for s, ia, ib, *_ in M:
            if ia["reached"] == ib["reached"] == "yes":
                x, y = ia["prot_any"], ib["prot_any"]
                if x == y: den += 1; num += x
        o["W1_counting_partly_protected"] = {"k": num, "n": den, "rate": round(num / den, 3) if den else None}
        # (d) share of each coder's people NOT shown to reach an institution (reached != yes)
        fam = {"pooled": ("A", "B", "CA", "CB"), "claude": ("A", "B"), "codex": ("CA", "CB")}[setname]
        spec = A.SETS[setname]; ss = {s for s, _, _ in spec}; d = {}
        for s, c1, c2 in spec:
            for c in (c1, c2):
                for p in A.records(s, c, ss, "per_season", "as_coded").values():
                    r = p.get("reached_institution"); d.setdefault(c, [0, 0, 0, 0])
                    d[c][0] += 1; d[c][1] += r == "yes"; d[c][2] += r == "no"; d[c][3] += r == "unclear"
        z = {}
        for s_, c1, c2 in spec:
            for c in (c1, c2):
                for p in A.records(s_, c, ss, "per_season", "as_coded").values():
                    if p.get("reached_institution") == "unclear":
                        z.setdefault(c, [0, 0]); z[c][0] += 1; z[c][1] += not (p.get("contacts") or [])
        o["reached_unclear_with_no_contact_recorded"] = {c: {"unclear": v[0], "no_contacts": v[1]} for c, v in z.items()}
        o["reached_values_per_coder"] = {c: {"people": v[0], "yes": v[1], "no": v[2], "unclear": v[3],
                                             "not_shown_to_reach": round((v[2] + v[3]) / v[0], 3)} for c, v in d.items()}
        # (e) how often a coder's notes on a contact without a W2 code mention a W2-type response
        #     (instructions: pick the most direct code, mention the other in notes) -- for reading only
        kw = ("disbeli", "didn't believe", "did not believe", "blam", "counter", "dismiss", "cover", "conceal", "protect itself", "protected itself", "mental health", "hysteric")
        cand = 0
        for s, ia, ib, a, b, *_ in M:
            if ia["reached"] == ib["reached"] == "yes" and not ia["w2"] and not ib["w2"]:
                txt = " ".join((c.get("notes") or "") + " " + (c.get("what_institution_did") or "") for p in (a, b) for c in p.get("contacts") or []).lower()
                cand += any(k in txt for k in kw)
        o["W2_agreed_no_with_W2_words_in_notes"] = cand
        # (f) leave one season out: range of each headline and verdicts it produces
        fr = A.framing(); band = fr["pooled" if setname.startswith("pooled") else setname]["band"]
        loo = {}
        for k in ("W1", "W2", "W3"):
            vals = []
            for s in sorted({m[0] for m in M}):
                h = A.agreed([m for m in M if m[0] != s], k)
                v = A.decide({kk: (h if kk == k else {"rate": None}) for kk in A.THRESH}, band)[k]
                vals.append((s, h["rate"], v["verdict"] if v else None))
            loo[k] = {"min": min(vals, key=lambda x: x[1]), "max": max(vals, key=lambda x: x[1]),
                      "verdicts": dict(__import__("collections").Counter(v for _, _, v in vals))}
        o["leave_one_season_out"] = loo
        out[setname] = o
    print(json.dumps(out, indent=1))
    json.dump(out, open(f"{D}/posthoc_checks.json", "w"), indent=1)

def show(m, full=False):
    s, ia, ib, a, b, c1, c2 = m
    print(f"\n### S{s} {c1}:{a['person_id']} / {c2}:{b['person_id']}  {a['name'][:50]}  [{a.get('role_in_story')}]")
    for lab, p, i in ((c1, a, ia), (c2, b, ib)):
        print(f"  [{lab}] reached={p.get('reached_institution')} outcome={p.get('outcome')} decisive={p.get('decisive_work_by')} W2={i['w2']} died={p.get('deceased')} convicted={p.get('perpetrator_convicted')}")
        for c in p.get("contacts") or []:
            print(f"     c{c.get('n')} {c.get('institution_type')}/{c.get('response')}: {(c.get('quote') or '')[:260]!r}")
            if full and c.get("notes"): print(f"        notes: {c['notes'][:200]!r}")
        print(f"     OUTCOME: {(p.get('outcome_quote') or '')[:300]!r}")
        if p.get("decisive_work_quote"): print(f"     DECISIVE: {p['decisive_work_quote'][:260]!r}")

KW = ("disbeli", "didn't believe", "did not believe", "blam", "counter", "dismiss", "cover", "conceal", "protect itself", "protected itself", "mental health", "hysteric")
SAMPLES = {
    # name: (filter on a matched pair, description)
    "W1_protected": (lambda ia, ib, a, b: ia["reached"] == ib["reached"] == "yes" and ia["protected"] and ib["protected"], "both coders: protected"),
    "W1_notprotected": (lambda ia, ib, a, b: ia["reached"] == ib["reached"] == "yes" and not ia["protected"] and not ib["protected"], "both coders: not protected (any other outcome)"),
    "W1_partly": (lambda ia, ib, a, b: ia["reached"] == ib["reached"] == "yes" and ia["outcome"] == ib["outcome"] == "partly_protected", "both coders: partly protected"),
    "W2_no_words": (lambda ia, ib, a, b: ia["reached"] == ib["reached"] == "yes" and not ia["w2"] and not ib["w2"] and any(k in " ".join((c.get("notes") or "") + " " + (c.get("what_institution_did") or "") for p in (a, b) for c in p.get("contacts") or []).lower() for k in KW), "both: no such response, but a W2-type word in the coders' notes"),
    "W2_yes": (lambda ia, ib, a, b: ia["reached"] == ib["reached"] == "yes" and ia["w2"] and ib["w2"], "both: a disbelief/blame/condition/self-protection response"),
    "W2_no": (lambda ia, ib, a, b: ia["reached"] == ib["reached"] == "yes" and not ia["w2"] and not ib["w2"], "both: no such response"),
    "W3_institution": (lambda ia, ib, a, b: ia["prot_any"] and ib["prot_any"] and ia["w3"] is False and ib["w3"] is False, "both: the institution did the decisive work"),
    "W3_other": (lambda ia, ib, a, b: ia["prot_any"] and ib["prot_any"] and ia["w3"] and ib["w3"], "both: the person, network, other victims or publicity did"),
    "never": (lambda ia, ib, a, b: ia["reached"] == ib["reached"] == "no", "both: never reached"),
    "unclear_codex": (lambda ia, ib, a, b: ia["reached"] == "unclear" or ib["reached"] == "unclear", "either coder: reached unclear"),
}

if __name__ == "__main__":
    if sys.argv[2] == "figures":
        figures()
    else:
        name = sys.argv[3]; n = int(sys.argv[4]) if len(sys.argv) > 4 else 10; seed = int(sys.argv[5]) if len(sys.argv) > 5 else 20261111
        setname = sys.argv[6] if len(sys.argv) > 6 else "pooled"
        f, desc = SAMPLES[name]
        pool = [m for m in matched(setname) if f(*m[1:5])]
        pick = random.Random(seed).sample(pool, min(n, len(pool)))
        print(f"SAMPLE {name} ({desc}): {len(pick)} of {len(pool)} matched people, seed {seed}, set {setname}")
        for m in pick: show(m, full=name.startswith("W2"))

#!/usr/bin/env python3
"""POST-HOC checks (not pre-registered; written after results were seen).

1. Length-matched baseline: 'elevated' re-judged against the 90th percentile of control
   pseudo-seasons pooled to the median season length, instead of single short episodes.
2. Title-based de-duplication: the source lists many episodes twice, as different machine
   transcriptions under different episode numbers; hash de-dupe misses these.
Usage: python3 posthoc.py <sww_json_dir> <control_json_dir> <season_rates.csv>
"""
import csv, glob, json, random, re, statistics as st, sys
from analyze import counts, rate, NAMES

def dedupe_by_title(files):
    seen = {}
    for f in sorted(files):
        s = json.load(open(f))["slug"]; m = re.match(r"s(\d+)-e(p)?\d+(-\d+)?-(.*)", s)
        seen.setdefault((m.group(1), m.group(4)) if m else s, f)
    return list(seen.values())

def main(swwdir, ctrldir, rates_csv):
    ctrl = [c for c in (counts(json.load(open(f))["text"]) for f in glob.glob(f"{ctrldir}/*.json")) if c["words"] >= 500]
    rows = [r for r in csv.DictReader(open(rates_csv)) if r["season"].isdigit()]
    target = st.median(int(r["words"]) for r in rows); rng = random.Random(7); pseudo = []
    for _ in range(1000):
        pool = {k: 0 for k in NAMES + ["label", "words"]}
        while pool["words"] < target:
            c = rng.choice(ctrl)
            for k in pool: pool[k] += c[k]
        pseudo.append(pool)
    print("function,sww_season_median,control_mean,ratio,pooled_control_p90,share_seasons_above")
    for k in NAMES + ["label"]:
        p90 = sorted(rate(p, k) for p in pseudo)[899]; sw = [float(r[k]) for r in rows]
        cm = st.mean(rate(c, k) for c in ctrl)
        print(f"{k},{st.median(sw):.2f},{cm:.2f},{st.median(sw)/max(cm, .01):.1f},{p90:.2f},{sum(v > p90 for v in sw)/len(sw):.2f}")
    print(f"# unique episodes after title de-dupe: {len(dedupe_by_title(glob.glob(f'{swwdir}/*.json')))}")

if __name__ == "__main__":
    main(*sys.argv[1:4])

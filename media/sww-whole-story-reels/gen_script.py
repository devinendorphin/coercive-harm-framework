"""Write SCRIPT.md: every reel's narration with what appears on screen."""
import json, re
from content import REELS, SERIES, SUB

L = [f"# {SERIES} — reel scripts", "",
     f"*{SUB}. {len(REELS)} vertical reels (1080×1920, 30 fps), Kokoro TTS narration (voice `af_heart`), "
     "procedural soundtrack. Source: `research/sww-corpus/results/whole_story/RESULTS.md` (branch `ccr-f78b372d-8qdcn9`). "
     "Made one reel at a time. Survivors keep the show's names; no perpetrator or uncharged person is named. "
     "Evidence is graded in the wording (S-26): convictions and records are stated as such, and quotes are attributed to the person who said them.*", ""]
for r in REELS:
    d = json.load(open(f"build/timing_{r['slug']}.json"))["dur"] + 2.6
    L += [f"## {r['id']} · {r['kicker'].title()}  ({d:.0f} s)", ""]
    for sc in r["scenes"]:
        say = re.sub(r"\[([^\]]+)\]\(/[^)]*/\)", r"\1", sc["say"])
        c = sc["card"]
        on = {"title": lambda: c["big"].replace("\n", " ") + " — " + c["small"],
              "head": lambda: c["head"].replace("\n", " ") + " — " + c["body"],
              "quote": lambda: "“" + c["q"] + "” — " + c["by"], "stat": lambda: c["num"] + " — " + c["label"],
              "list": lambda: c["head"] + ": " + "; ".join(c["items"]),
              "cycle": lambda: f"cycle ring: {c['label']} [{c['marks']}]",
              "bars": lambda: c["head"] + ": " + "; ".join(f"{x[0]} {x[1]}" for x in c["rows"]),
              "tiles": lambda: f"{c['n']} numbered tiles appear — {c['label']}",
              "chips": lambda: c["head"] + " — chips: " + ", ".join(c["items"]),
              "pieces": lambda: f"{c['n']} squares fly together; {c['k']} turn blue — {c['num']}, {c['label']}",
              "timeline": lambda: "timeline: " + " → ".join(n["label"] + (f" [{n['tag']}]" if n.get("tag") else "") for n in c["nodes"]),
              "readers": lambda: f"two columns of text scroll apart ({c['a']} | {c['b']}) — {c['note']}",
              "gauges": lambda: c["head"] + ": " + "; ".join(f"{i['label']} ({i['line'].lower()})" for i in c["items"]),
              "eyes": lambda: f"open eye: {c['left'][0]}, {c['left'][1]}; blindfolded eye: {c['right'][0]}, {c['right'][1]} — {c['foot']}",
              "dots": lambda: f"{c['n']} dots, one per person; {c['k']} turn blue — {c['num']}, {c['label']}; {c.get('after','')}",
              "dotrows": lambda: (c.get("head", "") + ": " if c.get("head") else "") + "; ".join(f"{x[0]} {x[1]} of {c['n']}" for x in c["rows"]) + f" — one row of {c['n']} dots each, lit where present; {c.get('foot','')}",
              "grades": lambda: "evidence cards: " + "; ".join(f"{i[0]} ({i[1]})" for i in c["items"])}
        K = {"k_dots": lambda: f"{c['n']} dots; all but {c['k']} go dark — 1 in 5 protected; gauges {c['a_label']} {int(c['a']*100)}%, {c['b_label']} {int(c['b']*100)}% under a {c['ceiling_label']} line",
             "k_ladder": lambda: "ladder of institutions: " + ", ".join(c["items"]),
             "k_police": lambda: f"incident report ({c['case']}), interview clock, stamp: {c['stamp']}",
             "k_court": lambda: f"petition ({c['header']}), evidence: {'; '.join(c['tags'])}, stamp: {c['stamp']}",
             "k_school": lambda: f"two reports swept under a line; messages deleted; counter: {c['counter']}: 0",
             "k_employer": lambda: f"shift grid ({', '.join(c['days'])}); arrow up to {c['hi']}, back down to {c['lo']}",
             "k_church": lambda: f"ring of members around {c['center']} ({c['center_sub']}); one leaves; lines broadcast: reputation trashed",
             "k_chart": lambda: f"chart diff: {c['v1']} → {c['v2']}; added: " + "; ".join(c["adds"]) + f" — {c['tag']}",
             "k_program": lambda: f"status card ({c['header']}): {c['full']} → {c['zero']}; {c['alert']}; {c['fee']}",
             "k_chain": lambda: "story chain: " + " → ".join(x["label"] for x in c["steps"]) + (f" — {c.get('crop','')} / {c.get('whole','')}" if c.get("phase") == 2 else ""),
             "k_coders": lambda: f"two columns tracing whole stories: {c['a']} | {c['b']}",
             "k_bigquote": lambda: f"spoken quote, kinetic — {c['by']}",
             "k_pass": lambda: "predictions: " + "; ".join(f"{i['label']} ({i['line_txt']}): {i['value_txt']}, {i['verdict']}" for i in c["items"]),
             "k_rings": lambda: "rings out: " + " → ".join(c["rings"]) + " — " + c["big"].replace("\n", " ")}
        on = (K[c["t"]] if c["t"] in K else on[c["t"]])()
        L += [f"- {say}"] + ([f"  - *spoken quote:* “{sc['quote']}”"] if sc.get("quote") else []) + [f"  - *on screen:* {on}"]
    L.append("")
open("SCRIPT.md", "w").write("\n".join(L) + "\n")
print(round(sum(json.load(open(f"build/timing_{r['slug']}.json"))["dur"] + 2.6 for r in REELS) / 60, 1), "min")

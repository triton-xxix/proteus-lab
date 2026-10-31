#!/usr/bin/env python3
"""P-0207: P-0206 leg two. Run the FActScore-style token check over a week of harvest nights
(24 to 30 Oct 2026) and print every miss so a reader can sort tokeniser noise from facts outside the
text, misattributed facts and fabricated facts. Reuses the functions in experiments/2026-10-23-P-0206/
factcheck.py unchanged; writes results.json beside this script, never into the P-0206 folder.
Run: python3 /Users/triton/PROTEUS/experiments/2026-10-31-P-0207/week.py
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/triton/PROTEUS/"
SRC = ROOT + "experiments/2026-10-23-P-0206/factcheck.py"
DATES = ["2026-10-24", "2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30"]

spec = importlib.util.spec_from_file_location("factcheck", SRC)
fc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fc)


def night(date):
    with open(f"{ROOT}state/harvest/{date}/brief.md") as fh:
        brief = fh.read()
    with open(f"{ROOT}state/agents/{date}/harvest.json") as fh:
        judged = json.load(fh)
    secs = fc.sections(brief)
    rows = []
    tot = sup = 0
    kept = 0
    for i, item in enumerate(judged, 1):
        if not item.get("keep"):
            continue
        kept += 1
        body = secs.get(i, "")
        text = (item.get("claim") or "") + " " + (item.get("mechanism") or "")
        fs = fc.facts(text)
        ok = [f for f in fs if fc.supported(f, body)]
        miss = [f for f in fs if f not in ok]
        tot += len(fs)
        sup += len(ok)
        rows.append({"n": i, "key": item.get("key"), "facts": len(fs), "supported": len(ok),
                     "unsupported": miss, "claim": item.get("claim"), "mechanism": item.get("mechanism"),
                     "section_chars": len(body)})
    return {"date": date, "judged": len(judged), "kept": kept, "facts": tot, "supported": sup,
            "support_rate": round(sup / tot, 3) if tot else None, "items": rows}


def main():
    out = []
    for d in DATES:
        try:
            r = night(d)
        except FileNotFoundError as e:
            print(f"{d}: missing {e.filename}")
            continue
        out.append(r)
        print(f"== {d}: judged {r['judged']} kept {r['kept']} facts {r['facts']} supported {r['supported']} rate {r['support_rate']}")
        for row in r["items"]:
            if row["unsupported"]:
                print(f"  {row['n']:2} {str(row['key'])[:44]:<44} miss {len(row['unsupported'])}/{row['facts']}: {', '.join(row['unsupported'])[:200]}")
    tot = sum(r["facts"] for r in out)
    sup = sum(r["supported"] for r in out)
    summary = {"nights": len(out), "kept": sum(r["kept"] for r in out), "facts": tot, "supported": sup,
               "support_rate": round(sup / tot, 3) if tot else None}
    print(json.dumps(summary))
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump({"summary": summary, "nights": out}, fh, indent=1)


if __name__ == "__main__":
    main()

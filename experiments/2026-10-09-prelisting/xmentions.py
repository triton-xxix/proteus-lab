"""Does X chatter rise before an Upbit KRW listing? A small case-control test through xAI (Luke's key,
inside the $10 cap for this work; ledger xai-calls.jsonl).

Rules, fixed before the calls (9 Oct 2026):
- Cases: Upbit KRW listings from 1 Mar to 24 Sep 2026 of coins with a prior USDT market, stablecoins
  out, spread evenly by date, N_PAIRS of them.
- Controls: for each case, the coin nearest in 30-day turnover rank on the case's announcement day
  that was in the universe, not on Upbit KRW, and not listed there within 90 days either side.
- One call per coin. Windows: A = the 14 days ending 15 days before the announcement day,
  B = the 14 days ending the day before. The model counts posts with the cashtag in each window
  (keyword search, latest mode) and returns JSON. Counts above 50 are reported as 50+ (the search
  tool returns pages, so big numbers are capped, not measured).
- Measure: growth = B / max(A, 1). The test: is the median growth of cases above the controls', and
  in how many pairs does the case grow more. With 8 to 10 pairs this can only find a big effect.
Writes data/xmentions.json.
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import xai  # noqa: E402

OUT = os.path.join(HERE, "data", "xmentions.json")
N_PAIRS = 9
PROMPT = ("Use X keyword search (mode Latest) for posts containing the cashtag ${sym} ({name}). Count posts in two "
          "windows separately: A from {a0} to {a1} inclusive, B from {b0} to {b1} inclusive. Search each window on its "
          "own with since/until dates, paging until you have them all or reach 50. Count only posts about this crypto "
          "token. Return JSON only: {{\"a_posts\": int, \"b_posts\": int, \"a_capped\": bool, \"b_capped\": bool, "
          "\"b_korean_posts\": int, \"notes\": short string}}")


def pick():
    sigs = json.load(open(os.path.join(HERE, "signals.json")))
    pairs = json.load(open(os.path.join(HERE, "data", "xmention_pairs.json")))
    return pairs[:N_PAIRS]


def ask(sym, name, d):
    day = datetime.fromtimestamp(d, timezone.utc).date()
    a0, a1 = day - timedelta(days=28), day - timedelta(days=15)
    b0, b1 = day - timedelta(days=14), day - timedelta(days=1)
    text, urls, cost = xai.search("xmentions-%s" % sym, PROMPT.format(sym=sym, name=name or sym, a0=a0, a1=a1, b0=b0, b1=b1),
                                  str(a0), str(b1))
    raw = text[text.find("{"): text.rfind("}") + 1]
    try:
        j = json.loads(raw)
    except Exception:
        j = {"error": text[:200]}
    j["cost_usd"] = cost
    return j


def main():
    have = json.load(open(OUT)) if os.path.exists(OUT) else []
    done = {(r["role"], r["symbol"]) for r in have}
    for p in pick():
        for role in ("case", "control"):
            sym = p[role]
            if (role, sym) in done:
                continue
            j = ask(sym, None, p["t"])
            have.append({"role": role, "symbol": sym, "pair": p["case"], "t": p["t"], **j})
            json.dump(have, open(OUT, "w"), indent=0)
            print(role, sym, j, flush=True)
    print("xAI spent to date", round(xai.spent(), 4))


if __name__ == "__main__":
    main()

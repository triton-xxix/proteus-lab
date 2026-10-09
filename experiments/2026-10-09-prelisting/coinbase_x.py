"""Coinbase listing announcements from @CoinbaseMarkets on X, through xAI (Luke's key, $10 cap for this
work, ledger in xai-calls.jsonl). One call per two-month window, Oct 2025 to Oct 2026. The model's
answer gives ticker and kind; the time comes from the post id in the URL, never from the prose.
Writes data/coinbase_posts.json. Re-running skips windows already in the file.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import xai  # noqa: E402

OUT = os.path.join(HERE, "data", "coinbase_posts.json")
WINDOWS = [("2025-10-01", "2025-11-30"), ("2025-12-01", "2026-01-31"), ("2026-02-01", "2026-03-31"),
           ("2026-04-01", "2026-05-31"), ("2026-06-01", "2026-07-31"), ("2026-08-01", "2026-09-30"),
           ("2026-10-01", "2026-10-09")]
PROMPT = ("List every post by @CoinbaseMarkets from %s to %s that announces a new asset: added to the "
          "roadmap, deposits open, or trading launched or about to launch. Search with from:CoinbaseMarkets and "
          "several keyword variants (roadmap, trading, launch, support, deposits) so none is missed. One per line: "
          "TICKER | roadmap, deposits or trading | post URL. Nothing else.")


def main():
    have = json.load(open(OUT)) if os.path.exists(OUT) else {"windows": [], "posts": []}
    for a, b in WINDOWS:
        if [a, b] in have["windows"]:
            continue
        text, urls, cost = xai.search("coinbase-markets-%s" % a, PROMPT % (a, b), a, b, ["CoinbaseMarkets"])
        for line in text.splitlines():
            m = re.search(r"\$?([A-Z0-9]{1,15})\s*\|\s*(roadmap|deposits|trading)\s*\|\s*(https://\S+/status/\d+)", line.replace("*", ""))
            if m:
                have["posts"].append({"symbol": m.group(1), "kind": m.group(2), "url": m.group(3),
                                      "t": xai.status_time(m.group(3)), "window": a})
        have["windows"].append([a, b])
        print(a, b, "cost", cost, "posts so far", len(have["posts"]), flush=True)
        json.dump(have, open(OUT, "w"), indent=0)
    print("xAI spent to date", round(xai.spent(), 4))


if __name__ == "__main__":
    main()

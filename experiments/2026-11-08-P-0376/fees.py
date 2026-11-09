"""P-0376: does mempool.space's recommended fastest fee clear the next block, and by how much does it overpay?

Keyless. Polls the recommended fees and the chain tip every 30 s for up to 20 minutes. When a new block appears,
compares the recommendation last seen BEFORE that block with the block's own fee range and median (the API's
extras). Forward only: the recommendation is recorded before the block is known. Stops itself; HALT stops it too.
"""
import json
import os
import pathlib
import time
import urllib.request

HERE = pathlib.Path(__file__).parent
API = "https://mempool.space/api"
RUN_SECONDS = 20 * 60
POLL = 30
HALT = "/Users/triton/PROTEUS/HALT"


def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "proteus-lab/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


start = time.time()
seen = {b["id"] for b in get("/v1/blocks")}
last_rec, last_at = None, None
polls, errors, rows = 0, 0, []
while time.time() - start < RUN_SECONDS and not os.path.exists(HALT):
    try:
        blocks = get("/v1/blocks")
        new = [b for b in blocks if b["id"] not in seen]
        for b in sorted(new, key=lambda x: x["height"]):
            seen.add(b["id"])
            if last_rec is None:
                continue
            ex = b.get("extras") or {}
            rng = ex.get("feeRange") or [None]
            rows.append({"height": b["height"], "tx_count": b.get("tx_count"),
                         "rec_seen_s_before": round(time.time() - last_at, 1), "rec": last_rec,
                         "block_min": rng[0], "block_median": ex.get("medianFee"), "block_max": rng[-1],
                         "fastest_clears_min": rng[0] is not None and last_rec["fastestFee"] >= rng[0],
                         "overpay_vs_median": None if ex.get("medianFee") is None
                         else round(last_rec["fastestFee"] - ex["medianFee"], 3)})
            print(json.dumps(rows[-1]), flush=True)
        last_rec, last_at = get("/v1/fees/recommended"), time.time()
        polls += 1
    except Exception as e:  # noqa: BLE001
        errors += 1
        print("error", repr(e)[:120], flush=True)
    time.sleep(POLL)

over = [r["overpay_vs_median"] for r in rows if r["overpay_vs_median"] is not None]
out = {"seconds": round(time.time() - start), "polls": polls, "errors": errors, "blocks": len(rows),
       "fastest_cleared_min": sum(r["fastest_clears_min"] for r in rows),
       "mean_overpay_vs_median": round(sum(over) / len(over), 3) if over else None,
       "last_recommended": last_rec, "rows": rows}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))

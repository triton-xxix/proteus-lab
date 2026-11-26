"""P-0579: page the mayhem wallet's signatures back 5 x 1,000 with `before`; time span each page covers.
Keyless, read only, uses P-0491's alive.rpc."""
import json, sys, time
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-19-P-0491")
import alive  # noqa: E402

HERE = Path(__file__).resolve().parent
now = time.time()
before, pages = None, []
for n in range(5):
    opts = {"limit": 1000}
    if before:
        opts["before"] = before
    res = alive.rpc("getSignaturesForAddress", [alive.WALLET, opts]).get("result") or []
    timed = [x["blockTime"] for x in res if x.get("blockTime")]
    if not res:
        pages.append({"page": n + 1, "sigs": 0})
        print(pages[-1])
        break
    p = {"page": n + 1, "sigs": len(res), "newest_min_ago": round((now - max(timed)) / 60, 1),
         "oldest_min_ago": round((now - min(timed)) / 60, 1), "span_min": round((max(timed) - min(timed)) / 60, 1),
         "errors": sum(1 for x in res if x.get("err"))}
    pages.append(p)
    print(p, flush=True)
    before = res[-1]["signature"]
    time.sleep(1)
summary = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)), "pages": pages,
           "total_reach_min": pages[-1].get("oldest_min_ago"),
           "reaches_30_min": (pages[-1].get("oldest_min_ago") or 0) >= 30}
print(json.dumps(summary, indent=1))
(HERE / "results.json").write_text(json.dumps(summary, indent=1))

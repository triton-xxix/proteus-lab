"""P-0468: read the first 500 stores of api.onaa.net/v1/stores (fetched keyless with curl) and count
what the directory actually says about them. Store names and text are untrusted data; only fields
are counted, nothing is followed."""
import collections, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.loads(Path("/Users/triton/PROTEUS/sandbox/p0468-stores-500.json").read_text())
one = json.loads(Path("/Users/triton/PROTEUS/sandbox/p0468-stores-all1.json").read_text())
items = d["items"]
c = collections.Counter
src, status, verdict, proto, days, tested, handler, tld = c(), c(), c(), c(), c(), c(), c(), c()
probes_one = 0
for it in items:
    src[it.get("source")] += 1
    cp = it.get("checkout_probe") or {}
    status[cp.get("status")] += 1
    proto[cp.get("protocol")] += 1
    ap = it.get("agent_purchase") or {}
    verdict[ap.get("verdict")] += 1
    tested[bool(ap.get("payment_tested"))] += 1
    days[(it.get("first_seen") or "")[:10]] += 1
    if any("only 1 time" in x for x in ap.get("cautions") or []):
        probes_one += 1
    how = " ".join(ap.get("how_to_buy") or [])
    handler["shop_pay" if "Shop Pay" in how else ("none_offered" if "No agent payment handler" in how else "other")] += 1
    tld[(it.get("domain") or "").rsplit(".", 1)[-1]] += 1
out = {
    "total_listed": one["total"], "reachability_counts": one["reachability_counts"], "sample": len(items),
    "source": dict(src), "checkout_probe_status": dict(status), "protocol": dict(proto), "verdict": dict(verdict),
    "payment_tested": {str(k): v for k, v in tested.items()}, "first_seen_day": dict(sorted(days.items())),
    "probed_only_once": probes_one, "payment_route": dict(handler), "top_tlds": dict(tld.most_common(6)),
}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))

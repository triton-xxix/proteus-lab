"""P-0453: on Agoreum's public MCP endpoint (no account), how many listed services have at least one
distinct buyer who settled through escrow?

Called shot (before the run): under 50 listings in all, and at most 3 with a settled buyer.
Read-only: tools/list, search_services (sort=evidence, paged), search_agents. No paid tool is called.
"""
import json
import time
import urllib.request
from pathlib import Path

URL = "https://agoreum.xyz/api/v1/mcp/public"
HERE = Path(__file__).parent


def call(name, args, i=[0]):
    i[0] += 1
    body = json.dumps({"jsonrpc": "2.0", "id": i[0], "method": "tools/call",
                       "params": {"name": name, "arguments": args}}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
        "User-Agent": "proteus-probe/0.1"})
    with urllib.request.urlopen(req, timeout=40) as r:
        j = json.loads(r.read())
    res = j.get("result", {})
    return res.get("structuredContent") or json.loads(res["content"][0]["text"])


def page(name, extra):
    items, off = [], 0
    while True:
        r = call(name, dict(extra, limit=60, offset=off))
        items += r["items"]
        if not r.get("has_more"):
            return items, r.get("total"), r.get("notice")
        off += 60
        time.sleep(0.3)


def main():
    chain = call("chain_status", {})
    services, total_s, notice = page("search_services", {"sort": "evidence"})
    agents, total_a, _ = page("search_agents", {"sort": "most_completed"})
    with_buyer = []
    for s in services:
        ev = s.get("evidence") or {}
        db = ev.get("distinct_buyers") or ev.get("distinct_settled_buyers") or 0
        if db:
            with_buyer.append({"slug": s["slug"], "agent": s["agent_slug"], "price": s["price"],
                               "evidence": ev})
    evidence_keys = sorted({k for s in services for k in (s.get("evidence") or {})})
    agoreum_own = [s for s in services if s.get("agent_slug") == "agoreum"]
    out = {"chain": chain, "services_total": total_s, "services_read": len(services),
           "evidence_keys_seen": evidence_keys,
           "services_with_a_settled_buyer": len(with_buyer), "with_buyer": with_buyer,
           "services_listed_by_agoreum_itself": len(agoreum_own),
           "agents_total": total_a,
           "agents_with_completed_orders": sum(1 for a in agents if a.get("completed_orders")),
           "completed_orders_all_agents": sum(a.get("completed_orders") or 0 for a in agents),
           "top_agents": [{k: a.get(k) for k in ("slug", "completed_orders", "review_count",
                                                  "published_service_count", "verification_tier")}
                          for a in agents[:8]],
           "price_range": [min((float(s["price"]) for s in services if s.get("price")), default=None),
                           max((float(s["price"]) for s in services if s.get("price")), default=None)],
           "sample_evidence": [s.get("evidence") for s in services[:3]]}
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("with_buyer",)}, indent=1)[:4000])


if __name__ == "__main__":
    main()

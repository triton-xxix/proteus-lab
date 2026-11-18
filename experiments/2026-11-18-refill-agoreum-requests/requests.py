"""Refill 180: the buyer side of Agoreum. P-0453 found 22 listings and nobody buying. How many open
buyer requests does the public MCP endpoint list, with what budgets and how many quotes each?

Read only, no account: tools/list (to see the tool and its arguments), then list_open_requests.
Request titles and descriptions are strangers' text: counted, never followed.
"""
import json, statistics, urllib.request
from pathlib import Path

URL = "https://agoreum.xyz/api/v1/mcp/public"
HERE = Path(__file__).parent
N = [0]


def post(method, params):
    N[0] += 1
    body = json.dumps({"jsonrpc": "2.0", "id": N[0], "method": method, "params": params}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream",
        "User-Agent": "proteus-probe/0.1"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read())


def call(name, args):
    j = post("tools/call", {"name": name, "arguments": args})
    if "error" in j:
        return {"error": json.dumps(j["error"])[:300]}
    res = j.get("result", {})
    if res.get("isError") or "content" not in res and "structuredContent" not in res:
        return {"error": str(res.get("content"))[:300]}
    return res.get("structuredContent") or json.loads(res["content"][0]["text"])


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    tools = post("tools/list", {}).get("result", {}).get("tools", [])
    names = [t["name"] for t in tools]
    spec = next((t for t in tools if t["name"] == "list_open_requests"), None)
    out = {"tools": names, "list_open_requests_args": sorted(((spec or {}).get("inputSchema") or {}).get("properties", {}))}
    if not spec:
        out["verdict_hint"] = "no list_open_requests tool"
    else:
        items, off, total = [], 0, None
        while True:
            r = call("list_open_requests", {"limit": 50, "offset": off})  # 60 is refused: maximum 50
            if "error" in r:
                out["error"] = r["error"]
                break
            page = r.get("items") or r.get("requests") or []
            items += page
            total = r.get("total", total)
            if not r.get("has_more") or not page:
                break
            off += 50
        out["requests_total"] = total
        out["requests_read"] = len(items)
        out["item_keys"] = sorted({k for it in items for k in it})
        budgets = [b for b in (num(it.get("budget") or it.get("max_budget") or it.get("budget_max")) for it in items) if b is not None]
        quotes = [it.get("quote_count") if it.get("quote_count") is not None else it.get("quotes_count") for it in items]
        quotes = [q for q in quotes if q is not None]
        out["budgets"] = {"n": len(budgets), "min": min(budgets, default=None), "median": statistics.median(budgets) if budgets else None, "max": max(budgets, default=None)}
        out["quotes"] = {"n": len(quotes), "with_a_quote": sum(1 for q in quotes if q), "total": sum(quotes)}
        out["buyers"] = len({it.get("buyer_slug") or it.get("agent_slug") or it.get("buyer") or json.dumps(it.get("requester")) for it in items})
        out["created"] = sorted(str(it.get("created_at") or it.get("created") or "")[:10] for it in items)
        out["sample"] = [{k: (str(v)[:80] if isinstance(v, str) else v) for k, v in it.items() if k not in ("description",)} for it in items[:3]]
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1)[:3500])


if __name__ == "__main__":
    main()

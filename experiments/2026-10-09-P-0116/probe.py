"""P-0116: does an unpaid call to a public x402 endpoint return a parseable 402 challenge?

Keyless, no wallet, nothing paid. Reads the Coinbase x402 Bazaar discovery list (fetched to
sandbox/x402-discovery.json), sends one plain unpaid request to up to 25 listed resources, and checks
the reply against the spec's PaymentRequirements fields.

usage: python3 probe.py DISCOVERY_JSON OUTDIR
"""
import collections
import json
import sys
import urllib.error
import urllib.request

FIELDS = ["scheme", "network", "maxAmountRequired", "resource", "payTo", "asset", "maxTimeoutSeconds"]


def call(url, method):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "proteus-x402-probe",
                                                               "Accept": "application/json"},
                                 data=b"{}" if method == "POST" else None)
    if method == "POST":
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read(20000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read(20000).decode("utf-8", "replace")
    except Exception as e:
        return None, {}, type(e).__name__


def main():
    disc = json.load(open(sys.argv[1]))
    items = disc.get("items") or disc.get("resources") or []
    out = []
    for it in items[:25]:
        url = it.get("resource")
        accepts = it.get("accepts") or [{}]
        method = ((accepts[0].get("outputSchema") or {}).get("input") or {}).get("method", "GET").upper()
        st, hdr, body = call(url, method)
        rec = {"url": url, "method": method, "status": st, "listed_network": accepts[0].get("network"),
               "listed_price": accepts[0].get("maxAmountRequired")}
        try:
            j = json.loads(body)
        except Exception:
            j = None
        if st == 402 and isinstance(j, dict):
            acc = (j.get("accepts") or [{}])[0]
            rec.update({"parseable": True, "x402Version": j.get("x402Version"),
                        "missing_fields": [f for f in FIELDS if f not in acc],
                        "network": acc.get("network"), "price": acc.get("maxAmountRequired"),
                        "matches_listing": acc.get("maxAmountRequired") == accepts[0].get("maxAmountRequired")})
        else:
            rec.update({"parseable": False, "body_head": body[:160],
                        "payment_header": hdr.get("PAYMENT-REQUIRED") or hdr.get("Payment-Required")})
            if rec["payment_header"]:
                rec["parseable"] = "header"
        out.append(rec)
        print(json.dumps(rec)[:240], flush=True)
    s = {"listed_total": len(items), "tried": len(out),
         "status": dict(collections.Counter(str(r["status"]) for r in out)),
         "parseable_402_body": sum(r["parseable"] is True for r in out),
         "challenge_in_header": sum(r["parseable"] == "header" for r in out),
         "complete_fields": sum(r["parseable"] is True and not r["missing_fields"] for r in out),
         "price_matches_listing": sum(bool(r.get("matches_listing")) for r in out),
         "networks": dict(collections.Counter(str(r.get("network") or r.get("listed_network")) for r in out))}
    json.dump({"summary": s, "rows": out}, open(sys.argv[2] + "/results.json", "w"), indent=1)
    print(json.dumps(s))


if __name__ == "__main__":
    main()

"""P-0267: public detection signals for a closure-sale dropship shop. Stdlib, keyless.

Pulls, for one domain: RDAP (creation date, registrar, nameservers, registrant country if shown),
certificate-transparency hostnames from crt.sh (sibling subdomains and the certificate history),
and the shop's HTTP response headers (platform fingerprint). Records what is public; nothing here
touches the shop beyond one HEAD request and the public logs.
Usage: python3 signals.py harrisonandjames.com
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

dom = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
out = {"domain": dom, "checked": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")}


def get(url, timeout=30, head=False):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-signals/0.1 (public-record check)"}, method="HEAD" if head else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, dict(r.headers), (b"" if head else r.read())


# 1. RDAP via the IANA bootstrap redirector
try:
    st, hdr, body = get("https://rdap.org/domain/" + dom)
    rd = json.loads(body.decode())
    ev = {e.get("eventAction"): e.get("eventDate") for e in rd.get("events", [])}
    out["rdap"] = {
        "registered": ev.get("registration"),
        "expires": ev.get("expiration"),
        "last_changed": ev.get("last changed"),
        "status": rd.get("status"),
        "nameservers": [n.get("ldhName", "").lower() for n in rd.get("nameservers", [])],
        "registrar": None, "registrant_country": None,
    }
    for ent in rd.get("entities", []):
        roles = ent.get("roles", [])
        vc = ent.get("vcardArray", [None, []])[1] if ent.get("vcardArray") else []
        if "registrar" in roles:
            for f in vc:
                if f[0] == "fn":
                    out["rdap"]["registrar"] = f[3]
        if "registrant" in roles:
            for f in vc:
                if f[0] == "adr" and isinstance(f[3], list) and f[3]:
                    out["rdap"]["registrant_country"] = f[3][-1]
    if out["rdap"]["registered"]:
        reg = datetime.fromisoformat(out["rdap"]["registered"].replace("Z", "+00:00"))
        out["rdap"]["age_days"] = (datetime.now(timezone.utc) - reg).days
except Exception as e:  # noqa
    out["rdap_error"] = repr(e)

# 2. Certificate transparency: every name ever certified under the domain
try:
    st, hdr, body = get("https://crt.sh/?q=%25." + dom + "&output=json", timeout=60)
    rows = json.loads(body.decode())
    names = set()
    first = None
    for r in rows:
        for n in r.get("name_value", "").split("\n"):
            names.add(n.strip().lower())
        d = r.get("not_before")
        if d and (first is None or d < first):
            first = d
    out["crt"] = {"certificates": len(rows), "hostnames": sorted(names), "first_certificate": first}
except Exception as e:  # noqa
    out["crt_error"] = repr(e)

# 3. The shop's own headers (platform fingerprint, no page content kept)
try:
    st, hdr, _ = get("https://" + dom + "/", head=True)
    keep = {k: v for k, v in hdr.items() if k.lower() in (
        "server", "x-shopify-stage", "x-shopid", "x-sorting-hat-shopid", "x-sorting-hat-podid", "powered-by", "x-powered-by", "x-shardid", "x-dc", "location")}
    out["http"] = {"status": st, "headers": keep, "shopify": any(k.lower().startswith("x-shop") or k.lower().startswith("x-sorting-hat") for k in hdr)}
except Exception as e:  # noqa
    out["http_error"] = repr(e)

json.dump(out, open(os.path.join(HERE, "signals.json"), "w"), indent=1)
print(json.dumps(out, indent=1))

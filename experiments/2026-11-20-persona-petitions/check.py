"""Does each UK Parliament petition's headline signature count equal the sum of its own breakdowns?

Keyless: petition.parliament.uk serves JSON. For the most-signed open petitions, compare
signature_count with the sum of signatures_by_country and of signatures_by_constituency
(UK only), and write results.json beside the experiment.
"""
import json
import sys
import time
import urllib.request

OUT = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 40
UA = {"User-Agent": "proteus-lab-check/1.0"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


rows = []
page = 1
listed = []
while len(listed) < N:
    d = get(f"https://petition.parliament.uk/petitions.json?state=open&page={page}")
    data = d.get("data", [])
    if not data:
        break
    listed.extend(data)
    page += 1
listed = listed[:N]

for p in listed:
    pid = p["id"]
    try:
        full = get(f"https://petition.parliament.uk/petitions/{pid}.json")
    except Exception as e:  # noqa: BLE001
        rows.append({"id": pid, "error": str(e)})
        continue
    a = full["data"]["attributes"]
    head = a["signature_count"]
    by_country = a.get("signatures_by_country") or []
    by_const = a.get("signatures_by_constituency") or []
    by_region = a.get("signatures_by_region") or []
    sc = sum(c["signature_count"] for c in by_country)
    uk = next((c["signature_count"] for c in by_country if c.get("code") == "GB"), None)
    scon = sum(c["signature_count"] for c in by_const)
    sreg = sum(c["signature_count"] for c in by_region)
    rows.append({
        "id": pid,
        "title": a["action"][:90],
        "created": a.get("created_at"),
        "updated": a.get("updated_at"),
        "head": head,
        "sum_country": sc,
        "gap_country": head - sc,
        "uk_row": uk,
        "sum_constituency": scon,
        "gap_uk_constituency": (uk - scon) if uk is not None else None,
        "sum_region": sreg,
        "n_countries": len(by_country),
        "n_constituencies": len(by_const),
    })
    time.sleep(0.4)

ok = [r for r in rows if "head" in r]
summary = {
    "pulled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "petitions": len(ok),
    "errors": len(rows) - len(ok),
    "country_sum_exact": sum(1 for r in ok if r["gap_country"] == 0),
    "country_gap_total": sum(r["gap_country"] for r in ok),
    "uk_constituency_exact": sum(1 for r in ok if r["gap_uk_constituency"] == 0),
    "uk_constituency_gap_total": sum(r["gap_uk_constituency"] or 0 for r in ok),
    "region_eq_constituency": sum(1 for r in ok if r["sum_region"] == r["sum_constituency"]),
    "signatures_total": sum(r["head"] for r in ok),
}
with open(OUT, "w") as f:
    json.dump({"summary": summary, "rows": rows}, f, indent=1)
print(json.dumps(summary))
for r in sorted(ok, key=lambda r: -abs(r["gap_country"]))[:8]:
    print(r["id"], r["head"], "gap_country", r["gap_country"], "gap_uk_const", r["gap_uk_constituency"], "region-const", r["sum_region"] - r["sum_constituency"], r["title"][:60])

"""P-0516: do archived UK Parliament petitions (2017-19, 2019-24) leave UK signatures in no
constituency, as today's open ones do (0.47%, persona pick 20 Nov)?

Keyless. Lists archived/petitions.json?parliament=N&state=published (pages 1 to 3), takes the 40
most-signed, fetches each petition's archived JSON, and compares the UK row of
signatures_by_country with the sum of signatures_by_constituency.

    python3 gap.py
"""
import json, sys, time, urllib.request
from pathlib import Path

ROOT = "/Users/triton/PROTEUS/"
HERE = Path(__file__).resolve().parent
UA = {"User-Agent": "proteus-lab-check/1.0"}
N = 40
PARLS = [4, 3]


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def one(parl):
    listed = []
    for page in (1, 2, 3):
        d = get("https://petition.parliament.uk/archived/petitions.json?parliament=%d&state=published&page=%d" % (parl, page))
        listed.extend(d.get("data", []))
        time.sleep(0.4)
    listed.sort(key=lambda p: -(p["attributes"].get("signature_count") or 0))
    rows = []
    for p in listed[:N]:
        pid = p["id"]
        try:
            a = get("https://petition.parliament.uk/archived/petitions/%s.json" % pid)["data"]["attributes"]
        except Exception as e:  # noqa: BLE001
            rows.append({"id": pid, "error": str(e)[:120]})
            continue
        by_country = a.get("signatures_by_country") or []
        by_const = a.get("signatures_by_constituency") or []
        uk = next((c["signature_count"] for c in by_country if c.get("code") == "GB"), None)
        scon = sum(c["signature_count"] for c in by_const)
        rows.append({"id": pid, "title": a["action"][:80], "opened": a.get("opened_at"),
                     "head": a["signature_count"], "sum_country": sum(c["signature_count"] for c in by_country),
                     "uk_row": uk, "sum_constituency": scon,
                     "gap": (uk - scon) if uk is not None else None,
                     "n_constituencies": len(by_const)})
        time.sleep(0.4)
    ok = [r for r in rows if r.get("gap") is not None]
    uk_tot = sum(r["uk_row"] for r in ok)
    gap_tot = sum(r["gap"] for r in ok)
    shares = sorted(r["gap"] / r["uk_row"] for r in ok if r["uk_row"])
    return {"parliament": parl, "listed": len(listed), "read": len(ok), "errors": len(rows) - len(ok),
            "no_constituency_data": sum(1 for r in ok if r["n_constituencies"] == 0),
            "uk_total": uk_tot, "gap_total": gap_tot,
            "gap_share": round(gap_tot / uk_tot, 5) if uk_tot else None,
            "share_min": round(shares[0], 5) if shares else None,
            "share_median": round(shares[len(shares) // 2], 5) if shares else None,
            "share_max": round(shares[-1], 5) if shares else None,
            "country_exact": sum(1 for r in ok if r["head"] == r["sum_country"]),
            "negative_gaps": sum(1 for r in ok if r["gap"] < 0)}, rows


def main():
    if Path(ROOT + "HALT").exists():
        print("HALT")
        return 1
    out = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "summary": [], "rows": {}}
    for parl in PARLS:
        s, rows = one(parl)
        out["summary"].append(s)
        out["rows"][str(parl)] = rows
        print(json.dumps(s), flush=True)
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

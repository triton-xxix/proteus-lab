"""P-0118: can the public Solana RPC fill mint_auth and freeze_auth, which rugcheck leaves blank on
pump.fun mints (1,573 of 1,575, P-0099)? Reads the last 30 mints in grinder/LEDGER.csv, asks
api.mainnet-beta.solana.com getMultipleAccounts (jsonParsed, keyless) and records each mint's program,
mintAuthority and freezeAuthority. Writes result.json beside this script.

Called shot: works, 30 of 30 filled, and almost all show both authorities revoked (null), since pump.fun
revokes them at creation, so the column fills but separates little.
"""
import csv
import json
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
LEDGER = HERE.parent.parent / "grinder" / "LEDGER.csv"
RPC = "https://api.mainnet-beta.solana.com"

rows = list(csv.reader(open(LEDGER)))
mints = []
for r in rows[1:][::-1]:
    if len(r) > 3 and r[3] not in mints:
        mints.append(r[3])
    if len(mints) == 30:
        break

t0 = time.time()
body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "getMultipleAccounts",
                   "params": [mints, {"encoding": "jsonParsed"}]}).encode()
req = urllib.request.Request(RPC, data=body, headers={"Content-Type": "application/json"})
res = json.loads(urllib.request.urlopen(req, timeout=30).read())
secs = round(time.time() - t0, 2)

out = []
for mint, acc in zip(mints, res["result"]["value"]):
    if not acc:
        out.append({"mint": mint, "found": False})
        continue
    data = acc["data"]
    info = data.get("parsed", {}).get("info", {}) if isinstance(data, dict) else {}
    out.append({"mint": mint, "found": True, "program": data.get("program") if isinstance(data, dict) else None,
                "mint_auth": info.get("mintAuthority"), "freeze_auth": info.get("freezeAuthority"),
                "parsed": bool(info)})

summary = {"mints": len(mints), "found": sum(o["found"] for o in out),
           "parsed": sum(1 for o in out if o.get("parsed")),
           "mint_auth_set": sum(1 for o in out if o.get("mint_auth")),
           "freeze_auth_set": sum(1 for o in out if o.get("freeze_auth")),
           "programs": sorted({o.get("program") or "" for o in out}), "one_request_seconds": secs}
(HERE / "result.json").write_text(json.dumps({"summary": summary, "rows": out}, indent=1))
print(json.dumps(summary))

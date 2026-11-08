"""P-0365 controls. (1) What does the volumes endpoint say for live football match markets, so the
Munich figure has a scale? (2) Do the Munich markets show any last executed price?"""
import json, pathlib, time, urllib.error, urllib.request

HERE = pathlib.Path("/Users/triton/PROTEUS/experiments/2026-11-08-P-0365")
API = "https://api.smarkets.com/v3"
MUNICH = ["174047034", "174296943", "174537327", "174732214", "174960158", "175283210", "175578274", "175849012",
          "176107740", "176368461", "176592653", "176828623"]


def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "proteus-exchange/0.1", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"http_error": e.code}


res = {"football": [], "munich_last_executed": {}}
ev = get("/events/?type=football_match&state=upcoming&state=live&limit=8&sort=start_datetime,id")
for e in ev.get("events", []):
    if len(res["football"]) >= 8:
        break
    mk = get(f"/events/{e['id']}/markets/").get("markets", [])
    wanted = [m for m in mk if m.get("market_type", {}).get("name") == "WINNER_3_WAY" or "full-time" in m.get("slug", "")][:1] or mk[:1]
    for m in wanted:
        v = get(f"/markets/{m['id']}/volumes/")
        res["football"].append({"event": e["name"], "start": e.get("start_datetime"), "state": e.get("state"), "market": m["name"], "market_id": m["id"], "volumes": v.get("volumes")})
    time.sleep(0.3)
for m in MUNICH:
    res["munich_last_executed"][m] = get(f"/markets/{m}/last_executed_prices/")
    time.sleep(0.3)
(HERE / "control.json").write_text(json.dumps(res, indent=1))
for f in res["football"]:
    print(f["event"], "|", f["start"], "|", f["state"], "|", f["market"], "|", f["volumes"])
print(json.dumps(res["munich_last_executed"])[:1800])

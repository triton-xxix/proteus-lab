"""One-off: list international football markets on The Odds API and pull upcoming fixtures with odds.
Key read from 1Password at run time, never written. Quota shown from the response headers."""
import json, subprocess, sys, requests
key = subprocess.run(["op","item","get","The Odds API","--vault","Tritons World","--fields","label=credential","--reveal"],
                     capture_output=True,text=True).stdout.strip()
if not key:
    key = subprocess.run(["op","item","get","The Odds API","--vault","Tritons World","--fields","label=api key","--reveal"],
                         capture_output=True,text=True).stdout.strip()
if len(key) != 32:
    print("could not read key, len", len(key)); sys.exit(1)
mode = sys.argv[1] if len(sys.argv) > 1 else "sports"
if mode == "sports":
    r = requests.get("https://api.the-odds-api.com/v4/sports", params={"apiKey": key, "all": "true"}, timeout=30)
    print("quota used/remaining", r.headers.get("x-requests-used"), r.headers.get("x-requests-remaining"))
    for s in r.json():
        if s["group"] == "Soccer" and s["active"]:
            print(s["key"], "|", s["title"], "|", s["description"])
else:
    out = {}
    for sport in sys.argv[2:]:
        r = requests.get("https://api.the-odds-api.com/v4/sports/%s/odds" % sport,
                         params={"apiKey": key, "regions": "uk", "markets": "h2h,totals", "oddsFormat": "decimal"}, timeout=30)
        print(sport, r.status_code, "quota used/remaining", r.headers.get("x-requests-used"), r.headers.get("x-requests-remaining"))
        out[sport] = r.json()
    json.dump(out, open("/Users/triton/PROTEUS/sandbox/intl_odds_2026-09-26.json","w"), indent=1)
    for sport, evs in out.items():
        for e in evs:
            print(e["commence_time"], e["home_team"], "v", e["away_team"], "| books", len(e["bookmakers"]))

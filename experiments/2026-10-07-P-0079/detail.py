"""P-0079: rules of the open bot tournament and the leaderboard of the last finished one."""
import json, os, re, sys, urllib.request
sys.path.insert(0, "/Users/triton/PROTEUS/bin")
from secrets import get  # noqa: E402
HERE = os.path.dirname(os.path.abspath(__file__))
H = {"Authorization": f"Token {get('MetaculusAPI Credentials')}", "User-Agent": "proteus-lab probe P-0079"}
def fetch(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60))
out = {}
for slug in ("fall-futureeval-2026", "spring-aib-2026", "fall-aib-2025"):
    try:
        d = fetch(f"https://www.metaculus.com/api/projects/tournaments/{slug}/")
    except Exception as e:
        out[slug] = {"error": str(e)}; continue
    desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", d.get("description") or ""))
    out[slug] = {"id": d.get("id"), "prize_pool": d.get("prize_pool"), "questions": d.get("questions_count"),
                 "forecasters": d.get("forecasters_count"), "description": desc[:6000]}
    for path in (f"/api/leaderboards/project/{d.get('id')}/", f"/api/projects/{d.get('id')}/leaderboard/"):
        try:
            lb = fetch("https://www.metaculus.com" + path)
            out[slug]["leaderboard_path"] = path
            out[slug]["leaderboard"] = lb
            break
        except Exception as e:
            out[slug].setdefault("leaderboard_errors", []).append(f"{path}: {e}")
json.dump(out, open(os.path.join(HERE, "detail.json"), "w"), indent=1, default=str)
for k, v in out.items():
    print(k, {x: v.get(x) for x in ("id", "prize_pool", "questions", "forecasters", "leaderboard_path", "leaderboard_errors")})

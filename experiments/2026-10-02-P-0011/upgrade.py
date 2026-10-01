"""P-0011: upgrade the Proteus Lichess account to a BOT account (Luke's go, 2 Oct 2026), then confirm it
and open the bot event stream for a few seconds. Prints no secret."""
import importlib.util, json, time, urllib.request, urllib.error
spec = importlib.util.spec_from_file_location("ps", "/Users/triton/PROTEUS/bin/secrets.py")
ps = importlib.util.module_from_spec(spec); spec.loader.exec_module(ps)
H = {"Authorization": "Bearer " + ps.get("LiChess Triton-proteus")}
out = {}
try:
    r = urllib.request.urlopen(urllib.request.Request("https://lichess.org/api/bot/account/upgrade", data=b"", headers=H, method="POST"), timeout=20)
    out["upgrade"] = [r.status, r.read().decode()[:200]]
except urllib.error.HTTPError as e:
    out["upgrade"] = [e.code, e.read().decode()[:200]]
a = json.load(urllib.request.urlopen(urllib.request.Request("https://lichess.org/api/account", headers=H), timeout=20))
out["title_after"] = a.get("title")
out["games"] = a.get("count", {}).get("all")
# event stream: a bot must hold this open to receive challenges; read for ~8 s
t0 = time.time(); lines = 0
try:
    s = urllib.request.urlopen(urllib.request.Request("https://lichess.org/api/stream/event", headers=H), timeout=10)
    out["stream_status"] = s.status
    while time.time() - t0 < 8:
        line = s.readline()
        if not line:
            break
        lines += 1
except Exception as e:
    out["stream_note"] = type(e).__name__
out["stream_lines_8s"] = lines
print(json.dumps(out))
json.dump(out, open("/Users/triton/PROTEUS/experiments/2026-10-02-P-0011/result.json", "w"), indent=1)

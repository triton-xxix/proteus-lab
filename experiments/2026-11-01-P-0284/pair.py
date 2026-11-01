"""P-0284: open the Sketch Stadium SSE stream, take the first snap event, and fetch the server's
canvas.png for that seq straight away. Saves snap.json, canvas-server.png and timing.json beside this script.

    python3 -I experiments/2026-11-01-P-0284/pair.py
"""
import json
import os
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = "https://sketch.wakeshift.ai/games/q5ucru"
req = urllib.request.Request(GAME + "/live", headers={"Accept": "text/event-stream", "User-Agent": "Mozilla/5.0"})
t0 = time.time()
snap = None
with urllib.request.urlopen(req, timeout=30) as r:
    ev, data = None, []
    for raw in r:
        line = raw.decode("utf-8", "replace").rstrip("\n")
        if line.startswith("event:"):
            ev = line[6:].strip()
        elif line.startswith("data:"):
            data.append(line[5:].strip())
        elif line == "":
            if ev == "snap" and data:
                snap = json.loads("".join(data))
                break
            ev, data = None, []
t1 = time.time()
seq = snap["seq"]
png = urllib.request.urlopen(urllib.request.Request(GAME + "/canvas.png?v=%s" % seq, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read()
t2 = time.time()
json.dump(snap, open(os.path.join(HERE, "snap.json"), "w"))
open(os.path.join(HERE, "canvas-server.png"), "wb").write(png)
timing = {"seq": seq, "round": snap.get("round"), "phase": snap.get("phase"), "marks": len(snap.get("strokes") or []),
          "stream_to_snap_s": round(t1 - t0, 2), "snap_to_png_s": round(t2 - t1, 2), "png_bytes": len(png)}
json.dump(timing, open(os.path.join(HERE, "timing.json"), "w"), indent=1)
print(timing)

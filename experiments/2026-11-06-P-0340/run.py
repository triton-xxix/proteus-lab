#!/usr/bin/env python3
"""Time the /graph skill's build.py twice (cold, then warm) on real numbers and check the mp4 it writes.

Data: my own called shots scored at 20, 24, 30 Oct and 6 Nov 2026 (48, 65, 90, 122), from the Field Notes drafts.
The skill's claim: "It takes about 10 seconds."
"""
import json
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = "/Users/triton/PROTEUS/sandbox/animskills/skills/graph/build.py"
base = {
    "label": "Called shots scored",
    "values": [48, 65, 90, 122],
    "labels": ["20 Oct", "24 Oct", "30 Oct", "6 Nov"],
    "final": 122,
}
results = []
for name, extra in (("cold", {}), ("warm", {"dark": True})):
    spec = HERE / f"shots-{name}.graph.json"
    spec.write_text(json.dumps({**base, **extra}, indent=1))
    t = time.time()
    r = subprocess.run(["python3", BUILD, str(spec)], capture_output=True, text=True, timeout=270)
    secs = round(time.time() - t, 1)
    mp4 = spec.with_suffix(".mp4")
    row = {"run": name, "secs": secs, "exit": r.returncode, "mp4": mp4.exists()}
    if mp4.exists():
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,r_frame_rate,nb_frames:format=duration,size", "-of", "json", str(mp4)],
            capture_output=True, text=True,
        )
        row["probe"] = json.loads(p.stdout)
    else:
        row["stdout"] = r.stdout[-1500:]
        row["stderr"] = r.stderr[-1500:]
    results.append(row)
    print(json.dumps(row, indent=1))
(HERE / "results.json").write_text(json.dumps(results, indent=1))

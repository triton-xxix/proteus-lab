"""P-0196: one HyperFrames composition, three per-business ads from a batch file, no HTML edits.

Uses the hyperframes CLI pinned in sandbox/p0192/hf (0.7.109). Lints, renders the default once,
then --batch with three rows, then pulls a frame from each output at 2.5 s and records its sha and
mean colour of the accent stripe so the outputs can be told apart by number, not by eye.
Usage: python3 run.py
"""
import hashlib
import json
import os
import subprocess
import time

HF = "/Users/triton/PROTEUS/sandbox/p0192/hf"
BIN = os.path.join(HF, "node_modules/.bin/hyperframes")
PROJ = "/Users/triton/PROTEUS/sandbox/p0196/ad"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-22-P-0196"
ENV = dict(os.environ, CI="1", HYPERFRAMES_NO_TELEMETRY="1")
R = {}


def sh(cmd, timeout=600):
    t = time.time()
    try:
        p = subprocess.run(cmd, cwd=PROJ, capture_output=True, text=True, timeout=timeout, env=ENV)
        return p.returncode, round(time.time() - t, 1), (p.stdout + p.stderr)[-1500:]
    except subprocess.TimeoutExpired as e:
        return "timeout", round(time.time() - t, 1), str(e.stdout or "")[-1500:]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


html_before = sha(os.path.join(PROJ, "index.html"))
R["lint"] = dict(zip(("rc", "secs", "tail"), sh([BIN, "lint", PROJ], 300)))
default_mp4 = os.path.join(PROJ, "renders/default.mp4")
R["default"] = dict(zip(("rc", "secs", "tail"), sh([BIN, "render", PROJ, "--quality", "draft", "--output", default_mp4])))
tmpl = os.path.join(PROJ, "renders/row-{index}.mp4")
R["batch"] = dict(zip(("rc", "secs", "tail"), sh([BIN, "render", PROJ, "--quality", "draft", "--batch", os.path.join(OUT, "batch.json"), "--output", tmpl, "--strict-variables"], 900)))
R["html_unchanged"] = sha(os.path.join(PROJ, "index.html")) == html_before

frames = {}
outs = sorted(f for f in os.listdir(os.path.join(PROJ, "renders")) if f.endswith(".mp4"))
for f in outs:
    mp4 = os.path.join(PROJ, "renders", f)
    png = os.path.join(OUT, f.replace(".mp4", ".png"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "2.5", "-i", mp4, "-frames:v", "1", png], check=False)
    # accent stripe sits at x 90..310, y 140..154 in a 1280x720 frame
    crop = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", "2.5", "-i", mp4, "-frames:v", "1",
                           "-vf", "crop=200:10:100:142,scale=1:1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          capture_output=True).stdout
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", mp4],
                         capture_output=True, text=True).stdout.strip()
    frames[f] = {"bytes": os.path.getsize(mp4), "duration": dur,
                 "frame_sha": sha(png) if os.path.exists(png) else None,
                 "stripe_rgb": list(crop[:3]) if len(crop) >= 3 else None}
R["outputs"] = frames
R["distinct_frames"] = len({v["frame_sha"] for v in frames.values() if v["frame_sha"]})
json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=2)
print(json.dumps({k: (v if k != "outputs" else v) for k, v in R.items() if k not in ("lint", "default", "batch")}, indent=1))
for k in ("lint", "default", "batch"):
    print(k, R[k]["rc"], R[k]["secs"], R[k]["tail"][-300:].replace("\n", " | "))

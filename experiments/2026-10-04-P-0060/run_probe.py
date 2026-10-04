"""P-0060: render live-panel-skill's codex-agents example to mp4, then run check_frames.py --repeat."""
import json
import os
import subprocess
import time

HERE = "/Users/triton/PROTEUS/experiments/2026-10-04-P-0060"
REPO = "/Users/triton/PROTEUS/sandbox/p0060/live-panel-skill-HEAD"
TMP = "/Users/triton/PROTEUS/sandbox/p0060/tmp"
os.makedirs(TMP, exist_ok=True)
env = dict(os.environ, TMPDIR=TMP)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FFMPEG = "/usr/local/bin/ffmpeg"
PY = "/Users/triton/PROTEUS/.venv/bin/python3"
cfg = f"{REPO}/examples/codex-agents/config.json"
mp4 = "/Users/triton/PROTEUS/sandbox/p0060/codex-agents.mp4"

out = {}
t0 = time.perf_counter()
p = subprocess.run([PY, f"{REPO}/scripts/render.py", "--config", cfg, "--out", mp4,
                    "--chrome", CHROME, "--ffmpeg", FFMPEG,
                    "--html-out", f"{HERE}/codex-agents.html"],
                   env=env, capture_output=True, text=True, timeout=600)
out["render"] = {"rc": p.returncode, "seconds": round(time.perf_counter() - t0, 1),
                 "stdout": p.stdout[-800:], "stderr": p.stderr[-800:],
                 "mp4_bytes": os.path.getsize(mp4) if os.path.exists(mp4) else 0}
if os.path.exists(mp4):
    pr = subprocess.run([FFMPEG.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries",
                         "format=duration:stream=codec_name,width,height,r_frame_rate", "-of", "json", mp4],
                        capture_output=True, text=True)
    out["ffprobe"] = pr.stdout if pr.returncode == 0 else pr.stderr[-300:]

t0 = time.perf_counter()
c = subprocess.run([PY, f"{REPO}/scripts/check_frames.py", "--config", cfg,
                    "--out-dir", f"{HERE}/frames", "--repeat", "--chrome", CHROME, "--ffmpeg", FFMPEG],
                   env=env, capture_output=True, text=True, timeout=600)
out["check"] = {"rc": c.returncode, "seconds": round(time.perf_counter() - t0, 1),
                "stdout": c.stdout[-1500:], "stderr": c.stderr[-800:]}
json.dump(out, open(f"{HERE}/results.json", "w"), indent=2)
print("render rc", out["render"]["rc"], "s", out["render"]["seconds"], "mp4 bytes", out["render"]["mp4_bytes"])
print("render stdout:", out["render"]["stdout"][-300:])
print("render stderr:", out["render"]["stderr"][-300:])
print("ffprobe:", out.get("ffprobe", "")[:400])
print("check rc", out["check"]["rc"], "s", out["check"]["seconds"])
print("check stdout:", out["check"]["stdout"][-900:])
print("check stderr:", out["check"]["stderr"][-300:])

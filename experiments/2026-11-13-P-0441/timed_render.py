"""P-0441: time cinematic-skill's render of its starter explainer, then ffprobe the result."""
import json, subprocess, sys, time
PY = "/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3"
S = "/Users/triton/PROTEUS/sandbox/p0441/src/cinematic-skill-main/skills/cinematic-film/scripts/render.py"
P = "/Users/triton/PROTEUS/sandbox/p0441/cherry"
size = sys.argv[1] if len(sys.argv) > 1 else "1280x720"
out = f"out/draft-{size}.mp4"
t0 = time.time()
r = subprocess.run([PY, S, "--project", P, "--size", size, "--out", out, "--audio", "audio/narration.m4a"], capture_output=True, text=True)
secs = time.time() - t0
print(r.stdout[-1500:], r.stderr[-1500:])
probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames",
                        "-of", "json", f"{P}/{out}"], capture_output=True, text=True)
res = {"size": size, "exit": r.returncode, "render_seconds": round(secs, 1), "ffprobe": json.loads(probe.stdout or "{}")}
print(json.dumps(res, indent=1))
json.dump(res, open(f"/Users/triton/PROTEUS/experiments/2026-11-13-P-0441/render-{size}.json", "w"), indent=1)

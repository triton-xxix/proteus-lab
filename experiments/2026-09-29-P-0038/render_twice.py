#!/usr/bin/env python3
"""P-0038: render motion-broll's first example clip twice, offline, and compare.
Measures wall time, frame count, file size, sha256 of each MP4, and whether decoded frames match."""
import hashlib, json, subprocess, time, os
SB = "/Users/triton/PROTEUS/sandbox/motion-broll/"
OUT = "/Users/triton/PROTEUS/experiments/2026-09-29-P-0038/"
NODE, FFPROBE, FFMPEG = "/usr/local/bin/node", "/usr/local/bin/ffprobe", "/usr/local/bin/ffmpeg"
res = {}
for tag in ("a", "b"):
    mp4 = SB + "out/%s.mp4" % tag
    os.makedirs(SB + "out", exist_ok=True)
    t = time.time()
    p = subprocess.run([NODE, SB + "run-render.js", SB + "dist/01-opus-drop.html", mp4], capture_output=True, text=True, timeout=900)
    r = {"secs": round(time.time() - t, 1), "rc": p.returncode, "stdout": p.stdout.strip()[-300:], "stderr": p.stderr.strip()[-600:]}
    if os.path.exists(mp4):
        r["bytes"] = os.path.getsize(mp4)
        r["sha256"] = hashlib.sha256(open(mp4, "rb").read()).hexdigest()
        pr = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                             "stream=codec_name,width,height,r_frame_rate,nb_read_frames,pix_fmt", "-of", "json", mp4],
                            capture_output=True, text=True)
        r["probe"] = json.loads(pr.stdout or "{}").get("streams", [{}])[0]
        fm = subprocess.run([FFMPEG, "-v", "error", "-i", mp4, "-f", "framemd5", "-"], capture_output=True, text=True)
        r["framemd5"] = hashlib.sha256(fm.stdout.encode()).hexdigest()
        r["frame_hashes"] = [ln.split(",")[-1].strip() for ln in fm.stdout.splitlines() if ln and not ln.startswith("#")]
    res[tag] = r
a, b = res["a"], res["b"]
fa, fb = a.get("frame_hashes", []), b.get("frame_hashes", [])
diff = [i for i, (x, y) in enumerate(zip(fa, fb)) if x != y]
summary = {
    "file_identical": a.get("sha256") == b.get("sha256") and a.get("sha256") is not None,
    "decoded_frames_identical": bool(fa) and fa == fb,
    "frames": [len(fa), len(fb)], "frames_differing": len(diff), "first_diffs": diff[:10],
}
# middle frame still for the write-up
if a.get("rc") == 0:
    subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", "5.0", "-i", SB + "out/a.mp4", "-frames:v", "1", "-vf", "scale=960:-1", OUT + "frame-5s.png"])
for r in res.values(): r.pop("frame_hashes", None)
json.dump({"runs": res, "summary": summary}, open(OUT + "result.json", "w"), indent=1)
print(json.dumps({"runs": res, "summary": summary}, indent=1))

"""P-0019: does hyperframes-student-kit's keyless demo lint, preview and render to a valid mp4?

Fetches the repo tarball (no git clone: not on the unattended safe list), installs with
--ignore-scripts, runs the demo scaffold, then hyperframes lint and render. Every step is timed
and its tail logged to the experiment folder. Usage: python3 p0019_student_kit.py STEP
STEP is fetch, install, demo, lint, render, probe (ffprobe the mp4) or all.
"""
import io
import json
import os
import subprocess
import sys
import tarfile
import time
import urllib.request

SANDBOX = "/Users/triton/PROTEUS/sandbox/hf-student-kit"
OUT = "/Users/triton/PROTEUS/experiments/2026-09-26-P-0019"
TARBALL = "https://codeload.github.com/nateherkai/hyperframes-student-kit/tar.gz/refs/heads/main"
LOG = os.path.join(OUT, "steps.jsonl")


def log(step, rc, secs, out):
    os.makedirs(OUT, exist_ok=True)
    tail = out[-2500:]
    with open(LOG, "a") as f:
        f.write(json.dumps({"step": step, "rc": rc, "secs": round(secs, 1), "tail": tail}) + "\n")
    print("== %s rc=%s %.1fs\n%s" % (step, rc, secs, tail))


def run(step, cmd, cwd=None, timeout=600):
    t = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd or SANDBOX, capture_output=True, text=True, timeout=timeout,
                           env=dict(os.environ, CI="1", HYPERFRAMES_NO_TELEMETRY="1"))
        log(step, p.returncode, time.time() - t, (p.stdout or "") + (p.stderr or ""))
        return p.returncode
    except subprocess.TimeoutExpired as e:
        log(step, "timeout", time.time() - t, str(e.stdout or "") + str(e.stderr or ""))
        return -1


def fetch():
    t = time.time()
    data = urllib.request.urlopen(TARBALL, timeout=120).read()
    os.makedirs(SANDBOX, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        members = []
        for m in tf.getmembers():
            parts = m.name.split("/", 1)
            if len(parts) < 2 or not parts[1]:
                continue
            m.name = parts[1]
            if m.name.startswith("/") or ".." in m.name.split("/"):
                continue
            members.append(m)
        tf.extractall(SANDBOX, members=members, filter="data")
    log("fetch", 0, time.time() - t, "%d bytes, %d members" % (len(data), len(members)))


def find_demo():
    d = os.path.join(SANDBOX, "video-projects", "demo")
    return [d] if os.path.isdir(d) else []


def main(step):
    if step in ("fetch", "all"):
        fetch()
    if step in ("install", "all"):
        run("install", ["npm", "install", "--ignore-scripts", "--no-audit", "--no-fund"], timeout=600)
    if step in ("demo", "all"):
        run("demo", ["npm", "run", "demo"], timeout=300)
        print("demo dirs:", find_demo())
    if step in ("lint", "all"):
        for d in find_demo():
            run("lint", ["npx", "--no-install", "hyperframes", "lint", d], timeout=300)
    if step in ("render", "all"):
        for d in find_demo():
            out = os.path.join(OUT, "demo.mp4")
            run("render", ["npx", "--no-install", "hyperframes", "render", d, "--quality", "draft",
                           "--output", out], timeout=900)
    if step in ("probe", "all"):
        run("ffprobe", ["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_name,width,height,r_frame_rate",
                        "-of", "json", os.path.join(OUT, "demo.mp4")], cwd=OUT, timeout=60)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")

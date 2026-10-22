"""P-0012: which of the four W39 Field Notes AI builder tools still run cleanly a month later?

Re-runs each tool from the copy already in sandbox/ (what a reader of the 26 Sep notes would have
installed), no reinstall, and compares the measured result with the 26 Sep experiment folders:
  reladraw   P-0020  same 3-node diagram rendered twice; sha v the September sha
  magpie     P-0022  the nine SetJSON/DelJSON cases on fresh copies; err strings v September
  golive     P-0023  version, detect, plan, bare apply with a fake HOME; rc per step v September
  hyperframes P-0019 lint and draft render of the demo; rc and seconds v September
"clean" = every step the September run passed still passes, same answer. Usage: python3 rerun.py
"""
import hashlib
import json
import os
import subprocess
import time
import xml.etree.ElementTree as ET

SB = "/Users/triton/PROTEUS/sandbox"
EXP = "/Users/triton/PROTEUS/experiments"
OUT = os.path.join(EXP, "2026-10-22-P-0012")
os.makedirs(OUT, exist_ok=True)
R = {}


def sh(cmd, cwd, env=None, timeout=600, stdin=None):
    t = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env,
                           stdin=stdin)
        return p.returncode, round(time.time() - t, 1), (p.stdout + p.stderr)[-1500:]
    except subprocess.TimeoutExpired as e:
        return "timeout", round(time.time() - t, 1), str(e.stdout or "")[-1500:]
    except FileNotFoundError as e:
        return "missing", 0.0, str(e)


# ---------------- reladraw (P-0020)
def reladraw():
    r = {}
    sb = os.path.join(SB, "reladraw")
    sept = json.load(open(os.path.join(EXP, "2026-09-26-P-0020", "results.json")))
    src = open(os.path.join(EXP, "2026-09-26-P-0020", "three.reladraw")).read()
    shas = []
    for i in (1, 2):
        svg = os.path.join(OUT, "reladraw-three-%d.svg" % i)
        path = os.path.join(OUT, "three.reladraw")
        open(path, "w").write(src)
        rc, secs, out = sh([os.path.join(sb, "node_modules/.bin/reladraw"), path, "-o", svg], sb)
        e = {"rc": rc, "secs": secs}
        if rc == 0 and os.path.exists(svg):
            data = open(svg, "rb").read()
            e["sha"] = hashlib.sha256(data).hexdigest()[:16]
            try:
                ET.fromstring(data)
                e["well_formed"] = True
            except ET.ParseError as ex:
                e["well_formed"] = str(ex)
            shas.append(e["sha"])
        else:
            e["out"] = out
        r["render_%d" % i] = e
    r["sept_sha"] = sept["three"].get("sha")
    r["deterministic"] = len(shas) == 2 and shas[0] == shas[1]
    r["same_as_sept"] = bool(shas) and shas[0] == r["sept_sha"]
    rc, secs, out = sh(["npm", "ls", "reladraw"], sb)
    r["version"] = out.strip()
    r["clean"] = bool(r["deterministic"] and r["render_1"].get("well_formed") is True)
    return r


# ---------------- magpie (P-0022)
def magpie():
    r = {}
    sb = os.path.join(SB, "magpie-probe")
    goroot = os.path.join(sb, "go")
    src = os.path.join(sb, "magpie")
    sept = json.load(open(os.path.join(EXP, "2026-09-26-P-0022", "results.json")))
    septcases = os.path.join(EXP, "2026-09-26-P-0022", "cases")
    cases = os.path.join(OUT, "magpie-cases")
    os.makedirs(cases, exist_ok=True)
    before = open(os.path.join(septcases, "before.json")).read()
    spec = json.load(open(os.path.join(septcases, "cases.json")))
    for name in spec:
        open(os.path.join(cases, name + ".after.json"), "w").write(before)
    open(os.path.join(cases, "cases.json"), "w").write(json.dumps(spec, indent=1))
    open(os.path.join(cases, "before.json"), "w").write(before)
    e = dict(os.environ)
    e.update(GOROOT=goroot, GOPATH=os.path.join(sb, "gopath"), GOMODCACHE=os.path.join(sb, "gomod"),
             GOCACHE=os.path.join(sb, "gocache"), GOTOOLCHAIN="local", GOFLAGS="-mod=mod",
             PROTEUS_CASES=cases, PATH=os.path.join(goroot, "bin") + ":" + e.get("PATH", ""))
    rc, secs, out = sh([os.path.join(goroot, "bin", "go"), "test", "./internal/edit/", "-run",
                        "TestProteusProbe", "-count=1"], src, env=e, timeout=600)
    r["go_test"] = {"rc": rc, "secs": secs, "tail": out[-600:]}
    same, diff = 0, []
    for name in spec:
        ep = os.path.join(cases, name + ".err")
        now = open(ep).read() if os.path.exists(ep) else "no run"
        then = sept["cases"][name]["err"]
        after_now = open(os.path.join(cases, name + ".after.json")).read()
        after_then = open(os.path.join(septcases, name + ".after.json")).read()
        if now == then and after_now == after_then:
            same += 1
        else:
            diff.append({"case": name, "err_now": now, "err_sept": then,
                         "output_identical": after_now == after_then})
    r["cases_total"] = len(spec)
    r["cases_identical_to_sept"] = same
    r["differences"] = diff
    r["clean"] = rc == 0 and same == len(spec)
    return r


# ---------------- golive (P-0023)
def golive():
    r = {}
    sb = os.path.join(SB, "golive-probe")
    home = os.path.join(sb, "fakehome")
    app = os.path.join(sb, "scratch-app")
    binp = os.path.join(sb, "node_modules", ".bin", "golive")
    env = {"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin", "HOME": home,
           "XDG_CONFIG_HOME": os.path.join(home, ".config"), "NO_COLOR": "1", "CI": "1"}
    sept = {e["label"]: e for e in json.load(open(os.path.join(EXP, "2026-09-26-P-0023", "results-run.json")))
            if "label" in e}
    steps = [("version", [binp, "version", "--json"]), ("detect", [binp, "detect", "--json"]),
             ("doctor", [binp, "doctor", "--json"]), ("plan", [binp, "plan", "--json"]),
             ("apply_bare", [binp, "apply"])]
    agree = 0
    for label, cmd in steps:
        rc, secs, out = sh(cmd, app, env=env, timeout=180, stdin=subprocess.DEVNULL)
        then = sept.get(label, {}).get("rc")
        r[label] = {"rc": rc, "secs": secs, "rc_sept": then, "tail": out[-300:]}
        if label == "detect":
            detect_out = out.lower()
        if rc == then:
            agree += 1
    r["steps_same_rc_as_sept"] = "%d of %d" % (agree, len(steps))
    # the two claims the notes made: detect names the stack, bare apply refuses
    r["detect_names_stack"] = all(k in detect_out for k in ("next", "supabase", "stripe", "resend"))
    r["apply_refused"] = r["apply_bare"]["rc"] not in (0, "missing", "timeout")
    r["clean"] = agree == len(steps) and r["detect_names_stack"] and r["apply_refused"]
    return r


# ---------------- hyperframes student kit (P-0019)
def hyperframes():
    r = {}
    sb = os.path.join(SB, "hf-student-kit")
    demo = os.path.join(sb, "video-projects", "demo")
    sept = [json.loads(l) for l in open(os.path.join(EXP, "2026-09-26-P-0019", "steps.jsonl"))]
    r["sept"] = {s["step"]: {"rc": s["rc"], "secs": s["secs"]} for s in sept}
    env = dict(os.environ, CI="1", HYPERFRAMES_NO_TELEMETRY="1")
    r["demo_dir_present"] = os.path.isdir(demo)
    rc, secs, out = sh(["npx", "--no-install", "hyperframes", "--version"], sb, env=env, timeout=120)
    r["version"] = {"rc": rc, "out": out.strip()[-200:]}
    rc, secs, out = sh(["npx", "--no-install", "hyperframes", "lint", demo], sb, env=env, timeout=300)
    r["lint"] = {"rc": rc, "secs": secs, "tail": out[-500:]}
    mp4 = os.path.join(OUT, "hf-demo.mp4")
    rc, secs, out = sh(["npx", "--no-install", "hyperframes", "render", demo, "--quality", "draft",
                        "--output", mp4], sb, env=env, timeout=600)
    r["render"] = {"rc": rc, "secs": secs, "tail": out[-500:]}
    if os.path.exists(mp4):
        rc2, _, probe = sh(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration,size:stream=codec_name,width,height", "-of", "json", mp4], OUT)
        r["ffprobe"] = probe[-600:]
        os.remove(mp4)  # 1080p mp4 does not belong in git
    r["clean"] = r["lint"]["rc"] == 0 and r["render"]["rc"] == 0 and "ffprobe" in r
    return r


for name, fn in (("reladraw", reladraw), ("magpie", magpie), ("golive", golive), ("hyperframes", hyperframes)):
    t = time.time()
    try:
        R[name] = fn()
    except Exception as ex:
        R[name] = {"clean": False, "exception": repr(ex)}
    R[name]["wall_secs"] = round(time.time() - t, 1)
    json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=2)
    print("== %s clean=%s %.0fs" % (name, R[name].get("clean"), R[name]["wall_secs"]))

R["still_clean"] = sum(1 for v in R.values() if isinstance(v, dict) and v.get("clean"))
json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=2)
print(json.dumps(R, indent=1)[-5000:])
print("STILL CLEAN: %d of 4" % R["still_clean"])

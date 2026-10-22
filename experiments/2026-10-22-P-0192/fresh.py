"""P-0192: fresh install today of the four W39 tools, same checks as P-0012, versions recorded.

New sandbox dirs under sandbox/p0192/. Reuses the Go toolchain from sandbox/magpie-probe/go (the
toolchain is not the tool under test). Compares with the 26 Sep experiment folders and with the
P-0012 re-run of the pinned copies. Usage: python3 fresh.py
"""
import hashlib
import io
import json
import os
import subprocess
import tarfile
import time
import urllib.request
import xml.etree.ElementTree as ET

SB = "/Users/triton/PROTEUS/sandbox/p0192"
OLD = "/Users/triton/PROTEUS/sandbox"
EXP = "/Users/triton/PROTEUS/experiments"
OUT = os.path.join(EXP, "2026-10-22-P-0192")
CACHE = os.path.join(OLD, ".npm-cache")
os.makedirs(OUT, exist_ok=True)
R = {}


def sh(cmd, cwd, env=None, timeout=600, stdin=None):
    t = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env, stdin=stdin)
        return p.returncode, round(time.time() - t, 1), (p.stdout + p.stderr)[-2000:]
    except subprocess.TimeoutExpired as e:
        return "timeout", round(time.time() - t, 1), str(e.stdout or "")[-2000:]
    except FileNotFoundError as e:
        return "missing", 0.0, str(e)


def extract(url, dest, strip=1):
    t = time.time()
    data = urllib.request.urlopen(url, timeout=300).read()
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        ms = []
        for m in tf.getmembers():
            parts = m.name.split("/", strip)
            if len(parts) <= strip or not parts[strip]:
                continue
            m.name = parts[strip]
            if m.name.startswith("/") or ".." in m.name.split("/"):
                continue
            ms.append(m)
        tf.extractall(dest, members=ms, filter="data")
    return {"bytes": len(data), "members": len(ms), "secs": round(time.time() - t, 1)}


def npm_install(dest, pkg):
    os.makedirs(dest, exist_ok=True)
    pj = os.path.join(dest, "package.json")
    if not os.path.exists(pj):
        open(pj, "w").write('{"name": "p0192", "private": true}\n')
    args = ["npm", "--prefix", dest, "install", "--ignore-scripts", "--no-audit", "--no-fund", "--cache", CACHE]
    if pkg:
        args.append(pkg)
    return sh(args, dest, timeout=600)


def installed_version(dest, name):
    pj = os.path.join(dest, "node_modules", name, "package.json")
    return json.load(open(pj)).get("version") if os.path.exists(pj) else None


def reladraw():
    r = {}
    d = os.path.join(SB, "reladraw")
    rc, secs, out = npm_install(d, "reladraw")
    r["install"] = {"rc": rc, "secs": secs}
    r["version"] = installed_version(d, "reladraw")
    r["version_sept"] = "0.5.0"
    sept = json.load(open(os.path.join(EXP, "2026-09-26-P-0020", "results.json")))
    src = os.path.join(EXP, "2026-09-26-P-0020", "three.reladraw")
    shas = []
    rc0, _, out0 = sh([os.path.join(d, "node_modules/.bin/reladraw"), src, "-o", os.path.join(OUT, "reladraw-sept-form.svg")], d)
    r["september_command_line"] = {"rc": rc0, "out": out0[-300:]}
    for i in (1, 2):
        svg = os.path.join(OUT, "reladraw-three-%d.svg" % i)
        rc, secs, out = sh([os.path.join(d, "node_modules/.bin/reladraw"), "render", src, "-o", svg], d)
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
            e["out"] = out[-400:]
        r["render_%d" % i] = e
    r["sept_sha"] = sept["three"].get("sha")
    r["deterministic"] = len(shas) == 2 and shas[0] == shas[1]
    r["same_bytes_as_sept"] = bool(shas) and shas[0] == r["sept_sha"]
    r["clean"] = r["deterministic"] and r["render_1"].get("well_formed") is True
    # migrated copy: the 0.18.0 error says "level with" is now "even with"
    mig = os.path.join(OUT, "three-migrated.reladraw")
    open(mig, "w").write(open(src).read().replace("level with", "even with"))
    mshas = []
    for i in (1, 2):
        svg = os.path.join(OUT, "reladraw-migrated-%d.svg" % i)
        rc, secs, out = sh([os.path.join(d, "node_modules/.bin/reladraw"), "render", mig, "-o", svg], d)
        e = {"rc": rc, "secs": secs}
        if rc == 0 and os.path.exists(svg):
            data = open(svg, "rb").read()
            e["sha"] = hashlib.sha256(data).hexdigest()[:16]
            e["bytes"] = len(data)
            try:
                ET.fromstring(data)
                e["well_formed"] = True
            except ET.ParseError as ex:
                e["well_formed"] = str(ex)
            mshas.append(e["sha"])
        else:
            e["out"] = out[-300:]
        r["migrated_render_%d" % i] = e
    r["migrated_deterministic"] = len(mshas) == 2 and mshas[0] == mshas[1]
    r["migrated_same_bytes_as_sept"] = bool(mshas) and mshas[0] == r["sept_sha"]
    r["sept_bytes"] = sept["three"].get("bytes")
    return r


def magpie():
    r = {}
    d = os.path.join(SB, "magpie")
    goroot = os.path.join(OLD, "magpie-probe", "go")
    r["fetch"] = extract("https://codeload.github.com/yetone/magpie/tar.gz/HEAD", d, 1)
    test_src = open(os.path.join(OLD, "magpie-probe", "magpie", "internal", "edit", "proteus_probe_test.go")).read()
    open(os.path.join(d, "internal", "edit", "proteus_probe_test.go"), "w").write(test_src)
    rc, _, out = sh(["git", "-C", d, "log", "-1"], d)  # tarball has no .git; version from go.mod/CHANGELOG instead
    r["head_marker"] = None
    for name in ("CHANGELOG.md", "VERSION", "go.mod"):
        p = os.path.join(d, name)
        if os.path.exists(p):
            r["head_marker"] = name + ": " + open(p).read()[:120].replace("\n", " | ")
            break
    septcases = os.path.join(EXP, "2026-09-26-P-0022", "cases")
    sept = json.load(open(os.path.join(EXP, "2026-09-26-P-0022", "results.json")))
    cases = os.path.join(OUT, "magpie-cases")
    os.makedirs(cases, exist_ok=True)
    before = open(os.path.join(septcases, "before.json")).read()
    spec = json.load(open(os.path.join(septcases, "cases.json")))
    for name in spec:
        open(os.path.join(cases, name + ".after.json"), "w").write(before)
    open(os.path.join(cases, "cases.json"), "w").write(json.dumps(spec, indent=1))
    e = dict(os.environ)
    sb_old = os.path.join(OLD, "magpie-probe")
    e.update(GOROOT=goroot, GOPATH=os.path.join(sb_old, "gopath"), GOMODCACHE=os.path.join(sb_old, "gomod"),
             GOCACHE=os.path.join(sb_old, "gocache"), GOTOOLCHAIN="local", GOFLAGS="-mod=mod",
             PROTEUS_CASES=cases, PATH=os.path.join(goroot, "bin") + ":" + e.get("PATH", ""))
    rc, secs, out = sh([os.path.join(goroot, "bin", "go"), "test", "./internal/edit/", "-run", "TestProteusProbe", "-count=1"], d, env=e, timeout=600)
    r["go_test"] = {"rc": rc, "secs": secs, "tail": out[-600:]}
    same, diff = 0, []
    for name in spec:
        ep = os.path.join(cases, name + ".err")
        now = open(ep).read() if os.path.exists(ep) else "no run"
        then = sept["cases"][name]["err"]
        a_now = open(os.path.join(cases, name + ".after.json")).read()
        a_then = open(os.path.join(septcases, name + ".after.json")).read()
        if now == then and a_now == a_then:
            same += 1
        else:
            diff.append({"case": name, "err_now": now[:200], "err_sept": then[:200], "output_identical": a_now == a_then})
    r["cases_total"] = len(spec)
    r["cases_identical_to_sept"] = same
    r["differences"] = diff
    r["clean"] = rc == 0 and same == len(spec)
    return r


def golive():
    r = {}
    d = os.path.join(SB, "golive")
    rc, secs, out = npm_install(d, "golive@alpha")
    r["install"] = {"rc": rc, "secs": secs, "tail": out[-300:]}
    r["version"] = installed_version(d, "golive")
    r["version_sept"] = "0.1.0-alpha.4"
    home = os.path.join(d, "fakehome")
    app = os.path.join(d, "scratch-app")
    os.makedirs(os.path.join(home, ".config"), exist_ok=True)
    os.makedirs(os.path.join(app, "app"), exist_ok=True)
    src_app = os.path.join(OLD, "golive-probe", "scratch-app")
    for rel in ("package.json", ".env.example", "app/page.tsx"):
        open(os.path.join(app, rel), "w").write(open(os.path.join(src_app, rel)).read())
    binp = os.path.join(d, "node_modules", ".bin", "golive")
    env = {"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin", "HOME": home,
           "XDG_CONFIG_HOME": os.path.join(home, ".config"), "NO_COLOR": "1", "CI": "1"}
    sept = {e["label"]: e for e in json.load(open(os.path.join(EXP, "2026-09-26-P-0023", "results-run.json"))) if "label" in e}
    steps = [("version", [binp, "version", "--json"]), ("detect", [binp, "detect", "--json"]),
             ("init", [binp, "init", "--stack", "hosting=vercel,db=supabase,payments=stripe,email=resend", "--json"]),
             ("doctor", [binp, "doctor", "--json"]), ("plan", [binp, "plan", "--json"]), ("apply_bare", [binp, "apply"])]
    agree = 0
    detect_out = ""
    for label, cmd in steps:
        rc, secs, out = sh(cmd, app, env=env, timeout=180, stdin=subprocess.DEVNULL)
        then = sept.get(label, {}).get("rc")
        r["step_" + label] = {"rc": rc, "secs": secs, "rc_sept": then, "tail": out[-300:]}
        if label == "detect":
            detect_out = out.lower()
        if rc == then:
            agree += 1
    r["steps_same_rc_as_sept"] = "%d of %d" % (agree, len(steps))
    r["detect_names_stack"] = all(k in detect_out for k in ("next", "supabase", "stripe", "resend"))
    r["apply_refused"] = r["step_apply_bare"]["rc"] not in (0, "missing", "timeout")
    r["clean"] = agree == len(steps) and r["detect_names_stack"] and r["apply_refused"]
    return r


def hyperframes():
    r = {}
    d = os.path.join(SB, "hf")
    r["fetch"] = extract("https://codeload.github.com/nateherkai/hyperframes-student-kit/tar.gz/refs/heads/main", d, 1)
    env = dict(os.environ, CI="1", HYPERFRAMES_NO_TELEMETRY="1")
    rc, secs, out = npm_install(d, None)
    r["install"] = {"rc": rc, "secs": secs, "tail": out[-300:]}
    r["version"] = installed_version(d, "hyperframes")
    r["version_sept"] = "0.7.109"
    rc, secs, out = sh(["npm", "run", "demo"], d, env=env, timeout=300)
    r["demo"] = {"rc": rc, "secs": secs, "tail": out[-300:]}
    demo = os.path.join(d, "video-projects", "demo")
    r["demo_dir_present"] = os.path.isdir(demo)
    rc, secs, out = sh(["npx", "--no-install", "hyperframes", "lint", demo], d, env=env, timeout=300)
    r["lint"] = {"rc": rc, "secs": secs, "tail": out[-400:]}
    mp4 = os.path.join(OUT, "hf-demo.mp4")
    rc, secs, out = sh(["npx", "--no-install", "hyperframes", "render", demo, "--quality", "draft", "--output", mp4], d, env=env, timeout=600)
    r["render"] = {"rc": rc, "secs": secs, "tail": out[-400:]}
    if os.path.exists(mp4):
        _, _, probe = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration,size:stream=codec_name,width,height", "-of", "json", mp4], OUT)
        r["ffprobe"] = probe[-500:]
        os.remove(mp4)
    r["clean"] = r["lint"]["rc"] == 0 and r["render"]["rc"] == 0 and "ffprobe" in r
    return r


import sys  # noqa: E402

ALL = (("reladraw", reladraw), ("golive", golive), ("magpie", magpie), ("hyperframes", hyperframes))
only = sys.argv[1:]
rp = os.path.join(OUT, "results.json")
if only and os.path.exists(rp):
    R = json.load(open(rp))  # second pass keeps the first pass's other tools
    R.pop("still_clean", None)
for name, fn in ALL:
    if only and name not in only:
        continue
    t = time.time()
    try:
        R[name] = fn()
    except Exception as ex:
        R[name] = {"clean": False, "exception": repr(ex)}
    R[name]["wall_secs"] = round(time.time() - t, 1)
    json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=2)
    print("== %s clean=%s version=%s %.0fs" % (name, R[name].get("clean"), R[name].get("version"), R[name]["wall_secs"]))

R["still_clean"] = sum(1 for v in R.values() if isinstance(v, dict) and v.get("clean"))
json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=2)
print(json.dumps(R, indent=1)[-6000:])
print("CLEAN FRESH: %d of 4" % R["still_clean"])

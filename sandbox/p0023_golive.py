"""P-0023: does golive detect/plan work with no provider account, and does apply refuse without --yes?

Installs golive@alpha from npm into the sandbox (not the skill installer, which writes into the
home directory), builds a scratch app, and runs the CLI with HOME and XDG_CONFIG_HOME pointed at a
fake home inside the sandbox and a minimal environment, so no real login, token or credentials
file can be seen. Never passes --yes. Usage: python3 p0023_golive.py [install|run|all]
"""
import json
import os
import subprocess
import sys
import time

SB = "/Users/triton/PROTEUS/sandbox/golive-probe"
HOME = os.path.join(SB, "fakehome")
APP = os.path.join(SB, "scratch-app")
OUT = "/Users/triton/PROTEUS/experiments/2026-09-26-P-0023"
BIN = os.path.join(SB, "node_modules", ".bin", "golive")

log = []


def env():
    return {"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin", "HOME": HOME,
            "XDG_CONFIG_HOME": os.path.join(HOME, ".config"), "NO_COLOR": "1", "CI": "1"}


def sh(label, cmd, cwd, timeout=180):
    t = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                           env=env(), stdin=subprocess.DEVNULL)
        rc, out = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        rc, out = "timeout", str(e.stdout or "") + str(e.stderr or "")
    entry = {"label": label, "cmd": cmd[1:] if cmd[0] == BIN else cmd, "rc": rc,
             "secs": round(time.time() - t, 1), "out": out[:30000]}
    log.append(entry)
    print("== %s rc=%s %.1fs\n%s\n" % (label, rc, entry["secs"], out[-1500:]))
    return entry


def install():
    os.makedirs(SB, exist_ok=True)
    if not os.path.exists(os.path.join(SB, "package.json")):
        with open(os.path.join(SB, "package.json"), "w") as f:
            f.write('{"name": "p0023", "private": true}\n')
    sh("install", ["npm", "install", "--ignore-scripts", "--no-audit", "--no-fund", "golive@alpha"], SB, 300)
    sh("ls", ["npm", "ls", "--all"], SB)


def scratch():
    os.makedirs(os.path.join(HOME, ".config"), exist_ok=True)
    os.makedirs(os.path.join(APP, "app"), exist_ok=True)
    files = {
        "package.json": json.dumps({"name": "scratch-app", "private": True,
                                    "scripts": {"build": "next build", "start": "next start"},
                                    "dependencies": {"next": "15.0.0", "react": "19.0.0",
                                                     "@supabase/supabase-js": "2.45.0",
                                                     "resend": "4.0.0", "stripe": "17.0.0"}}, indent=2),
        ".env.example": "NEXT_PUBLIC_SUPABASE_URL=\nNEXT_PUBLIC_SUPABASE_ANON_KEY=\nRESEND_API_KEY=\nSTRIPE_SECRET_KEY=\n",
        "app/page.tsx": "export default function Page() { return <h1>scratch</h1> }\n",
    }
    for rel, body in files.items():
        with open(os.path.join(APP, rel), "w") as f:
            f.write(body)


def run():
    scratch()
    sh("version", [BIN, "version", "--json"], APP)
    sh("help", [BIN, "help"], APP)
    sh("credentials", [BIN, "credentials"], APP)
    sh("detect", [BIN, "detect", "--json"], APP)
    sh("plan_before_init", [BIN, "plan", "--json"], APP)
    sh("init", [BIN, "init", "--stack", "hosting=vercel,db=supabase,payments=stripe,email=resend", "--json"], APP)
    sh("doctor", [BIN, "doctor", "--json"], APP)
    sh("plan", [BIN, "plan", "--json"], APP)
    sh("apply_bare", [BIN, "apply"], APP)
    plan_id = None
    for e in log:
        if e["label"] == "plan":
            try:
                plan_id = json.loads(e["out"][e["out"].find("{"):]).get("id") or None
            except Exception:
                pass
            if not plan_id:
                import re
                m = re.search(r'"?planId"?\s*[:=]\s*"?([A-Za-z0-9_.:-]+)', e["out"])
                plan_id = m.group(1) if m else None
    if plan_id:
        sh("apply_plan_no_yes", [BIN, "apply", "--plan", plan_id], APP)
        sh("apply_plan_confirm_live_no_yes", [BIN, "apply", "--plan", plan_id, "--confirm-live"], APP)
    written = []
    for root, dirs, files in os.walk(HOME):
        for f in files:
            written.append(os.path.relpath(os.path.join(root, f), HOME))
    app_files = []
    for root, dirs, files in os.walk(APP):
        for f in files:
            app_files.append(os.path.relpath(os.path.join(root, f), APP))
    log.append({"label": "fakehome_files", "files": written, "app_files": app_files, "plan_id": plan_id})


def main(step):
    os.makedirs(OUT, exist_ok=True)
    if step in ("install", "all"):
        install()
    if step in ("run", "all"):
        run()
    path = os.path.join(OUT, "results-%s.json" % step)
    json.dump(log, open(path, "w"), indent=2)
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")

"""P-0022: does magpie's config writer touch only the target key in a settings.json?

Downloads the official Go toolchain (go.dev) and the magpie source tarball into the sandbox, drops
one extra test file into magpie's internal/edit package that runs SetJSON/DelJSON on COPIES of
sample JSONC files under the experiment folder (never a real config), then diffs each output
against its input with difflib. Usage: python3 p0022_magpie.py [setup|test|diff|all]
"""
import difflib
import io
import json
import os
import platform
import subprocess
import sys
import tarfile
import time
import urllib.request

SB = "/Users/triton/PROTEUS/sandbox/magpie-probe"
GOROOT = os.path.join(SB, "go")
SRC = os.path.join(SB, "magpie")
OUT = "/Users/triton/PROTEUS/experiments/2026-09-26-P-0022"
CASES = os.path.join(OUT, "cases")

SAMPLE = """{
  // Claude Code settings, hand-edited
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "opus", /* the default */
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com",  // keep the comment
    "DISABLE_TELEMETRY": "1"
  },
  "permissions": {
    "allow": ["Bash(ls:*)", "Read"],
    "deny": []
  },
  "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo {"}]}]},
  "statusLine": {
\t"type": "command"
  },
  "trailing": true,
}
"""

# name -> (op, key path, value); every case starts from a fresh copy of SAMPLE
TESTS = {
    "replace_nested": ("set", "env.ANTHROPIC_BASE_URL", "http://127.0.0.1:3425"),
    "replace_top": ("set", "model", "kimi-k2"),
    "insert_into_existing": ("set", "env.ANTHROPIC_MODEL", "deepseek-chat"),
    "insert_new_parent": ("set", "magpie.enabled", True),
    "replace_scalar_with_object": ("set", "model.name", "x"),
    "replace_in_tab_block": ("set", "statusLine.type", "static"),
    "delete_member": ("del", "env.DISABLE_TELEMETRY", None),
    "delete_last_member": ("del", "permissions.deny", None),
    "key_with_wildcard": ("set", "env.WEIRD?KEY", "v"),
}

GO_TEST = r'''package edit

import (
	"encoding/json"
	"os"
	"path/filepath"
	"testing"
)

type proteusCase struct {
	Op    string `json:"op"`
	Path  string `json:"path"`
	Value any    `json:"value"`
}

func TestProteusProbe(t *testing.T) {
	dir := os.Getenv("PROTEUS_CASES")
	spec, err := os.ReadFile(filepath.Join(dir, "cases.json"))
	if err != nil {
		t.Fatal(err)
	}
	cases := map[string]proteusCase{}
	if err := json.Unmarshal(spec, &cases); err != nil {
		t.Fatal(err)
	}
	for name, c := range cases {
		f := filepath.Join(dir, name+".after.json")
		var err error
		if c.Op == "del" {
			err = DelJSON(f, c.Path)
		} else {
			err = SetJSON(f, KV{Path: c.Path, Value: c.Value})
		}
		msg := "ok"
		if err != nil {
			msg = err.Error()
		}
		os.WriteFile(filepath.Join(dir, name+".err"), []byte(msg), 0o644)
	}
}
'''


def sh(cmd, cwd, env=None, timeout=900):
    t = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
    return p.returncode, round(time.time() - t, 1), (p.stdout + p.stderr)[-3000:]


def extract(url, dest, strip):
    data = urllib.request.urlopen(url, timeout=300).read()
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        ms = []
        for m in tf.getmembers():
            parts = m.name.split("/", strip)
            if len(parts) <= strip or not parts[strip]:
                continue
            m.name = parts[strip]
            ms.append(m)
        tf.extractall(dest, members=ms, filter="data")
    return len(data)


def setup(log):
    arch = {"arm64": "arm64", "x86_64": "amd64"}[platform.machine()]
    if not os.path.exists(os.path.join(GOROOT, "bin", "go")):
        ver = urllib.request.urlopen("https://go.dev/VERSION?m=text", timeout=30).read().decode().split()[0]
        t = time.time()
        n = extract("https://go.dev/dl/%s.darwin-%s.tar.gz" % (ver, arch), GOROOT, 1)
        log["go"] = {"version": ver, "bytes": n, "secs": round(time.time() - t, 1)}
    if not os.path.exists(os.path.join(SRC, "go.mod")):
        t = time.time()
        n = extract("https://codeload.github.com/yetone/magpie/tar.gz/HEAD", SRC, 1)
        log["magpie"] = {"bytes": n, "secs": round(time.time() - t, 1)}
    with open(os.path.join(SRC, "internal", "edit", "proteus_probe_test.go"), "w") as f:
        f.write(GO_TEST)


def env():
    e = dict(os.environ)
    e.update(GOROOT=GOROOT, GOPATH=os.path.join(SB, "gopath"), GOMODCACHE=os.path.join(SB, "gomod"),
             GOCACHE=os.path.join(SB, "gocache"), GOTOOLCHAIN="local", GOFLAGS="-mod=mod",
             PROTEUS_CASES=CASES, PATH=os.path.join(GOROOT, "bin") + ":" + e.get("PATH", ""))
    return e


def test(log):
    os.makedirs(CASES, exist_ok=True)
    with open(os.path.join(CASES, "before.json"), "w") as f:
        f.write(SAMPLE)
    spec = {}
    for name, (op, path, value) in TESTS.items():
        with open(os.path.join(CASES, name + ".after.json"), "w") as f:
            f.write(SAMPLE)
        spec[name] = {"op": op, "path": path, "value": value}
    with open(os.path.join(CASES, "cases.json"), "w") as f:
        json.dump(spec, f, indent=1)
    rc, secs, out = sh([os.path.join(GOROOT, "bin", "go"), "test", "./internal/edit/", "-run",
                        "TestProteusProbe|TestSet|TestDel|TestJSON", "-count=1", "-v"], SRC, env())
    log["go_test"] = {"rc": rc, "secs": secs, "tail": out}


def diff(log):
    before = SAMPLE.splitlines(keepends=True)
    res = {}
    for name, (op, path, value) in TESTS.items():
        after = open(os.path.join(CASES, name + ".after.json")).read()
        err = open(os.path.join(CASES, name + ".err")).read() if os.path.exists(os.path.join(CASES, name + ".err")) else "no run"
        d = list(difflib.unified_diff(before, after.splitlines(keepends=True), "before", "after", n=0))
        removed = [l for l in d if l.startswith("-") and not l.startswith("---")]
        added = [l for l in d if l.startswith("+") and not l.startswith("+++")]
        comments_kept = all(c in after for c in ("// Claude Code settings, hand-edited", "/* the default */"))
        still_parses = None
        try:
            # strip // and /* */ comments crudely for a parse check (strings here hold no //)
            import re
            s = re.sub(r"/\*.*?\*/", "", after, flags=re.S)
            s = re.sub(r"(?m)(?<!:)//.*$", "", s)
            s = re.sub(r",(\s*[}\]])", r"\1", s)
            json.loads(s)
            still_parses = True
        except Exception as e:
            still_parses = "no: %s" % e
        res[name] = {"op": op, "path": path, "err": err, "lines_removed": len(removed),
                     "lines_added": len(added), "comments_kept": comments_kept,
                     "parses": still_parses, "diff": "".join(d[2:])}
    log["cases"] = res


def main(step):
    log = {}
    lp = os.path.join(OUT, "results.json")
    os.makedirs(OUT, exist_ok=True)
    if os.path.exists(lp):
        log = json.load(open(lp))
    if step in ("setup", "all"):
        setup(log)
    if step in ("test", "all"):
        test(log)
    if step in ("diff", "all"):
        diff(log)
    json.dump(log, open(lp, "w"), indent=2)
    print(json.dumps(log, indent=2)[-6000:])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")

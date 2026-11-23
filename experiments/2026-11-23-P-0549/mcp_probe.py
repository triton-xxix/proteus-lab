"""P-0549: drive `hermitcrm mcp` over stdio, list its tools, call one read tool.

Usage: python3 mcp_probe.py HERMITCRM_BIN DATA_DIR OUT_JSON
"""
import json, subprocess, sys, time

binp, data, out = sys.argv[1], sys.argv[2], sys.argv[3]
p = subprocess.Popen([binp, "--data", data, "mcp"], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def send(obj):
    p.stdin.write(json.dumps(obj) + "\n"); p.stdin.flush()

def recv():
    line = p.stdout.readline()
    return json.loads(line) if line else None

t0 = time.time()
send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
      "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                 "clientInfo": {"name": "proteus-probe", "version": "0"}}})
init = recv()
send({"jsonrpc": "2.0", "method": "notifications/initialized"})
send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
tools = recv()
names = [t["name"] for t in (tools or {}).get("result", {}).get("tools", [])]
readonly = [t["name"] for t in (tools or {}).get("result", {}).get("tools", [])
            if (t.get("annotations") or {}).get("readOnlyHint")]
call = None
pick = next((n for n in names if "pipeline" in n or "list" in n or "search" in n), None)
if pick:
    send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
          "params": {"name": pick, "arguments": {}}})
    call = recv()
elapsed = round(time.time() - t0, 2)
p.stdin.close()
try:
    p.wait(timeout=5)
except Exception:
    p.kill()
res = {"server": (init or {}).get("result", {}).get("serverInfo"),
       "protocol": (init or {}).get("result", {}).get("protocolVersion"),
       "n_tools": len(names), "tools": names, "readonly_hint": readonly,
       "called": pick, "call_is_error": (call or {}).get("result", {}).get("isError"),
       "call_text_head": json.dumps(call)[:1500] if call else None,
       "seconds": elapsed}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: res[k] for k in ("server", "n_tools", "called", "call_is_error", "seconds")}))
print(", ".join(names))

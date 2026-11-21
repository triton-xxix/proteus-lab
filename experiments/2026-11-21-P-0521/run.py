"""P-0521: does @kimtaeyoon83/mcp-server-youtube-transcript (npm 0.1.1) return a full transcript
keyless, within 10% of our own pipeline's word count (youtube-transcript-api)?

Drives the MCP server over stdio with JSON-RPC (initialize, tools/list, tools/call) and compares
words returned against youtube_transcript_api on the same videos. Writes results.json beside it.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SERVER = "/Users/triton/PROTEUS/sandbox/p0521/node_modules/@kimtaeyoon83/mcp-server-youtube-transcript/dist/index.js"
VIDEOS = sys.argv[1:] or ["co33P6bb0eg", "mdzIXanauYk", "odRxggAh3G8", "dQw4w9WgXcQ", "jNQXAC9IVRw"]


def rpc(proc, msg, want_id=None, timeout=60):
    proc.stdin.write((json.dumps(msg) + "\n").encode())
    proc.stdin.flush()
    if want_id is None:
        return None
    t0 = time.time()
    while time.time() - t0 < timeout:
        line = proc.stdout.readline()
        if not line:
            return {"error": "server closed"}
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if obj.get("id") == want_id:
            return obj
    return {"error": "timeout"}


def ours(vid):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        fetched = api.fetch(vid, languages=["en", "en-GB", "en-US"])
        text = " ".join(s.text for s in fetched)
        return {"ok": True, "words": len(text.split()), "segments": len(fetched)}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": type(e).__name__ + ": " + str(e)[:160]}


def main():
    proc = subprocess.Popen(["node", SERVER], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    init = rpc(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                      "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                                 "clientInfo": {"name": "proteus-probe", "version": "0.1"}}}, 1)
    rpc(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})
    tools = rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, 2)
    rows = []
    nid = 10
    for vid in VIDEOS:
        nid += 1
        t0 = time.time()
        res = rpc(proc, {"jsonrpc": "2.0", "id": nid, "method": "tools/call",
                         "params": {"name": "get_transcript",
                                    "arguments": {"url": "https://www.youtube.com/watch?v=" + vid,
                                                  "lang": "en"}}}, nid, timeout=90)
        secs = round(time.time() - t0, 2)
        mcp = {"secs": secs}
        r = res.get("result") or {}
        if res.get("error") or r.get("isError"):
            err = res.get("error") or (r.get("content") or [{}])[0].get("text", "")
            mcp.update(ok=False, error=str(err)[:200])
        else:
            text = "".join(c.get("text", "") for c in r.get("content", []))
            mcp.update(ok=True, words=len(text.split()), chars=len(text))
        o = ours(vid)
        ratio = None
        if mcp.get("ok") and o.get("ok") and o["words"]:
            ratio = round(mcp["words"] / o["words"], 3)
        rows.append({"video": vid, "mcp": mcp, "ours": o, "ratio": ratio})
        print(vid, json.dumps(mcp), json.dumps(o), "ratio", ratio)
    proc.terminate()
    out = {"server": "npm @kimtaeyoon83/mcp-server-youtube-transcript 0.1.1",
           "server_info": (init.get("result") or {}).get("serverInfo"),
           "tools": [t.get("name") for t in ((tools.get("result") or {}).get("tools") or [])],
           "tool_args": [list((t.get("inputSchema") or {}).get("properties", {}).keys())
                         for t in ((tools.get("result") or {}).get("tools") or [])],
           "rows": rows}
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=1)
    within = sum(1 for r in rows if r["ratio"] is not None and abs(r["ratio"] - 1) <= 0.10)
    both = sum(1 for r in rows if r["ratio"] is not None)
    print("tools", out["tools"], out["tool_args"])
    print("within 10%:", within, "of", both, "with both; mcp ok", sum(r["mcp"].get("ok", False) for r in rows),
          "ours ok", sum(r["ours"].get("ok", False) for r in rows), "of", len(rows))


main()

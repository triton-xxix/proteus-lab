"""P-0031: drive mcp-youtube-transcript over stdio, keyless, and page through a long transcript.
Copy of sandbox/ytmcp/probe.py. Run with the project interpreter; the server package sits in
sandbox/ytmcp/lib (pip --target, mcp pinned below 2) and is passed to the child through PYTHONPATH.
"""
import asyncio
import json
import os
import sys
import time

LIB = "/Users/triton/PROTEUS/sandbox/ytmcp/lib"
sys.path.insert(0, LIB)

from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402

VIDEOS = sys.argv[1:] or ["SiBhLYf8YJ4", "q4nKy_YPg2s"]
OUT = "/Users/triton/PROTEUS/experiments/2026-09-28-P-0031"


def unpack(res):
    text = "\n".join(c.text for c in res.content if getattr(c, "type", "") == "text")
    sc = getattr(res, "structuredContent", None)
    return text, sc


async def main():
    os.makedirs(OUT, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONPATH"] = LIB
    params = StdioServerParameters(command=sys.executable, args=["-m", "mcp_youtube_transcript"], env=env)
    report = {"videos": []}
    t0 = time.time()
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            tools = await s.list_tools()
            report["startup_secs"] = round(time.time() - t0, 2)
            report["tools"] = [t.name for t in tools.tools]
            print("startup", report["startup_secs"], "s; tools", report["tools"])
            for vid in VIDEOS:
                url = "https://www.youtube.com/watch?v=" + vid
                v = {"id": vid}
                for name in ("get_video_info", "get_available_languages"):
                    t = time.time()
                    try:
                        res = await s.call_tool(name, {"url": url})
                        text, sc = unpack(res)
                        v[name] = {"secs": round(time.time() - t, 2), "error": res.isError, "text": text[:300], "structured": sc}
                    except Exception as e:
                        v[name] = {"exception": repr(e)[:200]}
                pages, cursor, chars, errors, full = [], None, 0, [], []
                tool = "get_timed_transcript" if "get_timed_transcript" in report["tools"] else "get_transcript"
                for i in range(40):
                    args = {"url": url}
                    if cursor:
                        args["next_cursor"] = cursor
                    t = time.time()
                    try:
                        res = await s.call_tool(tool, args)
                    except Exception as e:
                        errors.append(repr(e)[:200])
                        break
                    text, sc = unpack(res)
                    if res.isError:
                        errors.append(text[:300])
                        break
                    body, nxt = text, None
                    if isinstance(sc, dict):
                        nxt = sc.get("next_cursor") or sc.get("nextCursor")
                        body = sc.get("transcript") or sc.get("text") or text
                    else:
                        try:
                            j = json.loads(text)
                            nxt = j.get("next_cursor")
                            body = j.get("transcript") or j.get("text") or text
                        except Exception:
                            pass
                    if not isinstance(body, str):
                        body = json.dumps(body)
                    pages.append({"secs": round(time.time() - t, 2), "chars": len(body), "next_cursor": nxt,
                                  "tail": body[-120:].replace("\n", " | ")})
                    full.append(body)
                    chars += len(body)
                    if not nxt:
                        break
                    cursor = nxt
                v["transcript"] = {"tool": tool, "pages": pages, "chars_total": chars, "errors": errors}
                open(os.path.join(OUT, "transcript-%s.txt" % vid), "w").write("\n".join(full))
                print(vid, tool, len(pages), "pages", chars, "chars", "errors", errors)
                report["videos"].append(v)
    json.dump(report, open(os.path.join(OUT, "probe.json"), "w"), indent=1, default=str)


asyncio.run(main())

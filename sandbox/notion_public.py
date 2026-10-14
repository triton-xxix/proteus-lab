#!/usr/bin/env python3
"""Text of a public Notion page (a <name>.notion.site share), keyless. Written 14 Oct 2026 for the
lead-gen Spark Notes. The site's own /api/v3/loadPageChunk answers without a login for public pages;
a share link's block id may be an alias whose first child page is the real one.

    notion_public.py <site host> <page-or-alias id> [--out file.md]
"""
import json, sys, urllib.request

def chunk(host, pid):
    body = json.dumps({"pageId": pid, "limit": 500, "cursor": {"stack": []}, "chunkNumber": 0,
                       "verticalColumns": False}).encode()
    req = urllib.request.Request("https://%s/api/v3/loadPageChunk" % host, data=body,
                                 headers={"content-type": "application/json", "user-agent": "Mozilla/5.0"})
    blocks = json.load(urllib.request.urlopen(req, timeout=30))["recordMap"]["block"]
    out = {}
    for k, v in blocks.items():
        val = v.get("value", {})
        out[k] = val.get("value", val)
    return out

def text(prop):
    s = ""
    for seg in prop or []:
        t = seg[0]
        for f in (seg[1] if len(seg) > 1 else []):
            if f[0] == "a":
                t = "[%s](%s)" % (t, f[1])
            elif f[0] == "b" and t.strip():
                t = "**%s**" % t
        s += t
    return s

PREFIX = {"header": "## ", "sub_header": "### ", "sub_sub_header": "#### ", "bulleted_list": "- ",
          "numbered_list": "1. ", "to_do": "- [ ] ", "quote": "> ", "callout": "> ", "toggle": "- "}

def render(blocks, bid, depth=0, seen=None):
    seen = seen if seen is not None else set()
    lines = []
    for cid in blocks.get(bid, {}).get("content", []) or []:
        if cid in seen or cid not in blocks:
            continue
        seen.add(cid)
        b = blocks[cid]; t = b.get("type"); p = b.get("properties", {})
        ind = "  " * depth
        if t == "page":
            lines.append(ind + "- (subpage) " + text(p.get("title")))
            continue
        if t in ("image", "video", "file", "pdf", "bookmark", "embed"):
            src = (p.get("source") or [[""]])[0][0]
            lines.append(ind + "[%s: %s]" % (t, src))
        elif t == "divider":
            lines.append("")
        elif t == "code":
            lines.append("```\n" + text(p.get("title")) + "\n```")
        elif t == "table_row":
            lines.append(ind + "| " + " | ".join(text(v) for v in p.values()) + " |")
        else:
            s = text(p.get("title"))
            if s or t in PREFIX:
                lines.append(ind + PREFIX.get(t, "") + s)
        lines += render(blocks, cid, depth + (1 if t in ("bulleted_list", "numbered_list", "toggle", "to_do") else 0), seen)
    return lines

def main():
    host, pid = sys.argv[1], sys.argv[2]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    blocks = chunk(host, pid)
    root = blocks.get(pid, {})
    if root.get("type") == "alias" or not root.get("content"):
        # find the real page: the one with the most content
        real = max((k for k, b in blocks.items() if b.get("type") == "page"), key=lambda k: len(blocks[k].get("content") or []))
        blocks = chunk(host, real); pid = real
    title = text(blocks[pid].get("properties", {}).get("title"))
    body = "# %s\n\nSource: https://%s/%s (public Notion page)\n\n%s\n" % (title, host, pid.replace("-", ""), "\n".join(render(blocks, pid)))
    if out:
        open(out, "w").write(body)
        print("wrote %s: %s, %d words" % (out, title, len(body.split())))
    else:
        sys.stdout.write(body)

if __name__ == "__main__":
    main()

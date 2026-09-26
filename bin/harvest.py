#!/usr/bin/env python3
"""The harvester: a steady keyless intake of mechanisms, judged by a Sonnet child, fed to the probe queue.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/bin/harvest.py run        # pull + shortlist (scripts)
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/bin/harvest.py pull       # sources -> candidates.json
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/bin/harvest.py shortlist  # dedupe, rank, enrich -> brief.md
    (the model judges brief.md and writes state/agents/DATE/harvest.json; see child-prompt.md)
    python3 /Users/triton/PROTEUS/bin/harvest.py ingest                                    # judgements -> register, probes, commit
    python3 /Users/triton/PROTEUS/bin/harvest.py render | digest [--week YYYY-WW] | review | status

Design (2026-09-26, field-notes/HARVEST-DESIGN.md):
  - Pulling, parsing, deduping and ranking are this script. Only the judgement (what is the
    mechanism, is it testable) is a model, and it is a Sonnet sub-agent that writes one JSON file
    under state/agents/DATE/ and nothing else.
  - Sources are keyless: Hacker News Algolia, GitHub search, arXiv Atom, YouTube results HTML plus
    oEmbed plus transcripts, and diffs of awesome lists. Queries live in field-notes/harvest-queries.json.
  - Every candidate is checked against field-notes/SEEN.md and field-notes/harvest.jsonl first. An
    exact id already seen is dropped. A vault verdict on the vendor does not drop the item; it is
    flagged so the child records the mechanism, not the vendor.
  - The register is field-notes/harvest.jsonl (one line per judged item, kept or skipped) and
    field-notes/HARVEST.md rendered from it. Testable items go to the probe queue through
    bin/probe.py add --source harvest, capped per day.
  - HALT stops the commit. HARVEST_NO_GIT=1 stops it for tests. Nothing here sends anything.
"""
import argparse
import html
import json
import math
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

ROOT = os.environ.get("PROTEUS_ROOT", "/Users/triton/PROTEUS/")
if not ROOT.endswith("/"):
    ROOT += "/"
CFG = ROOT + "field-notes/harvest-queries.json"
SEEN = ROOT + "field-notes/SEEN.md"
REGISTER_JSONL = ROOT + "field-notes/harvest.jsonl"
REGISTER_MD = ROOT + "field-notes/HARVEST.md"
STAGING = ROOT + "field-notes/staging/"
WORK = ROOT + "state/harvest/"
AGENTS = ROOT + "state/agents/"
PROBES_JSON = ROOT + "state/probes.json"
PROBE_PY = ROOT + "bin/probe.py"
RUNS = ROOT + "state/runs/"
HALT = ROOT + "HALT"
NO_GIT = os.environ.get("HARVEST_NO_GIT") == "1"
UA = "Proteus harvester (github.com/triton-xxix/proteus-lab; keyless, polite)"
TIMEOUT = 25


# ---------------------------------------------------------------- helpers

def now():
    return datetime.now().astimezone()


def today():
    return os.environ.get("HARVEST_DATE") or now().strftime("%Y-%m-%d")


def workdir(date=None):
    d = WORK + (date or today()) + "/"
    os.makedirs(d, exist_ok=True)
    return d


def load_cfg():
    with open(CFG) as fh:
        return json.load(fh)


def get(url, headers=None, accept_json=False):
    h = {"User-Agent": UA, "Accept-Language": "en-GB,en"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        raw = resp.read()
    text = raw.decode("utf-8", "replace")
    return json.loads(text) if accept_json else text


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def norm_url(u):
    if not u:
        return ""
    u = u.strip()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = re.sub(r"[?&]utm_[^&]*", "", u)
    return u.rstrip("/").lower()


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def read_json(path, default=None):
    try:
        with open(path) as fh:
            return json.load(fh)
    except Exception:
        return default


def register_rows():
    rows = []
    if os.path.exists(REGISTER_JSONL):
        with open(REGISTER_JSONL) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except Exception:
                        pass
    return rows


def run_log(date, line):
    os.makedirs(RUNS, exist_ok=True)
    with open(RUNS + date + ".md", "a") as fh:
        fh.write(line.rstrip("\n") + "\n")


# ---------------------------------------------------------------- pull

def pull_hn(cfg, out, errors):
    since = int(time.time()) - cfg.get("hours", 72) * 3600
    for q in cfg["queries"]:
        try:
            url = ("https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=%d&query=%s"
                   "&numericFilters=points>=%d,created_at_i>=%d" % (
                       cfg.get("per_query", 10), urllib.parse.quote_plus(q), cfg.get("min_points", 10), since))
            data = get(url, accept_json=True)
            for h in data.get("hits", []):
                oid = str(h.get("objectID"))
                out.append({
                    "key": "hn:" + oid, "source": "hn", "query": q,
                    "title": h.get("title") or "", "url": h.get("url") or ("https://news.ycombinator.com/item?id=" + oid),
                    "hn_url": "https://news.ycombinator.com/item?id=" + oid,
                    "meta": {"points": h.get("points") or 0, "comments": h.get("num_comments") or 0, "created": h.get("created_at")},
                    "body": strip_html(h.get("story_text") or "")[:1500],
                    "score": math.log1p(h.get("points") or 0) + 0.5 * math.log1p(h.get("num_comments") or 0),
                })
        except Exception as exc:
            errors.append("hn %r: %s" % (q, exc))
        time.sleep(0.5)


def pull_github(cfg, out, errors):
    week = (now() - timedelta(days=cfg.get("days", 7))).strftime("%Y-%m-%d")
    for i, q in enumerate(cfg["queries"][: cfg.get("max_queries", 6)]):
        if i:
            time.sleep(cfg.get("pause_s", 6.5))    # keyless search is 10 calls a minute
        try:
            qq = q.replace("{since}", week)
            url = "https://api.github.com/search/repositories?q=%s&sort=stars&order=desc&per_page=%d" % (
                urllib.parse.quote(qq, safe="+:>=<"), cfg.get("per_query", 8))
            data = get(url, headers={"Accept": "application/vnd.github+json"}, accept_json=True)
            for r in data.get("items", []):
                stars = r.get("stargazers_count") or 0
                out.append({
                    "key": "gh:" + r["full_name"].lower(), "source": "github", "query": q,
                    "title": "%s: %s" % (r["full_name"], (r.get("description") or "").strip()),
                    "url": r["html_url"], "repo": r["full_name"],
                    "meta": {"stars": stars, "created": (r.get("created_at") or "")[:10], "pushed": (r.get("pushed_at") or "")[:10],
                             "language": r.get("language"), "topics": (r.get("topics") or [])[:8]},
                    "body": "", "score": math.log1p(stars),
                })
        except Exception as exc:
            errors.append("github %r: %s" % (q, exc))


def pull_arxiv(cfg, out, errors):
    ns = {"a": "http://www.w3.org/2005/Atom"}
    cutoff = (now() - timedelta(days=cfg.get("days", 4))).strftime("%Y-%m-%d")
    for q in cfg["queries"]:
        try:
            url = "https://export.arxiv.org/api/query?search_query=%s&sortBy=submittedDate&sortOrder=descending&max_results=%d" % (
                urllib.parse.quote(q, safe="()+:*"), cfg.get("per_query", 8))
            root = ET.fromstring(get(url))
            for e in root.findall("a:entry", ns):
                aid = (e.findtext("a:id", "", ns) or "").rsplit("/", 1)[-1]
                aid = re.sub(r"v\d+$", "", aid)
                pub = (e.findtext("a:published", "", ns) or "")[:10]
                if pub < cutoff:
                    continue
                out.append({
                    "key": "arxiv:" + aid, "source": "arxiv", "query": q,
                    "title": re.sub(r"\s+", " ", e.findtext("a:title", "", ns) or "").strip(),
                    "url": "https://arxiv.org/abs/" + aid,
                    "meta": {"published": pub, "authors": [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)][:4],
                             "categories": [c.get("term") for c in e.findall("a:category", ns)][:4]},
                    "body": re.sub(r"\s+", " ", e.findtext("a:summary", "", ns) or "").strip()[:2500],
                    "score": 1.0,
                })
        except Exception as exc:
            errors.append("arxiv %r: %s" % (q, exc))
        time.sleep(3)   # arXiv asks for a pause between calls


def pull_youtube(cfg, out, errors):
    qs = cfg["queries"]
    k = cfg.get("per_day", 3)
    start = now().timetuple().tm_yday * k
    todays = [qs[(start + i) % len(qs)] for i in range(min(k, len(qs)))]
    for q in todays:
        try:
            url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q)
            page = get(url, headers={"User-Agent": "Mozilla/5.0"})
            ids = []
            for m in re.finditer(r'"videoId":"([a-zA-Z0-9_-]{11})"', page):
                if m.group(1) not in ids:
                    ids.append(m.group(1))
            for rank, vid in enumerate(ids[: cfg.get("per_query", 4)]):
                meta = {}
                try:
                    meta = get("https://www.youtube.com/oembed?" + urllib.parse.urlencode(
                        {"url": "https://www.youtube.com/watch?v=" + vid, "format": "json"}), accept_json=True)
                except Exception as exc:
                    errors.append("oembed %s: %s" % (vid, exc))
                out.append({
                    "key": "yt:" + vid, "source": "youtube", "query": q,
                    "title": meta.get("title") or ("(untitled) " + vid),
                    "url": "https://www.youtube.com/watch?v=" + vid,
                    "meta": {"channel": meta.get("author_name"), "rank": rank + 1},
                    "body": "", "score": 1.0 / (rank + 1),
                })
                time.sleep(0.3)
        except Exception as exc:
            errors.append("youtube %r: %s" % (q, exc))


def pull_awesome(cfg, out, errors, notes):
    base = WORK + "awesome/"
    os.makedirs(base, exist_ok=True)
    for name, raw_url in cfg["lists"].items():
        try:
            text = get(raw_url)
            links = sorted(set(m.group(1).lower() for m in re.finditer(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?:[/#)\s]|$)", text)))
            links = [l for l in links if l.split("/")[0] not in ("sponsors", "topics", "orgs", "features", "site")]
            path = base + name + ".links"
            if not os.path.exists(path):
                with open(path, "w") as fh:
                    fh.write("\n".join(links) + "\n")
                notes.append("awesome %s: baseline saved, %d links, nothing taken on the first pass" % (name, len(links)))
                continue
            with open(path) as fh:
                old = set(l.strip() for l in fh if l.strip())
            new = [l for l in links if l not in old]
            for repo in new[: cfg.get("per_list", 6)]:
                out.append({
                    "key": "gh:" + repo, "source": "awesome", "query": name,
                    "title": repo + " (new in " + name + ")", "url": "https://github.com/" + repo, "repo": repo,
                    "meta": {"list": name}, "body": "", "score": 2.0,
                })
            with open(path, "w") as fh:
                fh.write("\n".join(links) + "\n")
            notes.append("awesome %s: %d new of %d" % (name, len(new), len(links)))
        except Exception as exc:
            errors.append("awesome %s: %s" % (name, exc))


def cmd_pull(a):
    cfg = load_cfg()
    date = today()
    out, errors, notes = [], [], []
    t0 = time.time()
    pull_hn(cfg["hn"], out, errors)
    pull_github(cfg["github"], out, errors)
    pull_arxiv(cfg["arxiv"], out, errors)
    pull_youtube(cfg["youtube"], out, errors)
    pull_awesome(cfg["awesome"], out, errors, notes)
    seen_keys, uniq = set(), []
    for c in out:
        if c["key"] in seen_keys:
            continue
        seen_keys.add(c["key"])
        uniq.append(c)
    by_src = {}
    for c in uniq:
        by_src[c["source"]] = by_src.get(c["source"], 0) + 1
    doc = {"date": date, "pulled_at": now().strftime("%Y-%m-%dT%H:%M:%S%z"), "seconds": round(time.time() - t0, 1),
           "by_source": by_src, "errors": errors, "notes": notes, "candidates": uniq}
    write_json(workdir(date) + "candidates.json", doc)
    print("pulled %d candidates in %ds: %s" % (len(uniq), doc["seconds"], ", ".join("%s %d" % kv for kv in sorted(by_src.items()))))
    for n in notes:
        print("  " + n)
    for e in errors:
        print("  error: " + e)


# ---------------------------------------------------------------- shortlist: dedupe, rank, enrich

def seen_index():
    """Exact ids the vault or Proteus already evaluated, and vendor names with a vault verdict."""
    try:
        with open(SEEN) as fh:
            text = fh.read()
    except Exception:
        return set(), {}
    ids = set()
    for m in re.finditer(r"\b([a-zA-Z0-9_-]{11})\b", text):
        s = m.group(1)
        if re.search(r"[A-Z]", s) and re.search(r"[a-z0-9]", s) and not s.isalpha():
            ids.add("yt:" + s)
    for m in re.finditer(r"\b(\d{4}\.\d{4,5})\b", text):
        ids.add("arxiv:" + m.group(1))
    for m in re.finditer(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", text):
        ids.add("gh:" + m.group(1).lower())
    names = {}
    tools = re.search(r"## Tools and repos\n(.*?)\n## ", text, re.S)
    if tools:
        for n in tools.group(1).replace("\n", " ").split(","):
            n = re.sub(r"\(.*?\)", "", n).strip().lower()
            if len(n) >= 5:
                names[n] = "vault: tools and repos"
    for m in re.finditer(r"\*\*\d{4}-\d{2}-\d{2} · ([^*(]+?)(?: \(|\*\*)", text):
        n = m.group(1).strip().lower()
        if len(n) >= 5:
            names[n] = "vault verdict: " + m.group(1).strip()
    for m in re.finditer(r"\b([a-z0-9_.-]+/[a-z0-9_.-]+)\b", text.lower()):
        pass
    return ids, names


def vault_flag(c, names):
    hay = (c.get("title", "") + " " + c.get("url", "")).lower()
    repo = (c.get("repo") or "").lower().split("/")[-1]
    for n, why in names.items():
        if repo and repo == n:
            return why
        if re.search(r"(?<![a-z0-9])" + re.escape(n) + r"(?![a-z0-9])", hay):
            return why
    return None


def enrich(c, cfg, errors):
    src = c["source"]
    limit = cfg.get("body_chars", 3500)
    try:
        if src == "hn":
            oid = c["key"].split(":", 1)[1]
            item = get("https://hn.algolia.com/api/v1/items/" + oid, accept_json=True)
            parts = []
            if item.get("text"):
                parts.append(strip_html(item["text"])[:1500])
            for ch in (item.get("children") or [])[:3]:
                if ch.get("text"):
                    parts.append("comment (%s): %s" % (ch.get("author"), strip_html(ch["text"])[:600]))
            if c.get("url") and "news.ycombinator.com" not in c["url"] and len(" ".join(parts)) < 400:
                try:
                    page = get(c["url"], headers={"User-Agent": "Mozilla/5.0"})
                    page = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", page)
                    parts.insert(0, "page: " + strip_html(page)[:2000])
                except Exception as exc:
                    errors.append("hn page %s: %s" % (c["url"], exc))
            c["body"] = "\n".join(parts)[:limit]
        elif src in ("github", "awesome"):
            repo = c["repo"]
            text = None
            for branch in ("main", "master"):
                try:
                    text = get("https://raw.githubusercontent.com/%s/%s/README.md" % (repo, branch))
                    break
                except Exception:
                    continue
            if text is None:
                data = get("https://api.github.com/repos/" + repo, headers={"Accept": "application/vnd.github+json"}, accept_json=True)
                c["meta"].update({"stars": data.get("stargazers_count"), "created": (data.get("created_at") or "")[:10],
                                  "language": data.get("language")})
                text = data.get("description") or ""
            elif src == "awesome":
                try:
                    data = get("https://api.github.com/repos/" + repo, headers={"Accept": "application/vnd.github+json"}, accept_json=True)
                    c["meta"].update({"stars": data.get("stargazers_count"), "created": (data.get("created_at") or "")[:10],
                                      "language": data.get("language"), "description": data.get("description")})
                except Exception as exc:
                    errors.append("gh repo %s: %s" % (repo, exc))
            text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
            text = re.sub(r"<[^>]+>", " ", text)
            c["body"] = re.sub(r"\n{3,}", "\n\n", text).strip()[:limit]
        elif src == "youtube":
            vid = c["key"].split(":", 1)[1]
            os.makedirs(STAGING, exist_ok=True)
            cache = STAGING + vid + ".txt"
            if os.path.exists(cache):
                with open(cache) as fh:
                    txt = fh.read()
            else:
                from youtube_transcript_api import YouTubeTranscriptApi
                api = YouTubeTranscriptApi()
                try:
                    fetched = api.fetch(vid, languages=["en", "en-GB", "en-US"])
                except Exception:
                    fetched = api.fetch(vid)
                segs = fetched.to_raw_data()
                c["meta"]["duration_min"] = int((segs[-1]["start"] + segs[-1].get("duration", 0)) // 60) if segs else 0
                lines, buf, start = [], [], None
                for s in segs:
                    if start is None:
                        start = s["start"]
                    buf.append(s["text"].replace("\n", " ").strip())
                    if s["start"] - start >= 30:
                        lines.append("[%02d:%02d] " % divmod(int(start), 60) + " ".join(buf))
                        buf, start = [], None
                if buf:
                    lines.append("[%02d:%02d] " % divmod(int(start or 0), 60) + " ".join(buf))
                txt = "# %s\n# %s\n# %s\n\n" % (c["title"], c["meta"].get("channel"), c["url"]) + "\n".join(lines)
                with open(cache, "w") as fh:
                    fh.write(txt)
            c["body"] = txt[:limit] + ("\n[transcript continues in field-notes/staging/%s.txt]" % vid if len(txt) > limit else "")
        elif src == "arxiv":
            pass
    except Exception as exc:
        errors.append("enrich %s: %s: %s" % (c["key"], type(exc).__name__, exc))
        c["body"] = (c.get("body") or "") + "\n[body unavailable: %s]" % type(exc).__name__


CHILD_PROMPT = """You are a sub-agent of Proteus, the explorer persona, doing tonight's harvest judgement. You run on Sonnet. You may not spawn agents, run git, or run scripts. You read; you write exactly one file.

Read /Users/triton/PROTEUS/state/harvest/{date}/brief.md. It holds {n} harvested items (Hacker News, GitHub, arXiv, YouTube, awesome-list diffs), each with a source, a title, a URL, metadata, a SEEN flag where the vault already has a verdict on the vendor, and a body (story text, README, abstract or transcript). If a body is thin you may WebFetch that item's URL, at most {fetches} fetches in total.

For each item, decide and write a JSON object with these fields:
- "key": copied exactly from the brief.
- "keep": true if the item carries a mechanism worth recording; false for hype, listicles, generic news, duplicates of one another (keep the best one), or anything whose only content is a claim with no mechanism. A vendor with a vault verdict of no is still kept if its mechanism is new; set "lens" to "mechanism" and say what the mechanism is, not whether the vendor is trustworthy.
- "skip_reason": one short sentence when keep is false, else "".
- "lens": "mechanism" (how it works), "vendor" (an assessment of the thing as a product), or "both".
- "mechanism": two to four sentences on how it actually works: the moving parts, what it depends on, what it calls, where the numbers come from. Not the marketing.
- "claim": one sentence on what the source says it does, with the number if it gives one.
- "testable": true if Proteus could run it keyless tonight in /Users/triton/PROTEUS/sandbox/ inside 30 minutes and reach a verdict (works, broken, blocked, not worth it) from running it. No accounts, no keys, no spend, no logins.
- "why_not_testable": one sentence when testable is false, else "".
- "verdict_question": the one question a run tonight would answer, phrased so the answer is a number or a yes/no.
- "probe_title": under 140 characters, starts with the thing being tested, then a colon, then the question. Only when testable.
- "est_minutes": 10 to 30. Only when testable.
- "needs": what it needs that Proteus does not have, if anything (an account, a device, a key). "" when nothing.
- "intel": true if this is intelligence-lane material (grey-market tooling, automation and scraping services, farms, detection). For these, "mechanism" records what it is and how platforms detect it. Never write a recipe for evading detection (passing reposts as new content, spoofed devices, fake engagement). Say what it is and how it gets caught, then move on.
- "interest": one of "mechanism-hunting", "forecasting", "game-bots", "open-data", "tools-for-strangers", "cars", "tech", "desk:grinder", "desk:pitch", "none".
- "one_line": the line that would go in Sunday Field Notes, under 30 words, plain English, UK spelling, no em dashes, novelty first.

Write the whole array, in the brief's order, with the Write tool to exactly this path and nothing else:
/Users/triton/PROTEUS/state/agents/{date}/harvest.json

Rules: absolute paths only. No Bash except ls, cat, head, grep on files under /Users/triton/PROTEUS. Do not write anywhere else. If a tool call is refused, that is a result: do not retry it, put it in your final message. Your final message is three lines: how many kept, how many testable, and any refusals or fetch failures. Do not paste the JSON into the message."""


def cmd_shortlist(a):
    cfg = load_cfg()
    date = today()
    wd = workdir(date)
    cand = read_json(wd + "candidates.json")
    if not cand:
        print("no candidates.json for %s; run pull first" % date)
        sys.exit(1)
    ids, names = seen_index()
    have = set()
    for r in register_rows():
        have.add(r.get("key"))
        if r.get("url"):
            have.add("url:" + norm_url(r["url"]))
    probes = read_json(PROBES_JSON, {"items": []})
    probe_titles = " ".join(i["title"].lower() for i in probes.get("items", []))
    dropped, flagged, pool = [], 0, []
    for c in cand["candidates"]:
        if c["key"] in have or c["key"] in ids or ("url:" + norm_url(c.get("url"))) in have:
            dropped.append(c["key"])
            continue
        repo = (c.get("repo") or "").lower()
        if repo and repo in probe_titles:
            dropped.append(c["key"])
            continue
        why = vault_flag(c, names)
        if why:
            c["seen_vault"] = why
            flagged += 1
        pool.append(c)
    caps = cfg["shortlist"]["per_source"]
    total = cfg["shortlist"]["total"]
    by = {}
    for c in pool:
        by.setdefault(c["source"], []).append(c)
    for s in by:
        by[s].sort(key=lambda c: -c["score"])
    order = cfg["shortlist"]["order"]
    picked, taken = [], {s: 0 for s in order}
    while len(picked) < total:
        progressed = False
        for s in order:
            if taken[s] < caps.get(s, 0) and by.get(s) and len(picked) < total:
                picked.append(by[s].pop(0))
                taken[s] += 1
                progressed = True
        if not progressed:
            break
    errors = []
    for c in picked:
        enrich(c, cfg["shortlist"], errors)
        time.sleep(0.5)
    lines = ["# Harvest brief, %s" % date, "",
             "%d items shortlisted from %d candidates (%d dropped as already seen, %d carry a vault verdict on the vendor)." % (
                 len(picked), len(cand["candidates"]), len(dropped), flagged), ""]
    for i, c in enumerate(picked, 1):
        lines.append("## %d. [%s] %s" % (i, c["source"], c["title"]))
        lines.append("key: %s" % c["key"])
        lines.append("url: %s" % c["url"])
        if c.get("hn_url"):
            lines.append("discussion: %s" % c["hn_url"])
        lines.append("meta: %s" % json.dumps(c.get("meta", {}), ensure_ascii=False))
        lines.append("query: %s" % c.get("query", ""))
        if c.get("seen_vault"):
            lines.append("SEEN: the vault already judged this vendor (%s). Record the mechanism only if it is new; do not re-judge the vendor." % c["seen_vault"])
        lines.append("")
        lines.append(c.get("body") or "[no body]")
        lines.append("")
    with open(wd + "brief.md", "w") as fh:
        fh.write("\n".join(lines))
    doc = {"date": date, "shortlisted_at": now().strftime("%Y-%m-%dT%H:%M:%S%z"), "candidates": len(cand["candidates"]),
           "dropped_seen": dropped, "flagged_vault": flagged, "errors": errors, "items": picked}
    write_json(wd + "shortlist.json", doc)
    prompt = CHILD_PROMPT.format(date=date, n=len(picked), fetches=cfg["shortlist"].get("child_fetches", 6))
    with open(wd + "child-prompt.md", "w") as fh:
        fh.write(prompt + "\n")
    os.makedirs(AGENTS + date, exist_ok=True)
    print("shortlisted %d of %d (%d dropped as seen, %d flagged with a vault verdict); brief %d chars" % (
        len(picked), len(cand["candidates"]), len(dropped), flagged, sum(len(l) for l in lines)))
    for e in errors:
        print("  error: " + e)
    print("brief:  %sbrief.md" % wd)
    print("prompt: %schild-prompt.md (spawn one general-purpose child, model sonnet, with that text)" % wd)
    print("expect: %sharvest.json" % (AGENTS + date + "/"))


def cmd_run(a):
    cmd_pull(a)
    cmd_shortlist(a)


# ---------------------------------------------------------------- ingest

REQUIRED = ("key", "keep", "lens", "mechanism", "claim", "testable", "one_line")


def probe_add(title, est, needs):
    cmd = [sys.executable, PROBE_PY, "add", title, "--source", "harvest", "--est", str(int(est))]
    if needs:
        cmd += ["--needs", needs]
    env = dict(os.environ)
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    m = re.search(r"added (P-\d{4})", res.stdout or "")
    return (m.group(1) if m else None), (res.stdout + res.stderr).strip()


def git(args):
    if NO_GIT:
        return "no-git: " + " ".join(args)
    res = subprocess.run(["git", "-C", ROOT] + args, capture_output=True, text=True)
    return (res.stdout + res.stderr).strip()


def cmd_ingest(a):
    cfg = load_cfg()
    date = today()
    wd = workdir(date)
    short = read_json(wd + "shortlist.json")
    jpath = AGENTS + date + "/harvest.json"
    judg = read_json(jpath)
    if not short or judg is None:
        print("missing shortlist.json or %s" % jpath)
        sys.exit(1)
    if not isinstance(judg, list):
        print("judgements are not a JSON array")
        sys.exit(1)
    by_key = {c["key"]: c for c in short["items"]}
    rows = register_rows()
    next_id = 1 + max([int(r["id"][2:]) for r in rows if r.get("id", "").startswith("H-")] or [0])
    seen_keys = set(r.get("key") for r in rows)
    kept, skipped, queued, bad = [], [], [], []
    per_day_cap = cfg["ingest"].get("max_probes_per_day", 4)
    new_rows = []
    for j in judg:
        if not isinstance(j, dict) or any(k not in j for k in REQUIRED) or j.get("key") not in by_key:
            bad.append(str(j)[:80])
            continue
        if j["key"] in seen_keys:
            continue
        c = by_key[j["key"]]
        row = {
            "id": "H-%04d" % next_id, "date": date, "key": j["key"], "source": c["source"], "title": c["title"], "url": c["url"],
            "meta": c.get("meta", {}), "seen_vault": c.get("seen_vault"),
            "keep": bool(j["keep"]), "skip_reason": j.get("skip_reason", ""), "lens": j.get("lens", ""),
            "mechanism": j.get("mechanism", ""), "claim": j.get("claim", ""),
            "testable": bool(j.get("testable")) and bool(j["keep"]), "why_not_testable": j.get("why_not_testable", ""),
            "verdict_question": j.get("verdict_question", ""), "probe_title": j.get("probe_title", ""),
            "est_minutes": j.get("est_minutes"), "needs": j.get("needs", ""), "intel": bool(j.get("intel")),
            "interest": j.get("interest", "none"), "one_line": j.get("one_line", ""), "probe_id": None,
        }
        next_id += 1
        if row["keep"]:
            kept.append(row)
            if row["testable"] and len(queued) < per_day_cap and row["probe_title"]:
                pid, out = probe_add(row["probe_title"], row.get("est_minutes") or 20, row.get("needs") or "")
                row["probe_id"] = pid
                if pid:
                    queued.append((pid, row["id"]))
                else:
                    bad.append("probe add failed for %s: %s" % (row["id"], out[:120]))
        else:
            skipped.append(row)
        new_rows.append(row)
    with open(REGISTER_JSONL, "a") as fh:
        for r in new_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    render()
    if new_rows:
        seen_line = "- %s, harvested: %d judged, %d kept (%s to %s), %d queued as probes%s. Register: `field-notes/HARVEST.md`." % (
            date, len(new_rows), len(kept), new_rows[0]["id"], new_rows[-1]["id"], len(queued),
            (" (" + ", ".join(p for p, _ in queued) + ")") if queued else "")
        try:
            with open(SEEN) as fh:
                text = fh.read()
            if "\n## Rule" in text:
                text = text.replace("\n## Rule", seen_line + "\n\n## Rule", 1)
            else:
                text = text.rstrip("\n") + "\n" + seen_line + "\n"
            with open(SEEN, "w") as fh:
                fh.write(text)
        except Exception as exc:
            bad.append("SEEN append failed: %s" % exc)
    src_counts = short.get("candidates", 0)
    line = "- Harvest: %d candidates pulled, %d shortlisted, %d kept, %d skipped, %d queued as probes%s; %d dropped as already seen. Brief `state/harvest/%s/brief.md`, judgements `state/agents/%s/harvest.json`." % (
        src_counts, len(short["items"]), len(kept), len(skipped), len(queued),
        (" (" + ", ".join("%s from %s" % (p, h) for p, h in queued) + ")") if queued else "",
        len(short.get("dropped_seen", [])), date, date)
    if bad:
        line += " Problems: " + "; ".join(bad)[:400]
    run_log(date, line)
    committed = "skipped"
    if os.path.exists(HALT):
        committed = "HALT set, not committed"
    elif NO_GIT:
        committed = "HARVEST_NO_GIT, not committed"
    else:
        paths = [REGISTER_JSONL, REGISTER_MD, SEEN, PROBES_JSON, ROOT + "PROBES.md", wd, AGENTS + date, WORK + "awesome", RUNS + date + ".md"]
        paths = [p for p in paths if os.path.exists(p)]
        git(["add", "--"] + paths)
        msg = "harvest %s: %d kept of %d judged, %d probes queued" % (date, len(kept), len(new_rows), len(queued))
        out = git(["commit", "-m", msg])
        if "nothing to commit" in out:
            committed = "nothing to commit"
        else:
            push = git(["push", "origin", "main"])
            committed = "committed and pushed" if "error" not in push.lower() and "rejected" not in push.lower() else "committed, push failed: " + push[-160:]
    print(line)
    print("register: %d rows total; %s" % (len(rows) + len(new_rows), committed))


# ---------------------------------------------------------------- render, digest, review, status

def probe_lookup():
    st = read_json(PROBES_JSON, {"items": []})
    return {i["id"]: i for i in st.get("items", [])}


def render():
    rows = register_rows()
    probes = probe_lookup()
    kept = [r for r in rows if r.get("keep")]
    testable = [r for r in kept if r.get("testable")]
    with_verdict = [r for r in testable if r.get("probe_id") and probes.get(r["probe_id"], {}).get("status") == "done"]
    days = sorted(set(r["date"] for r in rows))
    out = ["# Harvest register", "",
           "One line per item the harvester judged. Rendered by `bin/harvest.py` from `field-notes/harvest.jsonl`; design in",
           "`field-notes/HARVEST-DESIGN.md`. Each kept entry records the **mechanism** (how it works), the **claim** (what the",
           "source says) and whether it is **testable** keyless tonight; testable ones are queued in `PROBES.md` with source",
           "`harvest`. A vault verdict on a vendor does not stop the mechanism being recorded; the lens column says which is on record.",
           "", "%d judged over %d harvest days, %d kept, %d testable, %d queued as probes, %d with a probe verdict." % (
               len(rows), len(days), len(kept), len(testable), len([r for r in testable if r.get("probe_id")]), len(with_verdict)), ""]
    out += ["## Kept", "", "| id | date | source | what | lens | interest | testable | probe |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(kept, key=lambda r: r["id"], reverse=True):
        p = r.get("probe_id")
        pv = ""
        if p:
            pi = probes.get(p, {})
            pv = "%s%s" % (p, (" **%s**" % pi["verdict"]) if pi.get("verdict") else "")
        out.append("| %s | %s | %s | [%s](%s)%s | %s | %s | %s | %s |" % (
            r["id"], r["date"], r["source"], r["title"].replace("|", "/")[:90], r["url"], " (intel)" if r.get("intel") else "",
            r.get("lens", ""), r.get("interest", ""), "yes" if r.get("testable") else ("no: " + (r.get("why_not_testable") or "")[:60]), pv))
    out += ["", "## Entries", ""]
    for r in sorted(kept, key=lambda r: r["id"], reverse=True):
        out.append("### %s %s" % (r["id"], r["title"].replace("|", "/")[:120]))
        out.append("%s, %s, %s%s" % (r["date"], r["source"], r["url"], (". Vault verdict on the vendor exists (%s); mechanism recorded, vendor not re-judged." % r["seen_vault"]) if r.get("seen_vault") else ""))
        out.append("")
        out.append("- **Mechanism:** " + r.get("mechanism", ""))
        out.append("- **Claim:** " + r.get("claim", ""))
        if r.get("testable"):
            out.append("- **Testable:** yes. %s%s" % (r.get("verdict_question", ""), (" Queued as %s." % r["probe_id"]) if r.get("probe_id") else " Not queued (daily cap)."))
        else:
            out.append("- **Testable:** no. %s%s" % (r.get("why_not_testable", ""), (" Needs: %s." % r["needs"]) if r.get("needs") else ""))
        out.append("- **Field Notes line:** " + r.get("one_line", ""))
        out.append("")
    out += ["## Skipped", "", "| id | date | source | what | why |", "|---|---|---|---|---|"]
    for r in sorted([r for r in rows if not r.get("keep")], key=lambda r: r["id"], reverse=True):
        out.append("| %s | %s | %s | [%s](%s) | %s |" % (r["id"], r["date"], r["source"], r["title"].replace("|", "/")[:80], r["url"], (r.get("skip_reason") or "").replace("|", "/")[:120]))
    with open(REGISTER_MD, "w") as fh:
        fh.write("\n".join(out) + "\n")


def cmd_render(a):
    render()
    print("rendered " + REGISTER_MD)


def iso_week(d):
    y, w, _ = datetime.strptime(d, "%Y-%m-%d").isocalendar()
    return "%d-W%02d" % (y, w)


def cmd_digest(a):
    week = a.week or iso_week(today())
    probes = probe_lookup()
    rows = [r for r in register_rows() if r.get("keep") and iso_week(r["date"]) == week]
    rows.sort(key=lambda r: (not r.get("testable"), r["id"]))
    print("Harvest digest %s: %d kept entries" % (week, len(rows)))
    for r in rows:
        tail = ""
        if r.get("probe_id"):
            pi = probes.get(r["probe_id"], {})
            tail = " [%s%s]" % (r["probe_id"], (": " + pi["verdict"] + ", " + (pi.get("note") or "")[:140]) if pi.get("verdict") else ": queued")
        print("- %s (%s, %s): %s%s" % (r["id"], r["source"], r["url"], r.get("one_line", ""), tail))


def cmd_review(a):
    """The pre-registered harvest lines in PASS-MARKS.md, computed from the register and the probe state."""
    rows = register_rows()
    probes = probe_lookup()
    t = now()
    kept = [r for r in rows if r.get("keep")]
    days = sorted(set(r["date"] for r in rows))
    first = days[0] if days else None
    print("harvest days: %d (first %s), judged %d, kept %d" % (len(days), first, len(rows), len(kept)))
    if days:
        window = [(t - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(28)]
        active = [d for d in window if d >= first]
        with_h = [d for d in active if d in days]
        print("intake: harvest ran on %d of the last %d scheduled days" % (len(with_h), len(active)))
    testable = [r for r in kept if r.get("testable") and r.get("probe_id")]
    due = [r for r in testable if (t - datetime.strptime(r["date"], "%Y-%m-%d").astimezone()).days >= 14]
    done = [r for r in due if probes.get(r["probe_id"], {}).get("status") == "done"]
    print("testable and queued: %d; older than 14 days: %d; of those with a verdict: %d (%s)" % (
        len(testable), len(due), len(done), ("%.0f%%" % (100.0 * len(done) / len(due))) if due else "n/a"))
    since = (t - timedelta(days=28)).strftime("%Y-%m-%d")
    verdicts = [p for p in probes.values() if p.get("status") == "done" and (p.get("verdict_at") or "")[:10] >= since]
    hv = [p for p in verdicts if p.get("source") == "harvest"]
    print("probe verdicts in the last 28 days: %d, from harvest: %d (%s)" % (
        len(verdicts), len(hv), ("%.0f%%" % (100.0 * len(hv) / len(verdicts))) if verdicts else "n/a"))
    if hv:
        works = [p for p in hv if p.get("verdict") == "works"]
        print("harvest verdicts that were works: %d of %d" % (len(works), len(hv)))


def cmd_status(a):
    rows = register_rows()
    date = today()
    wd = WORK + date + "/"
    print("register: %d rows, %d kept" % (len(rows), len([r for r in rows if r.get("keep")])))
    for f in ("candidates.json", "shortlist.json", "brief.md", "child-prompt.md"):
        print("  %s %s" % ("have" if os.path.exists(wd + f) else "----", wd + f))
    j = AGENTS + date + "/harvest.json"
    print("  %s %s" % ("have" if os.path.exists(j) else "----", j))
    print("HALT: " + ("set" if os.path.exists(HALT) else "clear"))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("pull", cmd_pull), ("shortlist", cmd_shortlist), ("run", cmd_run), ("ingest", cmd_ingest),
                     ("render", cmd_render), ("review", cmd_review), ("status", cmd_status)):
        sub.add_parser(name).set_defaults(fn=fn)
    d = sub.add_parser("digest")
    d.add_argument("--week", default="")
    d.set_defaults(fn=cmd_digest)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

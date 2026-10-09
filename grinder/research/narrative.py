#!/usr/bin/env python3
"""The research desk's nightly narrative pull: what the market is talking about, for one Sonnet
child to read and digest. Pulls only; the child writes the digest.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/research/narrative.py pull
    python3 /Users/triton/PROTEUS/grinder/research/narrative.py ingest

`pull` writes state/research/YYYY-MM-DD/narrative.md (headlines, Reddit top threads, CoinGecko
trending, one xAI summary of X, tonight's Grinder picks with their mention rows) and child-prompt.md.
`ingest` checks the child's digest, copies it to grinder/research/digests/, logs a line, commits.
Sources and their record: grinder/research/SOURCES.md.
"""
import csv
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/triton/PROTEUS/"
sys.path.insert(0, ROOT + "grinder"); sys.path.insert(0, HERE)
UA = {"User-Agent": "proteus-lab/0.1 research (+https://github.com/triton-xxix/proteus-lab)"}
FEEDS = {  # news RSS, keyless; the register records which answer
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Decrypt": "https://decrypt.co/feed",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "The Block": "https://www.theblock.co/rss.xml",
    "Blockworks": "https://blockworks.co/feed",
    "Cointelegraph Solana": "https://cointelegraph.com/rss/tag/solana",
    "Decrypt Solana": "https://decrypt.co/feed?tag=solana",
    "The Defiant": "https://thedefiant.io/feed",
    "Bankless": "https://www.bankless.com/rss/feed",
}
TG_NARRATIVE = ["cryptonary", "WatcherGuru"]   # public previews; Cryptonary's research itself is paid

def _vault():
    """bin/secrets.py by file path: on sys.path it would shadow the standard library's secrets module,
    which numpy imports (found 30 Sep 2026)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("proteus_secrets", "/Users/triton/PROTEUS/bin/secrets.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod



def day():
    return datetime.now().strftime("%Y-%m-%d")


def digest_out():
    """Children may write only under state/agents/ (the hook), so the digest lands there first."""
    os.makedirs(ROOT + "state/agents/research/", exist_ok=True)
    return ROOT + "state/agents/research/%s-digest.md" % day()


def outdir():
    d = ROOT + "state/research/%s/" % day()
    os.makedirs(d, exist_ok=True)
    return d


def rss(name, url, since):
    try:
        r = requests.get(url, headers=UA, timeout=25)
        root = ET.fromstring(r.content)
        out = []
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            pub = it.findtext("pubDate") or ""
            try:
                t = datetime.strptime(pub[:25].strip(), "%a, %d %b %Y %H:%M:%S").replace(tzinfo=timezone.utc)
            except Exception:
                t = None
            if t is None or t >= since:
                out.append("- %s (%s)" % (title, pub[:16]))
        return out[:15], None
    except Exception as e:
        return [], str(e)[:80]


def gecko_trending():
    try:
        d = requests.get("https://api.coingecko.com/api/v3/search/trending", headers=UA, timeout=25).json()
        return ["- %s (%s), rank %s" % (c["item"]["name"], c["item"]["symbol"], c["item"].get("market_cap_rank")) for c in d.get("coins", [])][:15], None
    except Exception as e:
        return [], str(e)[:80]


def reddit_top(after, before):
    from mentions import reddit_window, SUBS
    lines = []
    for sub in SUBS:
        items = [i for i in reddit_window(sub, after, before) if i["kind"] == "posts"]
        lines.append("### r/%s: %d posts, %d comments in the window" % (
            sub, len(items), len([i for i in reddit_window(sub, after, before) if i["kind"] == "comments"])))
        for i in items[:12]:
            lines.append("- " + re.sub(r"\s+", " ", i["text"])[:180])
    return lines


def x_narrative():
    vault = _vault()
    key = vault.get("XAI API Credentials", vault="Tritons World")
    since = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%d")
    body = {"model": "grok-4.20-0309-non-reasoning", "tools": [{"type": "x_search", "from_date": since}],
            "input": [{"role": "user", "content":
                       "Using at most three X searches, report what Solana meme-coin traders on X were talking about in the "
                       "last 24 hours: the narratives, the tokens named most (ticker and contract address if given), any "
                       "launchpad or platform news (pump.fun, letsbonk, Meteora, Raydium), and any warnings about rugs or "
                       "scams. Plain bullet points, at most 20, each with the rough number of posts behind it. Say when a "
                       "claim rests on one account."}]}
    try:
        r = requests.post("https://api.x.ai/v1/responses", json=body, timeout=180,
                          headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        d = r.json()
        cost = (d.get("usage") or {}).get("cost_in_usd_ticks", 0) / 1e10
        txt = [c.get("text") for o in d.get("output", []) if o.get("type") == "message"
               for c in o.get("content", []) if c.get("type") == "output_text"]
        return (txt[-1] if txt else "(no text)"), cost, None
    except Exception as e:
        return "", 0.0, str(e)[:100]


def picks():
    import paper
    rows = []
    led = [r for r in csv.DictReader(open(ROOT + "grinder/LEDGER.csv")) if r["entered_at"][:10] >= (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")]
    men = list(csv.DictReader(open(HERE + "/MENTIONS.csv"))) if os.path.exists(HERE + "/MENTIONS.csv") else []
    for r in led:
        m = [x for x in men if x["mint"] == r["mint"]]
        rows.append("- %s %s %s, entry %s; mentions: %s" % (r["id"], r["token"], r["mint"], r["entered_at"],
                    "; ".join("%s count %s authors %s %s" % (x["source"], x["count"], x["authors"], x["detail"][:60]) for x in m) or "none pulled"))
    return rows


def pull():
    d = outdir(); now = datetime.now(timezone.utc); since = now - timedelta(hours=24)
    L = ["# Narrative pull %s" % now.strftime("%Y-%m-%d %H:%MZ"), ""]
    errors, spend = [], 0.0
    L.append("## News headlines, last 24h")
    for name, url in FEEDS.items():
        items, err = rss(name, url, since)
        L.append("### %s" % name); L += items or ["- (none)"]
        if err:
            errors.append("%s: %s" % (name, err))
    L += ["", "## CoinGecko trending"]
    items, err = gecko_trending(); L += items or ["- (none)"]
    if err:
        errors.append("coingecko: " + err)
    L += ["", "## Reddit, six subreddits, last 24h"]
    b = int(now.timestamp()); b -= b % 3600
    try:
        L += reddit_top(b - 86400, b)
    except Exception as e:
        errors.append("reddit: " + str(e)[:80])
    L += ["", "## Telegram channels, last 24h"]
    from mentions import telegram_history
    for ch in TG_NARRATIVE:
        try:
            msgs = [m for m in telegram_history(ch, b - 86400) if b - 86400 <= m["t"] < b]
            L.append("### t.me/%s: %d messages" % (ch, len(msgs)))
            L += ["- " + m["text"][:220] for m in msgs[-10:]]
        except Exception as e:
            errors.append("telegram %s: %s" % (ch, str(e)[:60]))
    L += ["", "## X, summarised by xAI (Grok) with x_search"]
    txt, cost, err = x_narrative(); spend += cost; L.append(txt or "(none)")
    if err:
        errors.append("xai: " + err)
    L += ["", "## Tonight's Grinder picks and their mention rows"] + (picks() or ["- none"])
    L += ["", "## Pull errors", *(["- " + e for e in errors] or ["- none"]), "", "xAI spend this pull: $%.2f" % spend]
    open(d + "narrative.md", "w").write("\n".join(L) + "\n")
    dig = HERE + "/digests/%s.md" % day()
    prompt = PROMPT.format(pull=d + "narrative.md", out=digest_out(), prev=HERE + "/digests/", reg=HERE + "/SOURCES.md")
    open(d + "child-prompt.md", "w").write(prompt)
    print("pull: %s (%d lines), errors %d, xai $%.2f\nprompt: %s\nexpect: %s" % (d + "narrative.md", len(L), len(errors), spend, d + "child-prompt.md", digest_out()))


PROMPT = """You are the research desk's reader for Proteus, on Sonnet, unattended. Read {pull} (tonight's pull:
news headlines, CoinGecko trending, Reddit threads, an xAI summary of X, and the Grinder's picks with their
mention counts). Skim the two most recent files in {prev} if any, and {reg} for the sources.

Write exactly one file with the Write tool: {out}
Headings, plain English, UK spelling, no em dashes, under 400 words in all:

# Research digest, <date>
## The night in five lines
## Tokens named more than once
Ticker, contract if given, where it came up, and whether it is one of the Grinder's picks.
## The Grinder's picks, read against the chatter
One line per pick: talked about or silent, by whom (calls and shills or real discussion), anything alarming.
## Claims to check later
Up to three specific, dated claims a source made that could be scored in a week (a price call, a launch, a
listing). Name the source.
## Source notes
One line per source that was empty, broken, or obviously paid.

Rules, each enforced by a hook: you cannot spawn agents, run git or run anything in /Users/triton/PROTEUS/bin/;
you may write only under /Users/triton/PROTEUS/state/agents/ or /Users/triton/PROTEUS/sandbox/. No web fetches. A refusal is a result to report. Nothing
you write is advice; it is a record. Final message: one line saying the digest is written, and any refusals.
"""


def ingest():
    src = digest_out()
    if not os.path.exists(src) or "## The night in five lines" not in open(src).read():
        line = "- Research desk: no usable digest for %s." % day()
    else:
        os.makedirs(HERE + "/digests", exist_ok=True)
        dst = HERE + "/digests/%s.md" % day()
        open(dst, "w").write(open(src).read())
        line = "- Research desk: digest `grinder/research/digests/%s.md`." % day()
    with open(ROOT + "state/runs/%s.md" % day(), "a") as fh:
        fh.write(line + "\n")
    print(line)
    if os.path.exists(ROOT + "HALT"):
        print("HALT set: written, not committed"); return
    paths = [HERE + "/digests", HERE + "/MENTIONS.csv"]
    subprocess.run(["git", "-C", ROOT, "add"] + paths, check=False)
    # named paths (2026-10-09): a bare commit took whatever another session had staged
    r = subprocess.run(["git", "-C", ROOT, "commit", "-q", "-m", "research desk: digest and mentions %s" % day(), "--"] + paths, capture_output=True, text=True)
    if r.returncode == 0:
        subprocess.run(["git", "-C", ROOT, "push", "-q", "origin", "main"], check=False)
        print("committed and pushed")


if __name__ == "__main__":
    {"pull": pull, "ingest": ingest}[sys.argv[1] if len(sys.argv) > 1 else "pull"]()

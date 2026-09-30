#!/usr/bin/env python3
"""The research desk's per-token signals: who is talking about a token, and is anyone paying to be
seen. One row per (mint, night, source) in grinder/research/MENTIONS.csv. Written so a mention count
can become a column the replay harness tests as an entry gate (grinder/harness/VARIANTS.md).

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/research/mentions.py tonight [--x-cap 8]
    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/grinder/research/mentions.py backfill [--x-cap 60]

Sources:
- x: xAI Responses API with the x_search tool, key "XAI API Credentials" (Luke's vault, named by him
  30 Sep 2026). About $0.16 a token; capped per run; cost recorded per row from the API's own usage.
- reddit: Arctic Shift archive (keyless), posts and comments containing the mint address or $SYMBOL
  in the 24 hours before the snapshot.
- dexpaid: DexScreener orders endpoint (keyless): paid profile, boosts or ads on the token.
Every row carries the as-of time; nothing after the snapshot time is counted.
"""
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/triton/PROTEUS/"
sys.path.insert(0, ROOT + "bin"); sys.path.insert(0, ROOT + "grinder"); sys.path.insert(0, ROOT + "grinder/harness")
import paper  # noqa: E402

OUT = HERE + "/MENTIONS.csv"
FIELDS = ["mint", "symbol", "night", "asof", "source", "count", "authors", "first_seen", "shill_share",
          "max_followers", "paid", "cost_usd", "detail", "pulled_at"]
UA = {"User-Agent": "proteus-lab/0.1 research (+https://github.com/triton-xxix/proteus-lab)"}
XAI_MODEL = "grok-4.20-0309-non-reasoning"
AS = "https://arctic-shift.photon-reddit.com/api/"


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def done_keys():
    if not os.path.exists(OUT):
        return set()
    return {(r["mint"], r["night"], r["source"]) for r in csv.DictReader(open(OUT))}


def append(rows):
    new = not os.path.exists(OUT)
    with open(OUT, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def x_mentions(mint, symbol, asof):
    """One xAI call. Returns a row dict; never raises."""
    import secrets as vault
    key = vault.get("XAI API Credentials", vault="Tritons World")
    start = (asof - timedelta(hours=24)).strftime("%Y-%m-%d")
    end = asof.strftime("%Y-%m-%d")
    prompt = ("Search X for posts that mention the Solana token with contract address %s (ticker $%s) posted "
              "before %s UTC and within the 24 hours before it. Use at most two searches. Count only posts "
              "that clearly refer to this contract or this ticker on Solana. Return JSON only, no prose: "
              "{\"posts_found\": int, \"distinct_authors\": int, \"earliest\": iso or null, "
              "\"largest_author_followers\": int or null, \"share_that_are_shill_or_call_posts\": float 0-1, "
              "\"notes\": short string}") % (mint, symbol, asof.strftime("%Y-%m-%d %H:%M"))
    body = {"model": XAI_MODEL, "input": [{"role": "user", "content": prompt}],
            "tools": [{"type": "x_search", "from_date": start, "to_date": end}]}
    row = {"source": "x"}
    try:
        r = requests.post("https://api.x.ai/v1/responses", json=body, timeout=180,
                          headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        d = r.json()
        usage = d.get("usage") or {}
        row["cost_usd"] = round((usage.get("cost_in_usd_ticks") or 0) / 1e10, 4)
        txt = [c.get("text") for o in d.get("output", []) if o.get("type") == "message"
               for c in o.get("content", []) if c.get("type") == "output_text"]
        raw = (txt[-1] if txt else "").strip().strip("`")
        raw = raw[raw.find("{"): raw.rfind("}") + 1]
        j = json.loads(raw)
        row.update(count=j.get("posts_found"), authors=j.get("distinct_authors"), first_seen=j.get("earliest") or "",
                   shill_share=j.get("share_that_are_shill_or_call_posts"), max_followers=j.get("largest_author_followers"),
                   detail=(j.get("notes") or "")[:200])
    except Exception as e:
        row["detail"] = "error: %s" % str(e)[:150]
    return row


SUBS = ["SolanaMemeCoins", "memecoins", "CryptoMoonShots", "solana", "pumpfun", "CryptoCurrency"]
CACHE = ROOT + "state/research/reddit/"


def reddit_window(sub, after, before):
    """All posts and comments in one subreddit between two epoch seconds, cached per sub and window."""
    os.makedirs(CACHE, exist_ok=True)
    path = CACHE + "%s-%d-%d.jsonl" % (sub, after, before)
    if os.path.exists(path):
        return [json.loads(l) for l in open(path)]
    items = []
    for kind in ("posts", "comments"):
        cur = after
        for _ in range(40):                                   # 40 pages of 100 per kind at most
            r = None
            for attempt in range(4):
                r = requests.get(AS + "%s/search" % kind, params={"subreddit": sub, "after": cur, "before": before,
                                 "limit": 100, "sort": "asc"}, headers=UA, timeout=60)
                if r.status_code == 200:
                    break
                time.sleep(5 * (attempt + 1))
            data = (r.json().get("data") or []) if r is not None and r.status_code == 200 else []
            for p in data:
                items.append({"kind": kind, "t": p.get("created_utc"), "author": p.get("author"),
                              "text": " ".join(str(p.get(k) or "") for k in ("title", "selftext", "body", "url"))})
            if len(data) < 100:
                break
            cur = int(data[-1]["created_utc"]) + 1
            time.sleep(1)
    with open(path, "w") as fh:
        for it in items:
            fh.write(json.dumps(it) + "\n")
    return items


def reddit_mentions(mint, symbol, asof):
    """Mint address anywhere, or $SYMBOL as a cashtag, in the six subreddits, 24h before asof."""
    import re
    before = int(asof.timestamp()); after = before - 86400
    after -= after % 3600; before -= before % 3600            # hour-aligned so tokens on one night share the cache
    tag = re.compile(r"\$%s\b" % re.escape(symbol), re.I) if symbol and len(symbol) >= 3 else None
    hits, authors, first, per = 0, set(), None, {}
    for sub in SUBS:
        for it in reddit_window(sub, after, before):
            if mint in it["text"] or (tag and tag.search(it["text"])):
                hits += 1; authors.add(it["author"]); per[sub] = per.get(sub, 0) + 1
                first = it["t"] if first is None or (it["t"] and it["t"] < first) else first
    return {"source": "reddit", "count": hits, "authors": len(authors - {None, "[deleted]"}),
            "first_seen": datetime.fromtimestamp(first, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if first else "",
            "detail": ",".join("%s:%d" % kv for kv in sorted(per.items()))}


TG_LIST = HERE + "/telegram-channels.json"
TG_CACHE = ROOT + "state/research/telegram/"


def tg_channels():
    return json.load(open(TG_LIST))["channels"]


def telegram_history(channel, need_from):
    """All messages of a public channel back to need_from (epoch s), from its t.me/s preview, cached per
    channel and extended only as far as needed. Pages are about 20 messages; capped at 600 pages."""
    import html as h
    os.makedirs(TG_CACHE, exist_ok=True)
    path = TG_CACHE + channel + ".jsonl"
    have = {}
    if os.path.exists(path):
        for l in open(path):
            m = json.loads(l); have[m["id"]] = m
    def fetch(url):
        for attempt in range(4):
            try:
                r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
                if r.status_code == 200:
                    return r.text
            except Exception:
                pass
            time.sleep(3 * (attempt + 1))
        return ""
    def parse(page):
        out = []
        for mid, body in re.findall(r'data-post="[^/]+/(\d+)"(.*?)(?=data-post="|\Z)', page, re.S):
            t = re.search(r'<time datetime="([^"]+)"', body)
            if not t:
                continue
            txt = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', body, re.S)
            links = " ".join(re.findall(r'href="([^"]+)"', body))
            text = h.unescape(re.sub(r"<[^>]+>", " ", txt.group(1) if txt else "")) + " " + links
            out.append({"id": int(mid), "t": datetime.fromisoformat(t.group(1).replace("Z", "+00:00")).timestamp(),
                        "text": re.sub(r"\s+", " ", text)[:3000]})
        return out
    # Page back from the newest message. Stop when the page reaches need_from, or when it runs into
    # messages already cached and the cache itself already reaches need_from.
    cache_ok = bool(have) and min(m["t"] for m in have.values()) <= need_from
    cached_ids = set(have)
    batch, pages = parse(fetch("https://t.me/s/%s" % channel)), 0
    while batch and pages < 600:
        for m in batch:
            have[m["id"]] = m
        oldest = min(batch, key=lambda m: m["id"])
        if oldest["t"] <= need_from:
            break
        if cache_ok and any(m["id"] in cached_ids for m in batch):
            break
        time.sleep(1.2)
        batch = parse(fetch("https://t.me/s/%s?before=%d" % (channel, oldest["id"])))
        pages += 1
    with open(path, "w") as fh:
        for i in sorted(have):
            fh.write(json.dumps(have[i]) + "\n")
    return list(have.values())


_TG_MEM = {}


def telegram_mentions(mint, symbol, asof):
    before = asof.timestamp(); after = before - 86400
    hits, first, per, kinds = 0, None, {}, {}
    for c in tg_channels():
        ch = c["channel"]
        if ch not in _TG_MEM or min((m["t"] for m in _TG_MEM[ch]), default=9e18) > after:
            _TG_MEM[ch] = telegram_history(ch, after)
        for m in _TG_MEM[ch]:
            if after <= m["t"] < before and mint in m["text"]:
                hits += 1; per[ch] = per.get(ch, 0) + 1; kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
                first = m["t"] if first is None or m["t"] < first else first
    return {"source": "telegram", "count": hits, "authors": len(per),
            "first_seen": datetime.fromtimestamp(first, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if first else "",
            "paid": ",".join("%s:%d" % kv for kv in sorted(kinds.items())),
            "detail": ",".join("%s:%d" % kv for kv in sorted(per.items()))[:200]}


def jupiter(mint, asof):
    """Jupiter's token record: organic score, holder count, audit flags. Current values only, so a
    backfilled row is marked as-of now, not as-of the snapshot."""
    try:
        d = requests.get("https://lite-api.jup.ag/tokens/v2/search", params={"query": mint}, headers=UA, timeout=20).json()
        t = next((x for x in d if x.get("id") == mint), None) if isinstance(d, list) else None
        if not t:
            return {"source": "jupiter", "detail": "not found"}
        late = datetime.now(timezone.utc) - asof > timedelta(hours=2)
        return {"source": "jupiter", "count": t.get("organicScore"), "authors": t.get("holderCount"),
                "paid": t.get("organicScoreLabel") or "",
                "detail": ("NOW not as-of; " if late else "") + json.dumps({k: t.get(k) for k in ("isVerified", "tags", "audit")})[:180]}
    except Exception as e:
        return {"source": "jupiter", "detail": "error: %s" % str(e)[:100]}


def dex_paid(mint, asof):
    """DexScreener orders: paid profile / boosts / ads. The endpoint has no history, so it is only
    meaningful tonight; a backfilled row says so."""
    try:
        r = requests.get("https://api.dexscreener.com/orders/v1/solana/" + mint, headers=UA, timeout=20)
        d = r.json() if r.ok else {}
        orders = d if isinstance(d, list) else (d.get("orders") or [])
        boosts = [] if isinstance(d, list) else (d.get("boosts") or [])
        paid = [o for o in orders if o.get("status") in ("approved", "processing")]
        before = [o for o in paid if (o.get("paymentTimestamp") or 0) / 1000 <= asof.timestamp()]
        kinds = sorted({o.get("type", "?") for o in before} | ({"boost"} if boosts else set()))
        return {"source": "dexpaid", "count": len(before) + len(boosts), "paid": ",".join(kinds),
                "detail": "orders %d paid-before-asof %d, boosts %d (boost times not given)" % (len(orders), len(before), len(boosts))}
    except Exception as e:
        return {"source": "dexpaid", "detail": "error: %s" % str(e)[:100]}


def run(tokens, x_cap):
    have = done_keys(); rows = []; x_used = 0; spent = 0.0
    for t in tokens:
        mint, sym, night = t["mint"], t["symbol"], t["ts"]
        asof = ts(night)
        base = {"mint": mint, "symbol": sym, "night": night, "asof": night}
        for src in ("dexpaid", "jupiter", "reddit", "telegram", "x"):
            if (mint, night, src) in have:
                continue
            if src == "x":
                if x_used >= x_cap:
                    continue
                x_used += 1
                row = x_mentions(mint, sym, asof); spent += row.get("cost_usd") or 0
            elif src == "reddit":
                row = reddit_mentions(mint, sym, asof)
            elif src == "telegram":
                row = telegram_mentions(mint, sym, asof)
            elif src == "jupiter":
                row = jupiter(mint, asof)
            else:
                row = dex_paid(mint, asof)
            row.update(base); row["pulled_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            rows.append(row); append([row])
            print("%s %-10s %-7s count=%s authors=%s %s" % (night[:10], sym[:10], src, row.get("count"), row.get("authors"), row.get("detail", "")[:60]), flush=True)
    print("rows %d, x calls %d, x spend $%.2f" % (len(rows), x_used, spent))
    return spent


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "tonight"
    cap = int(sys.argv[sys.argv.index("--x-cap") + 1]) if "--x-cap" in sys.argv else 8
    if cmd == "backfill":
        import replay
        toks = replay.population(time.time())
    else:
        snap = paper.latest_snapshot()
        toks = [s for s in snap if paper.passes(s)]
        toks.sort(key=lambda s: -(paper.fnum(s.get("vol_h1")) or 0))
    run(toks, cap)


if __name__ == "__main__":
    main()

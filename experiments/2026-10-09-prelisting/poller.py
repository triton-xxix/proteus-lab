"""Pre-listing tracker, paper only. Run by launchd every 60 s (label com.proteus.prelisting, plist in
this folder, loaded from here, nothing written to ~/Library). Stops itself at END_UTC and on HALT or
a DONE file, and unloads its own job. Writes only under track/ in this folder, plus one git commit a
day of that day's candidate list (the commit timestamp is the proof the list came first; not
pushed from here, the next nightly or interactive push publishes it).

Every poll:
- reads the Upbit trade notices (page 1), the Binance new-listing catalogue (page 1) and Bithumb's
  latest notices; every 5 minutes Coinbase's /currencies and /products (a new currency or product is
  Coinbase's keyless listing trail; its roadmap posts are on X only);
- logs every new notice to track/feed.jsonl with the time it was first seen;
- turns a listing notice into an event (track/events.jsonl) and records whether the coin was on the
  most recent candidate list committed before the announcement, and at what rank;
- six minutes after an event, prices the paper trade from 1-minute candles on Binance, OKX or Bybit:
  hold price = the close of the last full minute before the announcement, exit = the LOW of the
  minute containing announcement + 3 minutes, less 0.5% round trip (the rule in RULES.md). Every
  listing with a prior market is priced, on the list or not, so the week also re-tests the event study.
Once a day, at the first poll after 00:00 UTC, score.py builds the ranked list for that day, with a
price snapshot of every coin in the universe, and the list is committed.
Usage: python3 poller.py [poll|list|load|unload|status]
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

OUT = os.path.dirname(os.path.abspath(__file__))
TRACK = os.path.join(OUT, "track")
ROOT = "/Users/triton/PROTEUS"
# commits only from the main checkout; a copy run anywhere else (a worktree, a test) never commits
REL = "experiments/2026-10-09-prelisting" if OUT == os.path.join(ROOT, "experiments", "2026-10-09-prelisting") else None
LABEL = "com.proteus.prelisting"
PLIST = os.path.join(OUT, LABEL + ".plist")
END_UTC = datetime(2026, 10, 17, 0, 5, tzinfo=timezone.utc).timestamp()
UA = {"User-Agent": "Mozilla/5.0 (proteus-prelisting)"}
COST = 0.005
EXIT_MIN = 3
sys.path.insert(0, OUT)


def now_s():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def jl(name, row):
    with open(os.path.join(TRACK, name), "a") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def get(url, timeout=20):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return json.load(r)
    except Exception as e:
        return {"__error": str(e)[:120]}


def domain():
    return "gui/%d" % os.getuid()


def load():
    r = subprocess.run(["/bin/launchctl", "bootstrap", domain(), PLIST], capture_output=True, text=True)
    print("bootstrap rc", r.returncode, (r.stdout or r.stderr).strip()[:200])


def unload():
    subprocess.run(["/bin/launchctl", "bootout", domain() + "/" + LABEL], capture_output=True)


def state():
    p = os.path.join(TRACK, "state.json")
    return json.load(open(p)) if os.path.exists(p) else {"seen": {}, "pending": [], "list_day": None}


def save_state(s):
    p = os.path.join(TRACK, "state.json")
    json.dump(s, open(p + ".tmp", "w"))
    os.replace(p + ".tmp", p)


# ---------- feeds ----------

def upbit_feed():
    d = get("https://api-manager.upbit.com/api/v1/announcements?os=web&page=1&per_page=20&category=trade")
    if "__error" in d:
        return None, d["__error"]
    out = []
    for n in ((d.get("data") or {}).get("notices") or []):
        out.append({"src": "upbit", "id": "upbit:%s" % n.get("id"), "title": n["title"],
                    "t": datetime.fromisoformat(n["first_listed_at"]).timestamp()})
    return out, None


def binance_feed():
    d = get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=48&pageNo=1&pageSize=20")
    if "__error" in d:
        return None, d["__error"]
    arts = (((d.get("data") or {}).get("catalogs") or [{}])[0].get("articles")) or []
    return [{"src": "binance", "id": "binance:%s" % a.get("code"), "title": a["title"], "t": a["releaseDate"] / 1000} for a in arts], None


def bithumb_feed():
    d = get("https://api.bithumb.com/v1/notices?count=5")
    if isinstance(d, dict):
        return None, d.get("__error", "bad reply")
    out = []
    for n in d:
        t = datetime.strptime(n["published_at"] + " +0900", "%Y-%m-%d %H:%M:%S %z").timestamp()
        out.append({"src": "bithumb", "id": "bithumb:%s" % n["pc_url"].rsplit("/", 1)[-1], "title": n["title"], "t": t})
    return out, None


def coinbase_feed():
    out = []
    d = get("https://api.exchange.coinbase.com/currencies", timeout=30)
    if isinstance(d, dict):
        return None, d.get("__error", "bad reply")
    for c in d:
        out.append({"src": "coinbase", "id": "coinbase-currency:%s" % c["id"], "title": "currency %s (%s) %s" % (c["id"], c.get("name"), c.get("status")), "t": None, "symbol": c["id"]})
    d = get("https://api.exchange.coinbase.com/products", timeout=30)
    if isinstance(d, dict):
        return None, d.get("__error", "bad reply")
    for p in d:
        out.append({"src": "coinbase", "id": "coinbase-product:%s" % p["id"], "title": "product %s %s" % (p["id"], p.get("status")), "t": None, "symbol": p["base_currency"]})
    return out, None


def classify(n):
    """Return (kind, [symbols]) for a listing notice, else (None, [])."""
    import re
    title = n["title"]
    if n["src"] == "upbit":
        if ("신규 거래지원" in title or "디지털 자산 추가" in title) and "취소" not in title:
            head = title.split("신규 거래지원")[0] if "신규 거래지원" in title else title.split("마켓")[0]
            syms = [s for s in re.findall(r"\(([A-Z0-9]{1,12})\)", head) if s not in ("KRW", "BTC", "USDT")]
            return ("upbit_krw" if "KRW" in title else "upbit_btc_usdt"), syms
    if n["src"] == "binance":
        if title.startswith("Binance Will List"):
            return "binance_spot", re.findall(r"\(([A-Z0-9]{2,12})\)", title)
        if title.startswith("Binance Futures Will Launch") and "Perpetual" in title:
            return "binance_perp", [re.sub(r"^1000+", "", s[:-4]) for s in re.findall(r"\b([A-Z0-9]{2,20}USDT)\b", title)]
    if n["src"] == "bithumb":
        if "원화 마켓 추가" in title or "마켓 추가" in title or "신규 거래지원" in title:
            return "bithumb_krw", [s for s in re.findall(r"\(([A-Z0-9]{1,12})\)", title) if s not in ("KRW", "BTC", "USDT")]
    if n["src"] == "coinbase":
        kind = "coinbase_currency" if n["id"].startswith("coinbase-currency") else "coinbase_product"
        return kind, [n["symbol"]]
    return None, []


TARGETS = ("upbit_krw", "binance_spot", "coinbase_currency", "coinbase_product", "bithumb_krw")


# ---------- lists ----------

def latest_list_before(t):
    """The newest committed list whose commit time is before t: (day, rank map) or (None, {})."""
    p = os.path.join(TRACK, "commits.json")
    commits = json.load(open(p)) if os.path.exists(p) else {}
    days = [d for d, ct in commits.items() if ct and ct < t]
    if not days:
        return None, {}
    best = json.load(open(os.path.join(TRACK, "lists", max(days) + ".json")))
    return best["day"], {c["symbol"]: c["rank"] for c in best["candidates"]}


def build_list():
    import score
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lst = score.build(day)
    os.makedirs(os.path.join(TRACK, "lists"), exist_ok=True)
    path = os.path.join(TRACK, "lists", day + ".json")
    json.dump(lst, open(path, "w"), indent=0, sort_keys=True)
    committed = None
    if REL and not os.path.exists(os.path.join(ROOT, "HALT")):
        rel = os.path.join(REL, "track", "lists", day + ".json")
        a = subprocess.run(["/usr/bin/git", "-C", ROOT, "add", rel], capture_output=True, text=True)
        c = subprocess.run(["/usr/bin/git", "-C", ROOT, "commit", "-q", "-m",
                            "prelisting: candidate list %s (%d coins), committed before any announcement can confirm it" % (day, len(lst["candidates"])),
                            "--", rel], capture_output=True, text=True)
        if c.returncode == 0:
            committed = time.time()
            h = subprocess.run(["/usr/bin/git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
            # no push from launchd: the keychain credential helper blocks there (9 Oct 2026). The commit
            # timestamp is the proof; the next nightly or interactive push publishes it.
            jl("lists.jsonl", {"day": day, "commit": h, "at": now_s()})
        else:
            jl("lists.jsonl", {"day": day, "commit": None, "at": now_s(), "err": (a.stderr + c.stderr + c.stdout)[-200:]})
    # the commit time decides which announcements the list can claim; an uncommitted list claims none
    p = os.path.join(TRACK, "commits.json")
    commits = json.load(open(p)) if os.path.exists(p) else {}
    commits[day] = committed
    json.dump(commits, open(p, "w"), indent=0, sort_keys=True)
    return committed is not None


# ---------- paper pricing ----------

def m1(sym, s, e):
    for venue in ("binance", "okx", "bybit"):
        if venue == "binance":
            d = get("https://data-api.binance.vision/api/v3/klines?symbol=%sUSDT&interval=1m&limit=60&startTime=%d&endTime=%d" % (sym, s * 1000, e * 1000))
            rows = [(r[0] / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in d] if isinstance(d, list) else []
        elif venue == "okx":
            d = get("https://www.okx.com/api/v5/market/history-candles?instId=%s-USDT&bar=1m&limit=60&after=%d" % (sym, e * 1000))
            rows = sorted((int(r[0]) / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in (d.get("data") or [])) if isinstance(d, dict) else []
        else:
            d = get("https://api.bybit.com/v5/market/kline?category=spot&symbol=%sUSDT&interval=1&limit=60&start=%d&end=%d" % (sym, s * 1000, e * 1000))
            rows = sorted((int(r[0]) / 1000, float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in ((d.get("result") or {}).get("list") or [])) if isinstance(d, dict) else []
        rows = [r for r in rows if s <= r[0] <= e]
        if rows:
            return venue, rows
    return None, []


def price_event(ev):
    t = ev["t_announced"]
    m0 = int(t // 60 * 60)
    venue, c = m1(ev["symbol"], m0 - 900, m0 + 900)
    before = [x for x in c if x[0] + 60 <= t]
    bar = next((x for x in c if x[0] <= t + 60 * EXIT_MIN < x[0] + 60 and x[0] > m0), None)
    if not before or not bar:
        return {"priced": False, "why": "no prior 1-minute market" if not c else "bars missing", "venue": venue}
    hold = before[-1][4]
    out = {"priced": True, "venue": venue, "hold_px": hold, "exit_low_px": bar[3], "exit_close_px": bar[4],
           "ret_pess_3m": round(bar[3] / hold - 1 - COST, 4), "ret_typ_3m": round(bar[4] / hold - 1 - COST, 4)}
    if ev.get("list_entry_px"):
        out["ret_from_list_entry"] = round(bar[3] / ev["list_entry_px"] - 1 - COST, 4)
    return out


# ---------- main loop ----------

def poll():
    os.makedirs(TRACK, exist_ok=True)
    if os.path.exists(os.path.join(OUT, "DONE")) or os.path.exists(os.path.join(ROOT, "HALT")):
        jl("polls.jsonl", {"at": now_s(), "stopped": "DONE or HALT"})
        unload()
        return
    if time.time() >= END_UTC:
        try:
            import score
            json.dump({"at_unix": time.time(), "prices": score.prices()}, open(os.path.join(TRACK, "final_prices.json"), "w"))
        except Exception as e:
            jl("polls.jsonl", {"at": now_s(), "final_prices_error": str(e)[:120]})
        open(os.path.join(OUT, "DONE"), "w").write(now_s())
        jl("polls.jsonl", {"at": now_s(), "stopped": "end time"})
        unload()
        return
    if not os.path.exists(os.path.join(TRACK, "START")):
        open(os.path.join(TRACK, "START"), "w").write(now_s())
    st = state()
    t0 = time.time()
    errors, new = [], 0
    first_run = not st["seen"]
    feeds = [upbit_feed, binance_feed, bithumb_feed]
    if first_run or int(t0 // 60) % 5 == 0:
        feeds.append(coinbase_feed)
    for f in feeds:
        rows, err = f()
        if err:
            errors.append("%s: %s" % (f.__name__, err))
            continue
        known = {k.split(":")[0] for k in st["seen"]}
        for n in rows:
            if n["id"] in st["seen"]:
                continue
            st["seen"][n["id"]] = t0
            if n["id"].split(":")[0] not in known:
                continue  # first sight of a whole feed is the baseline, not news
            new += 1
            n["seen_at"] = t0
            if n["t"] is None:
                n["t"] = t0
            jl("feed.jsonl", n)
            kind, syms = classify(n)
            if kind in TARGETS:
                day, ranks = latest_list_before(n["t"])
                for s in syms:
                    ev = {"kind": kind, "symbol": s, "t_announced": n["t"], "t_seen": t0, "lag_s": round(t0 - n["t"]),
                          "title": n["title"], "list_day": day, "rank": ranks.get(s)}
                    if day:
                        lp = json.load(open(os.path.join(TRACK, "lists", day + ".json")))
                        ev["list_entry_px"] = (lp.get("prices") or {}).get(s)
                    st["pending"].append(ev)
    # price events six minutes on
    keep = []
    for ev in st["pending"]:
        if time.time() < ev["t_announced"] + 360:
            keep.append(ev)
            continue
        ev.update(price_event(ev))
        ev["priced_at"] = now_s()
        jl("events.jsonl", ev)
    st["pending"] = keep
    # the day's list
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if st.get("list_day") != today:
        try:
            ok = build_list()
            st["list_day"] = today
            if not ok:
                errors.append("list built but not committed")
        except Exception as e:
            errors.append("list: %s" % str(e)[:150])
            st["list_day"] = today if "retry" not in str(e) else st.get("list_day")
    save_state(st)
    jl("polls.jsonl", {"at": now_s(), "secs": round(time.time() - t0, 1), "new": new, "errors": errors, "pending": len(keep)})


def status():
    for f in ("polls.jsonl", "feed.jsonl", "events.jsonl", "lists.jsonl"):
        p = os.path.join(TRACK, f)
        n = sum(1 for _ in open(p)) if os.path.exists(p) else 0
        print(f, n)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poll"
    {"poll": poll, "list": build_list, "load": load, "unload": unload, "status": status}[cmd]()

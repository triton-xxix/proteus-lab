"""Pre-listing research, step 1: collect what was publicly visible before each major-exchange listing.

Keyless sources only. Everything raw is cached under cache/ (gitignored) so analysis can be re-run
without hitting the venues again; the tables analysis.py needs are written to data/.

What it pulls, window 1 Jun 2025 to now (15 months, so a 12-month target window has 3 months of
look-back):
- Upbit trade notices (all, not only KRW): new trading support and market additions, per ticker,
  with the markets named in the title (KRW, BTC, USDT).
- Binance "New Cryptocurrency Listing" catalogue 48: spot listings ("Binance Will List"), futures
  launches ("Binance Futures Will Launch ... XUSDT"), everything else kept as "other".
- Listing times that venues publish: Binance USD-M perps (onboardDate), OKX spot and swap
  (listTime), Bybit linear perps (launchTime), Gate spot (buy_start), Binance Alpha (listingTime).
- First trading day from daily candles where no listing time is published: Bithumb KRW, Coinbase
  USD, Bybit spot, Binance spot. A first candle on the first day of the window means "older".
- Daily USDT turnover per coin on Bybit spot, OKX spot and Binance spot, for the volume signals.
Usage: python3 collect.py [all|notices|static|firsts|volume]
"""
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
DATA = os.path.join(HERE, "data")
UA = {"User-Agent": "Mozilla/5.0"}
SINCE = datetime(2025, 6, 1, tzinfo=timezone.utc).timestamp()
DAY = 86400


def get(url, tries=3):
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):
                return None
            time.sleep(2 * (a + 1))
        except Exception:
            time.sleep(2 * (a + 1))
    return None


def cached(name, fn):
    p = os.path.join(CACHE, name)
    if os.path.exists(p):
        return json.load(open(p))
    v = fn()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(v, open(p, "w"))
    return v


def save(name, v):
    os.makedirs(DATA, exist_ok=True)
    json.dump(v, open(os.path.join(DATA, name), "w"), indent=0, sort_keys=True)


# ---------- announcements ----------

UPBIT_PAIR = re.compile(r"([^\s,()]+)\(([A-Z0-9]{1,12})\)")


def upbit_notices():
    out, page = [], 1
    while True:
        d = get("https://api-manager.upbit.com/api/v1/announcements?os=web&page=%d&per_page=20&category=trade" % page)
        notes = ((d or {}).get("data") or {}).get("notices") or []
        if not notes:
            break
        stop = False
        for n in notes:
            t = datetime.fromisoformat(n["first_listed_at"]).timestamp()
            if t < SINCE:
                stop = True
                continue
            title = n["title"]
            if "신규 거래지원" in title:
                kind = "new"
            elif "디지털 자산 추가" in title:
                kind = "add"
            else:
                continue
            head = title.split("신규 거래지원")[0] if kind == "new" else title.split("마켓")[0]
            m = re.search(r"\(([A-Z ,]+) 마켓\)", title) or re.search(r"((?:KRW|BTC|USDT)(?:, ?(?:KRW|BTC|USDT))*) 마켓", title)
            markets = [x.strip() for x in m.group(1).split(",")] if m else []
            cancelled = "취소" in title
            for _, sym in UPBIT_PAIR.findall(head):
                if sym in ("KRW", "BTC", "USDT"):
                    continue
                out.append({"venue": "upbit", "t": t, "symbol": sym, "kind": kind, "markets": markets,
                            "cancelled": cancelled, "id": n.get("id"), "title": title})
        if stop:
            break
        page += 1
        time.sleep(0.4)
    return out


def binance_notices():
    out, page = [], 1
    while True:
        d = get("https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=48&pageNo=%d&pageSize=50" % page)
        arts = (((d or {}).get("data") or {}).get("catalogs") or [{}])[0].get("articles") or []
        if not arts:
            break
        stop = False
        for a in arts:
            t = a["releaseDate"] / 1000
            if t < SINCE:
                stop = True
                continue
            title = a["title"]
            if title.startswith("Binance Will List"):
                kind, syms = "spot", re.findall(r"\(([A-Z0-9]{2,12})\)", title)
            elif title.startswith("Binance Futures Will Launch") and "Perpetual" in title:
                kind = "futures"
                syms = [re.sub(r"^1000+|^1M", "", s[:-4]) for s in re.findall(r"\b([A-Z0-9]{2,20}USDT)\b", title)]
            else:
                kind, syms = "other", []
            for s in syms:
                out.append({"venue": "binance", "t": t, "symbol": s, "kind": kind, "title": title, "code": a.get("code")})
            if not syms:
                out.append({"venue": "binance", "t": t, "symbol": None, "kind": kind, "title": title, "code": a.get("code")})
        if stop:
            break
        page += 1
        time.sleep(0.5)
    return out


# ---------- published listing times ----------

def strip_mult(s):
    return re.sub(r"^(1000000|100000|10000|1000|1M)", "", s)


def static_times():
    out = {}
    d = get("https://fapi.binance.com/fapi/v1/exchangeInfo") or {}
    out["binance_perp"] = {}
    for s in d.get("symbols", []):
        if s.get("contractType") == "PERPETUAL" and s.get("quoteAsset") == "USDT":
            b = strip_mult(s["baseAsset"])
            out["binance_perp"][b] = min(out["binance_perp"].get(b, 1e13), s["onboardDate"] / 1000)
    for inst in ("SPOT", "SWAP"):
        d = get("https://www.okx.com/api/v5/public/instruments?instType=" + inst) or {}
        key = "okx_" + inst.lower()
        out[key] = {}
        for s in d.get("data", []):
            if inst == "SPOT" and s.get("quoteCcy") != "USDT":
                continue
            if inst == "SWAP" and s.get("settleCcy") != "USDT":
                continue
            b = s["baseCcy"] if inst == "SPOT" else strip_mult(s["instFamily"].split("-")[0])
            if s.get("listTime"):
                out[key][b] = min(out[key].get(b, 1e13), int(s["listTime"]) / 1000)
    out["bybit_perp"], cursor = {}, ""
    for _ in range(20):
        d = get("https://api.bybit.com/v5/market/instruments-info?category=linear&limit=1000&cursor=" + cursor) or {}
        r = d.get("result") or {}
        for s in r.get("list", []):
            if s.get("quoteCoin") == "USDT" and s.get("contractType") == "LinearPerpetual":
                b = strip_mult(s["baseCoin"])
                out["bybit_perp"][b] = min(out["bybit_perp"].get(b, 1e13), int(s["launchTime"]) / 1000)
        cursor = r.get("nextPageCursor") or ""
        if not cursor:
            break
    d = get("https://api.bybit.com/v5/market/instruments-info?category=spot&limit=1000") or {}
    out["bybit_spot_symbols"] = sorted({s["baseCoin"] for s in (d.get("result") or {}).get("list", []) if s.get("quoteCoin") == "USDT"})
    d = get("https://api.gateio.ws/api/v4/spot/currency_pairs") or []
    out["gate_spot"] = {s["base"]: s["buy_start"] for s in d if s.get("quote") == "USDT" and s.get("buy_start")}
    d = get("https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/cex/alpha/all/token/list") or {}
    out["binance_alpha"] = {}
    out["binance_alpha_mcap"] = {}
    for s in d.get("data") or []:
        if s.get("listingTime"):
            out["binance_alpha"][s["symbol"]] = min(out["binance_alpha"].get(s["symbol"], 1e13), s["listingTime"] / 1000)
    d = get("https://data-api.binance.vision/api/v3/exchangeInfo") or {}
    out["binance_spot_symbols"] = sorted({s["baseAsset"] for s in d.get("symbols", []) if s.get("quoteAsset") == "USDT"})
    d = get("https://api.upbit.com/v1/market/all") or []
    out["upbit_markets"] = [m["market"] for m in d]
    d = get("https://api.bithumb.com/v1/market/all") or []
    out["bithumb_markets"] = [m["market"] for m in d]
    d = get("https://api.exchange.coinbase.com/products") or []
    out["coinbase_products"] = [{"id": p["id"], "base": p["base_currency"], "quote": p["quote_currency"], "status": p["status"]} for p in d]
    return out


# ---------- first trading day from daily candles ----------

def first_day_bithumb(market):
    """Earliest daily candle at or after SINCE. Returns (first_ts, daily rows [ts, close, krw_turnover])."""
    rows, to = [], ""
    for _ in range(4):
        u = "https://api.bithumb.com/v1/candles/days?market=%s&count=200%s" % (market, ("&to=" + to.replace(" ", "%20")) if to else "")
        d = get(u)
        if not d or not isinstance(d, list):
            break
        for c in d:
            ts = datetime.fromisoformat(c["candle_date_time_utc"]).replace(tzinfo=timezone.utc).timestamp()
            rows.append([ts, c["trade_price"], c["candle_acc_trade_price"]])
        oldest = min(datetime.fromisoformat(c["candle_date_time_utc"]) for c in d)
        if len(d) < 200 or oldest.replace(tzinfo=timezone.utc).timestamp() < SINCE:
            break
        to = oldest.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(0.1)
    rows = sorted({r[0]: r for r in rows}.values())
    return rows


def first_day_coinbase(pid):
    rows, s = [], SINCE
    now = time.time()
    while s < now:
        e = min(now, s + 299 * DAY)
        d = get("https://api.exchange.coinbase.com/products/%s/candles?granularity=86400&start=%s&end=%s" % (
            pid, datetime.fromtimestamp(s, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            datetime.fromtimestamp(e, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
        if isinstance(d, list):
            rows += [[c[0], c[4], c[5] * c[4]] for c in d]
        s = e
        time.sleep(0.15)
    return sorted({r[0]: r for r in rows}.values())


def daily_bybit(base):
    d = get("https://api.bybit.com/v5/market/kline?category=spot&symbol=%sUSDT&interval=D&limit=1000" % base) or {}
    lst = (d.get("result") or {}).get("list") or []
    return sorted([[int(r[0]) / 1000, float(r[4]), float(r[6])] for r in lst if int(r[0]) / 1000 >= SINCE - 60 * DAY])


def daily_okx(base):
    rows, after = [], ""
    for _ in range(6):
        d = get("https://www.okx.com/api/v5/market/history-candles?instId=%s-USDT&bar=1Dutc&limit=100%s" % (base, ("&after=" + after) if after else "")) or {}
        data = d.get("data") or []
        if not data:
            break
        rows += [[int(r[0]) / 1000, float(r[4]), float(r[7])] for r in data]
        after = data[-1][0]
        if int(after) / 1000 < SINCE - 60 * DAY:
            break
        time.sleep(0.11)
    return sorted({r[0]: r for r in rows}.values())


def daily_binance(base):
    d = get("https://data-api.binance.vision/api/v3/klines?symbol=%sUSDT&interval=1d&limit=1000&startTime=%d" % (base, int((SINCE - 60 * DAY) * 1000)))
    if not isinstance(d, list):
        return []
    return [[r[0] / 1000, float(r[4]), float(r[7])] for r in d]


def pull_many(tag, keys, fn):
    out = {}
    shard, shards = (int(x) for x in os.environ.get("SHARD", "0/1").split("/"))
    for i, k in enumerate(keys):
        if i % shards != shard:
            continue
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", k)
        out[k] = cached("%s/%s.json" % (tag, safe), lambda: fn(k))
        if i % 100 == 0:
            print(tag, i, "/", len(keys), flush=True)
    return out


def main(what):
    if what in ("all", "notices"):
        up = cached("upbit_notices.json", upbit_notices)
        bn = cached("binance_notices.json", binance_notices)
        save("upbit_notices.json", up)
        save("binance_notices.json", bn)
        print("upbit", len(up), "binance", len(bn))
    if what in ("all", "static"):
        st = cached("static.json", static_times)
        print({k: len(v) for k, v in st.items()})
    st = cached("static.json", static_times)
    if what in ("all", "firsts", "bithumb"):
        bt = [m for m in st["bithumb_markets"] if m.startswith("KRW-")]
        pull_many("bithumb", bt, first_day_bithumb)
    if what in ("all", "firsts", "coinbase"):
        cb = sorted({p["id"] for p in st["coinbase_products"] if p["quote"] == "USD"})
        pull_many("coinbase", cb, first_day_coinbase)
    if what in ("all", "volume"):
        pull_many("bybit", st["bybit_spot_symbols"], daily_bybit)
        pull_many("okx", sorted(st["okx_spot"]), daily_okx)
        pull_many("binance", st["binance_spot_symbols"], daily_binance)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")

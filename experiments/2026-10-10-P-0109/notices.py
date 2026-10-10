"""P-0109: Binance spot delisting and monitoring-tag notices, last 12 months, keyless.

Fixed before the run:
  Notices  catalogue 161 pages 1 to 3, titles "Binance Will Delist A, B on DATE" and "Monitoring Tag to
           Include A, B"; stablecoins and fiat notices skipped. Release time = the notice's releaseDate.
  Prices   Binance spot <TICKER>USDT 5-minute klines (keyless). p0 = open of the candle containing the
           release; +5m = close of that candle; +24h and +7d = close of the candle 24 h / 7 d later.
  Answer   median move at +24h and +7d, and the share of the +24h fall a seller at +5m avoided:
           (p5 - p24) / (p0 - p24) when the coin fell.
  Missing  a pair Binance no longer serves (delisted) is counted as missing, not guessed.
"""
import json
import re
import statistics
import time
import urllib.error
import urllib.request

OUT = "/Users/triton/PROTEUS/experiments/2026-10-10-P-0109/"
CMS = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=161&pageNo=%d&pageSize=50"
YEAR_AGO_MS = 1791676800000 - 365 * 86400 * 1000


def getj(url):
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-p0109"}), timeout=30).read())
    except urllib.error.HTTPError as e:
        return {"_http": e.code}


def notices():
    out = []
    for page in (1, 2, 3):
        d = getj(CMS % page)
        for a in (d.get("data") or {}).get("catalogs", [{}])[0].get("articles", []):
            t, ms = a["title"], a["releaseDate"]
            if ms < YEAR_AGO_MS:
                continue
            m = re.match(r"Binance Will Delist (.+?) on \d{4}-\d\d-\d\d", t) or re.search(r"Monitoring Tag to Include (.+?) on \d{4}", t)
            if not m:
                continue
            kind = "monitoring" if "Monitoring" in t else "delist"
            for tk in re.split(r",|&| and ", m.group(1)):
                tk = tk.strip()
                if tk and tk.isupper() and tk not in ("USDP", "TUSD", "FDUSD", "AEUR"):
                    out.append({"ticker": tk, "kind": kind, "release_ms": ms, "title": t})
        time.sleep(0.5)
    return out


def klines(sym, start, n):
    d = getj("https://api.binance.com/api/v3/klines?symbol=%s&interval=5m&startTime=%d&limit=%d" % (sym, start, n))
    return d if isinstance(d, list) else None


def main():
    rows = []
    for n in notices():
        sym = n["ticker"] + "USDT"
        t0 = n["release_ms"] // 300000 * 300000
        a = klines(sym, t0, 2)
        b = klines(sym, t0 + 86400000, 1)
        c = klines(sym, t0 + 7 * 86400000, 1)
        time.sleep(0.25)
        if not a or not b:
            rows.append({**n, "missing": True})
            continue
        p0, p5, p24 = float(a[0][1]), float(a[0][4]), float(b[0][4])
        p7d = float(c[0][4]) if c else None
        avoided = (p5 - p24) / (p0 - p24) if p24 < p0 else None
        rows.append({**n, "missing": False, "m5_pct": round((p5 / p0 - 1) * 100, 2), "h24_pct": round((p24 / p0 - 1) * 100, 2),
                     "d7_pct": round((p7d / p0 - 1) * 100, 2) if p7d else None,
                     "avoided_share": round(avoided, 3) if avoided is not None else None})
        print(rows[-1]["ticker"], rows[-1]["kind"], rows[-1].get("m5_pct"), rows[-1].get("h24_pct"), rows[-1].get("d7_pct"), rows[-1].get("avoided_share"), flush=True)
    got = [r for r in rows if not r["missing"]]
    summ = {"notices_tickers": len(rows), "priced": len(got), "missing": len(rows) - len(got)}
    for kind in ("delist", "monitoring"):
        g = [r for r in got if r["kind"] == kind]
        if not g:
            continue
        d7 = [r["d7_pct"] for r in g if r["d7_pct"] is not None]
        av = [r["avoided_share"] for r in g if r["avoided_share"] is not None]
        summ[kind] = {"n": len(g), "median_5m_pct": statistics.median(r["m5_pct"] for r in g),
                      "median_24h_pct": statistics.median(r["h24_pct"] for r in g),
                      "median_7d_pct": statistics.median(d7) if d7 else None, "n_7d": len(d7),
                      "fell_by_24h": sum(r["h24_pct"] < 0 for r in g),
                      "median_share_avoided_selling_at_5m": statistics.median(av) if av else None, "n_avoided": len(av)}
    print(summ)
    json.dump({"summary": summ, "rows": rows}, open(OUT + "results.json", "w"), indent=1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""E-001 watcher: Binance delisting notices, detected within two minutes, perp prices snapshotted at once.

Run by launchd every 120 s (label com.proteus.e001, plist beside this file, loaded from here; nothing
written to ~/Library). Writes only append-only files under this folder:

  log/polls.jsonl       one line a poll: time, seconds, new notices, errors
  detections.jsonl      one line a new notice in catalogue 161 (every title, so the record shows what
                        was and was not acted on): detection time, Binance's release time, the lag,
                        kind (delist, monitoring, futures_delist, alpha_remove, other) and tickers
  snapshots.jsonl       one line a ticker a venue, taken in the same poll as the detection: best bid
                        and ask or last price on Binance USDT-M, Bybit, OKX, Gate, Bitget and Hyperliquid,
                        plus whether the Binance perp is live and when it settles
  state.json            the notice codes already seen (the first poll seeds it without acting)

The paper trade itself is not filled here: edges.py score reads detections.jsonl and fills from
1-minute klines at detection + 5 min, so the fill never depends on what this process saw. The
snapshot is the proof of what was quoted at detection. HALT: the poll logs and does nothing else
(no unload; it resumes when HALT goes). Keyless. No git from launchd (the keychain helper blocks
there, 9 Oct 2026); the nightly commits this folder.

Usage: python3 watcher.py [poll|load|unload|status|once]
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "log")
ROOT = "/Users/triton/PROTEUS"
LABEL = "com.proteus.e001"
PLIST = os.path.join(HERE, LABEL + ".plist")
CMS = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&catalogId=161&pageNo=1&pageSize=20"
UA = {"User-Agent": "Mozilla/5.0 (proteus-e001)", "Content-Type": "application/json"}
STABLES = {"USDP", "TUSD", "FDUSD", "AEUR", "USDC", "BUSD", "DAI"}


def now_s():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def jl(name, row):
    os.makedirs(LOG, exist_ok=True)
    path = os.path.join(LOG if name == "polls.jsonl" else HERE, name)
    with open(path, "a") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def get(url, data=None, timeout=15):
    try:
        req = urllib.request.Request(url, headers=UA, data=json.dumps(data).encode() if data is not None else None)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except Exception as e:
        return {"__error": str(e)[:120]}


def state():
    p = os.path.join(HERE, "state.json")
    return json.load(open(p)) if os.path.exists(p) else {"seen": {}}


def save_state(s):
    p = os.path.join(HERE, "state.json")
    json.dump(s, open(p + ".tmp", "w"), sort_keys=True)
    os.replace(p + ".tmp", p)


def classify(title):
    """(kind, tickers). Only delist and monitoring are E-001 events; the rest are recorded."""
    m = re.match(r"Binance Will Delist (.+?) on \d{4}-\d\d-\d\d", title)
    if m:
        return "delist", split(m.group(1))
    m = re.search(r"Monitoring Tag to Include (.+?) on \d{4}", title)
    if m:
        return "monitoring", split(m.group(1))
    if title.startswith("Binance Futures Will Delist"):
        return "futures_delist", [re.sub(r"^1000+", "", s[:-4]) for s in re.findall(r"\b([A-Z0-9]{2,20}USDT)\b", title)]
    if title.startswith("Binance Alpha Will Remove"):
        m = re.match(r"Binance Alpha Will Remove (.+?) \(\d{4}", title)
        return "alpha_remove", split(m.group(1)) if m else []
    return "other", []


def split(s):
    out = []
    for tk in re.split(r",|&| and ", s):
        tk = tk.strip()
        tk = re.sub(r"\s*\(.*\)$", "", tk)
        if tk and tk.isupper() and tk not in STABLES and re.match(r"^[A-Z0-9]{2,12}$", tk):
            out.append(tk)
    return out


# ---------- venue snapshots (keyless) ----------

def snap_binance(t):
    sym = t + "USDT"
    d = get("https://fapi.binance.com/fapi/v1/bookTicker?symbol=" + sym)
    if "bidPrice" not in d:
        return {"venue": "binance_usdtm", "ok": False, "err": d.get("__error") or d.get("msg", "no book")}
    info = get("https://fapi.binance.com/fapi/v1/exchangeInfo?symbol=" + sym)
    s = (info.get("symbols") or [{}])[0] if isinstance(info, dict) else {}
    return {"venue": "binance_usdtm", "ok": True, "bid": float(d["bidPrice"]), "ask": float(d["askPrice"]),
            "status": s.get("status"), "delivery_ms": s.get("deliveryDate")}


def snap_bybit(t):
    d = get("https://api.bybit.com/v5/market/tickers?category=linear&symbol=%sUSDT" % t)
    lst = ((d.get("result") or {}).get("list") or []) if isinstance(d, dict) else []
    if not lst:
        return {"venue": "bybit", "ok": False, "err": d.get("__error") or d.get("retMsg", "no ticker")}
    r = lst[0]
    return {"venue": "bybit", "ok": True, "bid": float(r["bid1Price"]), "ask": float(r["ask1Price"]), "funding": r.get("fundingRate"), "oi_value": r.get("openInterestValue")}


def snap_okx(t):
    d = get("https://www.okx.com/api/v5/market/ticker?instId=%s-USDT-SWAP" % t)
    lst = d.get("data") or [] if isinstance(d, dict) else []
    if not lst:
        return {"venue": "okx", "ok": False, "err": d.get("__error") or d.get("msg", "no ticker")}
    r = lst[0]
    return {"venue": "okx", "ok": True, "bid": float(r["bidPx"]), "ask": float(r["askPx"])}


def snap_gate(t):
    d = get("https://api.gateio.ws/api/v4/futures/usdt/tickers?contract=%s_USDT" % t)
    if not isinstance(d, list) or not d:
        return {"venue": "gate", "ok": False, "err": d.get("__error") or d.get("message", "no ticker") if isinstance(d, dict) else "empty"}
    r = d[0]
    return {"venue": "gate", "ok": True, "last": float(r["last"]), "funding": r.get("funding_rate_indicative")}


def snap_bitget(t):
    d = get("https://api.bitget.com/api/v2/mix/market/ticker?symbol=%sUSDT&productType=USDT-FUTURES" % t)
    lst = d.get("data") or [] if isinstance(d, dict) else []
    if not lst:
        return {"venue": "bitget", "ok": False, "err": d.get("__error") or d.get("msg", "no ticker")}
    r = lst[0]
    return {"venue": "bitget", "ok": True, "bid": float(r["bidPr"]), "ask": float(r["askPr"])}


def snap_hyperliquid(t, mids):
    for name in (t, "k" + t):
        if name in mids:
            return {"venue": "hyperliquid", "ok": True, "mid": float(mids[name]), "name": name}
    return {"venue": "hyperliquid", "ok": False, "err": "not in universe"}


def snapshot(detected_at, code, ticker, mids):
    for fn in (snap_binance, snap_bybit, snap_okx, snap_gate, snap_bitget):
        row = fn(ticker)
        jl("snapshots.jsonl", {"at": detected_at, "code": code, "ticker": ticker, **row})
    jl("snapshots.jsonl", {"at": detected_at, "code": code, "ticker": ticker, **snap_hyperliquid(ticker, mids)})


# ---------- the poll ----------

def poll():
    t0 = time.time()
    if os.path.exists(os.path.join(ROOT, "HALT")):
        jl("polls.jsonl", {"at": now_s(), "halt": True})
        return
    st = state()
    d = get(CMS, timeout=20)
    arts = (((d.get("data") or {}).get("catalogs") or [{}])[0].get("articles")) if isinstance(d, dict) and "__error" not in d else None
    if arts is None:
        jl("polls.jsonl", {"at": now_s(), "secs": round(time.time() - t0, 1), "error": d.get("__error") or "bad reply"})
        return
    first = not st["seen"]
    new, errors = 0, []
    mids = None
    for a in arts:
        code = str(a.get("code"))
        if code in st["seen"]:
            continue
        st["seen"][code] = t0
        if first:
            continue
        new += 1
        detected_at = now_s()
        kind, tickers = classify(a["title"])
        rel = a.get("releaseDate")
        jl("detections.jsonl", {"detected_at": detected_at, "detected_ms": int(t0 * 1000), "release_ms": rel, "lag_s": round(t0 - rel / 1000) if rel else None,
                                "code": code, "title": a["title"], "kind": kind, "tickers": tickers,
                                "event": kind in ("delist", "monitoring")})
        if tickers:
            if mids is None:
                m = get("https://api.hyperliquid.xyz/info", {"type": "allMids"})
                mids = m if isinstance(m, dict) and "__error" not in m else {}
            for tk in tickers:
                try:
                    snapshot(detected_at, code, tk, mids)
                except Exception as e:
                    errors.append("%s: %s" % (tk, str(e)[:80]))
    save_state(st)
    jl("polls.jsonl", {"at": now_s(), "secs": round(time.time() - t0, 1), "new": new, "seeded": first, "errors": errors})


def domain():
    return "gui/%d" % os.getuid()


def load():
    r = subprocess.run(["/bin/launchctl", "bootstrap", domain(), PLIST], capture_output=True, text=True)
    print("bootstrap rc", r.returncode, (r.stdout or r.stderr).strip()[:200])


def unload():
    r = subprocess.run(["/bin/launchctl", "bootout", domain() + "/" + LABEL], capture_output=True, text=True)
    print("bootout rc", r.returncode, (r.stdout or r.stderr).strip()[:200])


def loaded():
    r = subprocess.run(["/bin/launchctl", "list"], capture_output=True, text=True)
    return any(line.strip().endswith(LABEL) for line in r.stdout.splitlines())


def status():
    print("launchd", LABEL, "loaded" if loaded() else "NOT loaded")
    for f in ("log/polls.jsonl", "detections.jsonl", "snapshots.jsonl"):
        p = os.path.join(HERE, f)
        n = sum(1 for _ in open(p)) if os.path.exists(p) else 0
        last = ""
        if n:
            with open(p) as fh:
                for line in fh:
                    last = line
        print("%-18s %5d  last: %s" % (f, n, last.strip()[:160]))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "poll"
    {"poll": poll, "once": poll, "load": load, "unload": unload, "status": status}[cmd]()

#!/usr/bin/env python3
"""The exchange book: my forecasts on Smarkets politics and current-affairs markets, scored against
the exchange's own price. Paper only. Rules and pass marks in exchange/RULES.md.

    exchange.py snapshot                       every open market's best bid, offer and mid -> SNAPSHOTS.csv
    exchange.py markets [--days 180]           callable markets (event within N days), names only, NO prices
    exchange.py call MARKET CONTRACT P "why"   a blind call; commit it before running anchor
    exchange.py anchor                         fill the market's mid for calls committed without one
    exchange.py score                          settle calls whose contract has resolved; Brier v market

Keyless: api.smarkets.com/v3. Prices are in hundredths of a percent (4310 = 43.1 percent).
"""
import csv
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path("/Users/triton/PROTEUS/exchange")
API = "https://api.smarkets.com/v3"
DOMAINS = ["politics", "current_affairs"]
SNAP_FIELDS = ["snap_utc", "event_id", "event", "event_start", "market_id", "market", "contract_id", "contract",
               "bid", "offer", "mid", "state"]
BOOK_FIELDS = ["id", "committed_at", "event", "event_start", "market_id", "market", "contract_id", "contract",
               "p", "reason", "market_mid", "mid_at", "outcome", "brier", "market_brier", "settled_at"]


def get(path):
    for attempt in range(3):
        try:
            r = urllib.request.Request(API + path, headers={"User-Agent": "proteus-exchange/0.1", "Accept": "application/json"})
            with urllib.request.urlopen(r, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    raise RuntimeError("429 three times on " + path)


def events():
    seen = {}
    for dom in DOMAINS:
        path = f"/events/?type_domain={dom}&state=upcoming&state=live&limit=100&sort=id"
        while path:
            try:
                d = get(path)
            except Exception:
                break
            for e in d.get("events", []):
                seen[e["id"]] = e
            nxt = (d.get("pagination") or {}).get("next_page")
            path = ("/events/" + nxt) if nxt else None
    return list(seen.values())


def markets_for(e):
    return get(f"/events/{e['id']}/markets/").get("markets", [])


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def quotes(market_id):
    q = get(f"/markets/{market_id}/quotes/")
    out = {}
    for cid, side in q.items():
        bid = max([b["price"] for b in side.get("bids", [])], default=None)
        offer = min([o["price"] for o in side.get("offers", []) if o["price"] < 9999], default=None)
        mid = (bid + offer) / 2 if bid is not None and offer is not None else None
        out[cid] = (bid, offer, mid)
    return out


def chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def cmd_snapshot(a):
    # Batched: the API takes comma-separated ids, and one call per market drew 429s on 3 Oct.
    rows, ts = [], now()
    evs = {e["id"]: e for e in events()}
    mkts = []
    for ids in chunks(list(evs), 20):
        mkts += get(f"/events/{','.join(ids)}/markets/").get("markets", [])
        time.sleep(1)
    for batch in chunks(mkts, 15):
        ids = ",".join(m["id"] for m in batch)
        cs = get(f"/markets/{ids}/contracts/").get("contracts", [])
        time.sleep(1)
        qs = quotes(ids)
        time.sleep(1)
        by_id = {m["id"]: m for m in batch}
        for c in cs:
            m = by_id.get(c["market_id"])
            e = evs.get(m["event_id"]) if m else None
            if not m or not e:
                continue
            bid, offer, mid = qs.get(c["id"], (None, None, None))
            rows.append({"snap_utc": ts, "event_id": e["id"], "event": e["name"], "event_start": e.get("start_datetime"),
                         "market_id": m["id"], "market": m["name"], "contract_id": c["id"], "contract": c["name"],
                         "bid": bid, "offer": offer, "mid": mid, "state": c.get("state_or_outcome")})
    path = HERE / "SNAPSHOTS.csv"
    new = not path.exists()
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, SNAP_FIELDS)
        if new:
            w.writeheader()
        w.writerows(rows)
    print(f"snapshot {ts}: {len({r['market_id'] for r in rows})} markets, {len(rows)} contracts, "
          f"{sum(r['mid'] is not None for r in rows)} with a two-sided price")


def cmd_markets(a):
    days = 180
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])
    horizon = datetime.now(timezone.utc) + timedelta(days=days)
    evs = {}
    for e in events():
        st = e.get("start_datetime")
        if st and datetime.now(timezone.utc) <= datetime.fromisoformat(st.replace("Z", "+00:00")) <= horizon:
            evs[e["id"]] = e
    mkts = []
    for ids in chunks(list(evs), 20):
        mkts += get(f"/events/{','.join(ids)}/markets/").get("markets", [])
        time.sleep(1)
    for batch in chunks(mkts, 15):
        cs = get(f"/markets/{','.join(m['id'] for m in batch)}/contracts/").get("contracts", [])
        time.sleep(1)
        for m in batch:
            e = evs[m["event_id"]]
            names = ", ".join(f"{c['id']}={c['name']}" for c in cs if c["market_id"] == m["id"] and c.get("state_or_outcome") == "open")
            print(f"{e['start_datetime'][:10]}  market {m['id']}  {e['name']} / {m['name']}\n    {names[:400]}")


def book():
    p = HERE / "BOOK.csv"
    return list(csv.DictReader(open(p))) if p.exists() else []


def save(rows):
    with open(HERE / "BOOK.csv", "w", newline="") as f:
        w = csv.DictWriter(f, BOOK_FIELDS)
        w.writeheader()
        w.writerows(rows)


def cmd_call(a):
    _, market_id, contract_id, p, why = sys.argv[1:6]
    p = float(p)
    assert 0 < p < 1, "p is a probability strictly between 0 and 1"
    rows = book()
    cs = {c["id"]: c for c in get(f"/markets/{market_id}/contracts/").get("contracts", [])}
    assert contract_id in cs, "no such contract in that market"
    assert cs[contract_id].get("state_or_outcome") == "open", "contract is not open"
    m = get(f"/markets/{market_id}/").get("markets", [{}])[0]
    e = get(f"/events/{m.get('event_id')}/").get("events", [{}])[0]
    cid = "X-%04d" % (len(rows) + 1)
    rows.append({"id": cid, "committed_at": now(), "event": e.get("name"), "event_start": e.get("start_datetime"),
                 "market_id": market_id, "market": m.get("name"), "contract_id": contract_id,
                 "contract": cs[contract_id]["name"], "p": p, "reason": why})
    save(rows)
    print(f"{cid}: {cs[contract_id]['name']} in {m.get('name')} at {p:.2f}. Commit now, then run anchor.")


def committed(cid):
    out = subprocess.run(["git", "-C", str(HERE.parent), "log", "--format=%cI", "-S", cid + ",", "--", "exchange/BOOK.csv"],
                         capture_output=True, text=True).stdout.split()
    return out[-1] if out else None


def cmd_anchor(a):
    # One attempt per call. mid_at set with market_mid empty means "no two-sided price at anchor": final, never
    # retried, because a retry the next night reads a later price (and after the event, a post-result one).
    # Until 7 Oct this skipped on market_mid alone, so X-0001/2 were re-anchored nightly past the Quebec vote.
    rows, n = book(), 0
    for r in rows:
        if r.get("market_mid") or r.get("mid_at"):
            continue
        if not committed(r["id"]):
            print(f"{r['id']}: not committed yet; commit the call first")
            continue
        _, _, mid = quotes(r["market_id"]).get(r["contract_id"], (None, None, None))
        r["market_mid"] = "" if mid is None else round(mid / 10000, 4)
        r["mid_at"] = now()
        n += 1
        if mid is None:
            print(f"{r['id']}: no two-sided price, no anchor (final): scored for the record, not against the market")
        else:
            print(f"{r['id']}: market mid {r['market_mid']} against my {r['p']}")
    save(rows)
    print(f"anchored {n}")


def cmd_score(a):
    # Settlement is the contract's state_or_outcome: open, then halted from the event start until Smarkets
    # resolves it to winner or loser (void is dropped). Every anchored call is settled, with or without a mid;
    # market_brier stays empty without one, which keeps it out of me minus market (RULES.md, No anchor).
    rows, n, waiting = book(), 0, []
    for r in rows:
        if r.get("outcome") or not r.get("mid_at"):
            continue
        cs = {c["id"]: c for c in get(f"/markets/{r['market_id']}/contracts/").get("contracts", [])}
        st = (cs.get(r["contract_id"]) or {}).get("state_or_outcome")
        if st in ("winner", "loser"):
            o = 1.0 if st == "winner" else 0.0
            r["outcome"] = st
            r["brier"] = round((float(r["p"]) - o) ** 2, 4)
            r["market_brier"] = round((float(r["market_mid"]) - o) ** 2, 4) if r.get("market_mid") else ""
            r["settled_at"] = now()
            n += 1
        elif st == "void":
            r["outcome"], r["settled_at"] = "void", now()
            n += 1
        else:
            waiting.append(f"{r['id']} {st}")
    save(rows)
    done = [r for r in rows if r.get("brier") and r.get("market_brier")]
    unanchored = sum(1 for r in rows if r.get("brier") and not r.get("market_brier"))
    still = sum(1 for r in rows if not r.get("outcome"))
    print(f"settled {n} tonight; {still} open" + (f" (unresolved: {', '.join(waiting)})" if waiting else ""))
    if done:
        d = sum(float(r["brier"]) - float(r["market_brier"]) for r in done) / len(done)
        print(f"{len(done)} counted, me minus market {d:+.4f} (negative is better); {unanchored} settled without an anchor")
    elif unanchored:
        print(f"none counted yet; {unanchored} settled without an anchor")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    fn = {"snapshot": cmd_snapshot, "markets": cmd_markets, "call": cmd_call, "anchor": cmd_anchor, "score": cmd_score}.get(cmd)
    if not fn:
        print(__doc__)
        sys.exit(2)
    fn(None)


if __name__ == "__main__":
    main()

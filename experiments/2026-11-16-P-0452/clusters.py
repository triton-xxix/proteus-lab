"""P-0452: in the latest full quarter of Form 4 filings (2026 Q3), what is the median 21-trading-day
return minus SPY for open-market purchase clusters of 3 or more insiders?

Called shot (before the run): median excess near zero, between -2% and +2%, with a positive mean
pulled up by a few small caps.

Data, keyless:
- SEC's own quarterly Form 345 data set returns 403 without a contact User-Agent, and I will not
  put Luke's address in one, so the cluster list comes from OpenInsider's screener (purchases
  only, grouped by company, at least 3 insiders, filing dates 1 Jul to 30 Sep 2026), saved as
  sandbox/p0452-oi.html. OpenInsider builds it from the same EDGAR Form 4 filings.
- Daily closes from Yahoo's chart endpoint, entry at the close of the first trading day after the
  filing date (the cluster is public on the filing date), exit 21 trading days later, same days
  for SPY.
"""
import json
import statistics
import sys
import time
import urllib.request
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
# First try (sandbox/p0452-oi.html): the screener with a Q3 date range returned 500 blank rows,
# so this uses OpenInsider's latest-cluster-buys page (100 clusters, filed 16 Sep to 16 Nov 2026).
SRC = Path("/Users/triton/PROTEUS/sandbox/p0452-oi2.html")
UA = {"User-Agent": "Mozilla/5.0"}  # the full browser string drew 429s from Yahoo; the desks' plain one did not


class Table(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.rows, self.row, self.cell, self.in_cell = [], None, "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table" and a.get("class") == "tinytable":
            self.in_table = True
        elif self.in_table and tag == "tr":
            self.row = []
        elif self.in_table and tag in ("td", "th"):
            self.in_cell, self.cell = True, ""

    def handle_endtag(self, tag):
        if tag == "table" and self.in_table:
            self.in_table = False
        elif self.in_table and tag in ("td", "th") and self.row is not None:
            self.row.append(self.cell.strip())
            self.in_cell = False
        elif self.in_table and tag == "tr" and self.row:
            self.rows.append(self.row)
            self.row = None

    def handle_data(self, data):
        if self.in_cell:
            self.cell += data


def parse():
    p = Table()
    p.feed(SRC.read_text("utf-8", "replace"))
    head = [h.replace("\xa0", " ") for h in p.rows[0]]
    out = []
    for r in p.rows[1:]:
        if len(r) != len(head):
            continue
        out.append(dict(zip(head, r)))
    return head, out


def closes(ticker, start, end):
    p1 = int(datetime(start.year, start.month, start.day, tzinfo=timezone.utc).timestamp())
    p2 = int(datetime(end.year, end.month, end.day, tzinfo=timezone.utc).timestamp())
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={p1}&period2={p2}"
           "&interval=1d&events=split")
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                j = json.loads(r.read())
            res = j["chart"]["result"][0]
            ts = res["timestamp"]
            adj = res["indicators"].get("adjclose", [{}])[0].get("adjclose") or res["indicators"]["quote"][0]["close"]
            return [(datetime.fromtimestamp(t, timezone.utc).date(), c) for t, c in zip(ts, adj) if c]
        except Exception as e:
            err = e
            time.sleep(1 + attempt)
    return str(err)


def fwd(series, filed, n=21):
    after = [(d, c) for d, c in series if d > filed]
    if len(after) < n + 1:
        return None
    return after[n][1] / after[0][1] - 1, after[0][0], after[n][0]


def main():
    head, rows = parse()
    print("columns:", head)
    print("rows on the page:", len(rows))
    # 3+ insiders, and filed early enough to have 21 trading days of prices by 13 Nov
    rows = [r for r in rows if r.get("Ins", "0").isdigit() and int(r["Ins"]) >= 3
            and r["Filing Date"][:10] <= "2026-10-14" and r["Trade Type"].startswith("P")]
    print("3+ insider clusters filed by 14 Oct:", len(rows))
    spy = closes("SPY", date(2026, 6, 25), date(2026, 11, 16))
    spy_d = dict(spy)
    results, fails = [], []
    for r in rows:
        tk = r.get("Ticker", "").strip()
        filed = datetime.strptime(r["Filing Date"][:10], "%Y-%m-%d").date()
        s = closes(tk, date(2026, 6, 25), date(2026, 11, 16))
        time.sleep(0.15)
        if isinstance(s, str) or not s:
            fails.append({"ticker": tk, "why": s if isinstance(s, str) else "empty"})
            continue
        f = fwd(s, filed)
        if not f:
            fails.append({"ticker": tk, "why": "under 22 trading days after filing"})
            continue
        ret, d0, d1 = f
        if d0 not in spy_d or d1 not in spy_d:
            fails.append({"ticker": tk, "why": "SPY day missing"})
            continue
        sret = spy_d[d1] / spy_d[d0] - 1
        results.append({"ticker": tk, "filed": str(filed), "insiders": r.get("Ins"), "value": r.get("Value"),
                        "ret": round(ret * 100, 2), "spy": round(sret * 100, 2),
                        "excess": round((ret - sret) * 100, 2)})
    ex = [x["excess"] for x in results]
    out = {"source_rows": len(rows), "scored": len(results), "failed": len(fails),
           "median_excess_pct": round(statistics.median(ex), 2) if ex else None,
           "mean_excess_pct": round(statistics.mean(ex), 2) if ex else None,
           "share_beating_spy": round(sum(e > 0 for e in ex) / len(ex), 3) if ex else None,
           "mean_excess_trimmed_5pct": None, "results": results, "fails": fails}
    if len(ex) >= 20:
        s = sorted(ex)
        k = len(s) // 20
        out["mean_excess_trimmed_5pct"] = round(statistics.mean(s[k:len(s) - k]), 2)
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("results", "fails")}))
    print("fails sample:", fails[:5])


if __name__ == "__main__":
    if "--head" in sys.argv:
        h, rs = parse()
        print(h, len(rs), rs[:2])
    else:
        main()

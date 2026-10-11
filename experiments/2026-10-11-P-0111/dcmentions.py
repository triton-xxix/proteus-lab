"""P-0111: does Korean chatter (DCInside coin gallery, bitcoins_new1) rise before Upbit KRW listings?

Same design as ../2026-10-09-prelisting/xmentions.py, the same nine case/control pairs, a different source.
Called shot before running (11 Oct 2026, 23:55): the source works keyless, but no case/control gap shows,
and the short common tickers (AI, CC, CAP, SUN, BABY) are mostly noise.

DCInside search scans one 10,000-post chunk per request (search_pos). This script:
1. calibrates search_pos against dates by searching a word that appears everywhere and reading the
   newest and oldest timestamps in each chunk, then bisects to the chunk holding a target date;
2. for each coin, walks the chunks covering window A (days -28 to -15) and B (days -14 to -1) and counts
   result rows with a post date inside each window (title+body search, ticker as typed, case-insensitive
   on DCInside's side).
Growth = B / max(A, 1). Writes result.json beside this script. Keyless, 0.4 s between requests, 25 min cap.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
PAIRS = json.load(open(HERE.parent / "2026-10-09-prelisting" / "data" / "xmention_pairs.json"))[:9]
OUT = HERE / "dc-result.json"  # result.json is the first, broken run (search_pos=-0), kept as a record
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"
BASE = "https://gall.dcinside.com/board/lists/?id=bitcoins_new1&s_type=search_subject_memo"
KST = timezone(timedelta(hours=9))
T0 = time.time()
CAP_S = 20 * 60
calls = {"n": 0, "errors": 0}

date_re = re.compile(r'gall_date" title="(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)"')
num_re = re.compile(r'data-no="(\d+)"')


def get(keyword, pos, page=1):
    if time.time() - T0 > CAP_S:
        raise TimeoutError("25 minute cap")
    url = BASE + "&s_keyword=" + urllib.parse.quote(keyword) + "&page=%d" % page
    if pos:  # pos None or 0: the newest chunk, no search_pos (search_pos=-0 broke the first run, 11 Oct)
        url += "&search_pos=-%d" % pos
    calls["n"] += 1
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://gall.dcinside.com/"})
            html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
            time.sleep(0.4)
            # result rows sit inside the list table; the notice rows have no data-no on search pages
            dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S").replace(tzinfo=KST) for d in date_re.findall(html)]
            return dates, html
        except Exception as e:  # noqa: BLE001
            calls["errors"] += 1
            time.sleep(2)
    return [], ""


def chunk_span(pos):
    """newest and oldest post date in the chunk ending at pos, read from a common word."""
    dates, _ = get("코인", pos)
    if not dates:
        return None
    return max(dates), min(dates)


def latest_pos():
    dates, html = get("코인", None)
    m = re.search(r"search_pos=-(\d+)", html)
    if not m:
        raise SystemExit("no search_pos link on the newest chunk")
    return int(m.group(1)) + 10000


def pos_for(target, hi, lo):
    """largest chunk end pos whose oldest date is <= target, by bisection on pos (step 10,000)."""
    spans = {}
    while hi - lo > 10000:
        mid = lo + ((hi - lo) // 20000) * 10000
        s = chunk_span(mid)
        if s is None:
            lo = mid
            continue
        spans[mid] = s
        newest, oldest = s
        if oldest > target:
            hi = mid
        else:
            lo = mid
    return hi


def scan(sym, pos_hi, pos_lo):
    """every result date for sym in the chunks from pos_hi down to pos_lo (both windows in one pass)."""
    out = []
    pos = pos_hi
    pages = 0
    while pos >= pos_lo:
        page = 1
        while True:
            dates, html = get(sym, pos, page)
            pages += 1
            out += dates
            if len(dates) < 50 or page >= 4:
                break
            page += 1
        pos -= 10000
    return out, pages


def interp(anchors, when):
    """chunk pos for a date, piecewise linear between bisected (date, pos) anchors, rounded to 10,000."""
    anchors = sorted(anchors)
    for (d0, p0), (d1, p1) in zip(anchors, anchors[1:]):
        if d0 <= when <= d1:
            f = (when - d0).total_seconds() / max((d1 - d0).total_seconds(), 1)
            return int(round((p0 + f * (p1 - p0)) / 10000.0)) * 10000
    return anchors[0][1] if when < anchors[0][0] else anchors[-1][1]


def main():
    top = latest_pos()
    now = datetime.now(KST)
    print("latest pos", top, flush=True)
    days = [datetime.fromtimestamp(p["t"], timezone.utc).astimezone(KST).replace(hour=0, minute=0, second=0)
            for p in PAIRS]
    anchors = [(now, top)]
    for when in (min(days) - timedelta(days=28), days[len(days) // 2]):
        pos = pos_for(when, top, 0)
        anchors.append((when, pos))
        print("anchor", when.date(), pos, flush=True)
    results = []
    for p, day in zip(PAIRS, days):
        a0, a1 = day - timedelta(days=28), day - timedelta(days=15) + timedelta(hours=23, minutes=59, seconds=59)
        b0, b1 = day - timedelta(days=14), day - timedelta(days=1) + timedelta(hours=23, minutes=59, seconds=59)
        try:
            hi = interp(anchors, b1) + 20000
            lo = max(interp(anchors, a0) - 20000, 10000)
            span_lo = chunk_span(lo)
            span_hi = chunk_span(hi)
            covered = bool(span_lo and span_hi and span_lo[1] <= a0 and span_hi[0] >= b1)
            row = {"case": p["case"], "control": p["control"], "day": str(day.date()),
                   "pos_range": [lo, hi], "chunks": (hi - lo) // 10000 + 1, "windows_covered": covered}
            for role in ("case", "control"):
                sym = p[role]
                dates, pages = scan(sym, hi, lo)
                a = sum(1 for d in dates if a0 <= d <= a1)
                b = sum(1 for d in dates if b0 <= d <= b1)
                row[role] = {"symbol": sym, "a": a, "b": b, "growth": round(b / max(a, 1), 2), "pages": pages}
            results.append(row)
            print(json.dumps(row), flush=True)
        except TimeoutError:
            print("cap reached at", p["case"], flush=True)
            break
        OUT.write_text(json.dumps({"rows": results, "anchors": [[str(d), q] for d, q in anchors], "calls": calls},
                                  indent=1))
    cases = sorted(r["case"]["growth"] for r in results)
    ctrls = sorted(r["control"]["growth"] for r in results)
    med = lambda xs: xs[len(xs) // 2] if xs else None  # noqa: E731
    summary = {"pairs": len(results), "median_case_growth": med(cases), "median_control_growth": med(ctrls),
               "case_grew_more": sum(1 for r in results if r["case"]["growth"] > r["control"]["growth"]),
               "requests": calls["n"], "errors": calls["errors"], "seconds": round(time.time() - T0)}
    OUT.write_text(json.dumps({"rows": results, "summary": summary}, indent=1))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()

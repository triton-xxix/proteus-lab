#!/usr/bin/env python3
"""Run scan.py end to end on synthetic random-walk bars, so the code is checked without reading real windows."""
import sys
from datetime import datetime, timedelta, timezone

import numpy as np

sys.path.insert(0, "/Users/triton/PROTEUS/edges/scan")
import scan  # noqa: E402

g = np.random.default_rng(1)


def fake(kind):
    rows, px = [], 100.0
    today = datetime.now(timezone.utc).date()
    ndays = 60 if kind == "stock" else 35
    for d in range(ndays, -1, -1):
        day = today - timedelta(days=d)
        if kind == "stock" and day.weekday() >= 5:
            continue
        mins = range(570, 960, 5) if kind == "stock" else range(0, 1440, 5)
        for m in mins:
            o = px
            px *= 1 + g.normal(0, 0.002)
            h, l = max(o, px) * 1.0005, min(o, px) * 0.9995
            rows.append((0, day.isoformat(), m, o, h, l, px, float(g.integers(1000, 5000))))
        px *= 1 + g.normal(0, 0.01)  # overnight gap
    return rows


scan.yahoo_5m = lambda s: fake("stock")
scan.binance_5m = lambda s, days=35: fake("crypto")
scan.ROOT = "/Users/triton/PROTEUS/edges/scan/smoke-out"
sys.argv = ["scan.py", "--tag", "synthetic"]
scan.main()

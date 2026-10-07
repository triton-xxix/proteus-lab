"""P-0069: penaltyblog's Dixon-Coles against mine, same matches, same weeks, same decay.

Mine: pitch/model.py (xi 0.0065, L2 0.02 on attack and defence), predictions already in
pitch/backtest/predictions.csv. Theirs: penaltyblog 1.6.2 DixonColesGoalModel, refitted each test
week on every match before it, weighted exp(-0.0065 * days), no shrinkage.
Scope: ENG group (Premier League and Championship fitted jointly), season 2025-26.
"""
import json
import os
import time

import numpy as np
import pandas as pd
import penaltyblog.models as pbm

ROOT = "/Users/triton/PROTEUS/"
CACHE = ROOT + "pitch/cache/"
HERE = os.path.dirname(os.path.abspath(__file__))
XI = 0.0065


def read(path):
    df = pd.read_csv(path, encoding="utf-8-sig", on_bad_lines="skip")
    df = df.dropna(subset=["HomeTeam", "AwayTeam"])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    return df.dropna(subset=["FTHG", "FTAG", "Date"])


files = [f for f in sorted(os.listdir(CACHE)) if f.endswith(".csv") and "-" in f and f.split("-")[0] in ("E0", "E1")]
res = pd.concat([read(CACHE + f) for f in files], ignore_index=True).sort_values("Date")
res["FTHG"] = res["FTHG"].astype(int); res["FTAG"] = res["FTAG"].astype(int)

mine = pd.read_csv(ROOT + "pitch/backtest/predictions.csv")
mine = mine[(mine["model"] == "dc") & (mine["group"] == "ENG") & (mine["season"].astype(str) == "2526")]

rows, t0 = [], time.time()
for wk, g in mine.groupby("week"):
    as_of = pd.Timestamp(wk) - pd.Timedelta(days=1)
    train = res[res["Date"] <= as_of]
    w = np.exp(-XI * (as_of - train["Date"]).dt.days.to_numpy())
    # penaltyblog's Cython loss needs writable arrays; pandas hands it read-only views
    m = pbm.DixonColesGoalModel(
        np.array(train["FTHG"], dtype=np.int64), np.array(train["FTAG"], dtype=np.int64),
        np.array(train["HomeTeam"], dtype=str), np.array(train["AwayTeam"], dtype=str),
        weights=np.array(w, dtype=np.float64))
    m.fit()
    for _, r in g.iterrows():
        try:
            hda = m.predict(r["home"], r["away"], max_goals=10).home_draw_away
        except Exception:
            continue
        rows.append({**r.to_dict(), "pb_h": float(hda[0]), "pb_d": float(hda[1]), "pb_a": float(hda[2])})
fit_seconds = time.time() - t0
df = pd.DataFrame(rows)
df.to_csv(os.path.join(HERE, "paired.csv"), index=False)

y = np.stack([(df.hg > df.ag), (df.hg == df.ag), (df.hg < df.ag)], axis=1).astype(float)
P_mine = df[["ph", "pd", "pa"]].to_numpy()
P_pb = df[["pb_h", "pb_d", "pb_a"]].to_numpy()
close = 1 / df[["AvgCH", "AvgCD", "AvgCA"]].to_numpy()
close = close / close.sum(axis=1, keepdims=True)
ok = ~np.isnan(close).any(axis=1)


def brier(P, m=None):
    m = np.ones(len(P), bool) if m is None else m
    return float(np.mean(np.sum((P[m] - y[m]) ** 2, axis=1)))


def logloss(P, m=None):
    m = np.ones(len(P), bool) if m is None else m
    return float(np.mean(-np.log(np.clip(np.sum(P[m] * y[m], axis=1), 1e-12, None))))


diff = np.abs(P_mine - P_pb)
out = {
    "matches": int(len(df)), "weeks": int(df["week"].nunique()), "fit_seconds": round(fit_seconds, 1),
    "mean_abs_diff": round(float(diff.mean()), 4), "max_abs_diff": round(float(diff.max()), 4),
    "share_over_2_points": round(float((diff.max(axis=1) > 0.02).mean()), 3),
    "brier": {"mine": round(brier(P_mine), 4), "penaltyblog": round(brier(P_pb), 4), "closing": round(brier(close, ok), 4)},
    "logloss": {"mine": round(logloss(P_mine), 4), "penaltyblog": round(logloss(P_pb), 4), "closing": round(logloss(close, ok), 4)},
    "brier_same_rows_as_closing": {"mine": round(brier(P_mine, ok), 4), "penaltyblog": round(brier(P_pb, ok), 4)},
    "mean_draw": {"mine": round(float(P_mine[:, 1].mean()), 4), "penaltyblog": round(float(P_pb[:, 1].mean()), 4),
                  "closing": round(float(close[ok, 1].mean()), 4), "actual": round(float(y[:, 1].mean()), 4)},
}
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print(json.dumps(out, indent=1))

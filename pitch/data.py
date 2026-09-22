#!/usr/bin/env python3
"""The Pitch: data from football-data.co.uk (results, xG, opening and closing odds). No key.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/pitch/data.py --refresh

Downloads E0 (Premier League) and E1 (Championship) for the last three seasons plus fixtures.csv
into pitch/cache/ (gitignored). Exposes load_results() and load_fixtures() for model.py and friends.
"""
import argparse
import io
import os
from datetime import datetime

import pandas as pd
import requests

ROOT = "/Users/triton/PROTEUS/"
CACHE = ROOT + "pitch/cache/"
BASE = "https://www.football-data.co.uk/"
UA = {"User-Agent": "Mozilla/5.0 (proteus-lab)"}
DIVS = ("E0", "E1")


def season_codes(n=3):
    """Current season code plus the previous n-1, e.g. ['2627','2526','2425'] in September 2026."""
    t = datetime.utcnow()
    y = t.year if t.month >= 8 else t.year - 1
    return ["%02d%02d" % (yy % 100, (yy + 1) % 100) for yy in range(y, y - n, -1)]


def fetch(path):
    r = requests.get(BASE + path, headers=UA, timeout=40, allow_redirects=True)
    r.raise_for_status()
    return r.content.decode("utf-8-sig", errors="replace")


def refresh():
    os.makedirs(CACHE, exist_ok=True)
    for code in season_codes():
        for div in DIVS:
            try:
                txt = fetch("mmz4281/%s/%s.csv" % (code, div))
                open(CACHE + "%s-%s.csv" % (div, code), "w").write(txt)
                print("ok", div, code, txt.count("\n"), "rows")
            except Exception as e:
                print("skip", div, code, e)
    txt = fetch("fixtures.csv")
    open(CACHE + "fixtures.csv", "w").write(txt)
    print("ok fixtures", txt.count("\n"), "rows")


def _read(path):
    df = pd.read_csv(path, encoding="utf-8-sig", on_bad_lines="skip")
    df = df.dropna(subset=["HomeTeam", "AwayTeam"])
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    return df


def load_results():
    frames = []
    for f in sorted(os.listdir(CACHE)) if os.path.exists(CACHE) else []:
        if f[:2] in DIVS and f != "fixtures.csv" and f.endswith(".csv"):
            df = _read(CACHE + f)
            df = df.dropna(subset=["FTHG", "FTAG"])
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    df["FTHG"] = df["FTHG"].astype(int); df["FTAG"] = df["FTAG"].astype(int)
    return df.sort_values("Date").reset_index(drop=True)


def load_fixtures():
    p = CACHE + "fixtures.csv"
    if not os.path.exists(p):
        return pd.DataFrame()
    df = _read(p)
    df = df[df["Div"].isin(DIVS)]
    if "Time" in df.columns:
        df["Kickoff"] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Time"].fillna("15:00"), errors="coerce")
    else:
        df["Kickoff"] = df["Date"] + pd.Timedelta(hours=15)
    return df.reset_index(drop=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    if a.refresh:
        refresh()
    else:
        print(load_results().shape, load_fixtures().shape)

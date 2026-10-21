"""Check the Unabated video's claim that the closing line is the truest price, and that this
holds more in liquid leagues: per league, Brier of Pinnacle's opening 1X2 (PSH/PSD/PSA) against
its closing 1X2 (PSCH/PSCD/PSCA), margin removed proportionally, on the 2024-25 and 2025-26
football-data files already cached by the Pitch. Also: how often a bet at the opening price on
the side the close shortened would have won, against the close's own implied chance."""
import csv, os, sys

CACHE = "/Users/triton/PROTEUS/pitch/cache"
LEAGUES = ["E0", "E1", "SP1", "D1", "I1", "F1", "N1", "P1", "SC0"]
SEASONS = ["2425", "2526"]


def probs(row, cols):
    try:
        odds = [float(row[c]) for c in cols]
    except (KeyError, ValueError, TypeError):
        return None
    if min(odds) <= 1.0:
        return None
    inv = [1 / o for o in odds]
    s = sum(inv)
    return [x / s for x in inv]


def brier(p, res):
    idx = {"H": 0, "D": 1, "A": 2}[res]
    return sum((p[i] - (1.0 if i == idx else 0.0)) ** 2 for i in range(3))


print("league  n     brier_open  brier_close  close_better_by  steam_bets  steam_hit  close_implied  open_implied")
tot = [0, 0.0, 0.0]
for lg in LEAGUES:
    n = 0
    bo = bc = 0.0
    steam = hit = 0
    imp_c = imp_o = 0.0
    for se in SEASONS:
        path = os.path.join(CACHE, f"{lg}-{se}.csv")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            for row in csv.DictReader(f):
                res = row.get("FTR")
                if res not in ("H", "D", "A"):
                    continue
                po = probs(row, ["PSH", "PSD", "PSA"])
                pc = probs(row, ["PSCH", "PSCD", "PSCA"])
                if not po or not pc:
                    continue
                n += 1
                bo += brier(po, res)
                bc += brier(pc, res)
                # the side whose chance rose most from open to close: a bet at the open there had CLV
                moves = [pc[i] - po[i] for i in range(3)]
                i = max(range(3), key=lambda k: moves[k])
                if moves[i] >= 0.02:
                    steam += 1
                    imp_c += pc[i]
                    imp_o += po[i]
                    if "HDA"[i] == res:
                        hit += 1
    if n == 0:
        print(lg, "no rows")
        continue
    tot[0] += n; tot[1] += bo; tot[2] += bc
    print(f"{lg:6} {n:5} {bo/n:11.4f} {bc/n:12.4f} {(bo-bc)/n:16.4f} {steam:10} "
          f"{(hit/steam if steam else 0):10.3f} {(imp_c/steam if steam else 0):13.3f} {(imp_o/steam if steam else 0):13.3f}")
n, bo, bc = tot
print(f"ALL    {n:5} {bo/n:11.4f} {bc/n:12.4f} {(bo-bc)/n:16.4f}")

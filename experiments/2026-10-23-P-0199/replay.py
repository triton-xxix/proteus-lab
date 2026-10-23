"""P-0199: replay my Lichess rating through Glicko-2 (Glickman, 'Example of the Glicko-2 system', 2022)
and measure the gap to the rating Lichess printed after each game.

Lichess runs one game per rating period, tau 0.75, RD floor 45 and cap 500, and grows RD with idle time
(0.21436 rating periods per day); those constants are from memory of lila's source, not fetched here.
Opponent RD is not in GAMES.csv, so it is assumed (60, and 45 and 150 as sensitivity).

Two measures:
  chained  - my own rating carried forward from the first row's printed 'before', never corrected.
  one-step - each game starts from Lichess's printed 'before' (my RD and volatility still carried),
             so only that game's delta is tested.
Usage: python3 replay.py GAMES.csv results.json
"""
import csv
import json
import math
import sys
from datetime import datetime

SCALE = 173.7178
TAU = 0.75
EPS = 1e-6
PERIODS_PER_DAY = 0.21436


def g(phi):
    return 1 / math.sqrt(1 + 3 * phi * phi / math.pi ** 2)


def E(mu, mu_j, phi_j):
    return 1 / (1 + math.exp(-g(phi_j) * (mu - mu_j)))


def new_sigma(phi, sigma, v, delta):
    a = math.log(sigma ** 2)

    def f(x):
        ex = math.exp(x)
        return ex * (delta ** 2 - phi ** 2 - v - ex) / (2 * (phi ** 2 + v + ex) ** 2) - (x - a) / TAU ** 2

    A = a
    if delta ** 2 > phi ** 2 + v:
        B = math.log(delta ** 2 - phi ** 2 - v)
    else:
        k = 1
        while f(a - k * TAU) < 0:
            k += 1
        B = a - k * TAU
    fA, fB = f(A), f(B)
    while abs(B - A) > EPS:
        C = A + (A - B) * fA / (fB - fA)
        fC = f(C)
        if fC * fB <= 0:
            A, fA = B, fB
        else:
            fA /= 2
        B, fB = C, fC
    return math.exp(A / 2)


def update(r, rd, sigma, opp_r, opp_rd, score, idle_days):
    mu, phi = (r - 1500) / SCALE, rd / SCALE
    # idle time inflates RD before the game (Lichess; Glickman's step 6 for a player who did not play)
    phi = min(math.sqrt(phi ** 2 + PERIODS_PER_DAY * idle_days * sigma ** 2), 500 / SCALE)
    mu_j, phi_j = (opp_r - 1500) / SCALE, opp_rd / SCALE
    e = E(mu, mu_j, phi_j)
    v = 1 / (g(phi_j) ** 2 * e * (1 - e))
    delta = v * g(phi_j) * (score - e)
    sigma2 = new_sigma(phi, sigma, v, delta)
    phi_star = math.sqrt(phi ** 2 + sigma2 ** 2)
    phi2 = 1 / math.sqrt(1 / phi_star ** 2 + 1 / v)
    mu2 = mu + phi2 ** 2 * g(phi_j) * (score - e)
    rd2 = min(max(phi2 * SCALE, 45), 500)
    return mu2 * SCALE + 1500, rd2, sigma2


def run(rows, opp_rd, start_rd, start_sigma=0.06):
    score_of = {"win": 1.0, "loss": 0.0, "draw": 0.5}
    r_chain, rd, sig = float(rows[0]["my_rating_before"]), start_rd, start_sigma
    last = None
    out = []
    for row in rows:
        t = datetime.strptime(row["finished_utc"], "%Y-%m-%dT%H:%M:%SZ")
        idle = 0 if last is None else (t - last).total_seconds() / 86400
        last = t
        s = score_of[row["result"]]
        before, after = float(row["my_rating_before"]), float(row["my_rating_after"])
        one_r, _, _ = update(before, rd, sig, float(row["opp_rating"]), opp_rd, s, idle)
        r_chain, rd, sig = update(r_chain, rd, sig, float(row["opp_rating"]), opp_rd, s, idle)
        out.append({"game": row["game_id"], "result": row["result"], "opp": int(row["opp_rating"]),
                    "printed_before": before, "printed_after": after, "printed_delta": after - before,
                    "one_step_delta": round(one_r - before, 1), "chained": round(r_chain, 1), "rd": round(rd, 1)})
    return out


def summary(out):
    n = len(out)
    one = sum(abs(o["one_step_delta"] - o["printed_delta"]) for o in out) / n
    chain = sum(abs(o["chained"] - o["printed_after"]) for o in out) / n
    sign_ok = sum(1 for o in out if (o["one_step_delta"] > 0.5) == (o["printed_delta"] > 0.5)) / n
    return {"n": n, "one_step_mae": round(one, 2), "chained_mae": round(chain, 2),
            "final_chained": out[-1]["chained"], "final_printed": out[-1]["printed_after"],
            "sign_agreement": round(sign_ok, 3)}


def main():
    rows = [r for r in csv.DictReader(open(sys.argv[1])) if r.get("result") in ("win", "loss", "draw")]
    breaks = sum(1 for a, b in zip(rows, rows[1:]) if a["my_rating_after"] != b["my_rating_before"])
    res = {"games": len(rows), "chain_breaks_in_csv": breaks, "runs": {}}
    for opp_rd in (45, 60, 150):
        for start_rd in (60, 150, 350, 500):
            key = "opp_rd %d, start_rd %d" % (opp_rd, start_rd)
            out = run(rows, opp_rd, start_rd)
            res["runs"][key] = summary(out)
            if opp_rd == 60 and start_rd == 150:
                res["detail_opp60_start150"] = out
    json.dump(res, open(sys.argv[2], "w"), indent=1)
    print("games %d, places where after != next before: %d" % (len(rows), breaks))
    for k, v in res["runs"].items():
        print(k, v)
    print("worst one-step gaps (opp_rd 60, start_rd 150):")
    d = sorted(res["detail_opp60_start150"], key=lambda o: -abs(o["one_step_delta"] - o["printed_delta"]))
    for o in d[:8]:
        print("  ", o["game"], o["result"], "opp", o["opp"], "before", o["printed_before"],
              "printed d", o["printed_delta"], "mine d", o["one_step_delta"])


if __name__ == "__main__":
    main()

"""P-0455: does an ETAS-style secondary term close the plain Omori fit's under-call of days 2 to 30?

The 13 Nov persona pick (experiments/2026-11-13-persona-omori/) fitted Omori K/(c+t)^p to each
M7+ sequence's first two days and under-called days 2 to 30 on all three (99 v 141, 11.5 v 27,
13.1 v 22). The plain law counts only the mainshock's own aftershocks; every aftershock also has
its own. Here:

- Model O: as on 13 Nov, Omori from the mainshock alone, fitted on days 0.01 to 2.
- Model E: temporal ETAS, rate(t) = sum over earlier events i of K 10^(a (M_i - 4.5)) / (c + t - t_i)^p,
  mainshock included, fitted on days 0.01 to 2 by maximum likelihood (grid over p and a, c fixed
  at 0.01 day, K in closed form). Days 2 to 30 forecast by simulating the cascade forward 400
  times (Gutenberg-Richter b = 1 above M4.5 for new events), from the observed first two days.
- Mainshocks: every M7+ from 1 Apr to 14 Oct 2026 (USGS FDSN, keyless), aftershocks M4.5+
  within the 13 Nov radius for 30 days. Depth recorded for each mainshock.

Called shot (before the run): E forecasts more than O on every sequence and lands nearer the
observed count on at least 4 of the 6 or so sequences with enough early events, but still under.
"""
import json, math, random, urllib.request, urllib.parse, datetime as dt
from pathlib import Path

OUT = Path("/Users/triton/PROTEUS/experiments/2026-11-16-P-0455/")
BASE = "https://earthquake.usgs.gov/fdsnws/event/1/query"
MC, C = 4.5, 0.01
T0, TF, TE = 0.01, 2.0, 30.0


def get(params):
    with urllib.request.urlopen(BASE + "?" + urllib.parse.urlencode(params), timeout=60) as r:
        return json.load(r)


def kint(c, p, a, b):
    """integral of (c+s)^-p for s in [a, b]"""
    if b <= a:
        return 0.0
    if abs(p - 1) < 1e-9:
        return math.log(c + b) - math.log(c + a)
    return ((c + b) ** (1 - p) - (c + a) ** (1 - p)) / (1 - p)


def omori_fit(ts):
    best = None
    for p in [x / 100 for x in range(50, 201, 2)]:
        for c in [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]:
            K = len(ts) / kint(c, p, T0, TF)
            v = K * kint(c, p, T0, TF) - sum(math.log(K) - p * math.log(c + t) for t in ts)
            if best is None or v < best[0]:
                best = (v, K, c, p)
    return best[1:]


def etas_fit(ev, Mm):
    """ev: list of (t, M) aftershocks in (T0, TF]; mainshock at t=0 with magnitude Mm."""
    hist = [(0.0, Mm)] + ev
    best = None
    for a in [0.6, 0.8, 1.0, 1.2]:
        prod = [10 ** (a * (m - MC)) for _, m in hist]
        for p in [x / 100 for x in range(60, 181, 2)]:
            G = sum(pr * kint(C, p, max(T0 - ti, 0.0), TF - ti) for (ti, _), pr in zip(hist, prod) if ti < TF)
            K = len(ev) / G
            s = 0.0
            ok = True
            for j, (tj, _) in enumerate(ev):
                lam = sum(pr * (C + tj - ti) ** (-p) for (ti, _), pr in zip(hist, prod) if ti < tj)
                if lam <= 0:
                    ok = False
                    break
                s += math.log(K * lam)
            if not ok:
                continue
            v = K * G - s
            if best is None or v < best[0]:
                best = (v, K, p, a)
    return best[1:]


def sample_t(p, a, b, rnd):
    u = rnd.random()
    if abs(p - 1) < 1e-9:
        return math.exp(math.log(C + a) + u * (math.log(C + b) - math.log(C + a))) - C
    lo, hi = (C + a) ** (1 - p), (C + b) ** (1 - p)
    return (lo + u * (hi - lo)) ** (1 / (1 - p)) - C


def poisson(lam, rnd):
    if lam > 50:
        return max(0, int(round(rnd.gauss(lam, math.sqrt(lam)))))
    L, k, q = math.exp(-lam), 0, 1.0
    while True:
        q *= rnd.random()
        if q < L:
            return k
        k += 1


def simulate(hist, K, p, a, sims=400, seed=11, cap=5000):
    rnd = random.Random(seed)
    counts, capped = [], 0
    for _ in range(sims):
        queue = [(t, m, TF) for t, m in hist]  # (time, mag, offspring window start)
        n = 0
        while queue:
            ti, mi, start = queue.pop()
            lo = max(start - ti, 0.0)
            lam = K * 10 ** (a * (mi - MC)) * kint(C, p, lo, TE - ti)
            for _ in range(poisson(lam, rnd)):
                t = ti + sample_t(p, lo, TE - ti, rnd)
                m = MC - math.log10(1 - rnd.random())  # GR, b = 1
                n += 1
                queue.append((t, m, t))
            if n > cap:
                capped += 1
                break
        counts.append(n)
    counts.sort()
    return {"mean": round(sum(counts) / sims, 1), "median": counts[sims // 2],
            "p10": counts[sims // 10], "p90": counts[9 * sims // 10], "capped_runs": capped}


def main():
    mains = get({"format": "geojson", "starttime": "2026-04-01", "endtime": "2026-10-14",
                 "minmagnitude": 7.0, "orderby": "time-asc"})["features"]
    rows = []
    for f in mains:
        Mm = f["properties"]["mag"]
        lon, lat, dep = f["geometry"]["coordinates"]
        tms = f["properties"]["time"] / 1000
        t0 = dt.datetime.fromtimestamp(tms, dt.timezone.utc).replace(tzinfo=None)
        R = max(0.02 * 10 ** (0.5 * Mm) * 1.5, 100)
        ev = get({"format": "geojson", "starttime": t0.isoformat(), "endtime": (t0 + dt.timedelta(days=30)).isoformat(),
                  "latitude": lat, "longitude": lon, "maxradiuskm": round(R), "minmagnitude": MC})["features"]
        allev = sorted(((e["properties"]["time"] / 1000 - tms) / 86400, e["properties"]["mag"] or MC) for e in ev)
        allev = [(t, m) for t, m in allev if t > T0]
        early = [(t, m) for t, m in allev if t <= TF]
        late = [(t, m) for t, m in allev if TF < t <= TE]
        row = {"place": f["properties"]["place"], "mag": Mm, "depth_km": round(dep, 1),
               "time": t0.isoformat() + "Z", "n_early": len(early), "seen_day2_30": len(late)}
        if len(early) >= 10:
            Ko, co, po = omori_fit([t for t, _ in early])
            row["omori"] = {"p": round(po, 3), "c": co, "pred_day2_30": round(Ko * kint(co, po, TF, TE), 1)}
            Ke, pe, ae = etas_fit(early, Mm)
            # branching ratio for M>=4.5 offspring, GR b=1, over 30 days
            bexp = 1.0 / (1 - ae) if ae < 1 else float("inf")
            n_br = Ke * kint(C, pe, 0, TE) * (math.log(10) / (math.log(10) * (1 - ae)) if ae < 1 else float("inf"))
            sim = simulate([(0.0, Mm)] + early, Ke, pe, ae)
            row["etas"] = {"K": round(Ke, 4), "p": pe, "alpha": ae, "branching_ratio_30d": round(n_br, 3) if n_br != float("inf") else "inf",
                           "pred_day2_30": sim}
            o_err = abs(row["omori"]["pred_day2_30"] - len(late))
            e_err = abs(sim["mean"] - len(late))
            row["etas_nearer"] = e_err < o_err
        rows.append(row)
        print(json.dumps(row))
    fitted = [r for r in rows if "etas" in r]
    summ = {"mainshocks": len(rows), "fitted": len(fitted),
            "etas_nearer": sum(r["etas_nearer"] for r in fitted),
            "omori_under": sum(r["omori"]["pred_day2_30"] < r["seen_day2_30"] for r in fitted),
            "etas_under": sum(r["etas"]["pred_day2_30"]["mean"] < r["seen_day2_30"] for r in fitted),
            "observed_inside_etas_p10_p90": sum(r["etas"]["pred_day2_30"]["p10"] <= r["seen_day2_30"] <= r["etas"]["pred_day2_30"]["p90"] for r in fitted)}
    print(json.dumps(summ))
    (OUT / "results.json").write_text(json.dumps({"pulled": dt.datetime.now(dt.timezone.utc).isoformat(), "summary": summ, "rows": rows}, indent=1))


if __name__ == "__main__":
    main()

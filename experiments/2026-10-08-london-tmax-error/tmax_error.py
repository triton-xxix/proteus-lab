"""How wrong is a one-day-ahead London max-temperature forecast?

Open-Meteo historical forecast API (keyless) gives the day-ahead daily max as issued;
the ERA5-based archive API gives what happened. Central London, last 90 days to 7 Oct 2026.
Writes result.json beside this file and prints the summary.
"""
import json
import pathlib
import statistics
import urllib.request

HERE = pathlib.Path(__file__).parent
LAT, LON = 51.5072, -0.1276
START, END = "2026-07-09", "2026-10-06"


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def main():
    out = {}
    obs = get(
        "https://archive-api.open-meteo.com/v1/archive?latitude=%s&longitude=%s"
        "&start_date=%s&end_date=%s&daily=temperature_2m_max&timezone=Europe%%2FLondon"
        % (LAT, LON, START, END)
    )["daily"]
    observed = dict(zip(obs["time"], obs["temperature_2m_max"]))
    for model in ["best_match", "ukmo_seamless", "ecmwf_ifs025", "gfs_seamless"]:
        fc = get(
            "https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s"
            "&start_date=%s&end_date=%s&daily=temperature_2m_max&timezone=Europe%%2FLondon&models=%s"
            % (LAT, LON, START, END, model)
        )["daily"]
        key = [k for k in fc if k.startswith("temperature_2m_max")][0]
        errs = []
        for day, f in zip(fc["time"], fc[key]):
            o = observed.get(day)
            if f is None or o is None:
                continue
            errs.append(round(f - o, 2))
        if not errs:
            continue
        absd = [abs(e) for e in errs]
        same_bucket = sum(1 for d, f in zip(fc["time"], fc[key])
                          if f is not None and observed.get(d) is not None
                          and round(f) == round(observed[d]))
        out[model] = {
            "n": len(errs),
            "bias": round(statistics.mean(errs), 2),
            "mae": round(statistics.mean(absd), 2),
            "sd": round(statistics.pstdev(errs), 2),
            "within_0_5": round(sum(a <= 0.5 for a in absd) / len(absd), 3),
            "within_1": round(sum(a <= 1.0 for a in absd) / len(absd), 3),
            "same_whole_degree": round(same_bucket / len(errs), 3),
        }
        print(model, out[model])
    (HERE / "result.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

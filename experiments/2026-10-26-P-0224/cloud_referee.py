"""P-0224: Lichess cloud eval as referee for P-0214's 32 positions.

Question: how many of the 32 positions does lichess.org/api/cloud-eval cover, and on the covered
ones does P-0214's plain-v-quiescence ranking (mean move cost 75 v 61 cp, blunders 4 v 3) hold with
cloud evals in place of local Stockfish 19 depth 14?

Method: one keyless GET per position with multiPv=5, one at a time, 1.5 s apart (Lichess asks for
one request at a time). A position is covered on HTTP 200. Each engine's move is costed against the
cloud's best line only when the move is among the cloud's five lines; otherwise it is "outside top 5"
and counted separately, never guessed. Mates map to +-10000.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = "/Users/triton/PROTEUS"
SRC = ROOT + "/experiments/2026-10-24-P-0214/results.json"
OUT = ROOT + "/experiments/2026-10-26-P-0224"


def cp_of(pv):
    if "mate" in pv:
        return 10000 if pv["mate"] > 0 else -10000
    return pv["cp"]


def cloud(fen):
    url = "https://lichess.org/api/cloud-eval?" + urllib.parse.urlencode({"fen": fen, "multiPv": 5})
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None


def main():
    src = json.load(open(SRC))
    rows = []
    for row in src["rows"]:
        status, data = cloud(row["fen"])
        if status == 429:
            time.sleep(65)
            status, data = cloud(row["fen"])
        out = {"ply": row["ply"], "fen": row["fen"], "http": status, "sf_move": row["sf_move"],
               "sf_cp": row["sf_cp"]}
        if status == 200 and data and data.get("pvs"):
            lines = {pv["moves"].split()[0]: cp_of(pv) for pv in data["pvs"]}
            best_move = data["pvs"][0]["moves"].split()[0]
            best_cp = cp_of(data["pvs"][0])
            out.update({"depth": data["depth"], "lines": len(lines), "cloud_move": best_move,
                        "cloud_cp": best_cp, "agrees_with_sf14": best_move == row["sf_move"]})
            for name in ("plain", "quiescence"):
                m = row[name]["move"]
                out[name] = {"move": m, "agree": m == best_move,
                             "cost_cp": best_cp - lines[m] if m in lines else None,
                             "sf14_cost_cp": row[name]["cost_cp"]}
        rows.append(out)
        print(row["ply"], status, out.get("depth"), out.get("cloud_move"), out.get("cloud_cp"),
              out.get("plain", {}).get("cost_cp"), out.get("quiescence", {}).get("cost_cp"))
        time.sleep(1.5)

    covered = [r for r in rows if r["http"] == 200 and "cloud_move" in r]
    summary = {"positions": len(rows), "covered": len(covered),
               "covered_by_ply": {str(p): sum(1 for r in covered if r["ply"] == p) for p in src["plies"]},
               "cloud_best_equals_sf14_best": sum(r["agrees_with_sf14"] for r in covered),
               "median_cloud_depth": sorted(r["depth"] for r in covered)[len(covered) // 2] if covered else None}
    for name in ("plain", "quiescence"):
        costed = [r[name]["cost_cp"] for r in covered if r[name]["cost_cp"] is not None]
        sf14 = [r[name]["sf14_cost_cp"] for r in covered if r[name]["cost_cp"] is not None]
        summary[name] = {
            "agree_with_cloud": sum(r[name]["agree"] for r in covered),
            "costed": len(costed),
            "outside_top5": sum(r[name]["cost_cp"] is None for r in covered),
            "mean_cost_cloud_cp": round(sum(costed) / len(costed), 1) if costed else None,
            "mean_cost_sf14_same_positions_cp": round(sum(sf14) / len(sf14), 1) if sf14 else None,
            "blunders_over_200_cloud": sum(c > 200 for c in costed),
        }
    print(json.dumps(summary, indent=2))
    json.dump({"summary": summary, "rows": rows}, open(OUT + "/results.json", "w"), indent=1)


if __name__ == "__main__":
    main()

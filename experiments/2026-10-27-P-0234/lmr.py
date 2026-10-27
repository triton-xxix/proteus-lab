#!/usr/bin/env python3
"""P-0234: late move reductions in P-0214's toy engine.

The Chess Programming Wiki (Late Move Reductions) says LMR "can often reduce the effective branching
factor to less than 2". This takes P-0214's engine unchanged (material plus PST, MVV-LVA ordering,
capture-only quiescence) and adds the textbook LMR: the first two moves at full depth; after that, a
quiet move (no capture, no promotion, not giving check, side to move not in check) at remaining depth 3
or more is searched one ply shallower with a null window, and re-searched at full depth if it beats
alpha. Same 32 frozen positions from P-0214's results.json, depth 3 and 4, Stockfish 19 depth 14 as
referee for the move each engine picks at depth 4.

Effective branching factor here is nodes(depth 4) / nodes(depth 3), quiescence nodes included.
"""
import importlib.util
import json
import sys
import time

import chess
import chess.engine

ROOT = "/Users/triton/PROTEUS"
P14 = ROOT + "/experiments/2026-10-24-P-0214/"
OUT = ROOT + "/experiments/2026-10-27-P-0234"
sys.argv = sys.argv[:1]   # quiescence.py reads argv[1] as its game count at import
spec = importlib.util.spec_from_file_location("q14", P14 + "quiescence.py")
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)
SF_DEPTH = 14


class LMREngine(q.Engine):
    def __init__(self):
        super().__init__(True)
        self.reduced = 0
        self.researched = 0

    def negamax(self, board, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            if not board.is_game_over():
                return self.quiesce(board, alpha, beta)
            self.nodes += 1
            return q.evaluate(board)
        best = -1000000
        in_check = board.is_check()
        for i, m in enumerate(q.ordered(board)):
            quiet = not (board.is_capture(m) or m.promotion or board.gives_check(m) or in_check)
            board.push(m)
            if i >= 2 and depth >= 3 and quiet:
                self.reduced += 1
                score = -self.negamax(board, depth - 2, -alpha - 1, -alpha)
                if score > alpha:
                    self.researched += 1
                    score = -self.negamax(board, depth - 1, -beta, -alpha)
            else:
                score = -self.negamax(board, depth - 1, -beta, -alpha)
            board.pop()
            if score > best:
                best = score
            if score > alpha:
                alpha = score
            if alpha >= beta:
                break
        return best


def main():
    frozen = json.load(open(P14 + "results.json"))["rows"]
    sf = chess.engine.SimpleEngine.popen_uci(q.SF)
    rows = []
    for p in frozen:
        board = chess.Board(p["fen"])
        info = sf.analyse(board, chess.engine.Limit(depth=SF_DEPTH))
        ref_move = info["pv"][0]
        ref_cp = info["score"].pov(board.turn).score(mate_score=100000)
        row = {"game": p["game"], "ply": p["ply"], "fen": p["fen"], "sf_move": ref_move.uci(), "sf_cp": ref_cp}
        for name, make in (("base", lambda: q.Engine(True)), ("lmr", LMREngine)):
            eng = make()
            _, _, n3 = eng.search(board, 3)
            t0 = time.time()
            mv, score, n4 = eng.search(board, 4)
            secs = round(time.time() - t0, 2)
            board.push(mv)
            after = sf.analyse(board, chess.engine.Limit(depth=SF_DEPTH - 1))
            board.pop()
            after_cp = after["score"].pov(board.turn).score(mate_score=100000)
            row[name] = {"move": mv.uci(), "cp": score, "nodes_d3": n3, "nodes_d4": n4, "secs_d4": secs,
                         "ebf": round(n4 / n3, 2) if n3 else None, "agree": mv == ref_move,
                         "cost_cp": ref_cp - after_cp}
            if name == "lmr":
                row[name]["reduced"], row[name]["researched"] = eng.reduced, eng.researched
        rows.append(row)
        print(p["game"], p["ply"], "sf", row["sf_move"],
              "| base", row["base"]["move"], row["base"]["nodes_d4"], "cost", row["base"]["cost_cp"],
              "| lmr", row["lmr"]["move"], row["lmr"]["nodes_d4"], "cost", row["lmr"]["cost_cp"], flush=True)
    sf.quit()
    n = len(rows)
    summary = {}
    for name in ("base", "lmr"):
        tot3 = sum(r[name]["nodes_d3"] for r in rows)
        tot4 = sum(r[name]["nodes_d4"] for r in rows)
        summary[name] = {"positions": n, "agree": sum(r[name]["agree"] for r in rows),
                         "mean_cost_cp": round(sum(r[name]["cost_cp"] for r in rows) / n, 1),
                         "blunders_over_200cp": sum(r[name]["cost_cp"] > 200 for r in rows),
                         "mean_nodes_d4": round(tot4 / n), "mean_secs_d4": round(sum(r[name]["secs_d4"] for r in rows) / n, 2),
                         "ebf_pooled": round(tot4 / tot3, 2),
                         "ebf_median": sorted(r[name]["ebf"] for r in rows)[n // 2]}
    summary["node_saving_pct"] = round(100 * (1 - summary["lmr"]["mean_nodes_d4"] / summary["base"]["mean_nodes_d4"]), 1)
    summary["same_move"] = sum(r["base"]["move"] == r["lmr"]["move"] for r in rows)
    summary["lmr_reduced"] = sum(r["lmr"]["reduced"] for r in rows)
    summary["lmr_researched"] = sum(r["lmr"]["researched"] for r in rows)
    print(json.dumps(summary, indent=1))
    json.dump({"summary": summary, "rows": rows}, open(OUT + "/results.json", "w"), indent=1)


if __name__ == "__main__":
    main()

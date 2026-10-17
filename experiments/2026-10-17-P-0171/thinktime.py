"""P-0171: what does think time buy the Lichess bot on its own positions?

One position per saved game (after ply 30, side to move), up to N games. For each position the bot's
engine (same binary and default options as bin/lichess.py) plays at 0.3, 1.0 and 3.0 s with a fresh
hash. Every distinct candidate move, and the engine's own best, is then scored by a depth-limited
search restricted to that move (root_moves), so all moves are judged by the same yardstick.
Centipawn loss = best score minus the move's score, floored at 0, capped at 1000.
Writes results.json beside this script.
"""
import json, statistics, sys, math
from pathlib import Path

import chess, chess.engine, chess.pgn

ENGINE = "/Users/triton/PROTEUS/sandbox/stockfish/stockfish/stockfish-macos-universal"
PGN = Path("/Users/triton/PROTEUS/games/lichess/pgn")
OUT = Path(__file__).resolve().parent / "results.json"
ARMS = [0.3, 1.0, 3.0]
PLY = 30
DEPTH = 20
N = int(sys.argv[1]) if len(sys.argv) > 1 else 24


def cp(info, board):
    return max(-10000, min(10000, info["score"].pov(board.turn).score(mate_score=10000)))


def positions():
    out = []
    for f in sorted(PGN.glob("*.pgn")):
        g = chess.pgn.read_game(f.open())
        if g is None:
            continue
        b = g.board()
        moves = list(g.mainline_moves())
        if len(moves) <= PLY + 1:
            continue
        for m in moves[:PLY]:
            b.push(m)
        out.append((f.stem, b.fen()))
    return out[:N]


def main():
    eng = chess.engine.SimpleEngine.popen_uci(ENGINE)
    rows = []
    for gid, fen in positions():
        board = chess.Board(fen)
        picks = {}
        for t in ARMS:
            eng.configure({"Clear Hash": None})
            picks[t] = eng.play(board, chess.engine.Limit(time=t)).move
        eng.configure({"Clear Hash": None})
        ref = eng.analyse(board, chess.engine.Limit(depth=DEPTH))
        best, best_cp = ref["pv"][0], cp(ref, board)
        scored = {best: best_cp}
        for mv in set(picks.values()):
            if mv not in scored:
                eng.configure({"Clear Hash": None})
                info = eng.analyse(board, chess.engine.Limit(depth=DEPTH), root_moves=[mv])
                scored[mv] = cp(info, board)
        top = max(scored.values())
        row = {"game": gid, "fen": fen, "ref_best": best.uci(), "ref_cp": best_cp}
        for t in ARMS:
            row[f"move_{t}"] = picks[t].uci()
            row[f"loss_{t}"] = min(1000, max(0, top - scored[picks[t]]))
            row[f"agree_{t}"] = picks[t] == best
        rows.append(row)
        print(gid, {t: (row[f"move_{t}"], row[f"loss_{t}"]) for t in ARMS}, "ref", best.uci(), flush=True)
    eng.quit()

    summary = {}
    for t in ARMS:
        losses = [r[f"loss_{t}"] for r in rows]
        summary[str(t)] = {
            "mean_cp_loss": round(statistics.fmean(losses), 2),
            "se": round(statistics.stdev(losses) / math.sqrt(len(losses)), 2),
            "median_cp_loss": statistics.median(losses),
            "agree_with_ref": sum(r[f"agree_{t}"] for r in rows),
            "moves_over_50cp": sum(l > 50 for l in losses),
        }
    d = [r["loss_0.3"] - r["loss_1.0"] for r in rows]
    summary["paired_0.3_minus_1.0"] = {"mean": round(statistics.fmean(d), 2),
                                       "se": round(statistics.stdev(d) / math.sqrt(len(d)), 2)}
    res = {"positions": len(rows), "ply": PLY, "score_depth": DEPTH, "summary": summary, "rows": rows}
    OUT.write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

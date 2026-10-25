#!/usr/bin/env python3
"""Tapered evaluation in P-0214's toy engine, on P-0214's own 32 frozen positions.

CPW "Tapered Eval": score = (opening * (256 - phase) + endgame * phase) / 256, phase from the
non-pawn material left (knight and bishop 1, rook 2, queen 4, total 24). Here only the king table
tapers (CPW Simplified Evaluation's middlegame and endgame king tables), plus a passed-pawn bonus by
rank that also grows with the phase. Search is unchanged: depth 3 with quiescence, as P-0214.
Positions come from P-0214's results.json (its last-8-games window has moved since, F-0053), so the
baseline is re-run here on the same FENs with the same Stockfish settings.
"""
import importlib.util, json, sys, time
import chess, chess.engine

P14 = "/Users/triton/PROTEUS/experiments/2026-10-24-P-0214/"
OUT = sys.argv[1]
sys.argv = sys.argv[:1]   # quiescence.py reads argv[1] as its game count at import
spec = importlib.util.spec_from_file_location("q14", P14 + "quiescence.py")
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)

KING_EG = [-50, -40, -30, -20, -20, -30, -40, -50, -30, -20, -10, 0, 0, -10, -20, -30, -30, -10, 20, 30, 30, 20, -10, -30,
           -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 20, 30, 30, 20, -10, -30,
           -30, -30, 0, 0, 0, 0, -30, -30, -50, -30, -30, -30, -30, -30, -30, -50]
KING_MG = q.PST[chess.KING]
PASSED = [0, 10, 15, 25, 40, 60, 90, 0]   # by rank advanced from the pawn's own side, rank 2 to 7
PH = {chess.KNIGHT: 1, chess.BISHOP: 1, chess.ROOK: 2, chess.QUEEN: 4}


def passed(board, sq, color):
    f, r = chess.square_file(sq), chess.square_rank(sq)
    for ff in (f - 1, f, f + 1):
        if 0 <= ff < 8:
            for rr in (range(r + 1, 8) if color == chess.WHITE else range(0, r)):
                p = board.piece_at(chess.square(ff, rr))
                if p and p.piece_type == chess.PAWN and p.color != color:
                    return False
    return True


def evaluate_tapered(board):
    if board.is_checkmate():
        return -100000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    pm = board.piece_map()
    left = sum(PH.get(p.piece_type, 0) for p in pm.values())
    phase = (max(0, 24 - left) * 256 + 12) // 24   # 0 at the start, 256 with no pieces left
    score = 0
    for sq, piece in pm.items():
        idx = sq ^ 56 if piece.color == chess.WHITE else sq
        if piece.piece_type == chess.KING:
            v = (KING_MG[idx] * (256 - phase) + KING_EG[idx] * phase) // 256
        else:
            v = q.VAL[piece.piece_type] + q.PST[piece.piece_type][idx]
            if piece.piece_type == chess.PAWN and passed(board, sq, piece.color):
                adv = chess.square_rank(sq) if piece.color == chess.WHITE else 7 - chess.square_rank(sq)
                b = PASSED[adv]
                v += (b * (128 + phase)) // 256   # half weight in the middlegame, up to 1.5x in the endgame
        score += v if piece.color == chess.WHITE else -v
    return score if board.turn == chess.WHITE else -score


def run(evalf, label, rows, sf):
    q.evaluate = evalf   # Engine looks evaluate up in its module at call time
    eng = q.Engine(True)
    out = []
    for p in rows:
        board = chess.Board(p["fen"])
        ref_move, ref_cp = chess.Move.from_uci(p["sf_move_now"]), p["sf_cp_now"]
        t0 = time.time()
        mv, score, nodes = eng.search(board, q.DEPTH)
        board.push(mv)
        after = sf.analyse(board, chess.engine.Limit(depth=q.SF_DEPTH - 1))
        cp_after = after["score"].pov(not board.turn).score(mate_score=100000)
        board.pop()
        out.append({"move": mv.uci(), "cp": score, "nodes": nodes, "secs": round(time.time() - t0, 2),
                    "agree": mv == ref_move, "abs_err": abs(score - ref_cp), "cost_cp": ref_cp - cp_after})
    n = len(out)
    s = {"agree": sum(r["agree"] for r in out), "mean_cost_cp": round(sum(r["cost_cp"] for r in out) / n, 1),
         "blunders_over_200": sum(r["cost_cp"] > 200 for r in out),
         "mean_abs_eval_err": round(sum(r["abs_err"] for r in out) / n, 1),
         "median_abs_eval_err": sorted(r["abs_err"] for r in out)[n // 2],
         "mean_nodes": round(sum(r["nodes"] for r in out) / n), "mean_secs": round(sum(r["secs"] for r in out) / n, 2)}
    print(label, s)
    return s, out


src = json.load(open(P14 + "results.json"))["rows"]
sf = chess.engine.SimpleEngine.popen_uci(q.SF)
rows = []
for r in src:
    board = chess.Board(r["fen"])
    info = sf.analyse(board, chess.engine.Limit(depth=q.SF_DEPTH))
    rows.append({"fen": r["fen"], "game": r["game"], "ply": r["ply"], "sf_move_now": info["pv"][0].uci(),
                 "sf_cp_now": info["score"].pov(board.turn).score(mate_score=100000)})
base_eval = q.evaluate
s_base, o_base = run(base_eval, "baseline", rows, sf)
s_tap, o_tap = run(evaluate_tapered, "tapered", rows, sf)
sf.quit()
cheaper = sum(t["cost_cp"] < b["cost_cp"] for t, b in zip(o_tap, o_base))
dearer = sum(t["cost_cp"] > b["cost_cp"] for t, b in zip(o_tap, o_base))
same_move = sum(t["move"] == b["move"] for t, b in zip(o_tap, o_base))
res = {"positions": len(rows), "baseline": s_base, "tapered": s_tap,
       "paired": {"tapered_cheaper": cheaper, "tapered_dearer": dearer, "same_move": same_move},
       "rows": [dict(r, baseline=b, tapered=t) for r, b, t in zip(rows, o_base, o_tap)]}
json.dump(res, open(OUT + "/results.json", "w"), indent=1)
print("paired", res["paired"])

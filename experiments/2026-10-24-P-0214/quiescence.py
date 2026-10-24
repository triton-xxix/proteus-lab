#!/usr/bin/env python3
"""Lague's quiescence search, measured against Stockfish on positions from my own Lichess games.

Sebastian Lague's "Coding Adventure: Chess" (transcript at 16:33): "our evaluation function is only
going to be remotely reliable if no piece can be captured on the next move, so in our search
function instead of just evaluating once the depth is reached we can start a new search that looks
only at captures and just keeps going until no captures are left." That is quiescence search. This
script builds the same toy engine twice, the same evaluation (material plus piece-square tables) and
the same MVV-LVA move ordering he describes at 14:56, once with that capture search at the leaves
and once without, and asks Stockfish to referee.

Positions: the latest N finished games in games/lichess/GAMES.csv, PGN fetched keyless from
lichess.org/game/export, positions at plies 16, 24, 32 and 40 (middlegame, not the book).
For each position and each engine: best move and eval at depth 3 (plies). Stockfish at depth 14
gives the reference move and centipawn eval, and re-evaluates each engine's chosen move so a
disagreement has a cost in centipawns. Metrics: agreement with Stockfish's move, mean absolute
eval error, mean move cost, blunders over 200 cp, nodes searched.
"""
import csv
import json
import os
import sys
import time
import urllib.request

import chess
import chess.engine
import chess.pgn
import io

ROOT = "/Users/triton/PROTEUS"
OUT = os.path.dirname(os.path.abspath(__file__))
SF = ROOT + "/sandbox/stockfish/stockfish/stockfish-macos-universal"
GAMES = ROOT + "/games/lichess/GAMES.csv"
N_GAMES = int(sys.argv[1]) if len(sys.argv) > 1 else 8
PLIES = (16, 24, 32, 40)
DEPTH = 3
SF_DEPTH = 14

VAL = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}
# Piece-square tables from the Chess Programming Wiki "Simplified Evaluation Function", white's view, a8 first.
PST = {
    chess.PAWN: [0, 0, 0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5, 5, 10, 25, 25, 10, 5, 5,
                 0, 0, 0, 20, 20, 0, 0, 0, 5, -5, -10, 0, 0, -10, -5, 5, 5, 10, 10, -20, -20, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0],
    chess.KNIGHT: [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 0, 0, 0, -20, -40, -30, 0, 10, 15, 15, 10, 0, -30, -30, 5, 15, 20, 20, 15, 5, -30,
                   -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 10, 15, 15, 10, 5, -30, -40, -20, 0, 5, 5, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50],
    chess.BISHOP: [-20, -10, -10, -10, -10, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 0, 5, 10, 10, 5, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10,
                   -10, 0, 10, 10, 10, 10, 0, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10, 5, 0, 0, 0, 0, 5, -10, -20, -10, -10, -10, -10, -10, -10, -20],
    chess.ROOK: [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, 10, 10, 10, 10, 5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5,
                 -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 0, 0, 0, 5, 5, 0, 0, 0],
    chess.QUEEN: [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0, -10, -10, 0, 5, 5, 5, 5, 0, -10, -5, 0, 5, 5, 5, 5, 0, -5,
                  0, 0, 5, 5, 5, 5, 0, -5, -10, 5, 5, 5, 5, 5, 0, -10, -10, 0, 5, 0, 0, 0, 0, -10, -20, -10, -10, -5, -5, -10, -10, -20],
    chess.KING: [-30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30,
                 -20, -30, -30, -40, -40, -30, -30, -20, -10, -20, -20, -20, -20, -20, -20, -10, 20, 20, 0, 0, 0, 0, 20, 20, 20, 30, 10, 0, 0, 10, 30, 20],
}


def evaluate(board):
    """Centipawns from the side to move's view."""
    if board.is_checkmate():
        return -100000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    score = 0
    for sq, piece in board.piece_map().items():
        v = VAL[piece.piece_type]
        idx = sq ^ 56 if piece.color == chess.WHITE else sq   # tables are written a8 first
        v += PST[piece.piece_type][idx]
        score += v if piece.color == chess.WHITE else -v
    return score if board.turn == chess.WHITE else -score


def ordered(board, captures_only=False):
    moves = [m for m in board.legal_moves if (board.is_capture(m) or not captures_only)]

    def key(m):
        if board.is_capture(m):
            victim = board.piece_type_at(m.to_square) or chess.PAWN   # en passant
            attacker = board.piece_type_at(m.from_square)
            return 10 * VAL[victim] - VAL[attacker]
        return -1
    moves.sort(key=key, reverse=True)
    return moves


class Engine:
    def __init__(self, quiescence):
        self.q = quiescence
        self.nodes = 0

    def quiesce(self, board, alpha, beta):
        self.nodes += 1
        stand = evaluate(board)
        if stand >= beta:
            return beta
        if stand > alpha:
            alpha = stand
        for m in ordered(board, captures_only=True):
            board.push(m)
            score = -self.quiesce(board, -beta, -alpha)
            board.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha

    def negamax(self, board, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            if self.q and not board.is_game_over():
                return self.quiesce(board, alpha, beta)
            self.nodes += 1
            return evaluate(board)
        best = -1000000
        for m in ordered(board):
            board.push(m)
            score = -self.negamax(board, depth - 1, -beta, -alpha)
            board.pop()
            if score > best:
                best = score
            if score > alpha:
                alpha = score
            if alpha >= beta:
                break
        return best

    def search(self, board, depth):
        self.nodes = 0
        best_move, best = None, -1000000
        alpha, beta = -1000000, 1000000
        for m in ordered(board):
            board.push(m)
            score = -self.negamax(board, depth - 1, -beta, -alpha)
            board.pop()
            if score > best:
                best, best_move = score, m
            if score > alpha:
                alpha = score
        return best_move, best, self.nodes


def fetch_pgn(game_id):
    url = "https://lichess.org/game/export/%s?moves=true&clocks=false&evals=false&opening=false" % game_id
    req = urllib.request.Request(url, headers={"Accept": "application/x-chess-pgn", "User-Agent": "proteus-nightly"})
    return urllib.request.urlopen(req, timeout=30).read().decode()


def positions():
    rows = list(csv.DictReader(open(GAMES)))
    rows = [r for r in rows if r.get("game_id")][-N_GAMES:]
    out = []
    for r in rows:
        try:
            pgn = fetch_pgn(r["game_id"])
        except Exception as e:
            print("fetch failed", r["game_id"], e)
            continue
        game = chess.pgn.read_game(io.StringIO(pgn))
        if game is None:
            continue
        board = game.board()
        for i, mv in enumerate(game.mainline_moves(), start=1):
            board.push(mv)
            if i in PLIES and not board.is_game_over():
                out.append({"game": r["game_id"], "opponent": r["opponent"], "ply": i, "fen": board.fen()})
        time.sleep(0.5)
    return out


def main():
    pos = positions()
    print("positions", len(pos))
    sf = chess.engine.SimpleEngine.popen_uci(SF)
    plain, quiet = Engine(False), Engine(True)
    rows = []
    for p in pos:
        board = chess.Board(p["fen"])
        info = sf.analyse(board, chess.engine.Limit(depth=SF_DEPTH))
        ref_move = info["pv"][0]
        ref_cp = info["score"].pov(board.turn).score(mate_score=100000)
        row = dict(p)
        row["sf_move"] = ref_move.uci()
        row["sf_cp"] = ref_cp
        for name, eng in (("plain", plain), ("quiescence", quiet)):
            t0 = time.time()
            mv, score, nodes = eng.search(board, DEPTH)
            row[name] = {"move": mv.uci(), "cp": score, "nodes": nodes, "secs": round(time.time() - t0, 2),
                         "agree": mv == ref_move, "abs_err": abs(score - ref_cp)}
            # Stockfish's view of the move each engine chose, so a disagreement has a cost in centipawns.
            board.push(mv)
            after = sf.analyse(board, chess.engine.Limit(depth=SF_DEPTH - 1))
            row[name]["sf_cp_after_move"] = after["score"].pov(not board.turn).score(mate_score=100000)
            board.pop()
            row[name]["cost_cp"] = ref_cp - row[name]["sf_cp_after_move"]
        rows.append(row)
        print(p["game"], p["ply"], "sf", row["sf_move"], ref_cp,
              "| plain", row["plain"]["move"], row["plain"]["cp"], row["plain"]["nodes"], "cost", row["plain"]["cost_cp"],
              "| quiet", row["quiescence"]["move"], row["quiescence"]["cp"], row["quiescence"]["nodes"], "cost", row["quiescence"]["cost_cp"])
    sf.quit()
    summary = {}
    for name in ("plain", "quiescence"):
        n = len(rows)
        summary[name] = {
            "positions": n,
            "agree_with_stockfish": sum(r[name]["agree"] for r in rows),
            "agree_pct": round(100.0 * sum(r[name]["agree"] for r in rows) / n, 1) if n else None,
            "mean_abs_eval_err_cp": round(sum(r[name]["abs_err"] for r in rows) / n, 1) if n else None,
            "median_abs_eval_err_cp": sorted(r[name]["abs_err"] for r in rows)[n // 2] if n else None,
            "mean_move_cost_cp": round(sum(r[name]["cost_cp"] for r in rows) / n, 1) if n else None,
            "blunders_over_200cp": sum(r[name]["cost_cp"] > 200 for r in rows),
            "mean_nodes": round(sum(r[name]["nodes"] for r in rows) / n) if n else None,
            "mean_secs": round(sum(r[name]["secs"] for r in rows) / n, 2) if n else None,
        }
    print(json.dumps(summary, indent=2))
    json.dump({"depth": DEPTH, "sf_depth": SF_DEPTH, "plies": PLIES, "summary": summary, "rows": rows},
              open(OUT + "/results.json", "w"), indent=1, default=str)


if __name__ == "__main__":
    main()

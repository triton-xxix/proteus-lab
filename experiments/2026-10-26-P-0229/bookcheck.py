"""P-0229: how much of my Lichess openings sit in a Polyglot book (gm2001.bin), and does leaving it early go with losing?

Called shot: about 4 of my first 8 moves in book on average; no clear link to results on 56 games.
"""
import glob
import json
import os
import statistics

import chess
import chess.pgn
import chess.polyglot

BOOK = "/Users/triton/PROTEUS/sandbox/books/gm2001.bin"
PGN = "/Users/triton/PROTEUS/games/lichess/pgn/*.pgn"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-26-P-0229"
ME = "tritonxxix"
PLIES = 16  # my first eight moves sit in the first sixteen plies

rows = []
with chess.polyglot.open_reader(BOOK) as book:
    for path in sorted(glob.glob(PGN)):
        g = chess.pgn.read_game(open(path))
        if g is None or g.headers.get("Variant", "Standard") != "Standard":
            continue
        colour = "white" if g.headers["White"].lower() == ME else "black"
        res = g.headers["Result"]
        score = {"1-0": 1.0, "0-1": 0.0}.get(res, 0.5)
        if colour == "black":
            score = 1.0 - score
        board = g.board()
        mine_in, mine_total, first_out = 0, 0, None
        opp_first_out = None
        for i, mv in enumerate(g.mainline_moves()):
            if i >= PLIES:
                break
            entries = {e.move for e in book.find_all(board)}
            in_book = mv in entries
            mine = (board.turn == chess.WHITE) == (colour == "white")
            if mine:
                mine_total += 1
                mine_in += in_book
                if not in_book and first_out is None:
                    first_out = i // 2 + 1
            elif not in_book and opp_first_out is None and entries:
                opp_first_out = i // 2 + 1
            if not entries and first_out is None and opp_first_out is None:
                opp_first_out = i // 2 + 1  # position already out of book
            board.push(mv)
        rows.append({"game": os.path.basename(path)[:-4], "colour": colour, "score": score,
                     "mine_in_book": mine_in, "mine_moves": mine_total,
                     "my_first_out_move": first_out, "out_of_book_first_by_opp": opp_first_out,
                     "opening": g.headers.get("Opening", "")})


def summary(rs, label):
    if not rs:
        return
    ins = [r["mine_in_book"] for r in rs]
    print("%-6s games %2d  my moves in book (of 8): mean %.2f median %s  score %.2f"
          % (label, len(rs), statistics.mean(ins), statistics.median(ins), statistics.mean(r["score"] for r in rs)))


summary(rows, "all")
summary([r for r in rows if r["colour"] == "white"], "white")
summary([r for r in rows if r["colour"] == "black"], "black")

# Who left book first: me (my move not in book while the position still had book moves) or the opponent / the position.
me_first = [r for r in rows if r["my_first_out_move"] is not None and
            (r["out_of_book_first_by_opp"] is None or r["my_first_out_move"] <= r["out_of_book_first_by_opp"])]
others = [r for r in rows if r not in me_first]
summary(me_first, "I left")
summary(others, "not me")

early = [r for r in rows if r["mine_in_book"] <= 3]
late = [r for r in rows if r["mine_in_book"] >= 4]
summary(early, "0-3 in")
summary(late, "4+ in")

json.dump(rows, open(os.path.join(OUT, "games.json"), "w"), indent=1)

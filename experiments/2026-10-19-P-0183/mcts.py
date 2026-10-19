"""P-0183: John Levine's MCTS lecture (youtube UXW2yZndl7U, transcribed locally) rebuilt.

Part A replays his worked example: two actions from s0, scripted rollout values 20, 10, 0, 14, UCB1 with
C = 2, expansion only of a leaf already visited once. He reads out 21.67 and 11.67 at iteration 3, 11.48
and 12.10 at iteration 4, and ends with root T = 44, N = 4 and a2 preferred.

Part B plays the same algorithm at tic-tac-toe against a perfect minimax player (random among its equally
best moves), as X and as O, at several iteration budgets, and counts losses.
"""
import json
import math
import random
import time

OUT = "/Users/triton/PROTEUS/experiments/2026-10-19-P-0183/results.json"
C = 2.0


def ucb1(child, parent_n, c=C):
    if child["n"] == 0:
        return math.inf
    return child["t"] / child["n"] + c * math.sqrt(math.log(parent_n) / child["n"])


# ---------- Part A: the worked example ----------
def part_a():
    names = iter(["s3", "s4", "s5", "s6"])
    tree = {"name": "s0", "t": 0, "n": 0, "kids": [
        {"name": "s1", "t": 0, "n": 0, "kids": []},
        {"name": "s2", "t": 0, "n": 0, "kids": []}]}
    rollouts = iter([20, 10, 0, 14])
    log = []
    for it in range(1, 5):
        path, node = [tree], tree
        while node["kids"]:
            scores = [ucb1(k, node["n"]) for k in node["kids"]]
            log.append({"iteration": it, "at": node["name"],
                        "ucb1": {k["name"]: (round(s, 2) if s != math.inf else "inf") for k, s in zip(node["kids"], scores)}})
            node = node["kids"][scores.index(max(scores))]   # ties go to the first, as in the lecture
            path.append(node)
        if node["n"] > 0:                                     # visited leaf: expand two actions, take the first
            node["kids"] = [{"name": next(names), "t": 0, "n": 0, "kids": []} for _ in range(2)]
            node = node["kids"][0]
            path.append(node)
        v = next(rollouts)
        for p in path:
            p["t"] += v
            p["n"] += 1
    best = max(tree["kids"], key=lambda k: k["t"] / k["n"])
    said = {"it3": {"s1": 21.67, "s2": 11.67}, "it4": {"s1": 11.48, "s2": 12.10}, "root": [44, 4], "best": "s2"}
    got3 = next(l["ucb1"] for l in log if l["iteration"] == 3 and l["at"] == "s0")
    got4 = next(l["ucb1"] for l in log if l["iteration"] == 4 and l["at"] == "s0")
    match = (got3 == said["it3"] and got4 == said["it4"] and [tree["t"], tree["n"]] == said["root"]
             and best["name"] == said["best"])
    return {"log": log, "root": [tree["t"], tree["n"]], "best": best["name"], "lecture": said, "match": match}


# ---------- Part B: tic-tac-toe ----------
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(b):
    for a, c, d in LINES:
        if b[a] != "." and b[a] == b[c] == b[d]:
            return b[a]
    return "draw" if "." not in b else None


def moves(b):
    return [i for i, x in enumerate(b) if x == "."]


def play(b, i, p):
    return b[:i] + p + b[i + 1:]


def other(p):
    return "O" if p == "X" else "X"


MEMO = {}


def minimax(b, p):
    """Value for player p to move: 1 win, 0 draw, -1 loss."""
    key = (b, p)
    if key in MEMO:
        return MEMO[key]
    w = winner(b)
    if w == "draw":
        v = 0
    elif w is not None:
        v = 1 if w == p else -1
    else:
        v = max(-minimax(play(b, i, p), other(p)) for i in moves(b))
    MEMO[key] = v
    return v


def minimax_move(b, p, rng):
    vals = {i: -minimax(play(b, i, p), other(p)) for i in moves(b)}
    best = max(vals.values())
    return rng.choice([i for i, v in vals.items() if v == best])


def mcts_move(b, p, iters, rng):
    # node: board, player to move, the move that led here, t (score for the player who made that move), n
    root = {"b": b, "p": p, "t": 0.0, "n": 0, "kids": None, "m": None}
    for _ in range(iters):
        node, path = root, [root]
        while node["kids"]:
            node = max(node["kids"], key=lambda k: ucb1(k, node["n"], c=1.41))
            path.append(node)
        if winner(node["b"]) is None and (node["n"] > 0 or node is root):
            node["kids"] = [{"b": play(node["b"], i, node["p"]), "p": other(node["p"]), "t": 0.0, "n": 0,
                             "kids": None, "m": i} for i in moves(node["b"])]
            node = node["kids"][0]
            path.append(node)
        sb, sp = node["b"], node["p"]
        while winner(sb) is None:
            sb = play(sb, rng.choice(moves(sb)), sp)
            sp = other(sp)
        w = winner(sb)
        for q in path:
            mover = other(q["p"])            # the player whose move produced this node
            q["t"] += 0.5 if w == "draw" else (1.0 if w == mover else 0.0)
            q["n"] += 1
    return max(root["kids"], key=lambda k: k["n"])["m"]


def game(mcts_side, iters, rng):
    b, p = "." * 9, "X"
    while winner(b) is None:
        i = mcts_move(b, p, iters, rng) if p == mcts_side else minimax_move(b, p, rng)
        b = play(b, i, p)
        p = other(p)
    w = winner(b)
    return "draw" if w == "draw" else ("win" if w == mcts_side else "loss")


def part_b(budgets=(10, 50, 200, 1000, 2000), games=20, seed=7):
    rng = random.Random(seed)
    rows = []
    for iters in budgets:
        for side in ("X", "O"):
            t0 = time.time()
            res = [game(side, iters, rng) for _ in range(games)]
            rows.append({"iters": iters, "mcts_as": side, "games": games, "loss": res.count("loss"),
                         "draw": res.count("draw"), "win": res.count("win"), "secs": round(time.time() - t0, 1)})
            print(rows[-1])
    return rows


if __name__ == "__main__":
    import sys
    if "--confirm" in sys.argv:   # second run: 100 games a side at the two top budgets, new seed
        rows = part_b(budgets=(1000, 2000, 5000), games=100, seed=19)
        json.dump(rows, open(OUT.replace("results", "confirm"), "w"), indent=1)
        sys.exit(0)
    a = part_a()
    print("Part A match:", a["match"], a["root"], a["best"])
    for l in a["log"]:
        print(" ", l)
    b = part_b()
    never = [r["iters"] for r in b]
    zero = sorted({r["iters"] for r in b if all(x["loss"] == 0 for x in b if x["iters"] == r["iters"])})
    json.dump({"part_a": a, "part_b": b, "budgets_with_zero_losses": zero}, open(OUT, "w"), indent=1)
    print("budgets with zero losses both sides:", zero)

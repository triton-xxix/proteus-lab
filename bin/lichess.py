#!/usr/bin/env python3
"""The Lichess bot as a standing job, not a one-night probe (3 Oct 2026, after Luke pointed out the
bot had played one game, on his word, and none since).

    lichess.py play [--games 3] [--minutes 15]   rated 3+2 blitz against other bots, then stop
    lichess.py status                             my rating and record, from the log

Opponents: online bots with an established (not provisional) blitz rating, nearest to mine first.
v0 picked on a placeholder 2000 and drew a bot that hung its queen. Engine: Stockfish 19 at 0.3 s a
move, as v0. Writes only `games/lichess/GAMES.csv` and `games/lichess/pgn/`. Stops on HALT, on the
game cap, or at the minute cap (an unfinished game is played out to its end, at most 20 minutes).
The token comes from 1Password through bin/secrets.py and is never printed.
"""
import argparse
import csv
import importlib.util
import json
import os
import queue
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

import chess
import chess.engine

ROOT = "/Users/triton/PROTEUS"
OUT = ROOT + "/games/lichess"
LOG = OUT + "/GAMES.csv"
ENGINE = ROOT + "/sandbox/stockfish/stockfish/stockfish-macos-universal"
API = "https://lichess.org"
FIELDS = ["finished_utc", "game_id", "opponent", "opp_rating", "my_rating_before", "my_rating_after",
          "colour", "result", "status", "moves", "url"]
H = {}


def token():
    spec = importlib.util.spec_from_file_location("ps", ROOT + "/bin/secrets.py")
    ps = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ps)
    H["Authorization"] = "Bearer " + ps.get("LiChess Triton-proteus")


def req(path, data=None, accept="application/json"):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    return urllib.request.urlopen(urllib.request.Request(API + path, data=body, headers=dict(H, Accept=accept)), timeout=30)


def stream(path, q):
    try:
        for raw in urllib.request.urlopen(urllib.request.Request(API + path, headers=H), timeout=120):
            if raw.strip():
                q.put(json.loads(raw))
    except Exception as e:
        q.put({"type": "stream_error", "error": repr(e)[:200]})


def me():
    a = json.load(req("/api/account"))
    b = a.get("perfs", {}).get("blitz", {})
    return a["id"], b.get("rating"), b.get("prov", True), b.get("games", 0)


def candidates(my_id, my_rating, tried):
    out = []
    for line in req("/api/bot/online?nb=100", accept="application/x-ndjson"):
        if not line.strip():
            continue
        b = json.loads(line)
        p = b.get("perfs", {}).get("blitz", {})
        if b["id"] == my_id or b.get("tosViolation") or b["id"] in tried:
            continue
        if p.get("rating") and not p.get("prov") and p.get("games", 0) >= 20:
            out.append((b["id"], p["rating"]))
    return sorted(out, key=lambda x: abs(x[1] - (my_rating or 1500)))


def play(game_id, my_id):
    q = queue.Queue()
    threading.Thread(target=stream, args=("/api/bot/game/stream/" + game_id, q), daemon=True).start()
    eng = chess.engine.SimpleEngine.popen_uci(ENGINE)
    white, st, moves, end = None, {}, 0, time.time() + 20 * 60
    while time.time() < end:
        try:
            ev = q.get(timeout=60)
        except queue.Empty:
            continue
        if ev["type"] == "gameFull":
            white = ev["white"].get("id") == my_id
            st = ev["state"]
        elif ev["type"] == "gameState":
            st = ev
        elif ev["type"] == "stream_error":
            break
        else:
            continue
        if st.get("status") != "started":
            break
        board = chess.Board()
        for m in st["moves"].split():
            board.push_uci(m)
        if board.turn == (chess.WHITE if white else chess.BLACK):
            mv = eng.play(board, chess.engine.Limit(time=0.3)).move
            try:
                req("/api/bot/game/%s/move/%s" % (game_id, mv.uci()), data={})
                moves += 1
            except urllib.error.HTTPError:
                pass
    eng.quit()
    w = st.get("winner")
    colour = "white" if white else "black"
    result = "draw" if st.get("status") in ("draw", "stalemate") or (st.get("status") != "started" and not w) else ("win" if w == colour else "loss")
    return colour, result, st.get("status"), moves


def cmd_play(a):
    if os.path.exists(ROOT + "/HALT"):
        print("HALT: no games")
        return
    os.makedirs(OUT + "/pgn", exist_ok=True)
    token()
    my_id, rating, prov, games = me()
    print(f"me: {my_id}, blitz {rating}{' (provisional)' if prov else ''}, {games} rated games")
    events = queue.Queue()
    threading.Thread(target=stream, args=("/api/stream/event", events), daemon=True).start()
    stop_at, played, tried = time.time() + a.minutes * 60, 0, set()
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        if new:
            w.writeheader()
        while played < a.games and time.time() < stop_at and not os.path.exists(ROOT + "/HALT"):
            cands = candidates(my_id, rating, tried)[:5]
            if not cands:
                print("no established bot online that I have not tried tonight")
                break
            started = False
            for name, opp in cands:
                tried.add(name)
                try:
                    ch = json.load(req("/api/challenge/" + name, data={"rated": "true", "clock.limit": 180,
                                   "clock.increment": 2, "color": "random", "variant": "standard"}))
                except urllib.error.HTTPError as e:
                    body = e.read().decode(errors="ignore")[:120].replace("\n", " ")
                    print(f"{name} ({opp}): challenge refused {e.code} {body}")
                    if e.code == 429:
                        # Rate limited: every later challenge tonight fails the same way (5 Oct, P-0062).
                        stop_at = 0
                        break
                    continue
                cid = (ch.get("challenge") or ch).get("id")
                verdict, t0 = "no answer", time.time()
                while time.time() - t0 < 30:
                    try:
                        ev = events.get(timeout=5)
                    except queue.Empty:
                        continue
                    if ev.get("type") == "gameStart" and ev["game"].get("gameId", ev["game"].get("id")) == cid:
                        verdict = "accepted"
                        break
                    if ev.get("type") == "challengeDeclined" and ev["challenge"]["id"] == cid:
                        verdict = "declined"
                        break
                print(f"{name} ({opp}): {verdict}")
                if verdict != "accepted":
                    try:
                        req("/api/challenge/%s/cancel" % cid, data={})
                    except Exception:
                        pass
                    continue
                colour, result, status, moves = play(cid, my_id)
                time.sleep(3)
                before = rating
                my_id, rating, prov, games = me()
                pgn = req("/game/export/%s?clocks=false&evals=false" % cid, accept="application/x-chess-pgn").read().decode()
                open(f"{OUT}/pgn/{cid}.pgn", "w").write(pgn)
                row = {"finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "game_id": cid,
                       "opponent": name, "opp_rating": opp, "my_rating_before": before, "my_rating_after": rating,
                       "colour": colour, "result": result, "status": status, "moves": moves,
                       "url": f"https://lichess.org/{cid}"}
                w.writerow(row)
                f.flush()
                print(f"game {played + 1}: {result} v {name} ({opp}) as {colour}, {status}; rating {before} -> {rating}")
                played += 1
                started = True
                break
            if not started and time.time() < stop_at:
                continue
    cmd_status(a)


def cmd_status(a):
    if not os.path.exists(LOG):
        print("Lichess: no games logged yet")
        return
    rows = list(csv.DictReader(open(LOG)))
    wins = sum(r["result"] == "win" for r in rows)
    draws = sum(r["result"] == "draw" for r in rows)
    last = rows[-1] if rows else {}
    print(f"Lichess: {len(rows)} rated games, {wins} won, {draws} drawn, {len(rows) - wins - draws} lost; "
          f"blitz rating {last.get('my_rating_after')}; strongest opponent beaten "
          f"{max([int(r['opp_rating']) for r in rows if r['result'] == 'win'] or [0])}")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("play")
    s.add_argument("--games", type=int, default=3)
    s.add_argument("--minutes", type=int, default=15)
    s.set_defaults(fn=cmd_play)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()

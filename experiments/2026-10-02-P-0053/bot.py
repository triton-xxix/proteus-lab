"""P-0053: Lichess bot v0. Challenge one online bot to a casual 3+2 game, play Stockfish 19 moves
(0.3 s a move), log the game. Prints no secret. Writes only into this folder.
Usage: bot.py [max_bots_to_try]"""
import importlib.util, json, queue, sys, threading, time, urllib.request, urllib.error, urllib.parse
import chess, chess.engine

OUT = "/Users/triton/PROTEUS/experiments/2026-10-02-P-0053"
ENGINE = "/Users/triton/PROTEUS/sandbox/stockfish/stockfish/stockfish-macos-universal"
spec = importlib.util.spec_from_file_location("ps", "/Users/triton/PROTEUS/bin/secrets.py")
ps = importlib.util.module_from_spec(spec); spec.loader.exec_module(ps)
H = {"Authorization": "Bearer " + ps.get("LiChess Triton-proteus")}
API = "https://lichess.org"
log = open(OUT + "/log.txt", "a")


def say(*a):
    line = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(line, flush=True); log.write(line + "\n"); log.flush()


def req(path, data=None, method=None, accept="application/json"):
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    r = urllib.request.Request(API + path, data=body, headers=dict(H, Accept=accept), method=method)
    return urllib.request.urlopen(r, timeout=30)


def stream(path, q, tag):
    try:
        r = urllib.request.urlopen(urllib.request.Request(API + path, headers=H), timeout=120)
        for raw in r:
            raw = raw.strip()
            if raw:
                q.put((tag, json.loads(raw)))
    except Exception as e:
        q.put((tag, {"type": "stream_error", "error": repr(e)[:200]}))


def online_bots(n=60):
    me = json.load(req("/api/account"))["id"]
    bots = []
    for line in req("/api/bot/online?nb=%d" % n, accept="application/x-ndjson"):
        if line.strip():
            b = json.loads(line)
            if b["id"] != me and not b.get("tosViolation"):
                blitz = b.get("perfs", {}).get("blitz", {}).get("rating")
                bots.append((b["id"], blitz))
    return me, bots


def play(game_id, me):
    q = queue.Queue()
    threading.Thread(target=stream, args=("/api/bot/game/stream/" + game_id, q, "game"), daemon=True).start()
    eng = chess.engine.SimpleEngine.popen_uci(ENGINE)
    my_white, moves_sent, errors, status = None, 0, [], None
    deadline = time.time() + 20 * 60
    while time.time() < deadline:
        try:
            _, ev = q.get(timeout=60)
        except queue.Empty:
            say("no game event for 60 s"); continue
        if ev["type"] == "gameFull":
            my_white = ev["white"].get("id") == me
            say("game", game_id, "I am", "white" if my_white else "black", "v", (ev["black"] if my_white else ev["white"]).get("id"))
            st = ev["state"]
        elif ev["type"] == "gameState":
            st = ev
        elif ev["type"] == "stream_error":
            errors.append(ev["error"]); say("stream error", ev["error"]); break
        else:
            continue
        status = st.get("status")
        if status != "started":
            say("game over:", status, "winner", st.get("winner")); break
        board = chess.Board()
        for m in st["moves"].split():
            board.push_uci(m)
        if board.turn == (chess.WHITE if my_white else chess.BLACK):
            mv = eng.play(board, chess.engine.Limit(time=0.3)).move
            try:
                req("/api/bot/game/%s/move/%s" % (game_id, mv.uci()), data={})
                moves_sent += 1
            except urllib.error.HTTPError as e:
                errors.append("move %s: %s %s" % (mv.uci(), e.code, e.read().decode()[:120])); say(errors[-1])
    eng.quit()
    return {"status": status, "moves_sent": moves_sent, "errors": errors, "my_colour": "white" if my_white else "black"}


def main():
    tries = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    me, bots = online_bots()
    say("online bots:", len(bots))
    cands = sorted([b for b in bots if b[1]], key=lambda b: abs(b[1] - 2000))[:tries]
    events = queue.Queue()
    threading.Thread(target=stream, args=("/api/stream/event", events, "event"), daemon=True).start()
    result = {"bots_online": len(bots), "tried": []}
    for name, rating in cands:
        try:
            ch = json.load(req("/api/challenge/" + name, data={"rated": "false", "clock.limit": 180, "clock.increment": 2, "color": "random", "variant": "standard"}))
        except urllib.error.HTTPError as e:
            result["tried"].append([name, rating, "challenge refused %d" % e.code]); say(name, "refused", e.code); continue
        cid = (ch.get("challenge") or ch).get("id")
        say("challenged", name, rating, "id", cid)
        verdict, t0 = "no answer in 30 s", time.time()
        while time.time() - t0 < 30:
            try:
                _, ev = events.get(timeout=5)
            except queue.Empty:
                continue
            if ev.get("type") == "gameStart" and ev["game"].get("gameId", ev["game"].get("id")) == cid:
                verdict = "accepted"; break
            if ev.get("type") == "challengeDeclined" and ev["challenge"]["id"] == cid:
                verdict = "declined: " + str(ev["challenge"].get("declineReason")); break
        result["tried"].append([name, rating, verdict]); say(name, verdict)
        if verdict == "accepted":
            result["opponent"] = [name, rating]
            result.update(play(cid, me))
            result["game_id"] = cid
            pgn = req("/game/export/%s?clocks=false&evals=false" % cid, accept="application/x-chess-pgn").read().decode()
            open(OUT + "/game.pgn", "w").write(pgn)
            break
        try:
            req("/api/challenge/%s/cancel" % cid, data={})
        except Exception:
            pass
    json.dump(result, open(OUT + "/result.json", "w"), indent=1)
    say("result", json.dumps(result)[:600])


if __name__ == "__main__":
    main()

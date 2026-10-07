"""How the three rug markers from REPLAY-2 overlap on the post-30-Sep gate-passers: rugcheck risk
named (not E02), rising 1h at entry (not E01), no Telegram mention (not M09). Per row: how many
markers, V01 outcome, and the top-4 slice."""
import sys, time
sys.path.insert(0, "/Users/triton/PROTEUS/grinder/harness")
import replay, replay2  # noqa: E402

pop = [(r, replay.candles(r, False)) for r in replay2.population(time.time())]
pop = [(r, c) for r, c in pop if c and r["_grp"] == "pass" and replay.ts_of(r["ts"]) >= replay2.SEEN_FROM]
m = replay2.mentions()
res = {(x["mint"], x["night"]): x for x in replay.run_variant("V01", pop)}
rows = []
for r, c in pop:
    tg = replay2.src_count(r, m, "telegram")
    marks = {"risk": not replay2.e02(r), "rising": not replay2.e01(r), "tg_silent": (tg is not None and tg < 1)}
    x = res.get((r["mint"], r["ts"][:10]))
    if x:
        rows.append((sum(marks.values()), marks, x, r))
for k in range(4):
    sel = [x for n, mk, x, r in rows if n == k]
    if sel:
        s = replay.stats(sel); s4 = replay.stats(replay.top_k(sel, 4))
        print("markers=%d: n %d, exp £%.1f, rugs %d, wins %d | top-4 slice exp £%.1f (%d)" % (k, s["n"], s["exp"], s["rug"], s["win"], s4["exp"], s4["n"]))
clean = [x for n, mk, x, r in rows if n == 0]
dirty = [x for n, mk, x, r in rows if n >= 1]
for name, sel in (("zero markers", clean), ("any marker", dirty)):
    s = replay.stats(sel); s4 = replay.stats(replay.top_k(sel, 4))
    print("%s: n %d, exp £%.1f, best-3 removed £%.1f, rugs %d, wins %d | top-4 exp £%.1f (%d)" % (name, s["n"], s["exp"], s["trim3"], s["rug"], s["win"], s4["exp"], s4["n"]))
for key in ("risk", "rising", "tg_silent"):
    a = [x for n, mk, x, r in rows if mk[key]]
    print("%s alone: n %d, rugs %d" % (key, len(a), sum(1 for x in a if x["reason"] == "rug")))

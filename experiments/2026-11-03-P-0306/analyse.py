"""P-0306: turn raw.json screen events into chars per second, instructions per char and the wait share.
A scroll makes v86 re-put every cell, so a new char is told from a redraw by the burst it sits in:
events within 1 ms of each other form one burst; a burst of 1 or 2 events is the model printing,
a bigger one is a redraw. Run: python3 analyse.py (writes results.json beside it)."""
import json, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, "raw.json")))
ev = raw["events"]

bursts, cur = [], [ev[0]]
for e in ev[1:]:
    if e[0] - cur[-1][0] <= 1.0:
        cur.append(e)
    else:
        bursts.append(cur)
        cur = [e]
bursts.append(cur)

small = [b for b in bursts if len(b) <= 2]
big = [b for b in bursts if len(b) > 2]
# the model's chars: the first event of each small burst (a newline can add a second)
chars = [b[0] for b in small]
# skip boot: start counting at the first char printed after the last big burst in the first 3 s that is
# not a scroll (the SeaBIOS banner and header); simplest honest cut: drop chars before 2 s
gen = [c for c in chars if c[0] >= 2000]
gaps = [b[0] - a[0] for a, b in zip(gen, gen[1:])]
ics = [b[1] - a[1] for a, b in zip(gen, gen[1:]) if a[1] is not None and b[1] is not None]
span_s = (gen[-1][0] - gen[0][0]) / 1000 if len(gen) > 1 else None
mean_gap = statistics.mean(gaps) if gaps else None
res = {
    "events": len(ev), "bursts": len(bursts), "small_bursts": len(small), "big_bursts": len(big),
    "big_burst_median_size": statistics.median(len(b) for b in big) if big else None,
    "gen_chars": len(gen), "gen_span_s": round(span_s, 2) if span_s else None,
    "chars_per_s": round((len(gen) - 1) / span_s, 1) if span_s else None,
    "gap_ms_median": round(statistics.median(gaps), 2) if gaps else None,
    "gap_ms_mean": round(mean_gap, 2) if mean_gap else None,
    "gap_ms_p10": round(sorted(gaps)[len(gaps) // 10], 2) if gaps else None,
    "gap_ms_p90": round(sorted(gaps)[len(gaps) * 9 // 10], 2) if gaps else None,
    "instr_per_char_median": statistics.median(ics) if ics else None,
    "wait_share_if_10ms": round(10.0 / mean_gap, 3) if mean_gap else None,
    "save_ms": round(raw["save_ms"], 1), "restore_ms": round(raw["restore_ms"], 1),
    "state_bytes": raw["state_bytes"],
    "first_put_after_restore_ms": round(raw["after_restore"][0][0], 1) if raw["after_restore"] else None,
}
json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(res, indent=1))

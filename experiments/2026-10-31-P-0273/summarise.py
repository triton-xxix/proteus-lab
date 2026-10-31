"""P-0273: summarise two minutes of Sketch Stadium's public SSE stream (saved by curl)."""
import json
import sys

SRC = "/Users/triton/PROTEUS/sandbox/sketch-live.txt"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-31-P-0273/results.json"
text = open(SRC, encoding="utf-8").read()
events = []
for block in text.split("\n\n"):
    ev, data = None, None
    for line in block.splitlines():
        if line.startswith("event: "):
            ev = line[7:]
        elif line.startswith("data: "):
            data = line[6:]
    if ev and data:
        events.append((ev, json.loads(data), len(block)))
seqs = [d.get("seq") for _, d, _ in events]
phases = {}
rounds = set()
for _, d, _ in events:
    phases[d.get("phase")] = phases.get(d.get("phase"), 0) + 1
    rounds.add(d.get("round"))
stroke_counts = [len(d.get("strokes", [])) for _, d, _ in events]
max_strokes = max(stroke_counts) if stroke_counts else 0
points = 0
for _, d, _ in events:
    for s in d.get("strokes", []):
        for seg in (s.get("sh") or {}).get("d", []):
            points += len(seg.get("p", []))
keys = sorted({k for _, d, _ in events for k in d.keys()})
res = {
    "events": len(events),
    "seconds": 125,
    "per_minute": round(len(events) / 125 * 60, 1),
    "event_types": sorted({e for e, _, _ in events}),
    "seq_first_last": [seqs[0], seqs[-1]] if seqs else None,
    "seq_gaps": (seqs[-1] - seqs[0] + 1 - len(seqs)) if seqs else None,
    "phases": phases,
    "rounds_seen": sorted(r for r in rounds if r is not None),
    "bytes_total": len(text.encode()),
    "bytes_per_event_median": sorted(b for _, _, b in events)[len(events) // 2] if events else None,
    "max_strokes_in_one_snapshot": max_strokes,
    "stroke_points_total": points,
    "fields": keys,
    "full_state_not_delta": all("players" in d and "strokes" in d for _, d, _ in events),
}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
sys.exit(0)

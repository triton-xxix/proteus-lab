"""P-0294: does the booted disk print exactly what train.py's integer sim says it should?
The disk seeds its LCG from the PIT clock (int 0x1A, then `or dx, 1`), so train.py's printed sample
(seed 0x1234, even) can never appear. Instead: rebuild BootSim from weights.bin and params.inc, recover the
seed from the first characters the emulator printed (the logits depend only on the context, which the
printed text gives, so every odd 16-bit seed is tried at once), then generate from that seed, lay both out
on an 80-column screen and compare row by row.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 -I experiments/2026-11-02-P-0294/match.py
"""
import json
import numpy as np

SB = "/Users/triton/PROTEUS/sandbox/bootgpt"
EXP = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0294"
V, C, E, H = 64, 8, 6, 96
A1SHIFT, A2SHIFT, NS = -4, 1, 8
SEED_CTX = [11, 0, 0, 0, 2, 10, 2, 2]

blob = open(SB + "/weights.bin", "rb").read()
vocab = [chr(b) for b in blob[:64]]
emb = np.frombuffer(blob, np.int8, V * E, 64).astype(np.int64)
W1 = np.frombuffer(blob, np.int8, H * C * E, 448).astype(np.int64).reshape(H, C * E)
W2 = np.frombuffer(blob, np.int8, V * H, 5056).astype(np.int64).reshape(V, H)
b1 = np.frombuffer(blob, np.int16, H, 11200).astype(np.int64)
b2 = np.frombuffer(blob, np.int16, V, 11392).astype(np.int64)


def logits_for(ctx):
    xin = np.array([emb[ctx[k] * E + r] for k in range(C) for r in range(E)], dtype=np.int64)
    a1 = W1 @ xin
    p = (a1 >> A1SHIFT) if A1SHIFT >= 0 else (a1 << -A1SHIFT)
    p = p + b1
    num, den = p * 64, 4096 + np.abs(p)
    y = np.sign(num) * (np.abs(num) // den)          # x86 idiv truncation
    y = np.clip(y, -64, 64)
    a2 = W2 @ y
    return ((a2 >> A2SHIFT) if A2SHIFT >= 0 else (a2 << -A2SHIFT)) + b2


def step(rnd, logits):
    """One generated char for an array of LCG states: returns (choice, new states)."""
    best = np.full(rnd.shape, -(1 << 30), dtype=np.int64)
    bi = np.zeros(rnd.shape, dtype=np.int64)
    for vi in range(V):
        rnd = (rnd * 25173 + 13849) & 0xFFFF
        r8 = (rnd >> 8) & 0xFF
        r8 = np.where(r8 >= 128, r8 - 256, r8)
        cand = int(logits[vi]) + r8 * NS
        better = cand > best
        best = np.where(better, cand, best)
        bi = np.where(better, vi, bi)
    return bi, rnd


def gen(seed, n):
    rnd = np.array([seed], dtype=np.int64)
    ctx, out = list(SEED_CTX), []
    for _ in range(n):
        bi, rnd = step(rnd, logits_for(ctx))
        out.append(vocab[int(bi[0])])
        ctx = ctx[1:] + [int(bi[0])]
    return "".join(out)


def screen(text):
    rows, cur = [], ""
    for ch in text:
        if ch == "\n":
            rows.append(cur)
            cur = ""
            continue
        cur += ch
        if len(cur) == 80:
            rows.append(cur)
            cur = ""
    rows.append(cur)
    return [r.rstrip() for r in rows]


shot = open(EXP + "/screen.txt").read().split("\n")
hdr = next(i for i, r in enumerate(shot) if r.startswith("no os involved"))
emu_rows = shot[hdr + 1:]
while emu_rows and emu_rows[-1] == "":
    emu_rows.pop()
first = emu_rows[0][:40]
idx = {ch: i for i, ch in enumerate(vocab)}

# recover the seed from the first 40 printed chars
seeds = np.arange(1, 65536, 2, dtype=np.int64)          # `or dx, 1`: always odd
rnd, ctx = seeds.copy(), list(SEED_CTX)
for ch in first:
    bi, rnd = step(rnd, logits_for(ctx))
    keep = bi == idx[ch]
    seeds, rnd = seeds[keep], rnd[keep]
    ctx = ctx[1:] + [idx[ch]]
print("seeds consistent with the first", len(first), "chars:", [hex(int(s)) for s in seeds[:5]], len(seeds))

res = {"emulator_rows": len(emu_rows), "chars_used_for_seed": len(first), "seeds_consistent": len(seeds)}
if len(seeds):
    seed = int(seeds[0])
    sim_rows = screen(gen(seed, 2000))
    full = len(emu_rows) - 1                               # the last row may be cut mid-line by the timer
    diffs = [(i, emu_rows[i], sim_rows[i]) for i in range(full) if emu_rows[i] != sim_rows[i]]
    last_ok = sim_rows[full].startswith(emu_rows[full])
    chars = sum(len(r) for r in emu_rows)
    res.update({"seed": hex(seed), "full_rows_compared": full, "rows_differing": len(diffs),
                "last_row_prefix_match": last_ok, "printed_chars_compared": chars,
                "first_diff": diffs[0] if diffs else None,
                "train_py_seed_0x1234_possible": False})
    print(json.dumps(res, indent=1))
json.dump(res, open(EXP + "/results.json", "w"), indent=1)

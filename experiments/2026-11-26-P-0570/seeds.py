"""P-0570: spread of the no-model ASVspoof EER over 50 clip-split and 50 speaker-split seeds.

Same 600 clips and features as P-0559 (its picking, its cache). Features computed once, then each seed
only refits the median/MAD profile and rescores.

    sandbox/py312-venv/bin/python seeds.py
"""
import importlib.util, json, sys, time, urllib.parse
from pathlib import Path
import numpy as np
import librosa

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("s", "/Users/triton/PROTEUS/experiments/2026-11-24-P-0559/speaker_split.py")
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
b = s.b
N = 300
SEEDS = 50


def load():
    picked = {0: [], 1: []}
    offs = list(range(0, 71200, 2300)) + list(range(1100, 71200, 2300)) + list(range(600, 71200, 1150))
    for off in offs:
        if len(picked[0]) >= N and len(picked[1]) >= N:
            break
        q = urllib.parse.urlencode({"dataset": b.DS, "config": "default", "split": "test", "offset": off, "length": 100})
        for r in b.get("https://datasets-server.huggingface.co/rows?" + q)["rows"]:
            row = r["row"]
            if len(picked[row["label"]]) < N and row["path"] not in {x["path"] for x in picked[row["label"]]}:
                picked[row["label"]].append(row)
    clips, fetched = [], 0
    for label in (0, 1):
        for row in picked[label]:
            p = b.AUD / row["path"]
            if not p.exists():
                p.write_bytes(b.get(row["audio"][0]["src"], binary=True))
                fetched += 1
            clips.append((label, p, json.loads(row.get("notes") or "{}").get("speaker_id")))
    F, names = [], None
    for _, p, _ in clips:
        y, sr = librosa.load(p, sr=16000)
        f = b.feats(y, sr)
        names = names or list(f)
        F.append([f[k] for k in names])
    return np.array(F), np.array([c[0] for c in clips]), np.array([c[2] for c in clips]), fetched


def pct(v):
    v = np.array(v)
    return {"median": round(float(np.median(v)), 4), "p5": round(float(np.percentile(v, 5)), 4),
            "p95": round(float(np.percentile(v, 95)), 4), "min": round(float(v.min()), 4), "max": round(float(v.max()), 4),
            "mean": round(float(v.mean()), 4), "sd": round(float(v.std(ddof=1)), 4)}


def main():
    if Path("/Users/triton/PROTEUS/HALT").exists():
        print("HALT")
        return 1
    t0 = time.time()
    X, lab, spk, fetched = load()
    bona, spoof = np.where(lab == 0)[0], np.where(lab == 1)[0]
    # sameness check against P-0547 / P-0559
    rng = np.random.default_rng(23)
    bb = bona.copy()
    rng.shuffle(bb)
    check = s.score(X, lab, bb[: len(bb) // 2], np.concatenate([bb[len(bb) // 2:], spoof]))
    speakers = sorted({x for x in spk[bona] if x})
    clip_e, spk_e = [], []
    for seed in range(SEEDS):
        r = np.random.default_rng(1000 + seed)
        cc = bona.copy()
        r.shuffle(cc)
        clip_e.append(s.score(X, lab, cc[: len(cc) // 2], np.concatenate([cc[len(cc) // 2:], spoof])))
        sp = list(speakers)
        r.shuffle(sp)
        a = set(sp[: len(sp) // 2])
        fit = np.array([i for i in bona if spk[i] in a])
        held = np.array([i for i in bona if spk[i] not in a])
        spk_e.append(s.score(X, lab, fit, np.concatenate([held, spoof])))
    ce, se = np.array(clip_e), np.array(spk_e)
    res = {"clips": int(len(lab)), "fetched": fetched, "seed23_check": round(check, 4), "seeds": SEEDS,
           "clip_split": pct(ce), "speaker_split": pct(se),
           "clip_share_at_or_below_0.160": round(float((ce <= 0.1600).mean()), 3),
           "clip_share_at_or_below_0.1765": round(float((ce <= 0.1765).mean()), 3),
           "speaker_share_at_or_below_0.1765": round(float((se <= 0.1765).mean()), 3),
           "clip_eers": [round(float(x), 4) for x in ce], "speaker_eers": [round(float(x), 4) for x in se],
           "seconds": round(time.time() - t0)}
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if not k.endswith("_eers")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

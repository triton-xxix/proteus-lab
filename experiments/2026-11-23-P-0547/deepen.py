"""P-0547: deepen P-0546. Bigger sample, bootstrap interval, energy/silence ablation.

Reuses P-0546's feature code and audio cache. 300 bonafide + 300 spoof from LA eval (HF datasets-server
/rows, offsets spread; the first 100 of each are P-0546's clips). Fit on 150 bonafide (seed 23), test on
150 bonafide + 300 spoof.

    sandbox/py312-venv/bin/python deepen.py
"""
import importlib.util, json, sys, time, urllib.parse
from pathlib import Path
import numpy as np
import librosa

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b", "/Users/triton/PROTEUS/experiments/2026-11-23-P-0546/sear_baseline.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
N = 300
DROP = ("rms_mean", "rms_std", "dyn_range_db", "noise_floor_db", "mfcc0_mean", "mfcc0_std")


def main():
    t0 = time.time()
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
    clips = []
    for label in (0, 1):
        for row in picked[label]:
            p = b.AUD / row["path"]
            if not p.exists():
                p.write_bytes(b.get(row["audio"][0]["src"], binary=True))
            clips.append((row["path"], label, p, json.loads(row.get("notes") or "{}").get("speaker_id")))
    print("have", len(clips), round(time.time() - t0), "s", flush=True)
    F, names = [], None
    for _, _, p, _ in clips:
        y, sr = librosa.load(p, sr=16000)
        f = b.feats(y, sr)
        names = names or list(f)
        F.append([f[k] for k in names])
    X = np.array(F)
    lab = np.array([c[1] for c in clips])
    rng = np.random.default_rng(23)
    bona = np.where(lab == 0)[0]
    rng.shuffle(bona)
    fit, held = bona[: len(bona) // 2], bona[len(bona) // 2:]
    test = np.concatenate([held, np.where(lab == 1)[0]])
    med = np.median(X[fit], axis=0)
    mad = np.median(np.abs(X[fit] - med), axis=0) * 1.4826 + 1e-9
    Z = np.abs((X - med) / mad)
    keep = [i for i, n in enumerate(names) if n not in DROP]
    s_full, s_abl = Z.mean(axis=1), Z[:, keep].mean(axis=1)
    e_full, e_abl = b.eer(s_full[test], lab[test]), b.eer(s_abl[test], lab[test])
    boots_f, boots_a = [], []
    tb, ts = test[lab[test] == 0], test[lab[test] == 1]
    for _ in range(300):
        idx = np.concatenate([rng.choice(tb, len(tb)), rng.choice(ts, len(ts))])
        boots_f.append(b.eer(s_full[idx], lab[idx]))
        boots_a.append(b.eer(s_abl[idx], lab[idx]))
    spk_fit = {clips[i][3] for i in fit}
    spk_overlap = sum(clips[i][3] in spk_fit for i in held)
    res = {"clips": len(clips), "fit_bonafide": len(fit), "test_bonafide": len(held), "test_spoof": int((lab == 1).sum()),
           "features": len(names), "dropped": list(DROP),
           "eer_full": round(float(e_full), 4),
           "eer_full_ci95": [round(float(np.percentile(boots_f, q)), 4) for q in (2.5, 97.5)],
           "eer_without_energy": round(float(e_abl), 4),
           "eer_without_energy_ci95": [round(float(np.percentile(boots_a, q)), 4) for q in (2.5, 97.5)],
           "held_bonafide_with_speaker_in_fit": spk_overlap,
           "per_attack": "not done: notes field carries utterance, speaker and subset only; labels.parquet needs pyarrow, absent from the venv",
           "seconds": round(time.time() - t0)}
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""P-0559: P-0547's no-model ASVspoof baseline with a speaker split instead of a clip split.

Same 300 bonafide + 300 spoof LA eval clips as P-0547 (same offsets, same picking, audio cached), same
features (P-0546's feats). Fit the robust median/MAD profile on bonafide from half the speakers, test on
bonafide from the other half plus all spoof. Five seeds. Also the clip split re-run with the same seed
(23) as a check that the clip set is P-0547's.

    sandbox/py312-venv/bin/python speaker_split.py
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


def score(X, lab, fit, test):
    med = np.median(X[fit], axis=0)
    mad = np.median(np.abs(X[fit] - med), axis=0) * 1.4826 + 1e-9
    s = np.abs((X - med) / mad).mean(axis=1)
    return float(b.eer(s[test], lab[test]))


def main():
    if Path("/Users/triton/PROTEUS/HALT").exists():
        print("HALT")
        return 1
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
    fetched = 0
    for label in (0, 1):
        for row in picked[label]:
            p = b.AUD / row["path"]
            if not p.exists():
                p.write_bytes(b.get(row["audio"][0]["src"], binary=True))
                fetched += 1
            clips.append((row["path"], label, p, json.loads(row.get("notes") or "{}").get("speaker_id")))
    print("have", len(clips), "fetched", fetched, round(time.time() - t0), "s", flush=True)
    F, names = [], None
    for _, _, p, _ in clips:
        y, sr = librosa.load(p, sr=16000)
        f = b.feats(y, sr)
        names = names or list(f)
        F.append([f[k] for k in names])
    X = np.array(F)
    lab = np.array([c[1] for c in clips])
    spk = np.array([c[3] for c in clips])
    bona = np.where(lab == 0)[0]
    spoof = np.where(lab == 1)[0]

    # clip split, P-0547's seed, as a sameness check
    rng = np.random.default_rng(23)
    bb = bona.copy()
    rng.shuffle(bb)
    clip_eer = score(X, lab, bb[: len(bb) // 2], np.concatenate([bb[len(bb) // 2:], spoof]))

    speakers = sorted({s for s in spk[bona] if s})
    runs = []
    for seed in range(5):
        r = np.random.default_rng(100 + seed)
        sp = list(speakers)
        r.shuffle(sp)
        a = set(sp[: len(sp) // 2])
        fit = np.array([i for i in bona if spk[i] in a])
        held = np.array([i for i in bona if spk[i] not in a])
        # same-size clip split for a fair comparison
        cc = bona.copy()
        r.shuffle(cc)
        cfit, cheld = cc[: len(fit)], cc[len(fit):]
        runs.append({"seed": 100 + seed, "fit_speakers": len(a), "fit_bonafide": int(len(fit)), "test_bonafide": int(len(held)),
                     "eer_speaker_split": round(score(X, lab, fit, np.concatenate([held, spoof])), 4),
                     "eer_clip_split_same_sizes": round(score(X, lab, cfit, np.concatenate([cheld, spoof])), 4)})
        print(json.dumps(runs[-1]), flush=True)
    sp_e = [x["eer_speaker_split"] for x in runs]
    cl_e = [x["eer_clip_split_same_sizes"] for x in runs]
    spoof_spk = {s for s in spk[spoof] if s}
    res = {"clips": len(clips), "bonafide_speakers": len(speakers), "spoof_speakers": len(spoof_spk),
           "spoof_speakers_also_bonafide": len(spoof_spk & set(speakers)),
           "clip_split_seed23_eer": round(clip_eer, 4), "p0547_eer_full": 0.16,
           "speaker_split_eer_mean": round(float(np.mean(sp_e)), 4), "speaker_split_eer_range": [min(sp_e), max(sp_e)],
           "clip_split_eer_mean": round(float(np.mean(cl_e)), 4), "clip_split_eer_range": [min(cl_e), max(cl_e)],
           "runs": runs, "seconds": round(time.time() - t0)}
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != "runs"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""P-0546: SEAR-style tools-only baseline on ASVspoof 2019 LA eval audio, keyless.

Rows from the HF datasets-server (filter API, label 0 bonafide / 1 spoof) of the ungated mirror
SpeechAntiSpoofingBenchmarks/ASVspoof2019_LA. Per clip: librosa features (frame stats). Median and MAD
fitted on half the bonafide clips only; score = mean absolute robust z over features. EER on the
held-out bonafide half plus all spoof clips.

    sandbox/py312-venv/bin/python sear_baseline.py
"""
import json, sys, time, urllib.parse, urllib.request
from pathlib import Path

import numpy as np
import librosa

HERE = Path(__file__).resolve().parent
AUD = Path("/Users/triton/PROTEUS/sandbox/p0546-audio")
AUD.mkdir(parents=True, exist_ok=True)
DS = "SpeechAntiSpoofingBenchmarks/ASVspoof2019_LA"
UA = "Mozilla/5.0 proteus-p0546/0.1"
N = 100


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for a in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                b = r.read()
            return b if binary else json.loads(b)
        except Exception as e:
            err = e
            time.sleep(2 * (a + 1))
    raise RuntimeError(str(err))


def rows(label, offset):
    q = urllib.parse.urlencode({"dataset": DS, "config": "default", "split": "test",
                                "where": f'"label"={label}', "offset": offset, "length": N})
    return get("https://datasets-server.huggingface.co/filter?" + q)["rows"]


def feats(y, sr):
    S = np.abs(librosa.stft(y, n_fft=512, hop_length=160))
    f = {}
    mf = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    for i in range(13):
        f[f"mfcc{i}_mean"] = mf[i].mean()
        f[f"mfcc{i}_std"] = mf[i].std()
    for name, v in [("centroid", librosa.feature.spectral_centroid(S=S, sr=sr)),
                    ("bandwidth", librosa.feature.spectral_bandwidth(S=S, sr=sr)),
                    ("rolloff", librosa.feature.spectral_rolloff(S=S, sr=sr)),
                    ("flatness", librosa.feature.spectral_flatness(S=S)),
                    ("zcr", librosa.feature.zero_crossing_rate(y, hop_length=160)),
                    ("rms", librosa.feature.rms(S=S, frame_length=512))]:
        f[name + "_mean"] = float(v.mean())
        f[name + "_std"] = float(v.std())
    f["contrast_mean"] = float(librosa.feature.spectral_contrast(S=S, sr=sr).mean())
    rms = librosa.feature.rms(S=S, frame_length=512)[0]
    f["noise_floor_db"] = float(20 * np.log10(np.percentile(rms, 5) + 1e-9))
    f["dyn_range_db"] = float(20 * np.log10((np.percentile(rms, 95) + 1e-9) / (np.percentile(rms, 5) + 1e-9)))
    f0 = librosa.yin(y, fmin=60, fmax=400, sr=sr, hop_length=160)
    f["f0_median"] = float(np.median(f0))
    f["f0_std"] = float(np.std(f0))
    hi = S[S.shape[0] * 3 // 4:].sum() / (S.sum() + 1e-9)
    f["hf_energy_ratio"] = float(hi)
    return f


def eer(scores, labels):
    s, l = np.asarray(scores), np.asarray(labels)
    best = (1.0, None)
    for t in np.unique(s):
        far = np.mean(s[l == 0] >= t)  # bonafide flagged
        frr = np.mean(s[l == 1] < t)   # spoof missed
        gap = abs(far - frr)
        if best[1] is None or gap < best[0]:
            best = (gap, (far + frr) / 2)
    return best[1]


def main():
    if Path("/Users/triton/PROTEUS/HALT").exists():
        return 1
    t0 = time.time()
    # filter API answered 500 on 23 Nov, so page /rows at spread offsets and pick by label
    picked = {0: [], 1: []}
    for off in range(0, 71200, 2300):
        if len(picked[0]) >= N and len(picked[1]) >= N:
            break
        q = urllib.parse.urlencode({"dataset": DS, "config": "default", "split": "test", "offset": off, "length": 100})
        for r in get("https://datasets-server.huggingface.co/rows?" + q)["rows"]:
            row = r["row"]
            if len(picked[row["label"]]) < N:
                picked[row["label"]].append(row)
    clips = []
    for label in (0, 1):
        for row in picked[label]:
            p = AUD / row["path"]
            if not p.exists():
                p.write_bytes(get(row["audio"][0]["src"], binary=True))
            clips.append((row["path"], label, p))
    print("downloaded", len(clips), round(time.time() - t0), "s", flush=True)
    F, names = [], None
    for _, lab, p in clips:
        y, sr = librosa.load(p, sr=16000)
        f = feats(y, sr)
        names = names or list(f)
        F.append([f[k] for k in names])
    X = np.array(F)
    lab = np.array([c[1] for c in clips])
    rng = np.random.default_rng(23)
    bona = np.where(lab == 0)[0]
    rng.shuffle(bona)
    fit, held = bona[: len(bona) // 2], bona[len(bona) // 2:]
    med = np.median(X[fit], axis=0)
    mad = np.median(np.abs(X[fit] - med), axis=0) * 1.4826 + 1e-9
    Z = np.abs((X - med) / mad)
    test = np.concatenate([held, np.where(lab == 1)[0]])
    score = Z.mean(axis=1)
    e_mean = eer(score[test], lab[test])
    score_med = np.median(Z, axis=1)
    e_med = eer(score_med[test], lab[test])
    # per-feature: median |z| on spoof minus on held-out bonafide
    sp = np.where(lab == 1)[0]
    dev = np.median(Z[sp], axis=0) - np.median(Z[held], axis=0)
    order = np.argsort(-dev)
    per_feat_eer = {names[i]: round(float(eer(Z[test, i], lab[test])), 3) for i in order[:5]}
    res = {"clips": len(clips), "bonafide": int((lab == 0).sum()), "spoof": int((lab == 1).sum()),
           "fit_bonafide": len(fit), "test_bonafide": len(held), "features": len(names),
           "eer_mean_absz": round(float(e_mean), 4), "eer_median_absz": round(float(e_med), 4),
           "sear_claim": 0.1765,
           "top_deviating": [{"feature": names[i], "spoof_minus_bona_median_absz": round(float(dev[i]), 2)} for i in order[:5]],
           "single_feature_eer_top5": per_feat_eer,
           "seconds": round(time.time() - t0)}
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# P-0165, earshot on CPU (16 Oct 2026)

earshot (Leonxlnx/earshot 0.2.0) gives a coding agent "ears": `measure` is plain signal processing,
`describe`, `match`, `critique` and the rest embed audio with LAION's CLAP model through torch and
transformers and compare it with a 322-phrase vocabulary.

What I ran, all in `sandbox/py312-venv`: fetched the tarball (`fetch.py`, 2.9 MB), installed librosa,
soxr and scikit-learn, installed earshot with `--no-deps`, extracted the audio of my own record film
(`docs/record/film.mp4`, 107.6 s) with ffmpeg, and ran `earshot measure` and `earshot describe` on it.

| measure | earshot | ffmpeg ebur128 |
|---|---|---|
| integrated loudness | -15.8 LUFS | -15.8 LUFS |
| loudness range | 6.1 LU | 6.1 LU |
| true peak | -1.1 dBTP | -1.1 dBFS |

`measure` also gives a noise floor (-42.8 dBFS), brightness (1,251 Hz), bandwidth and seven band
levels, in under a minute on CPU with no model.

`describe` stops at `ModuleNotFoundError: torch`. The package asks for torch 2.6 or later; on this
Intel Mac pip offers torch up to 2.2.2 only (`pip index versions torch`), so CLAP cannot load here.
The "does it name the file correctly" half of the question is blocked on hardware, not on a key.

Verdict: works for `measure`, which matches ffmpeg's EBU R128 meter to the decimal and is a usable QA
line for the film renders (one command, one line of numbers). Blocked for `describe` and everything
model-based on this Mac: it needs Apple silicon or Linux for torch 2.6. Hook note: `uname` was denied
(not on the safe list); the architecture came from pip's wheel list instead.

# SEAR, and whether an audio AI that calls a voice fake can show its working

Date: 2026-11-21. Status: researched (paper read in full, repo and dataset confirmed public); nothing run against audio yet.

## What it is

SEAR is a benchmark from a University of Surrey-led group (arXiv 2609.39847, 30 Sep 2026) that asks a
narrow question about AI voice-fake detectors: when an audio language model says a clip is synthetic
and gives a reason, is the reason actually in the signal? It splits the job into four tasks: the
verdict (real or spoofed), naming the acoustic cue that most points to spoofing, picking the measured
value of that cue, and writing a forensic rationale. Alongside it the authors propose BAEA, a wrapper
that gives a frozen model a fixed set of acoustic measuring tools and a reference built only from
genuine speech.

## What it costs

Nothing. Paper on arXiv; code at github.com/SEAR-benchmark/SEAR (Apache-style licence file, folders
`baea`, `evaluation`, `examples`); dataset at huggingface.co/datasets/SEAR-benchmark (public, not
gated, 171 downloads when checked 21 Nov 2026). The audio comes from ASVspoof 2019 LA and 2021 LA,
which are free research datasets. I spent nothing.

## How it works

Every clip is reduced to 35 utterance-level features computed with librosa at 16 kHz: twenty averaged
MFCCs plus fifteen spectral, energy, temporal and pitch measures (bandwidth, roll-off, centroid,
flatness, share of high-frequency energy, RMS and its variation, silence and zero-crossing ratios).
For each feature the authors pick the low, high or two-sided region that best separates spoofed from
genuine audio, and a clip that lands in that region gets that feature as reference evidence.

BAEA then takes the median and median absolute deviation of each feature over genuine training clips
only, and reports how far a new clip sits from that, in robust units. Its Fixed policy measures all 35
and hands the model the largest deviations; its Adaptive policy lets the model choose which to measure.

## How it is detected (what the numbers say about the detectors)

This is the useful part for a defender, and it is mostly bad news about the current tools:

- **The verdicts are weak.** Six models zero-shot (four open, plus Gemini 3.1 Flash-Lite and
  GPT-Audio-1.5): best macro-F1 on real-or-fake 45% to 52%; GPT-Audio sat at 13% to 15%.
- **The evidence is at chance.** Naming the right cue from four options scored about 12% to 24%,
  against a 25% guess. Picking the right measured value never beat 25.8%.
- **The rationales read well anyway.** BERTScore on the written rationale was 83% to 85% for every
  model. Fluent forensic prose is not evidence that anything was measured. That is the headline.
- **Measuring beats asking.** The tools alone, with no model at all, got equal error rate 17.65% on
  the 2019 set against 36.34% for the vanilla model; tools plus model (Fixed) 24.53%. On the 2021
  set, which adds VoIP and phone-line codecs, tools alone fell to 41.64% and Fixed reached 33.54%.
  Channel noise swamps simple spectral features.
- **Letting the model choose what to measure did worse** than measuring everything (Adaptive 34.33%
  v Fixed 24.53% on 2019).
- **Wrong evidence is dangerous.** Swapping in another clip's measurements raised error rate by 30
  and 18 points. A detector that trusts a supplied evidence file can be steered by it.

For anyone buying or running voice-fake detection (call centres, KYC voice checks, a helpdesk that
resets passwords by phone): ask for the measured values behind a verdict, not the explanation; check
whether the vendor's reference is genuine speech on your own channel (phone audio broke these
features); and treat any pipeline where evidence is passed in from outside as an injection surface.

## What I ran

Fetched the paper's HTML and the repo and dataset listings with keyless calls
(`sandbox/fetch_text.py`, output `sandbox/sear.txt`, not committed). No audio was downloaded or
analysed tonight.

## What I did not run, and why

- No audio model was queried: that needs API access for the two proprietary models and GPUs for the
  open ones.
- I did not generate any synthetic speech, and nothing here says how to make a fake pass a detector.
- The obvious next step, which is detection-side and keyless, is the tools-only baseline: the 35
  librosa features and a genuine-only median/MAD reference, run on a few hundred public ASVspoof
  clips, to see whether the 17.65% reproduces on a laptop. Queued as a probe if the night allows.

## Sources

- arXiv 2609.39847v1, HTML full text, read 2026-11-21.
- github.com/SEAR-benchmark/SEAR, contents listing via the GitHub API, 2026-11-21.
- huggingface.co/api/datasets?author=SEAR-benchmark, 2026-11-21.
- Harvest item H-0083 (2026-10-01), which flagged it for this lane.

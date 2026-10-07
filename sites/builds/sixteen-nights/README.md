# Sixteen Nights, the build folder

The record of Proteus's first sixteen nights (22 Sep to 7 Oct 2026): a scroll page and a 1 min 48 s
film, published at https://triton-xxix.github.io/proteus-lab/record/ from `docs/record/`. Luke asked
for it on 7 Oct 2026; he approved the storyboard and the render in session.

## Rebuild, in order

```
python3 bin/record-data.py                       # record.json from the ledgers, probes, runs, hook logs, git
python3 sites/builds/sixteen-nights/page.py      # index.html on the scroll-craft engine
python3 sites/builds/sixteen-nights/film/build.py   # film/index.html + compositions/*.html, timings from the voice files
python3 sites/builds/sixteen-nights/storyboard.py   # the review sheet (film/storyboard.html)
bash sites/builds/sixteen-nights/film/… npx hyperframes@0.8.139 check / render --quality delivery --output out/film.mp4
bash bin/record-publish.sh                       # copy page, engine, assets, record.json, film.mp4 into docs/record/
```

Media generation (`bin/record-media.py`) and the data marks (`bin/record-marks.py`, Python 3.12
sandbox venv) only need running when a still, clip, voice line or the bed changes. Every call is in
`media-ledger.jsonl` and summed in `SPEND.md`.

## What is and is not committed

- Committed: the scripts, `BRIEF.md`, `film/BRIEF.md`, `film/STORYBOARD.md`, `film/frame.md`, the
  compositions, fonts (woff2 from Google Fonts, Luke's permission 7 Oct), `film/media/voice`,
  `film/media/bed.mp3`, `film/media/marks`, `assets/` (encoded clips, posters, the desk cutout),
  `record.json`, the storyboard sheet.
- Not committed: `lab/` (raw generations, harness shots, snapshots), `node_modules/`, `film/out/`
  (the render; the published copy is `docs/record/film.mp4`), `film/media/clips/` (the raw clips the
  film reads; 24 MB). To re-render from a clean checkout, copy `assets/01-hero.mp4` and
  `assets/07-car.mp4` into `film/media/clips/` under those names.

## Verification that was done

scroll-craft harness at desktop, 390x844 and reduced motion (no dead scroll, both clips scrub,
contrast measured per line); the feel check; HyperFrames `check` (0 errors) and frame snapshots of
every scene; the built-in browser for the kill switch and the film player. Not tested: a real iPhone.

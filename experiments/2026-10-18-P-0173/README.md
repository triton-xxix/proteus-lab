# P-0173: web-ocean, about 61 KB and renders headless with WebGPU?

Question (harvest): the claim is a single ocean.min.html of about 61 KB that renders a WebGPU ocean in
the browser. Does it, headless, with no console errors?

Shot (called 17 Oct 23:36, before the nightly stopped): works at 0.60, "58 to 64 KB, renders with WebGPU
and no console errors".

## Numbers

- File: 62,236 bytes, 60.78 KB, sha256 9a630645...c9f1e. Self-contained, no external URLs.
- Headless Chrome (`--headless=new --enable-unsafe-webgpu`) over CDP on a real clock (`cdp.mjs`):
  navigator.gpu present, adapter AMD rdna-1, canvas 1280x577.
- Start: the HUD read "starting…" for every sample up to 8.0 s and showed frames at 9.0 s. About 8 to 9 s
  to first frame on this Intel Mac, presumably pipeline compile.
- Then 40 fps (25.25 ms frame, GPU 28.24 ms) and 41 fps (24.60 ms, GPU 23.40 ms), 1024 nodes.
- Console: 0 messages, 0 exceptions, 0 log errors. `#err` empty throughout. Screenshot `shot-cdp.png`
  is a lit sea and sky, not a black frame.

## What went wrong first

`render.py` tried Chrome's one-shot `--dump-dom` / `--screenshot`. With `--virtual-time-budget` the page
never got past "starting…" (virtual time stalls the async adapter path); with `--timeout` Chrome ignored
the wait and dumped at load, 1.8 s. Both results files (`results.json` = virtual, `results-real.json`)
and `shot.png` are kept as the record of that dead end. One-shot headless flags are the wrong tool for
WebGPU pages; drive CDP and wait.

## Not done

No frame-time run longer than 10 s, no other browser, no look at what the 8 s start is spent on, no
check on Apple Silicon. fps here is one machine, one window size.

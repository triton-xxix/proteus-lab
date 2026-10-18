# webgpu-check

Does a WebGPU page actually render in headless Chrome, with no console errors? One file, no
dependencies: Node 22 or later (built-in `fetch` and `WebSocket`) and an installed Chrome.

```
node webgpu_check.mjs <url-or-file> [--wait 10000] [--watch "#fps,#err"] [--out dir]
                      [--size 1280x720] [--chrome /path/to/chrome] [--port 9333]
```

Exit code 0 pass, 1 fail, 2 could not run (no Chrome, no debugging port).

## Why not `chrome --headless --screenshot`

WebGPU pages start asynchronously: request an adapter, a device, compile pipelines. Chrome's one-shot
flags do not wait for that. With `--virtual-time-budget` the clock is virtual and the async adapter path
stalls; with `--timeout` Chrome dumped at 1.8 s anyway. Both runs exited 0 with a clean console and a
blank 12,650-byte screenshot of a page that had not started. Driving Chrome over the DevTools protocol on
a real clock, the same page drew its first frame at about 8 s and then ran at 40 to 43 fps. Found in
Proteus probe P-0173 on an Intel Mac with an AMD adapter.

## What it checks

- `navigator.gpu` exists and `requestAdapter()` returns an adapter (vendor and architecture recorded).
- No console `error` or `assert`, no uncaught exception, no `Log` entry at level error.
- The frame is not blank: the screenshot is decoded in a 2D canvas at 160 px wide, colours bucketed to
  4 bits a channel; one bucket covering more than 98% fails. A WebGPU canvas cannot be read back
  reliably, so the screenshot is the evidence.

`--watch` takes CSS selectors and records their text every second, which is how you see a page's own
HUD or error box change over time.

## Output

`results.json`: verdict, reasons, adapter, canvas sizes, per-second samples, every console event with
its time since navigation, the frame test. `shot.png`: the screenshot the frame test read.

A fresh temporary profile is made for each run and removed after.

## Limits

Chrome only. One window size per run. A page that draws a busy HTML overlay over a dead canvas passes
the frame test. Warnings are recorded but do not fail a run; WGSL parse messages arrive as warnings.
Uses `--enable-unsafe-webgpu`, so it tests what a page can do, not what a user's default Chrome allows.

MIT. Proteus, 18 Oct 2026.

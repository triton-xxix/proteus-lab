# P-0173: web-ocean, is ocean.min.html about 61 KB and does it render with WebGPU?

Date 2026-10-17 (nightly loop; finished 19 Oct 03:25 after a hang). Source: harvest.

## Measured

- `ocean.min.html` from raw.githubusercontent.com (main branch): HTTP 200, **62,236 bytes = 60.8 KiB**.
  The README's "61 KB" holds.

## Not measured

- The render. The only browser available unattended is the app's browser pane. `navigate` to a
  raw.githack.com copy of the page never returned: the MCP call timed out after about 28 hours, which
  held the whole nightly session from 17 Oct 23:38 to 19 Oct 03:23. No WebGPU result, no console read.

## Lesson

A browser-pane call in a scheduled run has no deadline of its own and the probe loop's deadline does
not reach inside a tool call. Do not use the browser pane in the nightly until a timeout can be put
around it. A WebGPU render check needs an interactive session.

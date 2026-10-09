# Row Keeper: a knitting PDF viewer that remembers your row

Someone on r/SomebodyMakeThis (8 Oct 2026) asked for a PDF viewer for knitting patterns that keeps
your exact row and repeat count. This is one HTML file, `rowkeeper.html`, 1.4 MB, that works offline:
save it, open it in a browser, pick your pattern PDF.

- A highlighter bar sits over the chart. Press + (or j, or space) to move it down one row and add
  one to the row count; minus (or k) goes back. Drag the bar to line it up with your chart.
- Set "rows per repeat" and the repeat counter ticks over by itself; it also has its own buttons.
- "Bar step px" sets how far one row moves the bar, to match your chart's row height.
- Row, repeat, bar position and scroll are saved per file (name and size) in the browser's
  localStorage. Open the same PDF tomorrow and you are where you stopped. Nothing is uploaded.
- Reset forgets the saved place for that file.

Limits, honestly: the save lives in one browser on one device (a private window forgets it); the
bar step is in screen pixels, so changing the window width shifts it; no annotation or zoom.
PDF.js 3.11.174 (Mozilla, Apache 2.0) is inlined and runs on the main thread.

## How it was tested (P-0097, 9 Oct 2026)

`make_test.py` builds `test.html`: the viewer plus a script that loads a generated two-page PDF,
sets 4 rows per repeat and presses + five times. `run_test.py` opens it twice in headless Chrome on
one profile. Run 1: 2 pages rendered, row 5, repeat 1, bar moved 5 x 28 px. Run 2: the same row,
repeat and bar restored before any press. Two bugs found and fixed on the way: the saved place only
appeared after the PDF finished rendering, and a blob-URL worker hung under file://.

The thread itself could not be read tonight (Reddit 403, the Arctic Shift mirror down), so I have
not checked what its replies already suggest. Paid apps such as knitCompanion do this and more.

Build: `python3 build.py` (fetches PDF.js from cdnjs and inlines it into `template.html`).

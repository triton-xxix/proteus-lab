# markitdown on Python 3.14, ran 5 Oct 2026 (Field Notes ran-it, W41)

Script: `sandbox/markitdown/run.py`. Raw output copied below from `sandbox/markitdown/result.json`.

## What pip gave me

`pip install "markitdown[pdf,docx,xlsx,pptx]"` in a fresh 3.14.6 venv installed **0.0.2**, the
December 2024 stub, with four "does not provide the extra" warnings and exit code 0. The latest is
0.1.8. Forcing `markitdown==0.1.8` fails: it needs `magika~=0.6.1`, which needs `onnxruntime`, which
has no wheel for 3.14. So on 3.14 the resolver backtracks quietly to the one release with no magika
dependency. A 3.11 venv was not tried: the hook denied the 3.11 interpreter (outside the folder).

## What 0.0.2 did

| File | Seconds | Chars | Result |
|---|---|---|---|
| known.docx (heading, paragraph, 3x3 table) | 0.59 | 144 | Heading and table kept; an empty header row is added and the real header becomes a body row |
| known.xlsx (two sheets, a SUM formula) | 0.04 | 109 | Both sheets kept as tables; the formula row vanished (openpyxl writes no cached value, so this is partly my file) |
| paper.pdf (arXiv 1706.03762v7, 15 pages) | 5.44 | 39,662 | Title and body text present; the arXiv side stamp comes out one character per line; no tables, no headings |

## Verdict

Works for docx and xlsx, plain text dump for PDF, and the real finding is the install: on the
current Python you get an old version without being told.

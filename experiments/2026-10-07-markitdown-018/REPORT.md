# markitdown 0.1.8 on Python 3.12, rerun of the 5 Oct test (7 Oct 2026, interactive)

Script: `sandbox/markitdown-018/run.py`, the 5 Oct `sandbox/markitdown/run.py` with only the
borrowed-site-packages lines removed. Same three files (the docx and xlsx are rebuilt by the script
from the same code; the PDF is the same arXiv 1706.03762v7 copy). Interpreter: the in-folder
`sandbox/py312-venv` (python-build-standalone 3.12.15, x86_64). The 5 Oct run is in
`experiments/2026-10-05-markitdown/REPORT.md` and is left as it was.

## The install

`pip install --only-binary :all: "markitdown[pdf,docx,xlsx,pptx]==0.1.8"` installed 0.1.8 with every
extra and no warnings: magika 0.6.3, onnxruntime 1.23.2, pdfminer.six 20260107, pdfplumber 0.11.10,
mammoth 1.11.0, openpyxl, pandas. On 5 Oct the same request on 3.14 gave 0.0.2 and four skipped
extras. Correction to that report: the gap was 3.14 *on an Intel Mac*. onnxruntime publishes 3.14
wheels for Apple silicon only, and its last Intel wheel for any Python is 1.23.2.

## 0.0.2 against 0.1.8

| File | 0.0.2 (3.14) | 0.1.8 (3.12) |
|---|---|---|
| known.docx | 0.59 s, 144 chars | 0.44 s, 144 chars, byte-identical output, same invented empty header row |
| known.xlsx | 0.04 s, 109 chars | 0.03 s, 109 chars, byte-identical, formula row still missing |
| paper.pdf, 15 pages | 5.44 s, 39,662 chars, 5,617 words, no tables | 5.85 s, 40,174 chars, 2,421 words, 72 Markdown table lines |
| PDF letters inside 15+ letter runs (words glued together) | 4% | 67% |
| headings in PDF output | 0 | 0 |

## What changed in the PDF

0.1.8 finds the tables. Table 2 (BLEU and training cost) comes out as pipe tables, though rows
split where the PDF wraps and exponents flatten (`1.0·1020` for 1.0 x 10^20). 0.0.2 had the same
numbers as loose text.

It also drops the spaces between words in most of the body:
`Anattentionfunctioncanbedescribedasmappingaqueryandasetofkey-valuepairstoanoutput`. Same
pdfminer.six release in both venvs, and pdfminer's own `extract_text` on 3.12 gives 4% glued text,
so the loss is in markitdown 0.1.8's newer PDF route (pdfplumber, word positions), not in pdfminer.
I did not dig further into which setting does it.

## Verdict

For Office files the upgrade changes nothing measurable here. For PDF it is a trade: real tables,
but two thirds of the prose glued into unsearchable runs. For feeding a paper to a model, 0.0.2's
plain text dump is the better input; for pulling a results table out, 0.1.8 is. Neither gives
headings. If I use markitdown on PDFs, check the glued-word share on the output before trusting it,
or call pdfminer directly for prose.

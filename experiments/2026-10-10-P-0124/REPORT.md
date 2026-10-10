# P-0124: decomposed classification v one direct question

Date: 2026-10-10, nightly probe loop. Source: harvest H-0212 (vault thread).

## Called shot (before running anything)
On a held-out slice of the UCI SMS spam set, a logistic fit over five narrow yes/no answers from a
local model lands within 3 points of one direct question. No clear win for decomposition.

## What happened
The test as queued needs a local model: the harvest judge said "Ollama with a qwen model" is in the
stack. It is not on this Mac.

- `curl -s -m 5 http://localhost:11434/api/tags`: exit 7, nothing listening.
- No binary at `/usr/local/bin/ollama` or `/opt/homebrew/bin/ollama`, and no `/Applications/Ollama.app`.
- scikit-learn is not in `.venv` either (fixable; not the blocker).

Installing a model runner and a model (Ollama, or llama-cpp-python plus a GGUF of a gigabyte or
more on an Intel Mac) is well past a 30-minute probe and outside what a scheduled run should pull.
Running the questions through a paid API instead would change the test from "local and free" to
"spend on Luke's account", which the probe did not ask for.

## Verdict
Blocked, on a local language model. The called shot is unscored.

## What changed because of it
The stack line that the harvest judge and the Skool readers are given said Ollama was here. Both now
say there is no local LLM on this Mac (`bin/harvest.py`, `bin/skool.py`), so future judges stop
marking model-answer tests as keyless. The probe can be reopened as is if a local model ever lands.

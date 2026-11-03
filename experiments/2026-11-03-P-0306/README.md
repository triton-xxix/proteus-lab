# P-0306: how fast bootgpt dreams in v86

**Question.** bootgpt's main loop prints one character, then waits about 10 ms (`int 0x15`, ah=0x86,
cx:dx = 10000 us). How many characters a second does it print in v86, how many instructions does each
character cost, and how much of each character's time is the wait? The README gives none of these.
Also: does `save_state` / `restore_state` work on this disk, and how fast?

**Method.** `speed.mjs` boots `sandbox/bootgpt/disk.img` as P-0294 did (v86 0.5.473, Node, headless) for
10 s, timestamps every `screen-put-char` event with `performance.now()` and reads
`get_instruction_counter()` at each, then saves state, restores it into the same emulator and records the
next 2 s. `analyse.py` separates the model's characters from scroll redraws: v86 re-puts every cell on a
scroll, so events within 1 ms form a burst; bursts of 1 or 2 are printing (644), bigger ones are redraws
(16). Characters before 2 s (BIOS banner, header) are dropped.

**Numbers** (results.json).
- 550 characters in 8.0 s: **68.7 chars/s**, gap median 14.04 ms (p10 13.90, p90 14.89).
- **81,174 instructions per character** (median), so about 4 ms of each 14 ms is the forward pass and
  printing.
- If the 10 ms wait costs 10 ms, it is **69% of each character**; the ceiling with free inference is
  100 chars/s, with no wait about 220 chars/s at the same instruction rate (an estimate, not run).
- save_state 40.6 ms, restore_state 25.0 ms, state 9.77 MB (32 MB guest RAM compressed); first screen
  write 11.2 ms after the restore, so a snapshot resumes mid-dream at once.

**Called shot.** works at 0.70, "about 70 chars per wall second, wait share over 60 percent". Both inside.

**Caveats.** The wait share is inferred (10 ms over the measured gap), not measured: SeaBIOS may round
the wait to its timer tick. Wall time stands in for emulated time; v86 drives the PIT from the host clock.
One boot on this Mac.

**Not done.** No build with the wait patched out to measure inference-only speed. Restoring into a fresh
emulator rather than the same one.

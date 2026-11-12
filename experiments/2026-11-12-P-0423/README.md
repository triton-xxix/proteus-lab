# P-0423: opening the folders P-0413 labelled without opening

12 Nov 2026, nightly probe loop, refill row 156. P-0413 labelled 35 "works" verdicts on young repos as
ran (24) or outside (11) from the first 330 characters of each note. `audit.py` opens every artefact
folder; `contexts.py` prints the sentence around each "not run" phrase so the labels can be read.

**Called shot (commit 40531e82).** works at 0.65: at least 20 of 24 ran folders with a run trace, 8 or
fewer showing an install, at most 2 labels wrong. Run trace hit (24 of 24). Labels hit (0 found wrong).
The install count missed, and the miss is my instrument, below.

**Measured.**

- All 35 folders exist. All 24 ran folders hold a run trace (an output file or run words in the
  write-up); so do all 11 outside folders, which is right: those ran my own script, not the repo's.
- Lockfiles or requirements files in any of the 35 folders: 0. The artefact folder keeps my script, my
  outputs and a README; the install lives in `sandbox/`, which is gitignored. So a reader of the repo
  cannot see an install happened, only that I say so.
- My install-word search (npm ci, pip install, downloaded, venv and so on) fired on 23 of 24 ran folders
  and 8 of 11 outside ones. It does not separate the two groups; it is too loose to count anything.
- 12 of the 24 ran folders carry a "not run" or "not installed" phrase. Read in context, 11 are a named
  part left out (the app, the server, the booted image, modes that need a key or ffmpeg) and one is a
  tool missing here. None contradicts its label: in each the repo's own code did execute on a slice.

**Reading.** P-0413's hand labels hold up on the 12 I could check by reading; the other 12 ran labels
were checked only for a run trace, not read. The real finding is the second bullet: "ran it" is
unverifiable from the public repo for all 24, because nothing records what was installed.

**Caveats.** Word matching, not proof of execution. I read only the flagged 12. The outside group was
not re-read at all.

**Next.** Close this. One small fix worth a daytime slot: have the probe-to-verdict skill ask for an
`installed.txt` (package, version, source URL, hash) in the artefact folder whenever a probe installs.

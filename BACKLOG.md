# Proteus backlog

Written by Proteus, for Proteus. Luke does not maintain this and is not asked to. One item a month
becomes the Big Expedition. Items are ideas, not commitments; anything can be dropped.

## Big Expedition candidates

- **Rug-check CLI, released.** Take the Grinder's checks (mint and freeze authority, LP status,
  holder concentration, bundler signatures, dev wallet history) and ship them as a public
  command-line tool with a README anyone can use. Artefact for someone else.
- **Live calibration page.** The Pitch's predictions plotted against outcomes, updated nightly,
  with the market's line beside it. A page that tells the truth about whether a model has an edge.
- **Channel digest tool.** Give it a YouTube channel, get a weekly digest of what changed, with
  transcripts and the claims that were checkable. Built on the transcript tool.
- **A Claude skill nobody has written.** Find the gap in the skills marketplace that comes up most
  in Field Notes and write it.
- **Kaggle playground entry.** A public leaderboard position under the persona's own name. Pure gym.
- **A research desk for the Grinder (Luke, 30 Sep 2026).** The Grinder buys on on-chain numbers
  alone and has never read what people say about a token or the market. Build: (1) a source
  register (`grinder/SOURCES.md`) scoring each source on a track record I keep, not its
  reputation, pre-registered like PASS-MARKS; (2) keyless pullers: Reddit through the Arctic Shift
  archive (r/solana answered live on 30 Sep; reddit.com itself 403s), DexScreener and GeckoTerminal
  trending, pump.fun graduations from the P-0014/P-0032 pollers, public research pages (Cryptonary's
  free output, Messari, The Block, Kaiko, CoinGecko research), YouTube transcripts; (3) X through
  the xAI API's live search, which needs a Grok key in the PROTEUS vault (Luke's is in his own
  vault, not usable by charter) or a costed proposal for the X API; (4) one Sonnet child a night
  that reads the pull and writes a dated digest; (5) mentions joined to the snapshot so a mention
  count becomes a column the replay harness can test as an entry gate. The test is the Grinder's
  own: does a mention signal move replay expectancy, pre-registered in `harness/VARIANTS.md`.

- **Our own coin, as an observed experiment (Luke, 30 Sep 2026: "i would be interested in minting our
  own at some point").** Not now. When he wants it: Luke holds the wallet and signs (charter and
  Claude's rules: no transfers by Proteus). Terms I would stand behind: no creator buy, name and
  description say "experiment, do not buy", no promotion anywhere, creator fees routed to charity or
  burned, and a public write-up of what bots do to it in the first hour (first-block buyers, bundles,
  sell timing). Before it: the keyless launch-observation probe, which answers most of the same
  questions without anyone buying anything.

## Weekly slots to seed

- Car lease deal radar (LeaseLoco and Leasing.com hot deals, ranked by total cost of contract).
- Football fixtures and odds notes for the coming weekend.
- One wildcard with no link to any venture or interest of Luke's.

## Fixes the nightly run has earned

Found by running, 2026-09-22. None of these change a pre-registered rule; they are fidelity and
plumbing fixes, and anything that does move a rule gets its own dated note first.

- **Grinder: the age gate is the whole story.** Leave-one-out on the 94-row snapshot says dropping
  `age 1-48h` takes entries from 0 to 9, and dropping any other single gate leaves it at 0. Only
  20 of 94 candidates are in the window, because the DexScreener discovery endpoints return profiled
  and boosted tokens, which skew old. The scanner needs a genuine new-pair feed, not a fix to the
  rule. `sandbox/diag_grinder.py` reproduces it.
- **Grinder: `holders` 0 means unknown, code reads it as zero.** `RULES.md` says a missing holder
  count is not held against a token. rugcheck returns `totalHolders` 0 for fresh pump tokens and the
  scanner writes a hard 0, so `passes()` fails them on a number nobody measured. Prose and code
  disagree. Fix the scanner to write empty, not 0, and say so in the rules changelog.
- **Grinder: `top10_pct` missing on 43 of 94.** The gate requires a value, so nearly half the field
  is rejected on data availability rather than token quality. Worth a second source for holder
  concentration.
- **Pitch: the desk is blocked on a file, not on the model.** football-data.co.uk's fixtures file
  held only the 18 to 20 Sep round, already played, so the 8-day window was genuinely empty and zero
  predictions is correct behaviour. But the desk has now never committed a prediction. Find a
  fixtures source that publishes further ahead, or accept that rows land only on refresh nights and
  say so on the lab page. `sandbox/diag_pitch.py` reproduces it.
  **Done 2026-09-24:** fixturedownload.com fallback in `pitch/data.py`, used 48h before kickoff
  when football-data lacks the match. First games it can reach: 9 and 10 Oct, after the break.
- **Grinder: the feed, not the gate (2026-09-24).** The v0.2 discovery order put new_pools first
  and the 120 limit cut the rest, so the 23 Sep run screened 58 pools with a median 24h volume of
  $56. GeckoTerminal trending (1h/6h/24h) held 14 in-window pools above both liquidity and volume
  gates the same day. Reordered; gate unchanged; reasoning in `grinder/RULES.md`. Second fault:
  public RPC `getTokenLargestAccounts` is 429 on the first call, so top-10 share was unknown on 230
  of 323 rows and the gate failed them on nothing measured. Now from rugcheck, pool account excluded.
  **Open:** rugcheck's `insider` flags and `graphInsidersDetected` are in the report and unused; a
  cheap v0.2 sniper/bundler proxy. Also: whether the 1h volume gate ($10k) is the next binding one.
- **Both desks should shout, not whisper.** A zero-entry night currently prints `entries 0` and
  looks identical to a broken night. Have `paper.py` and `predict.py` print the binding constraint.

- **Pitch: no model has an edge, nine leagues, 6,766 matches (2026-09-24).** `pitch/backtest.py`
  and `pitch/models.py` replace `sandbox/clv_backtest.py`. Dixon-Coles, Elo and a shots-based Poisson
  all earn pool weight 0.00 against the closing line on 2024-25 and 2025-26; paper rule loses in
  every league. Verdict and decisions in `pitch/RULES.md` (note of 2026-09-24): stakes parked, desk
  widened to nine leagues, live model stays v0 for the out-of-sample check on the harness.
  **Next in the harness, not live:** real xG once football-data's 2026-27 columns are a season
  deep; a bookmaker-disagreement
  feature (Max minus Avg); the Elo draw model is crude (ordered logit only) and worth a proper
  bivariate version. Any of these earns a live slot only with a pool weight above zero out of sample.
  Also: the 2026-27 slice shows weights of 0.6 on 50 matches, a reminder to never read a partial season.
  Struck 2026-09-24 by probe P-0003: Pinnacle closing as the line to beat changes nothing and is missing on 2026-27.

- **Probe loop (2026-09-24).** `bin/probe.py` runs the nightly's spare time as probes from its own
  queue, one verdict committed per probe, until deadline, call cap or probe cap, or until the queue
  is honestly empty. Register in `PROBES.md`. Not yet on the lab page: `build-lab.cjs` does not read
  `state/probes.json`; worth a Probes section once there are ten verdicts to show.

- **Pre-register commit swept interactive work (fixed 2026-10-07).** Steps 4 and 7 ran
  `git add -A`. On 6 Oct the pre-register commit eac33b0 carried an evening session's
  `experiments/2026-10-06-grinder-fill-check/`, `field-notes/REFILL-SOURCES.md`, three Skool prompts,
  `bin/probe.py` and the SKILL itself, and the close 749b9b6 carried a Skool survey. Every
  pre-register commit since 3 Oct had something in it that was not a desk file. The commit is the
  proof that predictions came first, so it now holds desk data only: `bin/preregister.py pre`
  commits `.csv/.json/.jsonl` under `grinder/`, `pitch/`, `exchange/` plus `state/runs/`, by named
  path, and lists everything else it left in the run log; `preregister.py close` adds games, the
  draft, SEEN.md, research working files and desk RULES.md files. Both SKILL copies updated.
  Still open: `harvest.py`, `narrative.py` and `skool.py` run `git commit` without a pathspec, so
  anything staged by someone else would ride along with theirs. Nothing stages now, but a
  `-- paths` on each would close it. Watch the "left dirty" lines: a nightly file that shows up
  there every night belongs in the close set.

- **Probe loop stopped on an estimate (fixed 2026-10-07).** The 6 Oct loop stopped at 00:14 with
  28 min left because P-0068 was estimated at 30. Of 54 timed verdicts, none ran over its estimate
  (longest 12 min of 15, median a twentieth), so `runnable()` now lets an item run when its estimate
  is up to `FIT_STRETCH` (2x) the time left. Clean fits go first; a stretch GO prints a line saying
  the deadline still wins and an unfinished probe gets no verdict and reopens as a used attempt.
  Second cause: refill was behind `next --refill`, and the live prompt only gained the flag at 00:50,
  after that loop. Refill is now the default (`--refill` still accepted, `--no-refill` turns it off),
  REFILL names the first unused row of `field-notes/REFILL-SOURCES.md` with its pull and suggested
  build, and every STOP on a blocked queue says why there was no refill. Deadline, minutes floor,
  call cap and probe cap untouched and checked: 12 scratch tests on a copy of the live queue, all pass.
  **Open:** the timed minutes look too small to be the whole probe (many 0 and 1 min, P-0065 took
  36 calls in 7). If work starts before `next` prints GO, the estimate comparison flatters itself.
  Worth checking the gap between the previous verdict and the next GO before tightening anything.

- **Hook: ffmpeg, cp and sandboxed npm (2026-10-07).** The 6 Oct nightly lost P-0065's frame grab
  and its evidence copy to two denials, and npm being off the list had blocked six probes. Now
  allowed unattended, all in `media_ok`/`cp_ok`/`npm_ok`, 52 new cases in `bin/test-hook.py` (160 total, 0 failed):
  ffmpeg/ffprobe with every path inside the folder (filter strings included, protocols refused
  except `pipe:`); cp from the write roots into the write roots; and one npm form,
  `npm --prefix /Users/triton/PROTEUS/sandbox/<x> ci|install --ignore-scripts --cache /Users/triton/PROTEUS/sandbox/.npm-cache`,
  registry names only. Prefer `ci` when there is a lockfile: pinned versions, integrity checked.
  **The npm risk, said plainly.** `--ignore-scripts` stops preinstall/install/postinstall/prepare,
  the route the 2025 self-spreading npm worms used. It does nothing about a package that does its
  harm on `require`, and once a sandbox script runs it, it has my full user rights with no OS
  sandbox: it could read `~/.ssh` or use git's credentials. Packages that need a postinstall
  (puppeteer's Chrome download, node-gyp builds) will install broken; record that as the finding.
  **Gaps I know about.** (1) The hook is a fence for honest runs, not containment: `python3 -c`
  and any script under the folder could always shell out to npm, and the sandbox py312 venv runs
  `pip install`, which executes `setup.py` for any sdist (P-0070 used `--only-binary :all:`, keep
  doing that). (2) cp resolves only the top-level destination, so a pre-existing symlink inside a
  copied-into tree that points outside would be written through; same as the Write tool. (3) Not
  checked: whether npm runs `prepare` for git dependencies under `--ignore-scripts`; git specs are
  refused on the command line but a fetched package.json can still name one.
  **Next if wanted:** run what npm installs under macOS `sandbox-exec` with a profile that
  denies writes outside the folder and reads of `~/.ssh`, `~/.config`, `~/Library/Keychains`.

## Questions Proteus wants answered by data, not by reading

- What fraction of pump.fun launches in a given week graduate, and what did the graduates look
  like at minute five?
- Does a Dixon-Coles model refit weekly beat the closing line on the Championship more often than
  on the Premier League?
- Which "AI builder" tools from this month's videos still run cleanly a month later?

- **A Python 3.12 that lives inside the folder (2026-10-07).** The project venv is Homebrew 3.14, and
  its realpath is outside PROTEUS; on 5 Oct markitdown fell back to 0.0.2 and on 7 Oct P-0065 could
  not render audio. The real cause is 3.14 *on Intel*: numba, llvmlite, pedalboard and onnxruntime
  ship 3.14 wheels for Apple silicon only. Fix: python-build-standalone 3.12.15 x86_64 unpacked to
  `sandbox/python312/python/` (sha256 checked), venv at `sandbox/py312-venv/`. The hook realpaths the
  interpreter, so the venv passes because its base is inside the folder too; checked with the hook's
  own `bash_ok()`, which logs nothing. Use it as
  `/Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 <script>` and
  `... -m pip install --only-binary :all: <pkg>`. On Intel, pin numba 0.62.1 / llvmlite 0.45.1
  (last x86_64 wheels) and expect onnxruntime 1.23.2 at most. Proof: P-0065's audio rendered and muxed,
  see `experiments/2026-10-07-P-0065/REPORT.md`. Both folders are gitignored (`sandbox/*/`); to rebuild,
  fetch `cpython-3.12.15+20261003-x86_64-apple-darwin-install_only.tar.gz` from
  astral-sh/python-build-standalone release 20261003 and run its `bin/python3.12 -m venv`.
  **Open:** markitdown 0.1.8 resolves on this venv (dry run) and could replace the 0.0.2 install.

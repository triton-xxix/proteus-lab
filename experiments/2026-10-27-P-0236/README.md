# P-0236: agent-purge 0.2.8, read and not run

The question came from harvest item H-0422: does its `ls` command run read-only from a sandbox home, and does it report which harnesses it detects?

## What I did

I fetched the npm metadata and the tarball (`agent-purge-0.2.8.tgz`: 25 files, 307 KB unpacked, no install scripts) into `sandbox/agent-purge-dl/`. I read it with `read_tarball.py` and `show.py`, which open the tarball in Python without extracting it. I did not run it. The package is two days old, its `install` binary-patches the `claude` executable, and I could only learn what `ls` does by reading it anyway. A shell `tar` was denied by the hook, so I used Python's tarfile instead.

## What the code says

- **The premise is wrong.** `ls` does not detect harnesses. It lists personas from the data home (`lsCmd`, entry script lines 536 to 548). Detection is a separate command, `detect`.
- **`detect` really is read-only.** It checks `existsSync` on one marker file per harness (for Claude Code, `~/.claude/settings.json` or `$CLAUDE_CONFIG_DIR`) and looks up the binary on PATH. It spawns `--version` only when given `--versions`.
- **No subcommand is fully read-only.** The entry script runs two writes before it dispatches anything. First, `ensureDataHome` runs `mkdir ~/.agent-purge`, or `$AGENT_PURGE_HOME` when that is set, and copies an old layout across. Second, `recover()` replays a crash journal.
- **The journal replay is the interesting part.** `recover()` reads every `*.json` in `os.tmpdir()/agent-purge-restore/` and writes each record's `backup` text to its `file` path, or deletes the file when `exists` is false. It checks neither the path nor the owner. So whatever can drop a JSON file in that folder decides which file the next `agent-purge ls` overwrites or deletes. On macOS `os.tmpdir()` is the per-user `$TMPDIR`, which limits that to the same user. On Linux it is the shared `/tmp`.

## Verdict

**Not worth it.** Running it would add nothing the source does not already show, and it costs running young, untrusted code with my home in reach. The mechanism is still worth recording for the intelligence lane: a prompt-swapping tool that keeps its own undo journal in a temp folder, where a restore step can be turned into a file-write gadget.

To detect it: look for files appearing under `$TMPDIR/agent-purge-restore/`, a `.agent-purge/` folder in the home directory, and same-name shims placed early on PATH ahead of `claude`, `codex` and similar commands.

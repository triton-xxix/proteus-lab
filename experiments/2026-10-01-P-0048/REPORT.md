# P-0048: Paperclip agent orchestrator, does it boot keyless and where does its state live

Queued 1 Oct 2026 from the Skool S-05 digest (verdict TRY). Taken as far as an unattended night allows.

## What I measured

- Repo: `paperclipai/paperclip`, MIT, created 2 Mar 2026, 95,810 stars and pushed 1 Oct 2026
  22:49 UTC (GitHub API). Repo is 306 MB. The transcript's "36,000 stars" was true once; it is
  now nearly three times that.
- Install path (README): `npx paperclipai@latest onboard --yes`, Node 24.11 or newer. This Mac has
  Node v25.6.0, so the version is not the obstacle.
- State on disk (from `packages/shared/src/home-paths.ts`): everything sits under
  `~/.paperclip/instances/<instance id>/`, holding config, an embedded Postgres data directory,
  logs, backups, a secrets key file and file storage. `PAPERCLIP_HOME` and `PAPERCLIP_INSTANCE_ID`
  override it, so it could be pinned inside `sandbox/`.
- Tasks, approvals and agent spend are rows in that Postgres, not files. So the answer to "what
  does the approval state look like on disk" is: a database, readable only with the server or psql.
  Proteus keeps the same things in flat files and git.
- Booting with no model key is plausible (the README splits `onboard` from a key-needing
  `test-drive`), but I did not run it.

## Why I stopped

Booting it means executing a freshly downloaded npm package and its embedded database server in a
run nobody is watching, plus npm's cache under `~/.npm`, outside my write roots. That belongs in an
interactive session with `PAPERCLIP_HOME` and `npm_config_cache` pointed into `sandbox/`.

Files: `sandbox/paperclip-README.md`, `sandbox/paperclip-home-paths.ts`, `sandbox/paperclip-tree.json`.

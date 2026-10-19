# P-0177 coop-anything MCP: engine detection from marker files

19 Oct 2026, nightly probe loop. Source: harvest H-0322 (github cranebeaker/coop-anything, 425 stars,
created 16 Oct 2026).

## What I did

Fetched `tools/mcp/coop_mcp.py` from raw.githubusercontent.com as text (curl to stdout, nothing saved,
nothing run) and read all of it. I did not execute it: the repo is three days old from an unknown
author, and running files from untrusted sources is outside what a scheduled run may do (charter,
"What Proteus never does"). So this is a static trace, not a run.

## What the detection is

`detect_engine(game_dir)` walks the folder to depth 4 (stops at 60,000 files), lowercases every file
and folder name, then tests 25 signatures in a fixed order and takes the FIRST hit as the best guess.
Pure filename matching: no file contents read, no network, no writes. The same file serves the
directory search, playbook reads and a PE header reader over JSON-RPC on stdio.

Traced against fake folders:

| Fake folder | Rule that fires | Best guess |
|---|---|---|
| `UnityPlayer.dll`, `GameAssembly.dll` | IL2CPP rule (GameAssembly present) | Unity (IL2CPP) |
| `UnityPlayer.dll`, `Game_Data/Managed/Assembly-CSharp.dll` (depth 2) | Mono rule | Unity (Mono) |
| `UnityPlayer.dll` only | plain Unity | Unity |
| `Game/Content/Paks/x.pak` | "paks" folder plus .pak | Unreal Engine 4 or 5 |
| `x.utoc` anywhere | .utoc | Unreal Engine 4 or 5 |
| `x.upk` or a `CookedPC` folder | UE3 | Unreal Engine 3 |
| `Core.u`, `Engine.u` | UE1/2 | Unreal Engine 1 or 2 |

So the answer to the probe question is yes by construction, for those layouts.

## Weak spots found by reading

- First match wins and Unreal 4/5 is tested before RE Engine: an RE Engine game (`re_chunk_000.pak`)
  that also had a `paks` folder would be called Unreal. Rare, but the order decides it silently.
- `.pak` alone without a `paks` folder never fires UE4/5, so a flattened or repacked UE install falls
  through to "unknown".
- Godot detection is any `.pck` file, which many non-Godot games also ship.
- Anti-cheat warning keys on four filenames (EasyAntiCheat, BattlEye); other anti-cheats pass silently.

## Verdict

blocked on running it: needs either a vetted copy (pinned commit, read and hashed) run in an
interactive session, or a decision that a pure file-name matcher read in full counts as vetted.
The static trace answers the question it was queued for.

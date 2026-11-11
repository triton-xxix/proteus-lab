# P-0411: does lot-map's shell classifier put the README's commands where the README says?

11 Nov 2026, nightly probe loop. Source: harvest H-0610, `alexeyw/lot-map`, a Claude Code mod that
draws a live map of tool calls. Its README says which "station" a shell command lights: Files,
Network or Shell, by the command's name.

## Called shot

works at 0.65; 13 of 13 README example commands found for the station the README names. Committed
0c7dbc48 before the source was fetched.

## What I did

I did not install the plugin or run any of its code. I fetched one file as text, `hooks/map.ts` at
commit 6370bf43 (42,268 bytes), read lines 120 to 217, and ported `classifyShell`, `segments` and
`base` line for line into `port.py`, with the word tables copied across. Memory commands are left
empty, so nothing here can land on the Memory station. Then two lists went through the port:

- **README, 21 cases**: every example the README names. The 13 in the Files and Network rows, the
  `$(…)` case, three PowerShell names, the full path, the quoted path with a space, `CURL.EXE`, and
  `python -c` as Shell.
- **Mine, 20 cases**: ordinary commands the README's prose covers but does not list.

## Numbers

| list | right | of |
|---|---|---|
| README examples | 21 | 21 |
| the 13 in the shot | 13 | 13 |
| my everyday cases | 8 | 20 |

The README is honest about its examples. The 12 misses on my list fall into five kinds:

1. **Splitting ignores quotes** (3). The line is cut at `|` and `;` before words are read, so
   `grep -E 'foo|bar' notes.txt` becomes two commands, the second called `bar`, and lands on Shell.
   The same cut makes `echo "first; curl is a tool"` a Network call. The word matcher respects quotes;
   the splitter in front of it does not.
2. **Delete is not in the table** (3). The Files row says "read, search, move, delete or edit in
   place", but `rm` and `chmod` are not file words, so `rm old.txt` is Shell. Only `find … -delete`
   deletes on Files.
3. **An option before the subcommand** (2). `git -C repo push` and `npm --prefix web install` read
   `-C` and `--prefix` as the subcommand and land on Shell.
4. **A wrapper before the command** (2). `sudo curl` and `env TOKEN=x curl` go by `sudo` and `env`.
5. **A network command run by another** (2). `find … -exec curl {} +` is Files, `xargs curl` is Shell.

Kinds 3 to 5 are the README's own caveat ("by the command's name, not by what it does") and it says
so. Kinds 1 and 2 are not covered by it: a quoted alternation in grep is about as common as grep gets.

## What this is not

A port, not the plugin. If I copied a table or a regex wrong, the miss is mine: the 21 of 21 on the
README list is some evidence the port is faithful, not proof. My 20 cases were written after reading
the source, so 8 of 20 is a count of holes I went looking for, not an error rate on real sessions.
Nothing was drawn, no hooks ran, and the Memory station and the non-shell tools were not tested.

Files: `port.py`, `results.json`. The fetched source is in `sandbox/p0411/map.ts` (gitignored).

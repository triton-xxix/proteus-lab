# P-0093: agent-workbench 0.5.2, does it list local Claude Code sessions read-only? (8 to 9 Oct 2026)

Verdict: **blocked**, on my own write roots, not on the tool.

Installed into `sandbox/agent-workbench` with `npm install --ignore-scripts` (74 packages, 6 s).
node-pty ships prebuilt binaries for darwin-arm64 and darwin-x64, so the missing install scripts
would not have stopped it. What I read in the installed `dist/server.js` before starting it:

- It binds `127.0.0.1` only, checks the Host header, and puts a token in the URL. Remote access is
  off by default (port 24837 when switched on). Good.
- It reads `~/.claude/projects`, `~/.claude/sessions` and `~/.claude/plans`, and lists `~/.claude`
  among protected directories. Its own comments say it only reads there.
- On macOS it writes its config to `~/Library/Application Support/agent-workbench` (no XDG override
  on darwin) and opens a browser tab at start unless `AGENT_WORKBENCH_NO_OPEN=1`.

Why I stopped: the first write is outside the two folders I may write to, and the browser tab would
pop on an unattended Mac. Pointing HOME at the sandbox would also hide the real sessions, which is
the thing under test. The session list is served over a websocket with that token, so a yes/no
needs the server up for a minute plus a small ws client; about 15 minutes in an interactive session.

Needs: one interactive run where a write to `~/Library/Application Support/agent-workbench` is fine.

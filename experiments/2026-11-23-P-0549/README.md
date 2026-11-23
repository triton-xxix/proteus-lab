# P-0549, Hermit CRM CLI and MCP on macOS (23 Nov 2026, nightly)

Question (harvest H-0746): does the CLI and MCP server run on macOS and list tools from a plain Markdown store?

Run: source tarball from codeload.github.com (no git clone), `pip install` into `sandbox/hermit-venv` (Python 3.14), `hermitcrm init sandbox/hermit-data --demo`, then `mcp_probe.py` speaks JSON-RPC to `hermitcrm mcp` over stdio.

Measured:
- Install clean, no build errors. `init --demo`: a git-backed folder; `check`: 13 companies, 15 contacts, 26 interactions, no problems.
- MCP server `hermitcrm` 1.1.0 answered initialize and `tools/list` with 18 tools in 0.32 s, then `list_pipeline` returned without error (`results.json`).
- Tools: 8 read (list_pipeline, show_company, search_companies, digest, report, followups, keep_in_touch, brief), add_company/contact/interaction, adjust_*, bulk_preview/apply, undo.
- CLI `followups` on demo data: 1 reply owed (2 days), 1 waiting (20 days).

Not run: the web app, LinkedIn import, IMAP BCC, the outreach bot, sending. No real data in the folder.

Verdict: works.

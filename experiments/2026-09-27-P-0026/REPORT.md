# P-0026 AgentMail hosted MCP, keyless

Question: does https://mcp.agentmail.to/mcp answer or refuse a tool-list call with no API key?

Answer: refuses. Both `initialize` and `tools/list` return HTTP 401 `{"error":"Unauthorized"}` in about 0.2 s,
before any MCP handshake. So the tool catalogue the npm and PyPI bridges fetch live is not public.

What the refusal shows about the mechanism:
- Express behind Cloudflare, auth by Clerk (`x-clerk-auth-reason: session-token-and-uat-missing`).
- The 401 is spec-shaped for MCP OAuth: `WWW-Authenticate: Bearer resource_metadata=...` pointing at an
  RFC 9728 protected-resource document, which answers 200 without auth.
- That document names Clerk (`clerk.console.agentmail.to`) as the authorisation server, PKCE S256, scopes
  `openid email profile user:org:read`. So an MCP client can discover how to log in, but logging in needs
  an AgentMail account, which I do not create.

Files: `init.headers`, `init.body`, `list.body`, `resource-metadata.json`, request bodies `init.json`, `list.json`.
Verdict: works, in the narrow sense asked: the endpoint behaves as a correctly gated MCP OAuth resource.

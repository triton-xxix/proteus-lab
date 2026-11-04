// P-0322: run mcp-video-analyzer's CLI with every fetch counted by host, OPENAI_API_KEY removed,
// WHISPER_BIN pointed at the whisper.cpp shim. Caches and temp stay inside the sandbox.
delete process.env.OPENAI_API_KEY;
delete process.env.WHISPER_HF_MODEL;
process.env.WHISPER_BIN = '/Users/triton/PROTEUS/experiments/2026-11-04-P-0322/whisper_shim.py';
process.env.MCP_CACHE_DIR = '/Users/triton/PROTEUS/sandbox/mcpva/cache';
process.env.FFMPEG_BIN = '/usr/local/bin/ffmpeg';
process.env.TMPDIR = '/Users/triton/PROTEUS/sandbox/mcpva/tmp';
const { mkdirSync, writeFileSync } = await import('node:fs');
mkdirSync(process.env.TMPDIR, { recursive: true });
const hosts = {};
const realFetch = globalThis.fetch;
globalThis.fetch = async (input, init) => {
  const u = new URL(typeof input === 'string' ? input : input.url ?? String(input));
  hosts[u.host] = (hosts[u.host] ?? 0) + 1;
  return realFetch(input, init);
};
const t0 = Date.now();
const { runCli } = await import('/Users/triton/PROTEUS/sandbox/mcpva/node_modules/mcp-video-analyzer/dist/cli.js');
const code = await runCli(process.argv.slice(2));
const summary = { exit: code, seconds: (Date.now() - t0) / 1000, fetch_hosts: hosts };
writeFileSync('/Users/triton/PROTEUS/experiments/2026-11-04-P-0322/fetches.json', JSON.stringify(summary, null, 1));
process.stderr.write(`\n[probe] ${JSON.stringify(summary)}\n`);
process.exitCode = code;

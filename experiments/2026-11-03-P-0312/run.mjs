// Keeps every cache and temp write inside the sandbox, then runs the package's own CLI.
process.env.MCP_CACHE_DIR = '/Users/triton/PROTEUS/sandbox/mcpva/cache';
process.env.FFMPEG_BIN = '/usr/local/bin/ffmpeg'; // --ignore-scripts skipped ffmpeg-static's download
process.env.TMPDIR ='/Users/triton/PROTEUS/sandbox/mcpva/tmp';
const { mkdirSync } = await import('node:fs');
mkdirSync(process.env.TMPDIR, { recursive: true });
const t0 = Date.now();
const { runCli } = await import('/Users/triton/PROTEUS/sandbox/mcpva/node_modules/mcp-video-analyzer/dist/cli.js');
const code = await runCli(process.argv.slice(2));
process.stderr.write(`\n[probe] exit ${code} in ${((Date.now() - t0) / 1000).toFixed(1)} s\n`);
process.exitCode = code;

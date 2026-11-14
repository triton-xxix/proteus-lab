// P-0259: does `bla harden` keep a small JS bundle's output identical, and how much bigger does it get?
"use strict";
const fs = require("fs");
const path = require("path");
const { execFileSync, spawnSync } = require("child_process");

const SANDBOX = "/Users/triton/PROTEUS/sandbox/bla";
const CLI = path.join(SANDBOX, "node_modules/bla-agents/dist/cli.js");
const SAMPLE = path.join(SANDBOX, "sample");
const WORK = path.join(SANDBOX, "work");
const OUT = "/Users/triton/PROTEUS/experiments/2026-10-29-P-0259/results.json";

fs.rmSync(WORK, { recursive: true, force: true });
const plain = path.join(WORK, "plain");
const hard = path.join(WORK, "hard");
fs.cpSync(SAMPLE, plain, { recursive: true });
fs.cpSync(SAMPLE, hard, { recursive: true });

function walk(dir, acc = []) {
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, acc); else acc.push({ file: path.relative(WORK, p), bytes: st.size });
  }
  return acc;
}

const res = { node: process.version, cli: CLI };
res.plain_out = execFileSync("node", [path.join(plain, "dist/app.js")], { encoding: "utf8" });
res.plain_bytes = fs.statSync(path.join(plain, "dist/app.js")).size;

const stages = [];
for (const args of [["harden", "."], ["protect", "dist/app.js"]]) {
  const t0 = Date.now();
  const r = spawnSync("node", [CLI, ...args], { cwd: hard, encoding: "utf8", timeout: 240000 });
  stages.push({ args, status: r.status, ms: Date.now() - t0,
    stdout: (r.stdout || "").slice(0, 6000), stderr: (r.stderr || "").slice(0, 3000) });
  const now = fs.statSync(path.join(hard, "dist/app.js")).size;
  if (now !== res.plain_bytes) break;  // the first stage that changed the file is enough
}
res.stages = stages;
res.hard_files = walk(hard);
res.hard_bytes = fs.statSync(path.join(hard, "dist/app.js")).size;
res.size_multiple = +(res.hard_bytes / res.plain_bytes).toFixed(2);
const r2 = spawnSync("node", [path.join(hard, "dist/app.js")], { encoding: "utf8", timeout: 60000 });
res.hard_status = r2.status;
res.hard_out = r2.stdout;
res.hard_stderr = (r2.stderr || "").slice(0, 2000);
res.identical = r2.status === 0 && r2.stdout === res.plain_out;
fs.writeFileSync(OUT, JSON.stringify(res, null, 2));
console.log(JSON.stringify({ plain_bytes: res.plain_bytes, hard_bytes: res.hard_bytes, size_multiple: res.size_multiple,
  identical: res.identical, hard_status: res.hard_status, stages: stages.map(s => [s.args.join(" "), s.status, s.ms]),
  files: res.hard_files.length }, null, 1));

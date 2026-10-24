// P-0213: does agent-usage-guard's prompt gate warn on a stale cache with a large context?
// The guard is a Claude Code mods plugin: it never reads a transcript file. Its context figure
// comes from the API usage the harness reports (input + cacheRead + cacheWrite), and idle time
// from the session's last response. So the testable slice is the pure core: feed promptGate a
// state with that context and an idle time, and read the verdict. The "transcript" here is the
// real one from tonight's own session, read for its last usage record.
import { readFileSync } from 'node:fs'
import { defaultConfig } from '/Users/triton/PROTEUS/sandbox/agent-usage-guard/agent-usage-guard-HEAD/core/config.ts'
import { promptGate } from '/Users/triton/PROTEUS/sandbox/agent-usage-guard/agent-usage-guard-HEAD/core/prompts.ts'
import { MAIN, newSession } from '/Users/triton/PROTEUS/sandbox/agent-usage-guard/agent-usage-guard-HEAD/core/state.ts'

const config = defaultConfig()
const HOUR = 3_600_000
const results: Array<Record<string, unknown>> = []

function run(name: string, context: number | undefined, idleMs: number | undefined, source: 'user' | 'headless' | 'other', canAsk: boolean, repeat = 1) {
  const state = newSession('p0213', canAsk)
  if (context !== undefined) state.loops[MAIN] = { heavyCalls: [], context }
  let verdict: any
  const t0 = performance.now()
  for (let i = 0; i < repeat; i++) verdict = promptGate(state, [], config, Date.now(), { source, text: 'hello', idleMs })
  const us = ((performance.now() - t0) * 1000) / repeat
  const row = { name, context, idleMin: idleMs === undefined ? null : idleMs / 60_000, source, canAsk, kind: verdict.kind, rule: verdict.rule ?? verdict.trips?.[0]?.rule ?? null, text: verdict.question ?? verdict.message ?? verdict.note ?? '', microseconds: Math.round(us) }
  results.push(row)
  console.log(`${name}: ${row.kind}${row.rule ? ' [' + row.rule + ']' : ''} ${row.text ? '- ' + row.text : ''}`)
}

// 1. The question itself: stale cache (2 h idle) and large context (160k), a person present.
run('stale+large, user, canAsk', 160_000, 2 * HOUR, 'user', true)
// 2. Same, nobody to ask (claude -p): first heavy resume on the machine is let through and counted...
const headless = newSession('p0213-headless', false)
headless.loops[MAIN] = { heavyCalls: [], context: 160_000 }
const h1 = promptGate(headless, [], config, Date.now(), { source: 'headless', text: 'x', idleMs: 2 * HOUR })
const h2 = promptGate(headless, [], config, Date.now(), { source: 'headless', text: 'x', idleMs: 2 * HOUR })
console.log(`stale+large, headless, 1st: ${h1.kind}; 2nd: ${h2.kind}${'rule' in h2 ? ' [' + (h2 as any).rule + ']' : ''}`)
results.push({ name: 'stale+large, headless, 1st then 2nd', first: h1.kind, second: h2.kind, secondText: (h2 as any).message ?? '' })
// 3. Boundaries: just under each threshold must pass, at the threshold must ask.
run('149,999 ctx, 2 h idle', 149_999, 2 * HOUR, 'user', true)
run('150,000 ctx, 2 h idle', 150_000, 2 * HOUR, 'user', true)
run('160k ctx, 59 min idle', 160_000, 59 * 60_000, 'user', true)
run('160k ctx, 60 min idle', 160_000, 60 * 60_000, 'user', true)
// 4. Fresh but big: the one-time context note at 300k, the hard ask at 500k.
run('350k ctx, 1 min idle', 350_000, 60_000, 'user', true)
run('600k ctx, 1 min idle', 600_000, 60_000, 'user', true)
run('600k ctx, 1 min idle, headless', 600_000, 60_000, 'headless', false)
// 5. A notification or another session's message is never held.
run('stale+large, source other', 160_000, 2 * HOUR, 'other', true)
// 6. No context known yet (first prompt of a session).
run('no context, 2 h idle', undefined, 2 * HOUR, 'user', true)
// 7. Speed of the gate itself.
run('speed: 160k, 2 h, 10,000 calls', 160_000, 2 * HOUR, 'user', true, 10_000)

// 8. Tonight's real transcript: the last usage record of this nightly session, as the harness would report it.
const transcript = '/Users/triton/.claude/projects/-Users-triton-PROTEUS/6d39858a-29db-48a2-ae83-af75b7834f78.jsonl'
let last: any
let lines = 0
try {
  for (const line of readFileSync(transcript, 'utf8').split('\n')) {
    if (!line) continue
    lines++
    try {
      const rec = JSON.parse(line)
      const u = rec?.message?.usage
      if (u && typeof u.input_tokens === 'number') last = u
    } catch {}
  }
} catch (e) {
  console.log('transcript not readable:', String(e))
}
if (last) {
  const ctx = (last.input_tokens ?? 0) + (last.cache_read_input_tokens ?? 0) + (last.cache_creation_input_tokens ?? 0)
  console.log(`transcript: ${lines} lines, last usage input ${last.input_tokens} cacheRead ${last.cache_read_input_tokens} cacheWrite ${last.cache_creation_input_tokens} => context ${ctx}`)
  run('tonight real ctx, 2 h idle', ctx, 2 * HOUR, 'user', true)
  run('tonight real ctx, 1 min idle', ctx, 60_000, 'user', true)
  results.push({ name: 'transcript', lines, context: ctx, last })
}

const fs = await import('node:fs')
fs.writeFileSync('/Users/triton/PROTEUS/experiments/2026-10-24-P-0213/results.json', JSON.stringify({ config, results }, null, 2))
console.log('wrote results.json')

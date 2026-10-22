// P-0194: test the alarm's core (parser, matcher, shuffle, timer maths) from alarm.html itself.
// Usage: node test.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, 'alarm.html'), 'utf8');
const core = html.split('// CORE START')[1].split('// CORE END')[0];
const api = new Function(core + '; return {parseM3U, isHlsMedia, matchFiles, order, msUntil};')();
const fixtures = path.join(__dirname, 'fixtures');
let pass = 0, fail = 0;
function check(name, cond, got) {
  if (cond) { pass++; console.log('ok   ' + name); }
  else { fail++; console.log('FAIL ' + name + ' got ' + JSON.stringify(got)); }
}

const cases = fs.readdirSync(fixtures).filter(f => !f.endsWith('.expect')).sort();
for (const f of cases) {
  const text = fs.readFileSync(path.join(fixtures, f), 'utf8');
  const exp = JSON.parse(fs.readFileSync(path.join(fixtures, f + '.expect'), 'utf8'));
  const hls = api.isHlsMedia(text);
  check(f + ' hls=' + exp.hls, hls === exp.hls, hls);
  if (exp.hls) continue;
  const e = api.parseM3U(text);
  check(f + ' entries=' + exp.n, e.length === exp.n, e.length);
  check(f + ' names', JSON.stringify(e.map(x => x.name)) === JSON.stringify(exp.names), e.map(x => x.name));
  check(f + ' titles', JSON.stringify(e.map(x => x.title)) === JSON.stringify(exp.titles), e.map(x => x.title));
  check(f + ' urls', JSON.stringify(e.map(x => x.url)) === JSON.stringify(exp.urls), e.map(x => x.url));
  if (exp.files) {
    const m = api.matchFiles(e, exp.files);
    check(f + ' playable=' + exp.playable, m.filter(x => x.playable).length === exp.playable, m.map(x => x.playable));
  }
}

// shuffle: a permutation, and deterministic with a fixed generator
let seed = 1; const rand = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const o = api.order(10, true, rand);
check('shuffle is a permutation of 0..9', JSON.stringify([...o].sort((a, b) => a - b)) === JSON.stringify([...Array(10).keys()]), o);
check('shuffle moved something', JSON.stringify(o) !== JSON.stringify([...Array(10).keys()]), o);
check('in order when off', JSON.stringify(api.order(4, false)) === '[0,1,2,3]', api.order(4, false));

// timer: later today, and tomorrow when the time has passed
const now = new Date(2026, 9, 22, 23, 30, 0);
check('07:00 from 23:30 is 7.5 h', api.msUntil('07:00', now) === 7.5 * 3600e3, api.msUntil('07:00', now));
check('23:45 from 23:30 is 15 min', api.msUntil('23:45', now) === 15 * 60e3, api.msUntil('23:45', now));
check('23:30 from 23:30 is tomorrow', api.msUntil('23:30', now) === 24 * 3600e3, api.msUntil('23:30', now));

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);

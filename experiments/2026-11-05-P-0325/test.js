// Side-pot test table for chips.html. Usage: node test.js /abs/path/chips.html
const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const src = html.split('<script id="core">')[1].split('</script>')[0];
const m = { exports: {} };
new Function('module', src)(m);
const { sidePots, splitPot } = m.exports;
const P = (c, f = false) => ({ committed: c, folded: f });
const cases = [
  ['heads-up, equal', [P(100), P(100)], [[200, [0, 1]]]],
  ['one short all-in', [P(50), P(100), P(100)], [[150, [0, 1, 2]], [100, [1, 2]]]],
  ['two short all-ins', [P(30), P(70), P(100), P(100)], [[120, [0, 1, 2, 3]], [120, [1, 2, 3]], [60, [2, 3]]]],
  ['folded player feeds main pot', [P(40, true), P(100), P(100)], [[240, [1, 2]]]],
  ['folded above short all-in', [P(50), P(80, true), P(200), P(200)], [[200, [0, 2, 3]], [330, [2, 3]]]],
  ['uncalled excess over a live cap goes back to the top pot', [P(60), P(100)], [[120, [0, 1]], [40, [1]]]],
  ['everyone folded to one', [P(10, true), P(20)], [[30, [1]]]],
  ['equal all-ins merge', [P(100), P(100), P(100)], [[300, [0, 1, 2]]]],
  ['folded chips above every live cap', [P(150, true), P(100), P(100)], [[350, [1, 2]]]],
  ['nothing in', [P(0), P(0)], []],
];
let pass = 0;
for (const [name, ps, want] of cases) {
  const got = sidePots(ps).map(p => [p.amount, p.eligible]);
  const ok = JSON.stringify(got) === JSON.stringify(want);
  const total = ps.reduce((s, p) => s + p.committed, 0), out = got.reduce((s, p) => s + p[0], 0);
  const cons = total === out;
  if (ok && cons) pass++;
  console.log(`${ok && cons ? 'PASS' : 'FAIL'}  ${name}  got ${JSON.stringify(got)}${ok ? '' : '  want ' + JSON.stringify(want)}${cons ? '' : '  chips not conserved'}`);
}
const splits = [
  ['even split', [100, [0, 1], 2, 3], { 0: 50, 1: 50 }],
  ['odd chip left of button', [101, [0, 2], 1, 3], { 0: 50, 2: 51 }],
  ['three ways, two odd chips', [101, [0, 1, 2], 0, 3], { 0: 33, 1: 34, 2: 34 }],
];
for (const [name, args, want] of splits) {
  const got = splitPot(...args);
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (ok) pass++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}  got ${JSON.stringify(got)}${ok ? '' : '  want ' + JSON.stringify(want)}`);
}
// Award main pots one at a time: every chip comes out exactly once and the pot sequence matches.
const seq = [
  ['two short all-ins, awarded in order', [P(30), P(70), P(100), P(100)], [120, 120, 60]],
  ['folded above short all-in, in order', [P(50), P(80, true), P(200), P(200)], [200, 330]],
  ['folded chips above every live cap', [P(150, true), P(100), P(100)], [350]],
];
for (const [name, ps, want] of seq) {
  const got = []; let guard = 0;
  while (sidePots(ps).length && guard++ < 10) got.push(m.exports.takeMainPot(ps));
  const ok = JSON.stringify(got) === JSON.stringify(want) && ps.every(p => p.committed === 0);
  if (ok) pass++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}  got ${JSON.stringify(got)}${ok ? '' : '  want ' + JSON.stringify(want)}`);
}
console.log(`${pass} of ${cases.length + splits.length + seq.length} passed`);

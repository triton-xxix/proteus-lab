// The career page "The company": who keeps coming back across the filmography. Camera, cut, score and
// writing credits, and the top five billed actors, read from films/<slug>.json (the research child's
// sourced facts: facts.dp, facts.editor, facts.composer, facts.writers, facts.cast_top5). Runs, handovers
// and counts are computed here, never typed. Built 24 Nov 2026 Workshop. HTML grids, not SVG.
'use strict';
const { esc, readJSON } = require('./render.cjs');

const CHAIRS = [
  { key: 'camera', fact: 'dp', label: 'Camera', role: 'cinematographer', colour: '#3C9AB4' },
  { key: 'cut', fact: 'editor', label: 'Cut', role: 'editor', colour: '#E0A04A' },
  { key: 'score', fact: 'composer', label: 'Score', role: 'composer', colour: '#B98AD6' },
];
const WRITING = { key: 'writing', fact: 'writers', label: 'Words', role: 'writer', colour: '#C9D2DC' };
const CAST = { key: 'cast', label: 'In front', role: 'top-five billed actor', colour: '#8FBF7F' };

// "Christopher Nolan (screenplay), based on American Prometheus by Kai Bird and Martin J. Sherwin" -> ["Christopher Nolan"]
function names(v) {
  const list = Array.isArray(v) ? v : [v];
  const out = [];
  for (const s of list) {
    if (typeof s !== 'string' || !s.trim()) continue;
    const bare = s.replace(/\([^)]*\)/g, '').replace(/,\s*based on.*$/i, '');
    for (const n of bare.split(/\s+and\s+|,\s*/)) if (n.trim()) out.push(n.trim().replace(/\s+/g, ' '));
  }
  return [...new Set(out)];
}

function model() {
  const reg = readJSON('films.json');
  const films = reg.films.map(f => {
    const d = readJSON(`films/${f.slug}.json`);
    const F = d.facts || {};
    const row = { slug: f.slug, title: d.title || f.title, year: d.year || f.year, deep: f.deep_page, src: {} };
    for (const c of CHAIRS.concat([WRITING])) {
      if (!F[c.fact] || F[c.fact].value == null) throw new Error(`${f.slug}: no ${c.fact}`);
      row[c.key] = names(F[c.fact].value);
      if (!row[c.key].length) throw new Error(`${f.slug}: empty ${c.fact}`);
      row.src[c.key] = F[c.fact].source;
    }
    const cast = (F.cast_top5 && F.cast_top5.value) || [];
    if (cast.length !== 5) throw new Error(`${f.slug}: cast_top5 has ${cast.length}`);
    row.cast = cast.map(x => x.name.trim());
    row.src.cast = F.cast_top5.source;
    return row;
  }).sort((a, b) => a.year - b.year);
  const n = films.length;

  function people(key) {
    const m = new Map();
    films.forEach((f, i) => f[key].forEach(p => { if (!m.has(p)) m.set(p, []); m.get(p).push(i); }));
    return [...m.entries()].map(([name, idx]) => {
      let run = 1, best = 1, bestFrom = idx[0], from = idx[0];
      for (let j = 1; j < idx.length; j++) {
        if (idx[j] === idx[j - 1] + 1) run++; else { run = 1; from = idx[j]; }
        if (run > best) { best = run; bestFrom = from; }
      }
      return { name, idx, count: idx.length, run: best, runFrom: bestFrom, runTo: bestFrom + best - 1 };
    }).sort((a, b) => a.idx[0] - b.idx[0] || b.count - a.count || a.name.localeCompare(b.name));
  }

  // a handover: nobody in this chair on film i also held it on film i-1
  const chairs = CHAIRS.map(c => {
    const ppl = people(c.key);
    const handovers = [];
    for (let i = 1; i < n; i++) if (!films[i][c.key].some(p => films[i - 1][c.key].includes(p))) handovers.push(i);
    return { ...c, people: ppl, handovers, top: ppl.slice().sort((a, b) => b.count - a.count)[0] };
  });
  const writing = { ...WRITING, people: people('writing') };
  const castAll = people('cast');
  const cast = { ...CAST, people: castAll.filter(p => p.count >= 2), all: castAll.length };
  const allRuns = chairs.flatMap(c => c.people.map(p => ({ ...p, chair: c })));
  const longest = Math.max(...allRuns.map(p => p.run));
  const longestRuns = allRuns.filter(p => p.run === longest);
  const shakeups = [];
  for (let i = 1; i < n; i++) {
    const which = chairs.filter(c => c.handovers.includes(i));
    if (which.length >= 2) shakeups.push({ film: films[i], prev: films[i - 1], chairs: which });
  }
  const steady = [];
  for (let i = 1; i < n; i++) if (!chairs.some(c => c.handovers.includes(i))) steady.push(films[i]);
  const cn = writing.people.find(p => p.name === 'Christopher Nolan');
  const castTop = cast.people.slice().sort((a, b) => b.count - a.count || a.idx[0] - b.idx[0]);
  const handoverTotal = chairs.reduce((t, c) => t + c.handovers.length, 0);
  return { films, n, chairs, writing, cast, castTop, longest, longestRuns, shakeups, steady, cn, handoverTotal };
}

function board(m, group, opts = {}) {
  const head = `<li class="cp-row cp-row--head" aria-hidden="true"><span></span><span class="cp-cells">${m.films.map(f => `<span class="cp-yr" title="${esc(f.title)}">${String(f.year).slice(2)}</span>`).join('')}</span><span></span></li>`;
  const rows = group.people.map(p => {
    const cells = m.films.map((f, i) => {
      const on = p.idx.includes(i), inRun = p.run >= 2 && i >= p.runFrom && i <= p.runTo;
      return `<span class="cp-cell${on ? ' cp-cell--on' : ''}${on && inRun ? ' cp-cell--run' : ''}"${on ? ` style="--c:${group.colour}" title="${esc(p.name)}, ${esc(f.title)} (${f.year})"` : ''}></span>`;
    }).join('');
    return `<li class="cp-row${p.count === 1 && !opts.keepOnes ? ' cp-row--once' : ''}"><span class="cp-name">${esc(p.name)}</span><span class="cp-cells">${cells}</span><span class="cp-n">${p.count}</span></li>`;
  }).join('\n');
  return `<ol class="cp-board" aria-label="${esc(group.label)}: ${group.people.length} people across ${m.n} films">
${head}
${rows}
  </ol>`;
}

function handoverLine(m, c) {
  if (!c.handovers.length) return `Nobody has handed over the ${c.role}'s chair.`;
  const hs = c.handovers.map(i => `${esc(m.films[i - 1].title)} to ${esc(m.films[i].title)}`);
  return `${c.handovers.length} handover${c.handovers.length === 1 ? '' : 's'}: ${hs.join('; ')}.`;
}

function renderCompany(prefix) {
  const m = model();
  const cam = m.chairs.find(c => c.key === 'camera'), cut = m.chairs.find(c => c.key === 'cut'), score = m.chairs.find(c => c.key === 'score');
  const runText = m.longestRuns.map(p => `${esc(p.name)} (${p.chair.role}, ${esc(m.films[p.runFrom].title)} to ${esc(m.films[p.runTo].title)})`).join(' and ');
  const caine = m.castTop[0];
  const sections = m.chairs.map(c => `<section class="cp-sec" aria-label="${esc(c.label)}">
    <h2 class="site__kicker" style="color:${c.colour}">${esc(c.label)} · ${c.people.length} ${c.role}s</h2>
    ${board(m, c, { keepOnes: true })}
    <p class="cp-cap">${handoverLine(m, c)}${c.top ? ` ${esc(c.top.name)} has held it on ${c.top.count} of ${m.n}.` : ''}</p>
  </section>`).join('\n');
  const filmKey = m.films.map(f => `<li><b>${String(f.year).slice(2)}</b> <a href="${prefix}${f.deep ? esc(f.deep) : `films/${esc(f.slug)}/`}">${esc(f.title)}</a></li>`).join('');
  const table = m.films.map(f => `<tr class="cp-tr"><th scope="row"><a href="${prefix}films/${esc(f.slug)}/">${esc(f.title)}</a></th><td>${f.year}</td><td>${esc(f.camera.join(', '))}</td><td>${esc(f.cut.join(', '))}</td><td>${esc(f.score.join(', '))}</td><td>${esc(f.writing.join(', '))}</td><td>${esc(f.cast.join(', '))}</td><td><a href="${esc(f.src.camera)}">source</a></td></tr>`).join('\n');
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>The company</title>
<meta name="description" content="Who keeps coming back across ${m.n} Christopher Nolan films: ${cam.people.length} cinematographers, ${cut.people.length} editors, ${score.people.length} composers, and the actors billed in the top five more than once. Unofficial fan page.">
<meta name="theme-color" content="#0B0D11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${prefix}shared/site.css">
<style>
.cp-big{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,12rem),1fr));gap:1rem;margin:2rem 0;padding:0;list-style:none}
.cp-big li{border-top:2px solid #2A313B;padding-top:.6rem}
.cp-big b{display:block;font:700 2.4rem/1 Archivo,sans-serif;color:#F2EFE8}
.cp-big span{color:#8A93A0;font-size:.95rem}
.cp-sec{margin:2.2rem 0}
.cp-board{list-style:none;padding:0;margin:.8rem 0}
.cp-row{display:grid;grid-template-columns:minmax(6rem,11rem) 1fr 2rem;gap:.7rem;align-items:center;min-height:1.7rem}
.cp-name{font-size:.95rem;line-height:1.2}
.cp-n{font:600 1rem Archivo,sans-serif;text-align:right;font-variant-numeric:tabular-nums;color:#8A93A0}
.cp-cells{display:grid;grid-template-columns:repeat(${m.n},minmax(0,1fr));gap:3px}
.cp-cell{height:1.15rem;background:#151A21;border-radius:2px}
.cp-cell--on{background:var(--c);opacity:.55}.cp-cell--run{opacity:1}
.cp-yr{text-align:center;color:#8A93A0;font-size:.75rem;font-variant-numeric:tabular-nums}
.cp-row--head{min-height:1.2rem}
.cp-cap,.cp-note{color:#8A93A0;font-size:.95rem;line-height:1.5;max-width:64ch}
.cp-key{list-style:none;padding:0;margin:1rem 0;display:flex;flex-wrap:wrap;gap:.3rem 1rem;font-size:.88rem;color:#8A93A0}
.cp-key b{color:#F2EFE8;font-weight:600;font-variant-numeric:tabular-nums}
.cp-shake{list-style:none;padding:0;margin:1rem 0}
.cp-shake li{border-left:3px solid #C8463A;padding:.3rem .8rem;margin:.6rem 0}
.cp-wrap{overflow-x:auto;margin:1rem 0}
.cp-table{border-collapse:collapse;font-size:.86rem;min-width:56rem}
.cp-table th,.cp-table td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid #1C2129;vertical-align:top}
@media (max-width:560px){.cp-row{grid-template-columns:5.4rem 1fr 1.4rem;gap:.4rem}.cp-name{font-size:.78rem}.cp-yr{font-size:.6rem}.cp-cells{gap:2px}.cp-big b{font-size:2rem}}
</style>
</head>
<body>
<main class="site cp">
  <header class="site__head">
    <p class="site__kicker"><a href="${prefix}">Christopher Nolan, film by film</a> · the whole career</p>
    <h1 class="site__h1">The company.</h1>
    <p class="site__lede">${m.n} films, ${cam.people.length} cinematographers, ${cut.people.length} editors, ${score.people.length} composers. The crew changes rarely and in eras: ${m.n - 1} steps from one film to the next in three chairs is ${3 * (m.n - 1)} chances, and there have been ${m.handoverTotal} handovers, and the longest unbroken run is ${m.longest} films in a row, by ${runText}. In front of the camera, ${esc(caine.name)} is billed in the top five ${caine.count} times, more than anyone.</p>
  </header>
  <ul class="cp-big" aria-label="The numbers">
    <li><b>${m.longest}</b><span>films in a row, the longest anyone has held one chair</span></li>
    <li><b>${m.handoverTotal}</b><span>handovers in camera, cut and score across ${m.n - 1} film-to-film steps</span></li>
    <li><b>${m.cn.count} of ${m.n}</b><span>films with Christopher Nolan in the writing credit</span></li>
    <li><b>${m.cast.people.length} of ${m.cast.all}</b><span>top-five billed actors who come back at least once</span></li>
  </ul>
  <ol class="cp-key" aria-label="Columns are films, by year">${filmKey}</ol>
${sections}
  <section class="cp-sec" aria-label="When the crew turned over">
    <h2 class="site__kicker">When two chairs changed at once</h2>
    <ul class="cp-shake">
${m.shakeups.map(s => `      <li><b>${esc(s.film.title)}</b> (${s.film.year}), after ${esc(s.prev.title)}: new ${s.chairs.map(c => `${c.role} (${esc(s.film[c.key].join(' and '))})`).join(' and new ')}.</li>`).join('\n')}
    </ul>
    <p class="cp-cap">${m.shakeups.length} films brought in two or more new crew heads at once; ${m.shakeups.filter(s => s.chairs.length === 3).length ? `${m.shakeups.filter(s => s.chairs.length === 3).map(s => esc(s.film.title)).join(', ')} changed all three` : 'none changed all three'}. ${m.steady.length} of ${m.n - 1} films kept someone in all three chairs from the film before${m.steady.length ? ` (${m.steady.map(f => esc(f.title)).join(', ')})` : ''}.</p>
  </section>
  <section class="cp-sec" aria-label="${esc(WRITING.label)}">
    <h2 class="site__kicker" style="color:${WRITING.colour}">${esc(WRITING.label)} · ${m.writing.people.length} credited writers</h2>
    ${board(m, m.writing, { keepOnes: true })}
    <p class="cp-cap">Screenplay and story credits as each film's research lists them, source writers included (the original Insomnia's, the short story Memento grew from); a novel or book a film is based on is left out.</p>
  </section>
  <section class="cp-sec" aria-label="${esc(CAST.label)}">
    <h2 class="site__kicker" style="color:${CAST.colour}">${esc(CAST.label)} · billed in the top five more than once</h2>
    ${board(m, m.cast)}
    <p class="cp-cap">Only the top five billed names of each film are in the research, ${m.n * 5} slots in all, held by ${m.cast.all} people. An actor who came back lower down the bill does not show here, so this counts the leads, not the whole company.</p>
  </section>
  <section aria-label="Every film">
    <h2 class="site__kicker">Every film, as the research has it</h2>
    <div class="cp-wrap"><table class="cp-table">
      <thead><tr><th scope="col">Film</th><th scope="col">Year</th><th scope="col">Camera</th><th scope="col">Cut</th><th scope="col">Score</th><th scope="col">Words</th><th scope="col">Top five billed</th><th scope="col">Source</th></tr></thead>
      <tbody>
${table}
      </tbody>
    </table></div>
    <p class="cp-note">A handover means nobody in that chair on a film also held it on the film before, so a composer joining a partner (or leaving one) is not counted. Names come from each film's fetched source, Wikipedia for most; shared credits are split into people.</p>
  </section>
  <footer class="site__foot">
    <p>Built ${new Date().toISOString().slice(0, 10)} by Proteus, an AI explorer, from the research on each film page. <a href="${prefix}data/company.json">The data</a>.</p>
    <p>Not affiliated with Christopher Nolan, Syncopy or any studio.</p>
  </footer>
</main>
</body>
</html>`;
}

function data() {
  const m = model();
  const ppl = g => g.people.map(p => ({ name: p.name, films: p.idx.map(i => m.films[i].slug), count: p.count, longest_run: p.run }));
  return {
    built_from: 'sites/nolan/films/*.json (facts.dp, facts.editor, facts.composer, facts.writers, facts.cast_top5)',
    films: m.films.map(f => ({ slug: f.slug, title: f.title, year: f.year, camera: f.camera, cut: f.cut, score: f.score, writing: f.writing, cast_top5: f.cast })),
    chairs: Object.fromEntries(m.chairs.map(c => [c.key, { people: ppl(c), handovers: c.handovers.map(i => m.films[i].slug) }])),
    writing: ppl(m.writing),
    cast_repeat: ppl(m.cast), cast_distinct: m.cast.all,
    longest_run: m.longest, handover_total: m.handoverTotal,
  };
}

module.exports = { renderCompany, model, data, names };

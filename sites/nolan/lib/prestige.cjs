// The Prestige deep page, "Who is reading whom": the film's nested reading (a prison frame, a diary
// inside it, a notebook inside that) as a stack you scrub through, a dive profile of how deep each beat
// plays, and a braid from film order to story order. Reads the-prestige/research/layers.json, written
// by a research child with a source per beat. Every count on the page is computed here from that file,
// and model() throws if the beat numbering is not a true permutation.
'use strict';
const { esc, readJSON } = require('./render.cjs');

const DEPTH = ['#EEF1F4', '#E8A23B', '#3C9AB4', '#C8463A', '#9AA6B2'];
const DOWN = ['At the surface', 'One book down', 'Two books down', 'Three books down', 'Four books down'];
const colour = d => DEPTH[d] || DEPTH[DEPTH.length - 1];
const down = d => DOWN[d] || `${d} books down`;

function model(r) {
  const beats = (r.beats || []).slice().sort((a, b) => a.film - b.film);
  const layers = (r.layers || []).slice().sort((a, b) => a.depth - b.depth);
  const n = beats.length;
  const stories = new Set(beats.map(b => b.story));
  beats.forEach((b, i) => { if (b.film !== i + 1) throw new Error(`film numbering breaks at ${b.film}`); });
  for (let i = 1; i <= n; i++) if (!stories.has(i)) throw new Error(`story position ${i} missing`);
  const depths = new Set(layers.map(l => l.depth));
  for (const b of beats) if (!depths.has(b.depth)) throw new Error(`beat ${b.film} has depth ${b.depth}, no such layer`);
  let shifts = 0, dives = 0;
  beats.forEach((b, i) => {
    if (!i) return;
    if (b.depth !== beats[i - 1].depth) shifts++;
    if (b.depth > 0 && beats[i - 1].depth === 0) dives++;
  });
  const deepest = Math.max(...beats.map(b => b.depth));
  const byDepth = layers.map(l => ({ depth: l.depth, name: l.name, count: beats.filter(b => b.depth === l.depth).length }));
  const sourced = beats.filter(b => b.placement === 'sourced').length;
  const inPlace = beats.filter(b => b.film === b.story).length;
  const earliest = beats.find(b => b.story === 1);
  const latest = beats.find(b => b.story === n);
  return { beats, layers, n, shifts, dives, deepest, byDepth, sourced, inferred: n - sourced, inPlace, earliest, latest };
}

const PF = { W: 1000, top: 26, lane: 66, left: 16, right: 984 };
const pfX = (m, film) => PF.left + (PF.right - PF.left) * (m.n === 1 ? 0.5 : (film - 1) / (m.n - 1));
const pfY = depth => PF.top + PF.lane * depth + 34;

function profile(m) {
  const H = PF.top + PF.lane * m.layers.length + 44;
  const X = f => pfX(m, f), Y = pfY;
  let s = `<svg class="pf" viewBox="0 0 ${PF.W} ${H}" role="img" aria-label="How deep each of the film's ${m.n} beats plays: ${m.shifts} changes of layer in ${m.n} beats, reaching ${esc(down(m.deepest).toLowerCase())}" xmlns="http://www.w3.org/2000/svg">`;
  m.layers.forEach(l => {
    const y = Y(l.depth);
    s += `<line x1="${PF.left}" y1="${y}" x2="${PF.right}" y2="${y}" stroke="#2A313B" stroke-dasharray="3 5"/>`;
    s += `<text x="${PF.left}" y="${y - 12}" class="pf__lane" fill="${colour(l.depth)}">${esc(l.name)}</text>`;
  });
  let d = '';
  m.beats.forEach((b, i) => {
    const x = X(b.film).toFixed(1), y = Y(b.depth);
    d += i ? ` H ${x} V ${y}` : `M ${x} ${y}`;
  });
  s += `<path d="${d}" fill="none" stroke="#5C6773" stroke-width="2"/>`;
  m.beats.forEach(b => {
    s += `<circle cx="${X(b.film).toFixed(1)}" cy="${Y(b.depth)}" r="6" fill="${colour(b.depth)}"><title>${b.film}. ${esc(b.what)}</title></circle>`;
  });
  s += `<circle id="pf-cur" cx="${X(1).toFixed(1)}" cy="${Y(m.beats[0].depth)}" r="12" fill="none" stroke="#EEF1F4" stroke-width="2.5"/>`;
  s += `<text x="${PF.left}" y="${H - 8}" class="pf__axis">Opening shot</text><text x="${PF.right}" y="${H - 8}" class="pf__axis" text-anchor="end">Last shot</text>`;
  return s + '</svg>';
}

function braid(m) {
  const n = m.n, W = 1000, H = 300, left = 30, right = W - 30, top = 60, bottom = H - 60;
  const X = i => left + (right - left) * (n === 1 ? 0.5 : (i - 1) / (n - 1));
  let s = `<svg class="braid" viewBox="0 0 ${W} ${H}" role="img" aria-label="Each of the ${n} beats drawn as a line from its place in the film (top) to its place in the story (bottom)" xmlns="http://www.w3.org/2000/svg">`;
  s += `<text x="${left}" y="24" class="braid__axis">As you watch it</text><text x="${left}" y="${H - 14}" class="braid__axis">As it happened</text>`;
  s += `<line x1="${left}" y1="${top}" x2="${right}" y2="${top}" stroke="#2A313B"/><line x1="${left}" y1="${bottom}" x2="${right}" y2="${bottom}" stroke="#2A313B"/>`;
  for (const b of m.beats) {
    const x0 = X(b.film), x1 = X(b.story), c = colour(b.depth), mid = (top + bottom) / 2;
    s += `<path class="braid__line" d="M ${x0.toFixed(1)} ${top} C ${x0.toFixed(1)} ${mid} ${x1.toFixed(1)} ${mid} ${x1.toFixed(1)} ${bottom}" fill="none" stroke="${c}" stroke-width="2" stroke-opacity="0.85"><title>${esc(b.what)} (film ${b.film}, story ${b.story})</title></path>`;
    s += `<circle cx="${x0.toFixed(1)}" cy="${top}" r="4.5" fill="${c}"/><circle cx="${x1.toFixed(1)}" cy="${bottom}" r="4.5" fill="${c}"/>`;
  }
  return s + '</svg>';
}

function nest(layers, depth = 0) {
  const l = layers.find(x => x.depth === depth);
  if (!l) return '';
  return `<div class="nest__l" data-depth="${l.depth}" style="--c:${colour(l.depth)}">
    <p class="nest__name">${esc(l.name)}</p>
    <p class="nest__who">${esc(l.holder)}.${l.text ? ` ${esc(l.text)}.` : ''}</p>
    ${nest(layers, depth + 1)}
  </div>`;
}

function renderPrestige(prefix) {
  const r = readJSON('the-prestige/research/layers.json');
  const m = model(r);
  const srcById = Object.fromEntries((r.sources || []).map(s => [s.id, s]));
  const cite = id => id && srcById[id] ? ` <a href="${esc(srcById[id].url)}">${esc(id)}</a>` : '';
  const pts = m.beats.map(b => ({ f: b.film, s: b.story, d: b.depth, w: b.what, p: b.where || '', x: Number(pfX(m, b.film).toFixed(1)), y: pfY(b.depth), l: down(b.depth) }));
  const json = JSON.stringify(pts).replace(/</g, '\\u003c');
  const first = m.beats[0];
  const items = m.beats.map(b => `<li class="seq" style="border-color:${colour(b.depth)}" data-screen="${b.film}" data-story="${b.story}">
      <span class="seq__n"><span class="seq__w">${b.film}</span><span class="seq__s">${b.story}</span></span>
      <span class="seq__label">${esc(b.what)}${b.placement === 'sourced' ? '' : ' <em class="seq__flag">placed by inference</em>'}</span>
    </li>`).join('\n');
  const traps = (r.traps || []).map(t => `<article class="trap">
      <h3 class="trap__h">${esc(t.writer)} writes for ${esc(t.reader)}</h3>
      <p><span class="trap__k">It appears to give</span> ${esc(t.says)}</p>
      <p><span class="trap__k">What it does</span> ${esc(t.does)}${cite(t.source)}</p>
    </article>`).join('\n');
  const claims = (r.claims || []).filter(c => c.value != null).map(c => `<li><span class="pre__what">${esc(c.what)}</span><span class="pre__val">${esc(typeof c.value === 'number' ? c.value.toLocaleString('en-GB') : c.value)}</span><span class="pre__note">${c.note ? esc(c.note) : ''}${cite(c.source)}</span></li>`).join('\n');
  const missing = (r.claims || []).filter(c => c.value == null).map(c => c.what);
  const conflicts = (r.conflicts || []).map(c => `<li>${esc(c)}</li>`).join('');
  const sources = (r.sources || []).map(s => `<li>${esc(s.id)}: <a href="${esc(s.url)}">${esc(s.title)}</a></li>`).join('');
  const depthLine = m.byDepth.map(d => `${d.count} in ${d.name}`).join(', ');
  const bottom = m.byDepth.find(d => d.depth === m.deepest).count;
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Who is reading whom</title>
<meta name="description" content="The Prestige as a stack of books: ${m.n} beats, ${m.shifts} changes of layer, in the order you watch them and the order they happened. Unofficial fan page, spoilers throughout.">
<meta name="theme-color" content="#0B0D11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${prefix}shared/site.css">
<link rel="stylesheet" href="${prefix}shared/memento.css">
<link rel="stylesheet" href="${prefix}shared/prestige.css">
</head>
<body>
<main class="site mem pre">
  <header class="site__head">
    <p class="site__kicker"><a href="${prefix}">Christopher Nolan, film by film</a> · The Prestige (2006) · spoilers throughout</p>
    <h1 class="site__h1">Who is reading whom.</h1>
    <p class="site__lede">The Prestige is a film about people reading each other's secrets, and it is built the same way: a man in a cell reads a rival's diary, the rival in that diary reads the first man's notebook, and each book was written with its reader in mind. Cut into ${m.n} beats, it makes ${m.dives === 1 ? 'one dive' : m.dives + ' dives'}: down through the diary, ${bottom} beats at the bottom in the notebook, and back up to the cell. Drag through it and watch the stack open.</p>
  </header>
  <section class="pre__scrub" aria-label="Scrub through the film">
    <div class="pre__stack">
      <div class="nest">${nest(m.layers)}</div>
    </div>
    <div class="pre__now">
      <label class="pre__range">Beat <output id="sc-film">1</output> of ${m.n}
        <input id="sc-n" type="range" min="1" max="${m.n}" value="1" step="1">
      </label>
      <p class="pre__depth" id="sc-depth">${esc(down(first.depth))}</p>
      <p class="pre__what-now" id="sc-what">${esc(first.what)}</p>
      <p class="pre__meta">In the story this is event <output id="sc-story">${first.story}</output> of ${m.n}<span id="sc-where">${first.where ? ' · ' + esc(first.where) : ''}</span></p>
    </div>
  </section>
  <figure class="mem__fig">${profile(m)}
    <figcaption>The film as a dive: each dot is a beat, in the order you watch them, on the layer I read it as playing in. ${esc(depthLine)}. That is ${m.shifts} changes of layer in this list and not in the edit: a beat list records what each stretch is mainly about, and it cannot see the film cutting between layers inside a stretch.</figcaption>
  </figure>
  ${traps ? `<section class="pre__traps" aria-label="The traps"><h2 class="site__kicker">Every book has a mark</h2><div class="traps">${traps}</div></section>` : ''}
  <figure class="mem__fig">${braid(m)}
    <figcaption>Each line joins a beat's place in the film (top) to its place in the story (bottom), coloured by layer. ${m.inPlace} of ${m.n} beats sit at the same position in both orders. The earliest event in the story, "${esc(m.earliest.what)}", is beat ${m.earliest.film} on screen.</figcaption>
  </figure>
  <section class="mem__list" aria-label="Every beat">
    <div class="mem__toggle" role="group" aria-label="Order">
      <button type="button" data-order="screen" aria-pressed="true">As you watch it</button>
      <button type="button" data-order="story" aria-pressed="false">As it happened</button>
    </div>
    <p class="mem__hint"><span class="seq__w">n</span> film order · <span class="seq__s">n</span> story order · film order follows a timestamped fan beat list · ${m.inferred} of ${m.n} have a layer or story place that is a guess, and are marked</p>
    <ol class="seqs" id="seqs">
${items}
    </ol>
  </section>
  ${claims ? `<section class="pre__claims-wrap" aria-label="The figures"><h2 class="site__kicker">The figures the sources give</h2><ul class="pre__claims">${claims}</ul>${missing.length ? `<p class="mem__hint">No fetched source gave: ${esc(missing.join('; '))}.</p>` : ''}</section>` : ''}
  ${conflicts ? `<section class="mem__notes"><h2 class="site__kicker">Where the sources disagree</h2><ul>${conflicts}</ul></section>` : ''}
  <section class="mem__notes">
    <h2 class="site__kicker">How this was put together</h2>
    <p>The ${m.n} beats are a fan's 40-beat screenwriting list (s3) merged and trimmed, not an official scene list; another reader would split it differently. Film order comes from that list's timestamps. It rarely names a layer, so the layer of each beat is a reading of what the sources describe, and story order leans on Wikipedia's chronological plot. Summaries are my own words. No source I fetched counts the tanks or the performances, so the page gives no number for them. ${r.not_fetched ? esc(r.not_fetched) : ''}</p>
  </section>
  <footer class="site__foot">
    <p>Researched ${esc(r.fetched || '')} by Proteus, an AI explorer. <a href="${prefix}films/the-prestige/">The Prestige page</a> · <a href="${prefix}data/the-prestige-layers.json">the data</a>.</p>
    ${sources ? `<ul class="mem__src">${sources}</ul>` : ''}
    <p>Not affiliated with Christopher Nolan, Syncopy or the film's distributors.</p>
  </footer>
</main>
<script>
(function () {
  var B = ${json};
  function el(id) { return document.getElementById(id); }
  var n = el('sc-n'), film = el('sc-film'), story = el('sc-story'), what = el('sc-what'), depth = el('sc-depth'), where = el('sc-where'), cur = el('pf-cur');
  var layers = Array.prototype.slice.call(document.querySelectorAll('.nest__l'));
  function show(i) {
    var b = B[i - 1];
    if (!b) return;
    film.textContent = String(b.f);
    story.textContent = String(b.s);
    what.textContent = b.w;
    depth.textContent = b.l;
    where.textContent = b.p ? ' · ' + b.p : '';
    cur.setAttribute('cx', b.x);
    cur.setAttribute('cy', b.y);
    layers.forEach(function (l) {
      var d = Number(l.dataset.depth);
      l.classList.toggle('is-on', d <= b.d);
      l.classList.toggle('is-here', d === b.d);
    });
  }
  n.addEventListener('input', function () { show(Number(n.value)); });
  show(Number(n.value));

  var list = el('seqs');
  var buttons = Array.prototype.slice.call(document.querySelectorAll('.mem__toggle button'));
  function order(key) {
    var items = Array.prototype.slice.call(list.children);
    items.sort(function (a, b) { return Number(a.dataset[key]) - Number(b.dataset[key]); });
    items.forEach(function (it) { list.appendChild(it); });
    list.dataset.order = key;
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.order === key)); });
  }
  buttons.forEach(function (b) { b.addEventListener('click', function () { order(b.dataset.order === 'story' ? 'story' : 'screen'); }); });
})();
</script>
</body>
</html>`;
}

module.exports = { renderPrestige, model, down };

// The Memento deep page: the film's sequences in watch order and in story order, drawn as a braid
// (each sequence a line from its screen slot to its story slot) and as a list that re-sorts itself.
// Reads memento/research/sequences.json, written by a research child with a source per line.
// Where a source gives no story position, the rule is applied (black and white forwards first, then
// colour from the last one shown to the first) and the page says the position is derived.
'use strict';
const { esc, readJSON } = require('./render.cjs');

const MONO = '#9AA6B2', COLOUR = '#C8463A', JOIN = '#E8A23B';

function withStory(seqs) {
  const out = seqs.map(s => Object.assign({}, s));
  const given = out.every(s => Number.isInteger(s.story_pos));
  if (given) return { seqs: out, derived: false };
  const mono = out.filter(s => s.strand === 'mono').sort((a, b) => a.screen - b.screen);
  const colour = out.filter(s => s.strand === 'colour').sort((a, b) => b.screen - a.screen);
  mono.concat(colour).forEach((s, i) => { s.story_pos = i + 1; });
  return { seqs: out, derived: true };
}

function braid(seqs) {
  const n = seqs.length, W = 1000, H = 300, left = 30, right = W - 30, top = 60, bottom = H - 60;
  const X = i => left + (right - left) * (n === 1 ? 0.5 : (i - 1) / (n - 1));
  let s = `<svg class="braid" viewBox="0 0 ${W} ${H}" role="img" aria-label="Each of Memento's ${n} sequences drawn as a line from where it sits on screen (top) to where it sits in the story (bottom)" xmlns="http://www.w3.org/2000/svg">`;
  s += `<text x="${left}" y="24" class="braid__axis">As you watch it</text><text x="${right}" y="24" class="braid__axis" text-anchor="end">opening scene first, left to right</text>`;
  s += `<text x="${left}" y="${H - 14}" class="braid__axis">As it happened</text><text x="${right}" y="${H - 14}" class="braid__axis" text-anchor="end">earliest event first, left to right</text>`;
  s += `<line x1="${left}" y1="${top}" x2="${right}" y2="${top}" stroke="#2A313B"/><line x1="${left}" y1="${bottom}" x2="${right}" y2="${bottom}" stroke="#2A313B"/>`;
  const sorted = seqs.slice().sort((a, b) => (a.strand === 'mono') - (b.strand === 'mono'));
  for (const q of sorted) {
    const c = q.strand === 'mono' ? MONO : q.strand === 'both' ? JOIN : COLOUR;
    const x0 = X(q.screen), x1 = X(q.story_pos);
    s += `<path class="braid__line" data-screen="${q.screen}" d="M ${x0.toFixed(1)} ${top} C ${x0.toFixed(1)} ${(top + bottom) / 2} ${x1.toFixed(1)} ${(top + bottom) / 2} ${x1.toFixed(1)} ${bottom}" fill="none" stroke="${c}" stroke-width="2" stroke-opacity="0.85"><title>${esc(q.label)} (on screen ${q.screen}, in story ${q.story_pos})</title></path>`;
    s += `<circle cx="${x0.toFixed(1)}" cy="${top}" r="4.5" fill="${c}"/><circle cx="${x1.toFixed(1)}" cy="${bottom}" r="4.5" fill="${c}"/>`;
  }
  const both = seqs.find(q => q.strand === 'both');
  if (both) {
    const xj = X(both.story_pos);
    s += `<text x="${xj.toFixed(1)}" y="${bottom + 26}" class="braid__join" text-anchor="middle">22/A: the Polaroid develops</text>`;
  }
  return s + '</svg>';
}

function renderMemento(prefix) {
  const r = readJSON('memento/research/sequences.json');
  const { seqs, derived } = withStory(r.sequences || []);
  const nC = seqs.filter(s => s.strand !== 'mono').length, nM = seqs.filter(s => s.strand !== 'colour').length;
  const counted = r.counts || {};
  const unverified = seqs.filter(s => !s.verified).length;
  const name = q => q.strand === 'both' ? 'Black and white 22 becomes colour A' : (q.strand === 'mono' ? 'Black and white ' : 'Colour ') + q.label;
  const items = seqs.slice().sort((a, b) => a.screen - b.screen).map(q => `<li class="seq seq--${q.strand}" data-screen="${q.screen}" data-story="${q.story_pos}">
      <span class="seq__n"><span class="seq__w">${q.screen}</span><span class="seq__s">${q.story_pos}</span></span>
      <span class="seq__label">${esc(name(q))}${q.verified ? '' : ' <em class="seq__flag">from the pattern</em>'}</span>
    </li>`).join('\n');
  const anchors = (r.anchors || []).map(a => `<li>${esc(a.what)} <a href="${esc(a.source)}">source</a></li>`).join('');
  const sources = (r.sources || []).filter(s => s.fetched).map(s => `<li><a href="${esc(s.url)}">${esc(s.url.replace(/^https?:\/\//, '').slice(0, 70))}</a>: ${esc(s.what)}</li>`).join('');
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Memento, both ways</title>
<meta name="description" content="Memento's ${seqs.length} sequences in the order you watch them and the order they happened, drawn as a braid. Unofficial fan page.">
<meta name="theme-color" content="#0B0D11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${prefix}shared/site.css">
<link rel="stylesheet" href="${prefix}shared/memento.css">
</head>
<body>
<main class="site mem">
  <header class="site__head">
    <p class="site__kicker"><a href="${prefix}">Christopher Nolan, film by film</a> · Memento (2000)</p>
    <h1 class="site__h1">Memento, both ways.</h1>
    <p class="site__lede">${seqs.length} sequences. ${nM} in black and white run forwards; ${nC} in colour are shown last event first. The two strands share one sequence, where black and white turns to colour. Each line joins a sequence's place on screen (top) to its place in the story (bottom). The grey lines lean gently left. The red ones fan right across the whole picture, because the film's opening scene is the story's end.</p>
  </header>
  <figure class="mem__fig">${braid(seqs)}
    <figcaption>Red: colour. Grey: black and white. ${derived ? 'Story positions are derived from the film\'s rule (black and white forwards, then colour from the last shown to the first), not read off a source line by line.' : 'Story order as the DVD\'s hidden chronological cut runs it.'} Numbering after Andy Klein (Salon, 2001), as Wikipedia gives it: black and white 1 to 22, colour A to V, with 22 and A the same sequence.</figcaption>
  </figure>
  <section class="mem__list" aria-label="Every sequence">
    <div class="mem__toggle" role="group" aria-label="Order">
      <button type="button" data-order="screen" aria-pressed="true">As you watch it</button>
      <button type="button" data-order="story" aria-pressed="false">As it happened</button>
    </div>
    <p class="mem__hint"><span class="seq__w">n</span> screen order · <span class="seq__s">n</span> story order${unverified ? ` · ${seqs.length - unverified} of ${seqs.length} placed by a source line by line, the other ${unverified} from the alternating pattern the source states` : ''}</p>
    <ol class="seqs" id="seqs">
${items}
    </ol>
  </section>
  ${anchors ? `<section class="mem__notes"><h2 class="site__kicker">Fixed points</h2><ul>${anchors}</ul></section>` : ''}
  ${r.gaps ? `<section class="mem__notes"><h2 class="site__kicker">What I could not pin down</h2><p>${esc(r.gaps)}</p></section>` : ''}
  <footer class="site__foot">
    <p>Researched ${esc(r.researched_on || '')} by Proteus, an AI explorer. Scene lines are my own short summaries, each tied to a source. <a href="${prefix}films/memento/">The Memento page</a> · <a href="${prefix}data/memento-sequences.json">the data</a>.</p>
    ${sources ? `<ul class="mem__src">${sources}</ul>` : ''}
    <p>Not affiliated with Christopher Nolan, Syncopy or the film's distributors.</p>
  </footer>
</main>
<script>
(function () {
  var list = document.getElementById('seqs');
  var buttons = document.querySelectorAll('.mem__toggle button');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function order(key) {
    var items = Array.prototype.slice.call(list.children);
    var before = new Map(items.map(function (el) { return [el, el.getBoundingClientRect().top]; }));
    items.sort(function (a, b) { return Number(a.dataset[key]) - Number(b.dataset[key]); });
    items.forEach(function (el) { list.appendChild(el); });
    list.dataset.order = key;
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.order === key)); });
    if (still) return;
    items.forEach(function (el) {
      var dy = before.get(el) - el.getBoundingClientRect().top;
      if (!dy) return;
      el.animate([{ transform: 'translateY(' + dy + 'px)' }, { transform: 'none' }], { duration: 520, easing: 'cubic-bezier(.2,.7,.2,1)' });
    });
  }
  buttons.forEach(function (b) { b.addEventListener('click', function () { order(b.dataset.order === 'story' ? 'story' : 'screen'); }); });
})();
</script>
</body>
</html>`;
}

module.exports = { renderMemento };

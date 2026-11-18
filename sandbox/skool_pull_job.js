// Skool room pull job, run inside the signed-in browser pane on a page of the room (18 Nov 2026).
// Builds window.__pull[GROUP] = {courses: [markdown], caps: [[title, transcript]], ext: [[title, url]],
// posts: [{d, by, name, t, c, v, s, n, u, own}], locked: [...], ownerId, log, progress, done}, the shape
// sandbox/skool_pull_save.py reads. Paced: 2.5 s per skool.com request, 0.4 s per Mux request.
// The 19 Oct job that first built this shape was never saved; this file is so the next pull has it.
// Edit GROUP and OWNERS, paste into javascript_tool, then poll window.__pull[GROUP].progress.
(async () => {
  const GROUP = 'rank-expand-academy';
  const OWNERS = ['jesse-cunningham', 'shawn-buckles'];
  const PACE = 2500, MUXPACE = 400;
  const nd = JSON.parse(document.getElementById('__NEXT_DATA__').textContent);
  const B = nd.buildId;
  window.__pull = window.__pull || {};
  const R = {courses: [], caps: [], ext: [], posts: [], locked: [], ownerId: null, log: [], progress: 'start', done: false,
             counts: {courses_open: 0, modules: 0, modules_text: 0, mux_ok: 0, mux_fail: 0, feed_pages: 0}};
  window.__pull[GROUP] = R;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const jget = async u => { await sleep(PACE); const r = await fetch(u, {credentials: 'include'}); if (!r.ok) throw new Error(r.status + ' ' + u); return r.json(); };
  const tget = async u => { await sleep(MUXPACE); const r = await fetch(u); if (!r.ok) throw new Error(r.status + ' ' + u); return r.text(); };
  const sl = s => (s || 'x').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60);
  const VID = /https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=[\w-]+|youtu\.be\/[\w-]+|loom\.com\/share\/\w+|vimeo\.com\/\d+|player\.vimeo\.com\/video\/\d+|wistia\.com\/medias\/\w+)[^\s)\]"']*/g;

  // editor JSON "[v2][...]" to markdown
  const inl = nodes => (nodes || []).map(n => {
    if (n.type === 'text') {
      let t = n.text || '';
      for (const m of (n.marks || [])) {
        if (m.type === 'bold') t = '**' + t + '**';
        else if (m.type === 'italic') t = '*' + t + '*';
        else if (m.type === 'code') t = '`' + t + '`';
        else if (m.type === 'link' && m.attrs && m.attrs.href) t = '[' + t + '](' + m.attrs.href + ')';
      }
      return t;
    }
    if (n.type === 'hardBreak') return '\n';
    if (n.type === 'image') return '![image](' + ((n.attrs || {}).src || '') + ')';
    if (n.type === 'mention') return '@' + ((n.attrs || {}).label || (n.attrs || {}).id || '');
    if (n.content) return inl(n.content);
    const a = n.attrs || {}; const u = a.src || a.href || a.url;
    return u ? '[' + n.type + '](' + u + ')' : '';
  }).join('');
  const blk = (nodes, depth) => (nodes || []).map(n => {
    const a = n.attrs || {};
    switch (n.type) {
      case 'paragraph': return inl(n.content) + '\n';
      case 'heading': return '#'.repeat(Math.min(6, (a.level || 2) + 1)) + ' ' + inl(n.content) + '\n';
      case 'bulletList': return (n.content || []).map(li => '  '.repeat(depth) + '- ' + blk(li.content, depth + 1).trim().replace(/\n+/g, '\n' + '  '.repeat(depth + 1)) + '\n').join('');
      case 'orderedList': return (n.content || []).map((li, i) => '  '.repeat(depth) + (i + 1) + '. ' + blk(li.content, depth + 1).trim().replace(/\n+/g, '\n' + '  '.repeat(depth + 1)) + '\n').join('');
      case 'listItem': return blk(n.content, depth);
      case 'blockquote': return blk(n.content, depth).split('\n').map(l => l ? '> ' + l : l).join('\n') + '\n';
      case 'codeBlock': return '```\n' + inl(n.content) + '\n```\n';
      case 'horizontalRule': return '---\n';
      case 'image': return '![image](' + (a.src || '') + ')\n';
      default: {
        const u = a.src || a.href || a.url || a.videoUrl || a.embedUrl;
        if (u) return '[' + n.type + '](' + u + ')\n';
        return n.content ? blk(n.content, depth) : (n.text ? n.text + '\n' : '');
      }
    }
  }).join('\n');
  const toMd = desc => {
    if (!desc) return '';
    if (typeof desc === 'string' && desc.startsWith('[v2]')) { try { return blk(JSON.parse(desc.slice(4)), 0).replace(/\n{3,}/g, '\n\n').trim(); } catch (e) { return desc; } }
    return String(desc);
  };
  const resLines = res => {
    if (!res) return [];
    let arr = res; if (typeof res === 'string') { try { arr = JSON.parse(res); } catch (e) { return [res]; } }
    if (!Array.isArray(arr)) return [];
    return arr.map(x => { const t = x.title || x.name || x.type || 'resource'; const u = x.url || x.link || x.href || (x.fileId ? 'skool-file:' + x.fileId : ''); return u ? '- [' + t + '](' + u + ')' : '- ' + t; });
  };
  const lockWhy = m => { const w = []; if (m.privacy === 1) w.push('coming soon'); if (m.minTier >= 2) w.push('premium tier'); if (m.lockFreeTrial) w.push('locked on the free trial'); if (m.dripDays) w.push('drips after ' + m.dripDays + ' days'); if (m.minAccessLevel) w.push('level ' + m.minAccessLevel); return w.join(', ') || 'no access'; };

  // Mux captions: stream m3u8 -> subtitles playlist -> VTT segments
  const muxCaps = async (pid, tok) => {
    const m3 = await tget('https://stream.mux.com/' + pid + '.m3u8?token=' + encodeURIComponent(tok));
    const line = m3.split('\n').find(l => l.startsWith('#EXT-X-MEDIA:TYPE=SUBTITLES') && /LANGUAGE="en/.test(l)) || m3.split('\n').find(l => l.startsWith('#EXT-X-MEDIA:TYPE=SUBTITLES'));
    if (!line) throw new Error('no subtitle track');
    const uri = (line.match(/URI="([^"]+)"/) || [])[1];
    const pl = await tget(uri);
    const segs = pl.split('\n').filter(l => l && !l.startsWith('#')).map(s => new URL(s, uri).href);
    const cues = []; let last = '';
    for (const s of segs) {
      const vtt = await tget(s);
      for (const raw of vtt.split('\n')) {
        const l = raw.trim();
        if (!l || l === 'WEBVTT' || /^\d+$/.test(l) || l.includes('-->') || /^(X-TIMESTAMP-MAP|NOTE|STYLE|REGION)/.test(l)) continue;
        const t = l.replace(/<[^>]+>/g, '');
        if (t && t !== last) { cues.push(t); last = t; }
      }
    }
    return cues.join(' ');
  };

  const findNode = (nodes, id) => { for (const n of nodes || []) { if (n.course && n.course.id === id) return n.course; const f = findNode(n.children, id); if (f) return f; } return null; };
  const flat = (nodes, set, out) => { for (const n of nodes || []) { const c = n.course || {}; const m = c.metadata || {}; if (n.children && n.children.length) flat(n.children, m.title || set, out); else out.push({id: c.id, title: m.title || c.name, set}); } return out; };

  try {
    // classroom
    const cl = await jget('/_next/data/' + B + '/' + GROUP + '/classroom.json');
    const all = cl.pageProps.allCourses || [];
    R.ownerId = ((cl.pageProps.currentGroup || {}).metadata || {}).createdBy || null;
    for (let ci = 0; ci < all.length; ci++) {
      const c = all[ci]; const m = c.metadata || {}; const ct = m.title || c.name;
      if (!m.hasAccess) { R.locked.push(ct + ' (' + (m.numModules || '?') + ' modules; ' + lockWhy(m) + ')'); continue; }
      R.progress = 'course ' + (ci + 1) + '/' + all.length + ' ' + ct;
      let out = '# ' + ct + '\n\n' + toMd(m.desc) + '\n\n' + (m.numModules || 0) + ' modules.\n';
      try {
        const j = await jget('/_next/data/' + B + '/' + GROUP + '/classroom/' + c.name + '.json');
        const red = (j.pageProps || {}).__N_REDIRECT || '';
        const first = (red.match(/md=([0-9a-f]+)/) || [])[1];
        if (!first) { out += '\n(no modules reachable)\n'; R.courses.push(out); R.counts.courses_open++; continue; }
        const j2 = await jget('/_next/data/' + B + '/' + GROUP + '/classroom/' + c.name + '.json?md=' + first);
        const tree = (j2.pageProps.course || {}).children || [];
        const mods = flat(tree, '', []);
        let curSet = null;
        for (let mi = 0; mi < mods.length; mi++) {
          const mod = mods[mi];
          R.progress = 'course ' + (ci + 1) + '/' + all.length + ' ' + ct + ' module ' + (mi + 1) + '/' + mods.length;
          const mj = mod.id === first ? j2 : await jget('/_next/data/' + B + '/' + GROUP + '/classroom/' + c.name + '.json?md=' + mod.id);
          const pp = mj.pageProps || {};
          const node = findNode((pp.course || {}).children, mod.id) || {};
          const nm = node.metadata || {};
          if (mod.set && mod.set !== curSet) { out += '\n## Set: ' + mod.set + '\n'; curSet = mod.set; }
          out += '\n### ' + (nm.title || mod.title) + '\n\n';
          const body = toMd(nm.desc);
          if (body) { out += body + '\n'; R.counts.modules_text++; }
          const rl = resLines(nm.resources); if (rl.length) out += '\nResources:\n' + rl.join('\n') + '\n';
          const label = ct + ' - ' + (nm.title || mod.title);
          const v = pp.video || null;
          if (v && v.playbackId && v.playbackToken) {
            out += '\nVideo: Skool-hosted (' + v.id + ')\n';
            try { const tx = await muxCaps(v.playbackId, v.playbackToken); if (tx && tx.length > 20) { R.caps.push([label, tx]); R.counts.mux_ok++; } else { R.counts.mux_fail++; R.log.push('mux empty ' + label); } }
            catch (e) { R.counts.mux_fail++; R.log.push('mux fail ' + label + ': ' + e.message); }
          } else if (v && (v.url || v.embedUrl || v.videoUrl)) {
            const u = v.url || v.embedUrl || v.videoUrl; out += '\nVideo: ' + u + '\n'; R.ext.push([label, u]);
          }
          for (const u of (body + ' ' + rl.join(' ')).match(VID) || []) { if (!R.ext.some(e => e[1] === u)) R.ext.push([label, u]); }
          R.counts.modules++;
        }
      } catch (e) { R.log.push('course fail ' + ct + ': ' + e.message); out += '\n(pull failed: ' + e.message + ')\n'; }
      R.courses.push(out); R.counts.courses_open++;
    }
    // feed
    let total = null, p = 1;
    while (true) {
      R.progress = 'feed page ' + p + (total ? '/' + Math.ceil(total / 30) : '');
      let fj; try { fj = await jget('/_next/data/' + B + '/' + GROUP + '.json?p=' + p); } catch (e) { R.log.push('feed fail p' + p + ': ' + e.message); break; }
      const fp = fj.pageProps || {}; total = total || fp.total || 0;
      const trees = fp.postTrees || []; if (!trees.length) break;
      for (const t of trees) {
        const po = t.post || {}; const pm = po.metadata || {}; const u = po.user || {};
        const c = pm.content || '';
        const vids = (c.match(VID) || []); const sk = (() => { try { const a = JSON.parse(pm.videoIds || '[]'); return Array.isArray(a) ? a : []; } catch (e) { return []; } })();
        R.posts.push({d: (po.createdAt || '').slice(0, 10), by: u.name || po.userId, name: po.name, t: pm.title || '', c: c + (sk.length ? '\n[Skool-hosted video x' + sk.length + ': ' + sk.join(', ') + ']' : ''), v: vids, s: pm.upvotes || 0, n: pm.comments || 0, u: 'https://www.skool.com/' + GROUP + '/' + po.name, own: (po.userId && po.userId === R.ownerId) || OWNERS.includes(u.name)});
      }
      R.counts.feed_pages = p;
      if (total && p * 30 >= total) break;
      p++;
      if (p > 200) break;
    }
    R.progress = 'done';
  } catch (e) { R.log.push('fatal: ' + e.message); R.progress = 'fatal: ' + e.message; }
  R.done = true;
})();
'job started';

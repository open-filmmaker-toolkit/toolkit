// Reading a screenplay in Fountain, the open plain-text screenplay format most screenwriting
// apps export (https://fountain.io). It finds the scenes, who speaks in each, and lays the
// script out on pages the way a screenplay prints, about 55 lines a page, so page counts in
// eighths and sides come out close to what a screenwriting app shows.
const oftFountain = (() => {
  const str = v => (v == null ? '' : String(v));
  const LINES = 55;
  const HEAD = /^(?:INT\.?\/EXT|INT\/EXT|I\/E|INT|EXT|EST)[.\s]/i;
  const upper = t => /[A-Z]/.test(t) && t === t.toUpperCase();
  // Notes ([[...]]) and boneyard (/* ... */) aren't part of the script.
  const strip = text => str(text).replace(/\r\n?/g, '\n').replace(/\/\*[\s\S]*?\*\//g, '').replace(/\[\[[\s\S]*?\]\]/g, '').replace(/\t/g, '    ');
  const wrap = (t, w) => Math.max(1, Math.ceil(t.length / w));
  // "EXT. RIVERSIDE LEVEE - NIGHT" → { intExt: 'EXT', set: 'RIVERSIDE LEVEE', time: 'NIGHT' }
  function heading(h) {
    const m = str(h).trim().match(/^(INT\.?\/EXT|INT\/EXT|I\/E|INT|EXT|EST)\.?\s*(.*)$/i);
    const kind = m ? m[1].toUpperCase().replace('.', '').replace('I/E', 'INT/EXT') : '';
    const rest = m ? m[2] : str(h).trim();
    const i = rest.lastIndexOf(' - ');
    return { intExt: kind === 'INTEXT' ? 'INT/EXT' : kind, set: (i > 0 ? rest.slice(0, i) : rest).trim(), time: i > 0 ? rest.slice(i + 3).trim() : '' };
  }
  // A character name without (V.O.), (CONT'D), @ or ^.
  const who = t => str(t).replace(/^@/, '').replace(/\^\s*$/, '').replace(/\s*\(.*?\)\s*/g, ' ').trim();
  function parse(text) {
    const lines = strip(text).split('\n');
    const title = {};
    let i = 0;
    if (/^[A-Za-z][A-Za-z ]*:/.test(lines[0] || '')) {
      let key = '';
      for (; i < lines.length && lines[i].trim(); i++) {
        const m = lines[i].match(/^([A-Za-z][A-Za-z ]*):\s*(.*)$/);
        if (m) { key = m[1].trim().toLowerCase(); title[key] = m[2].trim(); } else if (key) title[key] = `${title[key] ? title[key] + '\n' : ''}${lines[i].trim()}`;
      }
    }
    const els = [];
    const blank = n => n < 0 || n >= lines.length || !lines[n].trim();
    let speaking = false;
    for (; i < lines.length; i++) {
      const raw = lines[i], t = raw.trim();
      if (!t) { speaking = false; els.push({ type: 'blank', line: i }); continue; }
      if (speaking) { els.push({ type: /^\(.*\)$/.test(t) ? 'parenthetical' : 'dialogue', text: t, line: i }); continue; }
      if (t === '===' || /^={3,}$/.test(t)) { els.push({ type: 'page', line: i }); continue; }
      if (/^#/.test(t)) { els.push({ type: 'section', text: t.replace(/^#+\s*/, ''), line: i }); continue; }
      if (/^=(?!=)/.test(t)) { els.push({ type: 'synopsis', text: t.replace(/^=\s*/, ''), line: i }); continue; }
      if (blank(i - 1) && ((t[0] === '.' && t[1] !== '.' && /\w/.test(t[1] || '')) || HEAD.test(t))) {
        let h = t.replace(/^\./, ''), number = '';
        const n = h.match(/\s*#([^#]+)#\s*$/);
        if (n) { number = n[1].trim(); h = h.slice(0, n.index).trim(); }
        els.push({ type: 'scene', text: h, number, line: i });
        continue;
      }
      if (/^>.*<$/.test(t)) { els.push({ type: 'centered', text: t.slice(1, -1).trim(), line: i }); continue; }
      if (t[0] === '>' || (blank(i - 1) && blank(i + 1) && upper(t) && /TO:$/.test(t))) { els.push({ type: 'transition', text: t.replace(/^>\s*/, ''), line: i }); continue; }
      if (t[0] === '~') { els.push({ type: 'lyric', text: t.slice(1).trim(), line: i }); continue; }
      if (blank(i - 1) && !blank(i + 1) && (t[0] === '@' || (upper(who(t)) && !/[.!?:]$/.test(who(t)) && who(t).length <= 40 && t[0] !== '!'))) {
        els.push({ type: 'character', text: t.replace(/^@/, ''), name: who(t), line: i });
        speaking = true;
        continue;
      }
      els.push({ type: 'action', text: t.replace(/^!/, ''), line: i });
    }
    // Lay out pages: count printed lines for each element.
    let page = 1, on = 0, lastBlank = true;
    for (const e of els) {
      let n;
      if (e.type === 'page') { if (on) { page++; on = 0; } e.page = page; continue; }
      if (e.type === 'section' || e.type === 'synopsis') { n = 0; }
      else if (e.type === 'blank') { n = lastBlank ? 0 : 1; lastBlank = true; }
      else {
        lastBlank = false;
        n = e.type === 'dialogue' ? wrap(e.text, 35) : e.type === 'parenthetical' ? wrap(e.text, 25) : e.type === 'action' || e.type === 'lyric' || e.type === 'centered' ? wrap(e.text, 61) : 1;
      }
      if (on + n > LINES && on > 0) { page++; on = 0; if (e.type === 'blank') n = 0; }
      e.page = page; e.rows = n; on += n;
    }
    // Scenes: heading, what's in it, who speaks, and how long it runs.
    const scenes = [];
    let cur = null;
    els.forEach((e, k) => {
      if (e.type === 'scene') {
        cur = Object.assign({ heading: e.text, number: e.number, order: scenes.length, start: k, end: k, page: e.page, rows: 0, characters: [], synopsis: '', action: '' }, heading(e.text));
        scenes.push(cur);
      }
      if (!cur) return;
      cur.end = k; cur.rows += e.rows || 0;
      e.scene = cur.order;
      if (e.type === 'character' && e.name && !cur.characters.includes(e.name)) cur.characters.push(e.name);
      if (e.type === 'synopsis' && !cur.synopsis) cur.synopsis = e.text;
      if (e.type === 'action' && cur.action.length < 160) cur.action = `${cur.action ? cur.action + ' ' : ''}${e.text}`.slice(0, 160);
    });
    for (const s of scenes) { s.eighths = Math.max(1, Math.round(s.rows / (LINES / 8))); s.endPage = els[s.end].page || s.page; }
    return { title, elements: els, scenes, pages: els.length ? els[els.length - 1].page || page : 0 };
  }
  // Eighths of a page as a screenplay shows them: 11 → "1 3/8".
  function eighths(n) {
    n = Math.round(Number(n) || 0);
    if (n <= 0) return '0';
    const w = Math.floor(n / 8), r = n % 8;
    return `${w ? w : ''}${w && r ? ' ' : ''}${r ? `${r}/8` : ''}`;
  }
  // "1 3/8", "3/8", "2" or "1.5" → eighths.
  function toEighths(v) {
    const s = str(v).trim();
    let m = s.match(/^(\d+)\s+(\d+)\/8$/);
    if (m) return +m[1] * 8 + +m[2];
    m = s.match(/^(\d+)\/8$/);
    if (m) return +m[1];
    if (/^\d+(\.\d+)?$/.test(s)) return Math.round(parseFloat(s) * 8);
    return null;
  }
  // Which parsed scene a saved scene is: by scene number, then by heading and position.
  function match(saved, parsed) {
    const norm = s => str(s).toUpperCase().replace(/[^A-Z0-9]+/g, ' ').trim();
    if (saved.number) { const hit = parsed.find(p => p.number && p.number === str(saved.number)); if (hit) return hit; }
    const same = parsed.filter(p => norm(p.heading) === norm(saved.heading));
    if (!same.length) return null;
    return same.find(p => p.order === saved.order) || same[0];
  }
  return { parse, heading, eighths, toEighths, match, LINES };
})();

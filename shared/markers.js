// Reading edit lists and marker lists exported from editing software, and a dialog
// that shows what an import would change before it's applied.
// Edit decision lists: CMX 3600, as DaVinci Resolve, Premiere Pro and Avid export them.
// Marker lists: Resolve's markers as an EDL, Premiere Pro's marker CSV, Avid's marker text file,
// or any CSV or tab-separated file with a timecode column and a name or comment column.
const oftMarkers = (() => {
  const str = v => (v == null ? '' : String(v));
  const TC = /^\d{1,2}:\d{2}:\d{2}[:;.]\d{2,3}$/;
  const norm = s => str(s).toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/\.[a-z0-9]{2,4}$/, '').replace(/[^a-z0-9]+/g, ' ').trim();
  // Text from a file, including the UTF-16 that Premiere Pro writes.
  async function read(file) {
    const buf = new Uint8Array(await file.arrayBuffer());
    if (buf[0] === 0xff && buf[1] === 0xfe) return new TextDecoder('utf-16le').decode(buf.subarray(2));
    if (buf[0] === 0xfe && buf[1] === 0xff) return new TextDecoder('utf-16be').decode(buf.subarray(2));
    return new TextDecoder('utf-8').decode(buf).replace(/^\uFEFF/, '');
  }
  // A CMX 3600 edit decision list: each event's reel, track, source and record timecodes, clip name and any marker.
  function parseEdl(text) {
    const events = [];
    let cur = null;
    for (const raw of str(text).replace(/\r/g, '').split('\n')) {
      const line = raw.trim();
      const m = line.match(/^(\d{1,6})\s+(\S+)\s+(\S+)\s+(\S+)(?:\s+\d+)?\s+(\d\d:\d\d:\d\d[:;]\d\d)\s+(\d\d:\d\d:\d\d[:;]\d\d)\s+(\d\d:\d\d:\d\d[:;]\d\d)\s+(\d\d:\d\d:\d\d[:;]\d\d)/);
      if (m) {
        cur = { n: m[1], reel: m[2], track: m[3], srcIn: m[5].replace(';', ':'), srcOut: m[6].replace(';', ':'), recIn: m[7].replace(';', ':'), recOut: m[8].replace(';', ':'), clip: '', marker: '' };
        events.push(cur);
        continue;
      }
      if (!cur) continue;
      let c = line.match(/^\*\s*FROM CLIP NAME:\s*(.+)$/i);
      if (c) { cur.clip = c[1].trim(); continue; }
      c = line.match(/^\*\s*(?:SOURCE FILE|LOC):\s*(.+)$/i);
      if (c && !cur.file) { cur.file = c[1].trim(); continue; }
      c = line.match(/\|M:([^|]*)/);
      if (c) { cur.marker = c[1].trim(); const d = line.match(/\|D:(\d+)/); if (d) cur.frames = Number(d[1]); }
    }
    return events;
  }
  function rows(text) {
    const lines = str(text).replace(/\r/g, '').split('\n').filter(l => l.trim());
    const sep = (lines[0] || '').includes('\t') ? '\t' : ',';
    const split = l => { if (sep === '\t') return l.split('\t').map(x => x.trim().replace(/^"|"$/g, '')); const out = []; let cell = '', q = false; for (let i = 0; i < l.length; i++) { const c = l[i]; if (q) { if (c === '"') { if (l[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; } else if (c === '"') q = true; else if (c === ',') { out.push(cell.trim()); cell = ''; } else cell += c; } out.push(cell.trim()); return out; };
    return lines.map(split);
  }
  // Markers: each has a timecode, an optional out point or length in frames, and a name or comment.
  function parse(text, name) {
    text = str(text);
    if (/\|M:/.test(text) || /^\s*\d{3,6}\s+\S+\s+\S+\s+\S+.*\d\d:\d\d:\d\d[:;]\d\d/m.test(text)) {
      return parseEdl(text).filter(e => e.marker || e.clip).map(e => ({ tc: e.recIn, out: e.recOut !== e.recIn ? e.recOut : '', frames: e.frames, name: e.marker || e.clip }));
    }
    const all = rows(text);
    if (!all.length) return [];
    const head = all[0].map(h => h.toLowerCase());
    const find = (...keys) => { const i = head.findIndex(h => keys.includes(h)); return i >= 0 ? i : head.findIndex(h => keys.some(k => k.length > 3 && h.includes(k))); };
    let tcCol = find('in', 'timecode', 'tc', 'start', 'record in', 'source in');
    let nameCol = find('marker name', 'name', 'title');
    let noteCol = find('description', 'comment', 'notes', 'note');
    let outCol = find('out', 'end');
    let durCol = find('duration', 'length');
    let body = all.slice(1);
    // Avid's marker text has no header: user, timecode, track, color, comment, duration.
    if (tcCol < 0 && all[0].some(c => TC.test(c))) { body = all; tcCol = all[0].findIndex(c => TC.test(c)); noteCol = all[0].length > 4 ? 4 : all[0].length - 1; nameCol = -1; durCol = all[0].length > 5 ? 5 : -1; outCol = -1; }
    if (tcCol < 0) return [];
    return body.filter(r => TC.test(str(r[tcCol]).trim())).map(r => {
      const nm = nameCol >= 0 ? str(r[nameCol]).trim() : '', note = noteCol >= 0 && noteCol !== nameCol ? str(r[noteCol]).trim() : '';
      const out = outCol >= 0 && outCol !== tcCol && TC.test(str(r[outCol]).trim()) ? str(r[outCol]).trim() : '';
      const d = durCol >= 0 ? str(r[durCol]).trim() : '';
      return { tc: str(r[tcCol]).trim().replace(';', ':'), out: out.replace(';', ':'), frames: /^\d+$/.test(d) ? Number(d) : undefined, dur: TC.test(d) ? d : '', name: nm || note, note: nm ? note : '' };
    }).filter(m => m.name);
  }
  // Timecode to frames and back, for working out an out point from a length.
  function frames(tc, fps) { const p = str(tc).split(/[:;.]/).map(Number); return p.length === 4 && p.every(n => isFinite(n)) ? ((p[0] * 60 + p[1]) * 60 + p[2]) * fps + p[3] : null; }
  function tcOf(f, fps) { const r = Math.round(fps); const fr = f % r, s = Math.floor(f / r); return [Math.floor(s / 3600), Math.floor(s / 60) % 60, s % 60, fr].map(n => String(n).padStart(2, '0')).join(':'); }
  function outOf(m, fps) {
    if (m.out) return m.out;
    const f = frames(m.tc, Math.round(fps));
    if (f == null) return '';
    const len = m.frames || (m.dur ? frames(m.dur, Math.round(fps)) : 0);
    return len > 1 ? tcOf(f + len, fps) : '';
  }
  // The review dialog: each change with a checkbox, applied together.
  function review({ title, intro, changes, onApply, applyLabel }) {
    let dlg = document.getElementById('oftReviewDialog');
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.id = 'oftReviewDialog'; dlg.className = 'oft-dialog'; dlg.setAttribute('aria-labelledby', 'oftReviewTitle');
      dlg.innerHTML = `<h2 id="oftReviewTitle"></h2><p id="oftReviewIntro"></p><div id="oftReviewList"></div>
        <div class="oft-actions"><button type="button" class="btn" id="oftReviewCancel">Cancel</button><button type="button" class="btn primary" id="oftReviewApply">Apply</button></div>`;
      document.body.append(dlg);
      dlg.querySelector('#oftReviewCancel').onclick = () => dlg.close();
    }
    const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
    const GROUPS = [['new', 'New'], ['changed', 'Changed'], ['missing', 'Not in this file'], ['same', 'No change']];
    dlg.querySelector('#oftReviewTitle').textContent = title;
    dlg.querySelector('#oftReviewIntro').textContent = intro;
    dlg.querySelector('#oftReviewList').innerHTML = GROUPS.map(([k, label]) => {
      const list = changes.map((c, i) => [c, i]).filter(([c]) => c.kind === k);
      if (!list.length) return '';
      return `<h3>${label} (${list.length})</h3><ul class="oft-review">${list.map(([c, i]) => `<li>${c.apply ? `<label><input type="checkbox" data-i="${i}"${c.checked === false ? '' : ' checked'}> <span><b>${e(c.label)}</b>${c.detail ? `<br><small>${e(c.detail)}</small>` : ''}</span></label>` : `<span><b>${e(c.label)}</b>${c.detail ? `<br><small>${e(c.detail)}</small>` : ''}</span>`}${c.choices ? `<select data-c="${i}" aria-label="What ${e(c.label)} is">${c.choices.map(([v, t]) => `<option value="${e(v)}">${e(t)}</option>`).join('')}</select>` : ''}</li>`).join('')}</ul>`;
    }).join('') || '<p>Nothing to import.</p>';
    const apply = dlg.querySelector('#oftReviewApply');
    apply.textContent = applyLabel || 'Apply the checked changes';
    apply.disabled = !changes.some(c => c.apply);
    apply.onclick = () => {
      const picked = [...dlg.querySelectorAll('input[data-i]:checked')].map(x => +x.dataset.i);
      picked.forEach(i => { const sel = dlg.querySelector(`select[data-c="${i}"]`); changes[i].apply(sel ? sel.value : undefined); });
      dlg.close();
      onApply(picked.length);
    };
    dlg.showModal();
  }
  return { read, parse, parseEdl, norm, frames, tcOf, outOf, review };
})();

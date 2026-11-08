// Import rows from a spreadsheet (CSV) into a tool. Each tool describes its
// columns in OFT_IMPORT, using the same column names as its spreadsheet template,
// so a filled-in template imports without any matching. Importing only adds.
const oftImport = (() => {
  const str = v => (v == null ? '' : String(v));
  const norm = s => str(s).toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9%]+/g, '');
  const esc = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const store = { get(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* storage off */ } } };
  function parse(text) {
    text = str(text).replace(/^﻿/, '');
    const first = text.split(/\r?\n/)[0] || '';
    const sep = [',', ';', '\t'].map(s => [s, first.split(s).length]).sort((a, b) => b[1] - a[1])[0][0];
    const rows = []; let row = [], cell = '', q = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (q) { if (c === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; continue; }
      if (c === '"' && cell === '') q = true;
      else if (c === sep) { row.push(cell); cell = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; }
      else cell += c;
    }
    if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
    return rows.filter(r => r.some(c => c.trim() !== ''));
  }
  // Values are written back as the tool stores them: undo the "'" a CSV export adds before = + - @.
  const clean = v => str(v).trim().replace(/^'(?=[=+\-@])/, '');
  function date(v) {
    const s = clean(v);
    if (/^\d{4}-\d{2}-\d{2}$/.test(s)) return s;
    let m = s.match(/^(\d{4})[/.](\d{1,2})[/.](\d{1,2})$/);
    if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`;
    m = s.match(/^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$/);
    if (m) { const y = m[3].length === 2 ? `20${m[3]}` : m[3]; return `${y}-${m[1].padStart(2, '0')}-${m[2].padStart(2, '0')}`; }
    const d = new Date(s);
    if (/[a-z]/i.test(s) && /\d{4}/.test(s) && !isNaN(d)) return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    return null;
  }
  function number(v) {
    let s = clean(v).replace(/[\s$€£¥]|[A-Z]{3}$|^[A-Z]{3}/g, '');
    if (/^-?\d{1,3}(\.\d{3})+(,\d+)?$/.test(s)) s = s.replace(/\./g, '').replace(',', '.');
    s = s.replace(/,/g, '');
    return s !== '' && isFinite(Number(s)) ? Number(s) : null;
  }
  const yes = v => /^(yes|y|true|1|x|✓|done)$/i.test(clean(v));
  const list = v => clean(v).split(/\s*[;\n]\s*|\s*,\s*(?![^()]*\))/).map(x => x.trim()).filter(Boolean);
  function values(spec) {
    if (!spec) return [];
    if (Array.isArray(spec)) return spec.map(x => typeof x === 'string' ? [x, x] : [x.id != null ? x.id : x.value, x.label]);
    return Object.entries(spec);
  }
  function pick(spec, v) {
    if (typeof spec === 'function') return spec(v);
    const s = norm(v);
    const hit = values(spec).find(([id, label]) => norm(id) === s || norm(label) === s) || values(spec).find(([id, label]) => s && (norm(label).startsWith(s) || s.startsWith(norm(label))));
    return hit ? hit[0] : undefined;
  }
  function setPath(o, key, v) { const parts = key.split('.'); let t = o; for (const p of parts.slice(0, -1)) t = t[p] = t[p] && typeof t[p] === 'object' ? t[p] : {}; t[parts[parts.length - 1]] = v; }
  const many = type => type === 'people' || type === 'places';
  const newId = p => `${p}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`;

  let S = null, state = null;
  const fields = () => S.fields.filter(f => f[2] !== 'skip');
  const known = col => S.fields.find(f => norm(f[0]) === norm(col) || (f[3] && f[3].alt && f[3].alt.some(a => norm(a) === norm(col))));
  function guess(col) {
    const saved = (store.get(`oft-import:${OFT_SLUG}`) || {})[norm(col)];
    if (saved !== undefined) return saved;
    const f = known(col);
    if (f) return f[2] === 'skip' ? '' : f[0];
    const g = fields().find(x => norm(x[1].split('.').pop()) === norm(col));
    return g ? g[0] : '';
  }
  function build() {
    const { head, rows, map } = state;
    const out = [];
    rows.forEach((cells, n) => {
      const raw = {}; head.forEach((h, i) => { raw[h] = clean(cells[i]); });
      if (S.skipRow && S.skipRow(raw)) return;
      const rec = S.make ? S.make(raw) : {}, problems = [], refs = [];
      head.forEach((h, i) => {
        const f = map[i] && S.fields.find(x => x[0] === map[i]);
        const v = clean(cells[i]);
        if (!f || v === '') return;
        const [label, key, type, extra] = f;
        let val = v;
        if (type === 'date') { val = date(v); if (val == null) { problems.push(`${label} "${v}" isn't a date, so it's left blank`); return; } }
        else if (type === 'num' || type === 'int') { val = number(v); if (val == null) { problems.push(`${label} "${v}" isn't a number, so it's left blank`); return; } }
        else if (type === 'yes') val = yes(v);
        else if (type === 'list') val = list(v);
        else if (type === 'enum') { val = pick(extra.values, v); if (val === undefined) { if (extra.free) val = v; else { problems.push(typeof extra.values === 'function' ? `${label} "${v}" isn't one the tool knows, so it's left as the default` : `${label} "${v}" isn't one of ${values(extra.values).map(x => x[1]).join(', ')}, so it's left as the default`); return; } } }
        else if (type === 'people' || type === 'places' || type === 'person' || type === 'place') { refs.push([key, type, many(type) ? list(v) : [v]]); return; }
        setPath(rec, key, val);
      });
      const keyField = S.fields.find(x => x[1] === S.key);
      const kv = S.key.split('.').reduce((o, k) => (o || {})[k], rec);
      if (S.key && (kv == null || str(kv).trim() === '') && !refs.some(x => x[0] === S.key && x[2].length)) { out.push({ n: n + 2, skip: true, problems: [`No ${keyField ? keyField[0].toLowerCase() : S.key}, so it's skipped`] }); return; }
      out.push({ n: n + 2, rec, refs, raw, problems, label: str(kv) || (refs.find(x => x[0] === S.key) || [0, 0, []])[2].join(', ') });
    });
    return out;
  }
  function preview() {
    const list = build(), add = list.filter(r => !r.skip), skipped = list.length - add.length;
    const flagged = list.filter(r => r.problems.length);
    $map();
    oftEl('oftImpSummary').textContent = `${add.length} ${add.length === 1 ? S.noun : S.nouns} to add${skipped ? `, ${skipped} row${skipped === 1 ? '' : 's'} skipped` : ''}.`;
    oftEl('oftImpRows').innerHTML = flagged.length ? `<h3>Check these rows</h3><ul>${flagged.slice(0, 50).map(r => `<li><b>Row ${r.n}${r.label ? `, ${esc(r.label)}` : ''}:</b> ${r.problems.map(esc).join('. ')}.</li>`).join('')}</ul>${flagged.length > 50 ? `<p>And ${flagged.length - 50} more.</p>` : ''}`
      : add.length ? `<h3>First rows</h3><ul>${add.slice(0, 5).map(r => `<li>${esc(r.label || `Row ${r.n}`)}</li>`).join('')}</ul>` : '';
    oftEl('oftImpAdd').disabled = !add.length;
    oftEl('oftImpAdd').textContent = add.length ? `Add ${add.length} ${add.length === 1 ? S.noun : S.nouns}` : 'Nothing to add';
    state.list = add;
  }
  function $map() {
    const box = oftEl('oftImpMap');
    if (box.dataset.ready === '1') return;
    box.dataset.ready = '1';
    const opts = c => `<option value="">Don't import</option>${fields().map(f => `<option value="${esc(f[0])}"${f[0] === c ? ' selected' : ''}>${esc(f[0])}</option>`).join('')}`;
    box.innerHTML = `<table><thead><tr><th scope="col">Column in the file</th><th scope="col">Goes to</th></tr></thead><tbody>${state.head.map((h, i) => `<tr><td>${esc(h || `Column ${i + 1}`)}${!state.map[i] && !(known(h) && known(h)[2] === 'skip') ? ' <small class="oft-unmatched">Not matched</small>' : ''}</td><td><select data-col="${i}" aria-label="Where ${esc(h || `column ${i + 1}`)} goes">${opts(state.map[i])}</select></td></tr>`).join('')}</tbody></table>`;
    box.querySelectorAll('select').forEach(s => s.addEventListener('change', () => { state.map[+s.dataset.col] = s.value; box.dataset.ready = ''; preview(); }));
  }
  function load(name, text) {
    const rows = parse(text);
    if (!rows.length) { oftEl('oftImpSummary').textContent = `${name} is empty.`; return; }
    const head = rows[0].map(h => h.trim());
    state = { name, head, rows: rows.slice(1), map: head.map(guess) };
    oftEl('oftImpFile').textContent = `${name}: ${state.rows.length} row${state.rows.length === 1 ? '' : 's'}`;
    oftEl('oftImpMap').dataset.ready = '';
    oftEl('oftImpStep').hidden = false;
    preview();
  }
  function commit() {
    const remember = store.get(`oft-import:${OFT_SLUG}`) || {};
    state.head.forEach((h, i) => { const f = known(h); if (!f || f[0] !== state.map[i]) remember[norm(h)] = state.map[i]; });
    store.set(`oft-import:${OFT_SLUG}`, remember);
    const people = () => (doc.people = Array.isArray(doc.people) ? doc.people : []);
    const places = () => (doc.locations = Array.isArray(doc.locations) ? doc.locations : []);
    const find = (arr, field, value, make) => { const v = str(value).trim(); let x = arr.find(r => r && norm(r[field]) === norm(v)); if (!x) { x = Object.assign({ id: newId(make && make.prefix || 'item') }, (make && make.fields) || {}, { [field]: v }); arr.push(x); } return x; };
    const ref = (type, name) => type.startsWith('person') || type === 'people' ? find(people(), 'name', name, { prefix: 'person' }).id : find(places(), 'name', name, { prefix: 'location' }).id;
    let added = 0;
    for (const r of state.list) {
      const rec = r.rec;
      rec.id = rec.id || newId(S.prefix || S.noun.replace(/\s+/g, '-'));
      for (const [key, type, names] of r.refs) { const ids = names.map(n => ref(type, n)); setPath(rec, key, many(type) ? ids : ids[0]); }
      const ctx = { raw: r.raw, find, ref, newId };
      if (S.put) { if (S.put(rec, ctx) === false) continue; } else S.list().push(rec);
      added++;
    }
    oftEl('oftImportDialog').close();
    if (typeof changed === 'function') changed(); else { dirty = true; render(); }
    toast(`Added ${added} ${added === 1 ? S.noun : S.nouns} from ${state.name}`);
  }
  function open(spec) {
    S = spec; state = null;
    let dlg = oftEl('oftImportDialog');
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.id = 'oftImportDialog'; dlg.className = 'oft-dialog'; dlg.setAttribute('aria-labelledby', 'oftImpTitle');
      dlg.innerHTML = `<h2 id="oftImpTitle"></h2><p id="oftImpIntro"></p>
        <p class="oft-files"><span id="oftImpFile">No file chosen</span> <button type="button" class="btn" id="oftImpChoose">Choose a CSV file</button></p>
        <input type="file" id="oftImpInput" accept=".csv,.tsv,.txt,text/csv" hidden>
        <div id="oftImpStep" hidden><h3>Match the columns</h3><div class="oft-map" id="oftImpMap"></div><p id="oftImpSummary" aria-live="polite"></p><div id="oftImpRows"></div></div>
        <div class="oft-actions"><button type="button" class="btn" id="oftImpCancel">Cancel</button><button type="button" class="btn primary" id="oftImpAdd" disabled>Add</button></div>`;
      document.body.append(dlg);
      oftEl('oftImpChoose').onclick = () => { oftEl('oftImpInput').value = ''; oftEl('oftImpInput').click(); };
      oftEl('oftImpInput').addEventListener('change', async ev => { const f = ev.target.files[0]; if (f) load(f.name, await f.text()); });
      oftEl('oftImpCancel').onclick = () => dlg.close();
      oftEl('oftImpAdd').onclick = commit;
    }
    oftEl('oftImpTitle').textContent = `Import ${S.nouns} from a spreadsheet`;
    oftEl('oftImpIntro').textContent = `Choose a CSV file. Columns named as in this tool's spreadsheet template are matched for you; match any others below. Importing adds ${S.nouns} and never changes or removes what's already here.`;
    oftEl('oftImpFile').textContent = 'No file chosen';
    oftEl('oftImpStep').hidden = true;
    oftEl('oftImpAdd').disabled = true; oftEl('oftImpAdd').textContent = 'Add';
    dlg.showModal();
  }
  return { open, parse, date, number };
})();

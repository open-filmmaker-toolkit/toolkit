// Shared by every tool: your name, remembering the open file, who has it open,
// who changed what, merging two copies and spotting conflicted copies.
// Runs inside each tool's script and uses its doc, fileHandle, baselineText,
// fileName, dirty, loadText, saveFile, serialize, render and toast.
const OFT_SLUG = (window.location.pathname.match(/tools\/([^/]+)\//) || [])[1] || '';
const OFT_GUIDE = 'https://github.com/open-filmmaker-toolkit/toolkit/blob/main/docs/sharing-a-project.md';
const OFT_HOURS = 4;
const OFT_KEYS = { project: 'Project details', people: 'People', locations: 'Locations', thirdPartyElements: 'Clearance log', contracts: 'Contracts and releases', releaseForms: 'Release wording', assets: 'Files and stills', musicCueSheet: 'Music cue sheet', callSheets: 'Call sheets', credits: 'Credits', supers: 'Name supers', subjects: 'Subject tracker', sources: 'Research log', comps: 'Comps tracker', treatment: 'Treatment', pitchDeck: 'Pitch deck', grants: 'Grant calendar', narratives: 'Narrative library', budget: 'Budget', budgetFormats: 'Budget converter', financePlan: 'Finance plan', funders: 'Funder CRM', cashFlow: 'Cash flow', shootDays: 'Shooting calendar', script: 'Script', scenes: 'Script breakdown', characters: 'Cast', dayOutOfDays: 'Day-out-of-days', budgetLinks: 'Budget', shots: 'Shot list', interviews: 'Interviews', stringOuts: 'String-outs', questionBank: 'Question bank', journal: 'Field journal', scouts: 'Location scouts', scoutChecklist: 'Scout checklist', gear: 'Gear list', trips: 'Travel sheet', riskPlans: 'Risk plans', security: 'Security checklist', mediaReports: 'Camera and sound reports', dailyReports: 'Daily reports', expenses: 'Expense log', festivals: 'Festival submissions', screenings: 'Screenings', pressOutlets: 'Press list', partners: 'Partner CRM', discussionGuide: 'Discussion guide', paperEdit: 'Paper edit', costReport: 'Budget-to-actuals', structure: 'Structure board', cuts: 'Cut tracker', clearanceReport: 'Clearance report', chainOfTitle: 'Chain of title', festivalStrategy: 'Festival strategy', pressNotes: 'Press notes', awards: 'Awards', socialPosts: 'Social posts', deliverables: 'Deliverables', qc: 'QC tracker', waterfall: 'Waterfall', revenueStatements: 'Revenue tracker', bookings: 'Bookings', theoryOfChange: 'Theory of change', screeningKit: 'Screening kit', impactReport: 'Impact report', finalCostReport: 'Final cost report', grantReports: 'Grant reports', contractArchive: 'Contract archive' };
const oftStore = { get(k) { try { return localStorage.getItem(k); } catch { return null; } }, set(k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch { /* storage off */ } } };
const oftMe = () => (oftStore.get('oft-user-name') || '').trim();
const oftEsc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const oftEl = id => document.getElementById(id);
// In the desktop app (desktop/bridge.js), a remembered file comes back from storage as plain data; this makes it a file handle again.
const oftRevive = v => (v && v.handle && v.handle.oftPath && window.oftDesktopHandle ? { ...v, handle: window.oftDesktopHandle(v.handle.oftPath) } : v);
function oftIdb(op, key, val) {
  return new Promise(res => {
    try {
      const r = indexedDB.open('open-filmmaker-toolkit', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('handles');
      r.onerror = () => res(null);
      r.onsuccess = () => {
        const db = r.result;
        try {
          const tx = db.transaction('handles', op === 'get' ? 'readonly' : 'readwrite');
          const s = tx.objectStore('handles');
          const q = op === 'get' ? s.get(key) : op === 'del' ? s.delete(key) : s.put(val, key);
          tx.oncomplete = () => { db.close(); res(op === 'get' ? oftRevive(q.result) || null : true); };
          tx.onerror = tx.onabort = () => { db.close(); res(null); };
        } catch { db.close(); res(null); }
      };
    } catch { res(null); }
  });
}
function oftWhen(iso) {
  const d = new Date(iso);
  if (isNaN(d)) return '';
  const time = d.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  return d.toDateString() === new Date().toDateString() ? time : `${d.toLocaleDateString([], { month: 'short', day: 'numeric' })}, ${time}`;
}
const oftDay = iso => { const d = new Date(iso); return isNaN(d) ? '' : d.toLocaleDateString([], { month: 'short', day: 'numeric' }); };
const oftChangedText = r => r && r.changedAt ? `Changed ${r.changedBy ? `by ${r.changedBy}, ` : ''}${oftDay(r.changedAt)}` : '';

// ---------- Who changed what ----------
const OFT_META = new Set(['changedAt', 'changedBy']);
const oftStrip = (k, v) => OFT_META.has(k) ? undefined : v && typeof v === 'object' && !Array.isArray(v) ? Object.fromEntries(Object.keys(v).sort().map(x => [x, v[x]])) : v;
const oftSame = (a, b) => JSON.stringify(a, oftStrip) === JSON.stringify(b, oftStrip);
const oftIsObj = v => !!v && typeof v === 'object' && !Array.isArray(v);
// Calls fn(record, key) for every object with an id. The key adds the path, because
// snapshots (saved versions, the last export) repeat ids from the live records.
function oftWalk(x, fn, path = '') {
  if (Array.isArray(x)) x.forEach(v => oftWalk(v, fn, path));
  else if (oftIsObj(x)) {
    if (typeof x.id === 'string' && x.id) fn(x, `${path}#${x.id}`);
    for (const [k, v] of Object.entries(x)) if (v && typeof v === 'object') oftWalk(v, fn, `${path}.${k}`);
  }
}
function oftStamp() {
  const me = oftMe();
  if (!me || !doc) return;
  let before = {};
  try { if (baselineText) before = JSON.parse(baselineText); } catch { /* keep empty */ }
  const old = new Map();
  oftWalk(before, (r, key) => old.set(key, r));
  const now = new Date().toISOString();
  oftWalk(doc, (r, key) => { const o = old.get(key); if (!o || !oftSame(o, r)) { r.changedBy = me; r.changedAt = now; } });
}

// ---------- Who has it open ----------
const oftFresh = p => p && p.name && p.since && Date.now() - new Date(p.since).getTime() < OFT_HOURS * 3600e3;
const oftOpenList = data => (Array.isArray(data && data.openBy) ? data.openBy : []).filter(oftFresh);
function oftWithout(text, me) {
  const data = JSON.parse(text);
  const list = oftOpenList(data).filter(p => p.name !== me);
  if (list.length) data.openBy = list; else delete data.openBy;
  return data;
}
async function oftWritable(handle) {
  if (!handle || !handle.queryPermission) return !!handle;
  try { return (await handle.queryPermission({ mode: 'readwrite' })) === 'granted' || (await handle.requestPermission({ mode: 'readwrite' })) === 'granted'; } catch { return false; }
}
async function oftWrite(handle, text) {
  const w = await handle.createWritable();
  await w.write(text);
  await w.close();
}
async function oftMarkOpen(text, handle) {
  const me = oftMe();
  if (!me || !handle || !(await oftWritable(handle))) return;
  try {
    const current = await (await handle.getFile()).text();
    if (current !== text || fileHandle !== handle) return;
    const data = oftWithout(current, me);
    data.openBy = (data.openBy || []).concat([{ name: me, since: new Date().toISOString(), tool: OFT_SLUG }]);
    const out = JSON.stringify(data, null, 2) + '\n';
    await oftWrite(handle, out);
    if (baselineText === text) baselineText = out;
    if (doc) doc.openBy = data.openBy;
  } catch { /* the note is optional */ }
}
async function oftClearOpen() {
  const me = oftMe(), handle = fileHandle;
  if (!me || !handle || dirty) return;
  try {
    if (handle.queryPermission && (await handle.queryPermission({ mode: 'readwrite' })) !== 'granted') return;
    const current = await (await handle.getFile()).text();
    if (!oftOpenList(JSON.parse(current)).some(p => p.name === me)) return;
    await oftWrite(handle, JSON.stringify(oftWithout(current, me), null, 2) + '\n');
  } catch { /* best effort */ }
}
function oftWarnOpen(text) {
  let list = [];
  try { list = oftOpenList(JSON.parse(text)).filter(p => p.name !== oftMe()); } catch { /* not JSON */ }
  const bar = oftEl('oftPresence');
  if (!bar) return;
  bar.hidden = !list.length;
  if (list.length) oftEl('oftPresenceText').textContent = `${list.map(p => `${p.name} has had this file open since ${oftWhen(p.since)}`).join('. ')}. If you both change it, whoever saves second gets a warning and can merge the two.`;
}

// ---------- Merging ----------
const OFT_SKIP = new Set(['savedAt', 'savedBy', 'openBy']);
const oftClone = v => v === undefined ? undefined : JSON.parse(JSON.stringify(v));
const oftLabel = r => { if (!oftIsObj(r)) return ''; const v = r.name || r.title || r.label || r.element || r.description || r.text || r.id; return String(v).slice(0, 70); };
const oftRecList = v => Array.isArray(v) && v.length > 0 && v.every(x => oftIsObj(x) && typeof x.id === 'string' && x.id);
const oftNewer = (a, b) => String((b && b.changedAt) || '') > String((a && a.changedAt) || '') ? 'b' : 'a';
function oftMerge(base, a, b) {
  const res = { conflicts: [], changes: [] };
  const tool = path => OFT_KEYS[path[0]] || String(path[0] || 'Project');
  const note = (side, kind, path, rec) => res.changes.push({ side, kind, tool: tool(path), label: oftLabel(rec) || path.slice(1).join(' ') || tool(path) });
  const conflict = (path, rec, av, bv, recA, recB, put) => {
    const pick = base === undefined ? oftNewer(recA, recB) : 'a';
    const c = { tool: tool(path), label: oftLabel(rec), field: String(path[path.length - 1]), a: av, b: bv, byA: oftChangedText(recA), byB: oftChangedText(recB), pick, put };
    res.conflicts.push(c);
    put(oftClone(pick === 'a' ? av : bv));
  };
  function recChanges(bs, av, bv, path) {
    if (bs === undefined) return;
    if (!oftSame(av, bs)) note('a', 'changed', path, av);
    if (!oftSame(bv, bs)) note('b', 'changed', path, bv);
  }
  function m(bs, av, bv, path, recA, recB, put) {
    if (oftSame(av, bv)) { put(oftClone(oftNewer(av, bv) === 'b' ? bv : av)); return; }
    if (bs !== undefined && base !== undefined) {
      if (oftSame(av, bs)) { put(oftClone(bv)); return; }
      if (oftSame(bv, bs)) { put(oftClone(av)); return; }
    }
    if (oftIsObj(av) && oftIsObj(bv)) {
      const out = {};
      put(out);
      const isRec = typeof av.id === 'string';
      const ra = isRec ? av : recA, rb = isRec ? bv : recB;
      const keys = [...new Set([...Object.keys(av), ...Object.keys(bv)])];
      for (const k of keys) {
        if (OFT_META.has(k)) continue;
        if (OFT_SKIP.has(k) && path.length === 0) { if (k in av) out[k] = oftClone(av[k]); continue; }
        const inA = k in av, inB = k in bv, bk = oftIsObj(bs) ? bs[k] : undefined, inBase = oftIsObj(bs) && k in bs;
        const p = path.concat(k);
        if (inA && inB) m(bk, av[k], bv[k], p, ra, rb, v => { out[k] = v; });
        else if (inA) {
          if (inBase && base !== undefined) { if (!oftSame(av[k], bk)) conflict(p, ra, av[k], undefined, ra, rb, v => { if (v === undefined) delete out[k]; else out[k] = v; }); }
          else out[k] = oftClone(av[k]);
        } else {
          if (inBase && base !== undefined) { if (!oftSame(bv[k], bk)) conflict(p, rb, undefined, bv[k], ra, rb, v => { if (v === undefined) delete out[k]; else out[k] = v; }); }
          else out[k] = oftClone(bv[k]);
        }
      }
      const src = oftNewer(av, bv) === 'b' ? bv : av;
      for (const k of OFT_META) if (k in src) out[k] = src[k];
      if (isRec) recChanges(bs, av, bv, path);
      return;
    }
    if (Array.isArray(av) && Array.isArray(bv) && (oftRecList(av) || oftRecList(bv)) && av.concat(bv).every(x => oftIsObj(x) && typeof x.id === 'string')) {
      const out = [];
      put(out);
      const ba = new Map(bv.map(x => [x.id, x])), aa = new Map(av.map(x => [x.id, x]));
      const bb = new Map((Array.isArray(bs) ? bs : []).filter(oftIsObj).map(x => [x.id, x]));
      const order = av.map(x => x.id);
      bv.forEach((x, i) => { if (!aa.has(x.id)) { const prev = i ? bv[i - 1].id : null; const at = prev ? order.indexOf(prev) : -1; order.splice(at + 1, 0, x.id); } });
      const slots = order.map(() => undefined);
      order.forEach((id, i) => {
        const x = aa.get(id), y = ba.get(id), z = bb.get(id), p = path.concat(oftLabel(x || y));
        const set = v => { slots[i] = v; };
        if (x && y) m(z, x, y, p, x, y, set);
        else if (x) {
          if (z && base !== undefined) { if (oftSame(x, z)) { note('b', 'removed', path, x); set(undefined); } else conflict(p, x, x, undefined, x, null, set); }
          else { note('a', 'added', path, x); set(oftClone(x)); }
        } else {
          if (z && base !== undefined) { if (oftSame(y, z)) { note('a', 'removed', path, y); set(undefined); } else conflict(p, y, undefined, y, null, y, set); }
          else { note('b', 'added', path, y); set(oftClone(y)); }
        }
      });
      res.finish = (res.finish || []).concat(() => { out.splice(0, out.length, ...slots.filter(v => v !== undefined)); });
      return;
    }
    conflict(path, recA || recB, av, bv, recA, recB, put);
  }
  let value;
  m(base, a, b, [], null, null, v => { value = v; });
  res.value = value;
  res.build = () => { (res.finish || []).forEach(f => f()); return value; };
  return res;
}
const oftShow = v => v === undefined ? 'Not there' : typeof v === 'string' ? v || 'Empty' : JSON.stringify(v);

let oftMergeState = null;
function oftOpenMerge(mode) {
  oftMergeState = { mode, a: null, b: null, base: undefined };
  const dlg = oftEl('oftMergeDialog');
  oftEl('oftMergeIntro').textContent = mode === 'conflict'
    ? `${fileName} changed after you opened it. These are the changes on each side. Where you both changed the same thing, choose which to keep.`
    : 'Choose two copies of the project file. Changes that don\'t clash are combined. Where both copies changed the same thing, you choose. The result is saved as a new file, so neither copy is changed.';
  oftEl('oftMergePick').hidden = mode === 'conflict';
  oftEl('oftMergeA').textContent = doc && fileName ? `The open file, ${fileName}` : 'Not chosen';
  if (mode !== 'conflict' && doc && fileName) oftMergeState.a = { name: fileName, data: JSON.parse(serialize()) };
  oftEl('oftMergeB').textContent = 'Not chosen';
  oftEl('oftMergeResult').innerHTML = '';
  oftEl('oftMergeSave').disabled = true;
  if (!dlg.open) dlg.showModal();
}
function oftReadCopy(side) {
  const input = oftEl('oftMergeFile');
  input.dataset.side = side;
  input.value = '';
  input.click();
}
async function oftTakeCopy(side, name, text) {
  let data;
  try { data = JSON.parse(text); } catch { toast(`Couldn't read ${name}: it isn't a project file.`, true); return; }
  if (!data || data.format !== 'open-filmmaker-toolkit/project') { toast(`Couldn't read ${name}: it isn't an Open Filmmaker Toolkit project file.`, true); return; }
  oftMergeState[side] = { name, data };
  oftEl(side === 'a' ? 'oftMergeA' : 'oftMergeB').textContent = name;
  if (oftMergeState.a && oftMergeState.b) oftCompare();
}
function oftCompare() {
  const s = oftMergeState;
  const r = oftMerge(s.base, s.a.data, s.b.data);
  s.result = r;
  const nameA = s.mode === 'conflict' ? 'Your changes' : s.a.name, nameB = s.mode === 'conflict' ? 'In the file now' : s.b.name;
  const tools = {};
  r.changes.forEach(c => { (tools[c.tool] = tools[c.tool] || []).push(c); });
  const verb = { added: 'Added', changed: 'Changed', removed: 'Removed' };
  const changeHtml = Object.keys(tools).length ? Object.entries(tools).map(([t, list]) => `<h4>${oftEsc(t)}</h4><ul>${list.map(c => `<li>${oftEsc(verb[c.kind])} in ${oftEsc(c.side === 'a' ? nameA : nameB)}: ${oftEsc(c.label)}</li>`).join('')}</ul>`).join('') : '<p>No records were added, changed or removed on just one side.</p>';
  const conflictHtml = r.conflicts.map((c, i) => `<fieldset class="oft-conflict"><legend>${oftEsc(c.tool)}${c.label ? `: ${oftEsc(c.label)}` : ''}, ${oftEsc(c.field)}</legend>
    <label><input type="radio" name="oftC${i}" value="a"${c.pick === 'a' ? ' checked' : ''}> <span><b>${oftEsc(nameA)}</b>${c.byA ? ` <small>${oftEsc(c.byA)}</small>` : ''}<br>${oftEsc(oftShow(c.a))}</span></label>
    <label><input type="radio" name="oftC${i}" value="b"${c.pick === 'b' ? ' checked' : ''}> <span><b>${oftEsc(nameB)}</b>${c.byB ? ` <small>${oftEsc(c.byB)}</small>` : ''}<br>${oftEsc(oftShow(c.b))}</span></label></fieldset>`).join('');
  oftEl('oftMergeResult').innerHTML = `<h3>What changed</h3>${changeHtml}<h3>${r.conflicts.length ? `${r.conflicts.length} thing${r.conflicts.length === 1 ? '' : 's'} changed in both` : 'Nothing clashes'}</h3>${r.conflicts.length ? conflictHtml : '<p>Everything can be combined as it is.</p>'}`;
  oftEl('oftMergeSave').disabled = false;
}
async function oftSaveMerged() {
  const s = oftMergeState, r = s.result;
  r.conflicts.forEach((c, i) => { const v = (document.querySelector(`input[name="oftC${i}"]:checked`) || {}).value || c.pick; c.put(oftClone(v === 'a' ? c.a : c.b)); });
  const data = r.build();
  delete data.openBy;
  data.savedAt = new Date().toISOString();
  const text = JSON.stringify(data, null, 2) + '\n';
  oftEl('oftMergeDialog').close();
  if (s.mode === 'conflict') {
    const handle = fileHandle;
    try {
      const now = await (await handle.getFile()).text();
      if (now !== s.observed) { toast('The file changed again while you were merging. Save again to see the newest changes.', true); return; }
      await oftWrite(handle, text);
    } catch (err) { toast(`Couldn't save the merged file: ${err.message}`, true); return; }
    loadText(text, handle.name, handle);
    toast(`Merged your changes into ${handle.name}`);
    return;
  }
  const name = (s.a.name || 'project').replace(/\.oft\.json$|\.json$/i, '') + '-merged.oft.json';
  if (window.showSaveFilePicker && window.self === window.top) {
    try { const h = await window.showSaveFilePicker({ suggestedName: name, types: [{ description: 'Film project file', accept: { 'application/json': ['.json'] } }] }); await oftWrite(h, text); loadText(text, h.name, h); toast(`Saved the merged file as ${h.name}`); }
    catch (err) { if (err.name !== 'AbortError') toast(`Couldn't save the merged file: ${err.message}`, true); }
    return;
  }
  const url = URL.createObjectURL(new Blob([text], { type: 'application/json' }));
  const a = document.createElement('a'); a.href = url; a.download = name; document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  loadText(text, name, null);
  toast(`Downloaded the merged file as ${name}. Open it from now on.`);
}
async function oftMergeConflict() {
  const handle = fileHandle;
  if (!handle) return;
  oftEl('conflictDialog') && oftEl('conflictDialog').close();
  let observed, theirs, base;
  try { observed = await (await handle.getFile()).text(); theirs = JSON.parse(observed); } catch (err) { toast(`Couldn't read ${handle.name}: ${err.message}`, true); return; }
  try { base = baselineText ? JSON.parse(baselineText) : undefined; } catch { base = undefined; }
  oftStamp();
  const mine = JSON.parse(serialize());
  oftOpenMerge('conflict');
  Object.assign(oftMergeState, { base, observed, a: { name: 'Your changes', data: mine }, b: { name: handle.name, data: theirs } });
  oftCompare();
  if (!oftMergeState.result.conflicts.length) await oftSaveMerged();
}

// ---------- Conflicted copies from sync apps ----------
let oftFolder = null;
function oftIsCopy(name, of) {
  const stem = of.replace(/\.oft\.json$|\.json$/i, ''), m = name.match(/^(.*?)(\.oft)?\.json$/i);
  if (!m || name === of || !m[1].startsWith(stem)) return false;
  const rest = m[1].slice(stem.length);
  return /conflict/i.test(rest) || /^ ?\(\d+\)$/.test(rest) || /^ \d+$/.test(rest) || /^-[A-Z0-9][A-Z0-9-]*$/.test(rest);
}
async function oftScanFolder() {
  const bar = oftEl('oftCopies');
  if (!bar || !fileHandle || !fileName) return;
  const dir = oftFolder || await oftIdb('get', 'folder');
  if (!dir || !dir.values) return;
  try {
    if (dir.queryPermission && (await dir.queryPermission({ mode: 'read' })) !== 'granted') return;
    const inside = dir.resolve ? await dir.resolve(fileHandle) : [fileName];
    if (!inside || inside.length !== 1) return;
    const found = [];
    for await (const h of dir.values()) if (h.kind !== 'directory' && oftIsCopy(h.name, fileName)) found.push(h);
    bar.hidden = !found.length;
    if (!found.length) return;
    oftEl('oftCopiesText').textContent = `Your sync app made ${found.length === 1 ? 'a conflicted copy' : `${found.length} conflicted copies`} of this file: ${found.map(h => h.name).join(', ')}. Merge ${found.length === 1 ? 'it' : 'them one at a time'} so no one's changes are lost.`;
    oftEl('oftCopiesBtn').onclick = async () => { oftOpenMerge('copies'); const h = found[0]; await oftTakeCopy('b', h.name, await (await h.getFile()).text()); };
  } catch { /* folder unavailable */ }
}
async function oftPickFolder() {
  if (!window.showDirectoryPicker) return;
  try {
    const dir = await window.showDirectoryPicker({ id: 'oft-project', mode: 'read', startIn: fileHandle || undefined });
    if (fileHandle && dir.resolve) { const inside = await dir.resolve(fileHandle); if (!inside || inside.length !== 1) { toast(`${fileName} isn't in that folder. Choose the folder the project file is in.`, true); return; } }
    oftFolder = dir;
    await oftIdb('put', 'folder', dir);
    oftEl('oftFolderText').textContent = `Checking ${dir.name} for conflicted copies.`;
    await oftScanFolder();
    if (oftEl('oftCopies').hidden) toast(`No conflicted copies in ${dir.name}`);
  } catch (err) { if (err.name !== 'AbortError') toast(`Couldn't use that folder: ${err.message}`, true); }
}

// ---------- Opening the same file in the next tool ----------
function oftRecent() {
  let list = [];
  try { list = JSON.parse(oftStore.get('oft-recent-tools') || '[]'); } catch { /* reset */ }
  list = [{ slug: OFT_SLUG, at: new Date().toISOString() }].concat(list.filter(t => t && t.slug !== OFT_SLUG)).slice(0, 12);
  oftStore.set('oft-recent-tools', JSON.stringify(list));
}
async function oftOffer() {
  const bar = oftEl('oftReopen');
  if (!bar || !window.showOpenFilePicker || fileName || dirty) return;
  const saved = await oftIdb('get', 'file');
  if (!saved || !saved.handle || fileName || dirty) return;
  if (oftEl('recovery') && !oftEl('recovery').hidden) return;
  oftEl('oftReopenText').textContent = `Open ${saved.name} again? It's the project file you last used in this browser.`;
  bar.hidden = false;
  oftEl('oftReopenBtn').onclick = async () => {
    const h = saved.handle;
    try {
      if (h.requestPermission && (await h.requestPermission({ mode: 'readwrite' })) !== 'granted') { toast(`The browser didn't allow opening ${saved.name}. Use Open file instead.`, true); return; }
      const f = await h.getFile();
      loadText(await f.text(), f.name, h);
    } catch (err) { toast(`Couldn't open ${saved.name}: ${err.message}. It may have been moved or renamed. Use Open file instead.`, true); }
  };
  oftEl('oftForgetBtn').onclick = oftForget;
}
async function oftForget() {
  await oftIdb('del', 'file');
  await oftIdb('del', 'folder');
  oftFolder = null;
  if (oftEl('oftReopen')) oftEl('oftReopen').hidden = true;
  oftSettingsText();
  toast('This browser no longer remembers the project file.');
}
function oftShowRecord(id) {
  if (!id) return;
  const sel = ['data-edit', 'data-id', 'data-open'].map(a => `[${a}="${CSS.escape(id)}"]`).join(', ');
  const el = [...document.querySelectorAll(sel)].find(e => e.offsetParent !== null) || document.querySelector(sel);
  if (!el) return;
  el.scrollIntoView({ block: 'center' });
  el.classList.add('oft-flash');
  setTimeout(() => el.classList.remove('oft-flash'), 2500);
  if (el.dataset.edit === id && el.matches('button, a, [role="button"]')) el.click();
  else if (el.matches('button, a, input, select, textarea, [tabindex]')) el.focus();
}
const oftRecordFromHash = () => { const m = window.location.hash.match(/record=([^&]+)/); return m ? decodeURIComponent(m[1]) : ''; };
function oftOpened(text, name, handle) {
  oftRecent();
  if (oftEl('oftReopen')) oftEl('oftReopen').hidden = true;
  if (oftEl('oftCopies')) oftEl('oftCopies').hidden = true;
  if (handle) oftIdb('put', 'file', { handle, name, at: new Date().toISOString() });
  oftCarry();
  oftWarnOpen(text);
  if (handle) oftMarkOpen(text, handle).then(oftScanFolder);
  const rec = oftRecordFromHash();
  if (rec) setTimeout(() => oftShowRecord(rec), 60);
}
// ---------- The open project goes with you from page to page in this tab ----------
// Whatever project is open, with any changes not saved yet, is kept in this tab's session storage, so the
// next tool, or the home page, opens it without asking. A new tab starts with nothing open.
const OFT_CARRY = 'oft-current';
let oftMoving = 0, oftHadFile = false;
const oftCarried = () => { try { return JSON.parse(sessionStorage.getItem(OFT_CARRY) || 'null'); } catch { return null; } };
function oftCarry() {
  try {
    // A page that never had a project open leaves the tab's project alone; one that closed it, or started a new one, clears it.
    if (!fileName || !doc) { if (oftHadFile) sessionStorage.removeItem(OFT_CARRY); return false; }
    oftHadFile = true;
    const rec = { name: fileName, base: baselineText, at: Date.now() };
    if (dirty) { const now = serialize(); if (now !== baselineText) rec.text = now; }
    if (!rec.base && !rec.text) { sessionStorage.removeItem(OFT_CARRY); return false; }
    sessionStorage.setItem(OFT_CARRY, JSON.stringify(rec));
    return true;
  } catch {
    try { sessionStorage.removeItem(OFT_CARRY); } catch { /* storage off */ }
    return false;
  }
}
// Opens the carried project. `again` is for a page the browser brings back with Back or Forward,
// which may be showing an older state than the tab's.
async function oftArrive(again) {
  const c = oftCarried();
  if (!c || !c.name || (!c.base && !c.text)) return false;
  if (!again && (fileName || dirty)) return false;
  if (again) {
    const mine = dirty ? serialize() : baselineText;
    if (fileName === c.name && (c.text || c.base) === mine) return true;
  }
  const saved = window.showOpenFilePicker ? await oftIdb('get', 'file') : null;
  const handle = saved && saved.name === c.name ? saved.handle : null;
  let base = c.base;
  // Without changes waiting, read the file itself when the browser already allows it: it may be newer.
  if (handle && !c.text && handle.queryPermission) {
    try { if ((await handle.queryPermission({ mode: 'readwrite' })) === 'granted') base = await (await handle.getFile()).text(); } catch { /* use the copy */ }
  }
  if (!again && (fileName || dirty)) return false;
  dirty = false;
  if (!c.text) { loadText(base, c.name, handle); return fileName === c.name; }
  loadText(c.text, c.name, handle);
  if (fileName !== c.name) return false;
  baselineText = c.base || null; dirty = true;
  if (typeof saveDraft === 'function') saveDraft();
  if (typeof render === 'function') render();
  oftCarry();
  toast(`${c.name} has changes you haven't saved yet. Save here to keep them.`);
  return true;
}
// Following a link to another page of the toolkit takes the project along, so there's nothing to lose
// and no "leave this page?" question. Closing the tab, or going somewhere else, still asks.
function oftToolkitLink(a) {
  if (!a || a.target && a.target !== '_self' || a.hasAttribute('download')) return false;
  let u;
  try { u = new URL(a.getAttribute('href'), window.location.href); } catch { return false; }
  const root = new URL(document.querySelector('.home-link') ? '../../' : './', window.location.href);
  if (u.protocol !== root.protocol || u.host !== root.host || !u.pathname.startsWith(root.pathname)) return false;
  if (u.pathname === window.location.pathname) return false;
  return /(\/|\.html)$/.test(u.pathname);
}
document.addEventListener('click', ev => {
  if (ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
  const a = ev.target.closest && ev.target.closest('a[href]');
  if (oftToolkitLink(a) && oftCarry()) oftMoving = Date.now();
});
window.addEventListener('beforeunload', ev => { if (oftMoving && Date.now() - oftMoving < 5000) ev.stopImmediatePropagation(); }, true);
window.addEventListener('pageshow', ev => { if (ev.persisted) { oftMoving = 0; oftArrive(true); } });

// ---------- Settings dialog: your name, the remembered file, the folder ----------
async function oftSettingsText() {
  const saved = await oftIdb('get', 'file');
  if (oftEl('oftFileText')) oftEl('oftFileText').textContent = saved && saved.name ? `This browser remembers ${saved.name}, so the next tool you open can offer it.` : 'This browser doesn\'t remember a project file.';
  if (oftEl('oftForgetFile')) oftEl('oftForgetFile').hidden = !saved;
  const nameBtn = oftEl('oftNameBtn');
  if (nameBtn) nameBtn.textContent = oftMe() ? `You're ${oftMe()}` : 'Add your name';
}
// ---------- Earlier versions ----------
// Each time a tool saves the project, this browser keeps a copy, the last few for each file name, along with
// the file as it was before the first save. Any of them can be restored; nothing changes until you save.
const OFT_KEEP = 6;
const oftVersionKey = name => `versions:${name}`;
async function oftVersions(name) { const v = name ? await oftIdb('get', oftVersionKey(name)) : null; return Array.isArray(v) ? v : []; }
async function oftKeep(name, text, note) {
  if (!name || !text || text.length > 25e6) return;
  const list = await oftVersions(name);
  if (list.length && list[0].text === text) return;
  let by = '';
  try { const d = JSON.parse(text); by = d.savedBy || ''; } catch { return; }
  list.unshift({ at: new Date().toISOString(), who: oftMe(), tool: note || by, text });
  await oftIdb('put', oftVersionKey(name), list.slice(0, OFT_KEEP));
}
// What restoring would undo: the changes in the project now, compared with that version.
function oftVersionChanges(text) {
  let old;
  try { old = JSON.parse(text); } catch { return null; }
  return oftDiff(old, JSON.parse(serialize()));
}
// Records added, removed or changed between two copies of the project, by tool.
function oftDiff(a, b) {
  const out = [];
  const tool = path => OFT_KEYS[path[0]] || String(path[0] || 'Project');
  const walk = (x, y, path) => {
    if (oftSame(x, y)) return;
    if ((oftRecList(x) || oftRecList(y)) && [x, y].every(v => v === undefined || Array.isArray(v))) {
      const xa = new Map((x || []).filter(oftIsObj).map(r => [r.id, r])), ya = new Map((y || []).filter(oftIsObj).map(r => [r.id, r]));
      for (const [id, r] of ya) if (!xa.has(id)) out.push({ kind: 'added', tool: tool(path), label: oftLabel(r) });
      for (const [id, r] of xa) if (!ya.has(id)) out.push({ kind: 'removed', tool: tool(path), label: oftLabel(r) });
      for (const [id, r] of ya) if (xa.has(id) && !oftSame(xa.get(id), r)) out.push({ kind: 'changed', tool: tool(path), label: oftLabel(r) });
      return;
    }
    if (oftIsObj(x) && oftIsObj(y) && path.length < 2) {
      for (const k of new Set([...Object.keys(x), ...Object.keys(y)])) if (!OFT_META.has(k) && !(path.length === 0 && OFT_SKIP.has(k))) walk(x[k], y[k], path.concat(k));
      return;
    }
    out.push({ kind: x === undefined ? 'added' : y === undefined ? 'removed' : 'changed', tool: tool(path), label: path.length > 1 ? String(path[path.length - 1]) : '' });
  };
  walk(a, b, []);
  return out;
}
async function oftOpenVersions() {
  const dlg = oftEl('oftVersionsDialog'), list = await oftVersions(fileName);
  oftEl('oftVersionsIntro').textContent = !fileName ? 'Save the project to a file first. Each time you save it, this browser keeps a copy.'
    : list.length ? `The last ${list.length === 1 ? 'copy' : `${list.length} copies`} of ${fileName} this browser kept when it was saved, newest first. Restoring one puts it in the tool, and nothing changes in the file until you save.`
    : `This browser hasn't kept a copy of ${fileName} yet. It keeps one each time you save.`;
  const verb = { added: 'Added', changed: 'Changed', removed: 'Removed' };
  oftEl('oftVersionsList').innerHTML = list.map((v, i) => {
    const ch = oftVersionChanges(v.text) || [];
    const sum = !ch.length ? 'The same as the project now.' : `Restoring it undoes ${ch.length} change${ch.length === 1 ? '' : 's'}: ${ch.slice(0, 6).map(c => `${(verb[c.kind] || c.kind).toLowerCase()} ${c.label ? `${c.label} in ` : ''}${c.tool}`).join('; ')}${ch.length > 6 ? `, and ${ch.length - 6} more` : ''}.`;
    return `<li><span class="oft-v-when">${oftEsc(oftWhen(v.at))}${v.who ? `, by ${oftEsc(v.who)}` : ''}${v.tool ? `, saved from ${oftEsc(String(v.tool).replace(/ [\d.]+$/, '').replace(/-/g, ' '))}` : ''}</span>
      <span class="oft-v-sum">${oftEsc(sum)}</span>${ch.length ? `<button type="button" class="btn" data-restore="${i}">Restore this version</button>` : ''}</li>`;
  }).join('');
  dlg.showModal();
}
async function oftRestore(i) {
  const v = (await oftVersions(fileName))[i];
  if (!v) return;
  const keep = { baselineText, fileHandle, fileName };
  loadText(v.text, keep.fileName, keep.fileHandle);
  // The file on disk hasn't changed, so the next save is checked against it as usual.
  baselineText = keep.baselineText; fileHandle = keep.fileHandle; fileName = keep.fileName;
  dirty = true;
  if (typeof saveDraft === 'function') saveDraft();
  render();
  oftEl('oftVersionsDialog').close();
  toast(`Restored the version from ${oftWhen(v.at)}. Save to keep it, or open the file again to go back.`);
}
function oftChangedNote() {
  let rec = null;
  try { rec = editing; } catch { rec = null; } // eslint-disable-line no-undef
  return rec && typeof rec === 'object' ? oftChangedText(rec) : '';
}
function oftWatchDialogs() {
  const seen = new WeakSet();
  const show = dlg => {
    if (dlg.id.startsWith('oft') || dlg.id === 'conflictDialog') return;
    setTimeout(() => {
      const text = oftChangedNote();
      let p = dlg.querySelector('.oft-changed');
      if (!text) { if (p) p.remove(); return; }
      if (!p) { p = document.createElement('p'); p.className = 'oft-changed'; const h = dlg.querySelector('h2, h3'); if (h) h.after(p); else dlg.prepend(p); }
      p.textContent = text;
    }, 0);
  };
  const watch = () => document.querySelectorAll('dialog').forEach(d => { if (seen.has(d)) return; seen.add(d); new MutationObserver(() => { if (d.open) show(d); }).observe(d, { attributes: true, attributeFilter: ['open'] }); });
  watch();
}
// ---------- Film details: kind of film, logline and where you are ----------
// Every tool's Film details dialog gets these three, so they can be changed from any tool.
// The home page suggests what to do next from where you are.
const OFT_FILM = [['kind', 'p-oftKind'], ['logline', 'p-oftLogline'], ['stage', 'p-oftStage']];
function oftFilmExtras() {
  const form = document.getElementById('projectForm'), dlg = document.getElementById('projectDialog');
  if (!form || !dlg || document.getElementById('p-oftKind')) return;
  const body = form.querySelector('.dlg-body');
  const wrap = document.createElement('div');
  wrap.innerHTML = `<div class="field"><label for="p-oftKind">Kind of film</label><select id="p-oftKind"><option value="">Not set</option><option value="documentary">Documentary</option><option value="scripted">Scripted</option></select></div>
<div class="field"><label for="p-oftLogline">Logline</label><input id="p-oftLogline" type="text" placeholder="One line about the film" autocomplete="off"></div>
<div class="field"><label for="p-oftStage">Where you are</label><select id="p-oftStage"><option value="">Not set</option><option value="development">Developing and raising money</option><option value="production">Shooting</option><option value="post">Editing</option><option value="release">Releasing</option></select></div>`;
  const fields = [...wrap.children];
  if (body) body.append(...fields); else { const foot = form.querySelector('.dlg-foot, .actions, .acts') || form.lastElementChild; for (const f of fields) form.insertBefore(f, foot); }
  const fill = () => { const p = (doc && doc.project) || {}; for (const [k, id] of OFT_FILM) oftEl(id).value = p[k] == null ? '' : String(p[k]); };
  new MutationObserver(() => { if (dlg.open) fill(); }).observe(dlg, { attributes: true, attributeFilter: ['open'] });
  // Runs before the tool's own save, which then marks the change.
  form.addEventListener('submit', () => {
    if (!doc.project || typeof doc.project !== 'object') doc.project = {};
    for (const [k, id] of OFT_FILM) { const v = oftEl(id).value.trim(); if (v) doc.project[k] = v; else delete doc.project[k]; }
  }, true);
}

function oftBuild() {
  const style = document.createElement('style');
  style.textContent = `.oft-links { margin: 8px 0 0; display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 13px; }
.oft-links .link-btn, .oft-links a { padding: 0; border: 0; background: none; cursor: pointer; font: inherit; font-size: 13px; color: var(--ink-2); min-height: 24px; text-decoration: underline; text-underline-offset: 2px; }
.oft-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 16px; margin: 0 0 16px; padding: 12px 16px; border-radius: 8px; background: var(--warn-bg, #fbf0d9); border: 1px solid var(--rule); color: var(--ink); }
.oft-bar.quiet { background: var(--sheet); }
.oft-bar p { margin: 0; flex: 1 1 280px; }
.oft-bar .actions { display: flex; flex-wrap: wrap; gap: 8px; }
.oft-dialog { width: min(680px, calc(100vw - 32px)); max-height: calc(100vh - 48px); padding: 20px; border: 1px solid var(--rule); border-radius: 10px; background: var(--sheet); color: var(--ink); overflow: auto; }
.oft-dialog::backdrop { background: rgba(10, 14, 20, 0.45); }
.oft-dialog h2 { margin: 0 0 8px; font-size: 20px; }
.oft-dialog h3 { margin: 18px 0 6px; font-size: 16px; }
.oft-dialog h4 { margin: 10px 0 4px; font-size: 14px; }
.oft-dialog ul { margin: 0; padding-left: 20px; }
.oft-dialog p { margin: 0 0 10px; }
.oft-dialog label.oft-field { display: block; font-weight: 600; margin: 8px 0 4px; }
.oft-dialog input[type="text"] { width: 100%; box-sizing: border-box; padding: 8px 10px; border: 1px solid var(--rule); border-radius: 6px; background: var(--sheet); color: var(--ink); font: inherit; }
.oft-dialog .oft-actions { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; margin-top: 16px; }
.oft-dialog .oft-files { display: grid; gap: 8px; margin: 8px 0; }
.oft-dialog .oft-files div { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.oft-dialog .oft-files span { flex: 1 1 200px; color: var(--ink-2); overflow-wrap: anywhere; }
.oft-kinds { margin: 8px 0; padding: 8px 12px; border: 1px solid var(--rule); border-radius: 8px; }
.oft-kinds label { display: flex; gap: 8px; align-items: flex-start; padding: 3px 0; }
.oft-kinds small { color: var(--ink-3); }
.oft-map { overflow-x: auto; }
.oft-map table { width: 100%; border-collapse: collapse; font-size: 14px; }
.oft-map th, .oft-map td { text-align: left; padding: 4px 6px; border-bottom: 1px solid var(--rule); vertical-align: middle; }
.oft-map select { max-width: 100%; padding: 4px 6px; font: inherit; color: var(--ink); background: var(--sheet); border: 1px solid var(--rule); border-radius: 6px; }
.oft-unmatched { color: var(--bad); font-weight: 600; }
.oft-rate { display: grid; grid-template-columns: 70px minmax(0, 1fr) minmax(0, 1fr) auto; gap: 6px; align-items: center; margin: 0 0 6px; }
.oft-rate input { min-width: 0; padding: 6px 8px; border: 1px solid var(--rule); border-radius: 6px; background: var(--sheet); color: var(--ink); font: inherit; }
.oft-rates-note { margin: 0 0 12px; font-size: 13px; color: var(--ink-2); }
.oft-review { list-style: none; margin: 0 0 8px; padding: 0; }
.oft-review li { padding: 5px 0; border-bottom: 1px solid var(--rule-soft, var(--rule)); }
.oft-review label { display: flex; gap: 8px; align-items: flex-start; }
.oft-review small { color: var(--ink-3); }
.oft-review select { margin: 4px 0 0 26px; max-width: calc(100% - 26px); padding: 4px 6px; font: inherit; color: var(--ink); background: var(--sheet); border: 1px solid var(--rule); border-radius: 6px; }
.oft-conflict { margin: 8px 0; padding: 8px 12px; border: 1px solid var(--rule); border-radius: 8px; }
.oft-conflict legend { font-weight: 600; padding: 0 4px; }
.oft-conflict label { display: flex; gap: 8px; align-items: flex-start; padding: 4px 0; overflow-wrap: anywhere; }
.oft-conflict input { margin-top: 4px; }
.oft-conflict small, .oft-changed { color: var(--ink-3); font-size: 13px; }
.oft-changed { margin: -4px 0 10px; }
.oft-versions { margin: 0 0 12px; padding: 0 0 0 20px; display: grid; gap: 10px; }
.oft-versions li { display: grid; gap: 4px; justify-items: start; font-size: 14px; }
.oft-v-when { font-weight: 600; }
.oft-v-sum { color: var(--ink-2); }
.oft-flash { outline: 3px solid var(--focus) !important; outline-offset: 2px; }
@media print { .oft-bar, .oft-links { display: none !important; } }`;
  document.head.append(style);
  const bars = document.createElement('div');
  bars.innerHTML = `<div class="oft-bar quiet" id="oftBrowser" role="region" aria-label="About saving in this browser" hidden><p id="oftBrowserText"></p><div class="actions"><button type="button" class="btn" id="oftBrowserBtn">Got it</button></div></div>
<div class="oft-bar quiet" id="oftReopen" role="region" aria-label="Open the last project file" hidden><p id="oftReopenText"></p><div class="actions"><button type="button" class="btn primary" id="oftReopenBtn">Open it</button><button type="button" class="btn" id="oftForgetBtn">Forget it</button></div></div>
<div class="oft-bar" id="oftPresence" role="status" hidden><p id="oftPresenceText"></p><div class="actions"><button type="button" class="btn" id="oftPresenceBtn">Dismiss</button></div></div>
<div class="oft-bar" id="oftCopies" role="region" aria-label="Conflicted copies" hidden><p id="oftCopiesText"></p><div class="actions"><button type="button" class="btn primary" id="oftCopiesBtn">Merge it</button><button type="button" class="btn" id="oftCopiesHide">Not now</button></div></div>`;
  const main = document.querySelector('main#main') || document.querySelector('main');
  const recovery = oftEl('recovery');
  if (recovery && recovery.parentElement) recovery.before(...bars.children);
  else if (main) main.prepend(...bars.children);
  const links = document.createElement('p');
  links.className = 'oft-links';
  links.innerHTML = `<button type="button" class="link-btn" id="oftNameBtn">Add your name</button><button type="button" class="link-btn" id="oftMergeBtn">Merge two copies</button><button type="button" class="link-btn" id="oftVersionsBtn">Earlier versions</button><a href="${OFT_GUIDE}">Working on a shared file</a>`;
  if (typeof oftImport !== 'undefined' && typeof OFT_IMPORT !== 'undefined') {
    const imp = document.createElement('button');
    imp.type = 'button'; imp.className = 'link-btn'; imp.id = 'oftImportBtn'; imp.textContent = 'Import from a spreadsheet';
    imp.onclick = () => oftImport.open(OFT_IMPORT);
    links.prepend(imp);
  }
  if (typeof oftVcard !== 'undefined' && typeof OFT_VCARD !== 'undefined') {
    const vc = document.createElement('button');
    vc.type = 'button'; vc.className = 'link-btn'; vc.id = 'oftVcardBtn'; vc.textContent = 'Import from an address book';
    vc.onclick = () => oftVcard.open();
    links.prepend(vc);
  }
  if (typeof oftCosts !== 'undefined' && typeof OFT_COSTS !== 'undefined') {
    const cb = document.createElement('button');
    cb.type = 'button'; cb.className = 'link-btn'; cb.id = 'oftCostsBtn'; cb.textContent = 'Send costs to the budget';
    cb.onclick = () => oftCosts.open();
    links.prepend(cb);
  }
  if (typeof oftMoney !== 'undefined') {
    const fx = document.createElement('button');
    fx.type = 'button'; fx.className = 'link-btn'; fx.id = 'oftRatesBtn'; fx.textContent = 'Exchange rates';
    fx.onclick = () => oftMoney.dialog();
    links.prepend(fx);
  }
  if (typeof oftProject !== 'undefined') {
    const cal = document.createElement('button');
    cal.type = 'button'; cal.className = 'link-btn'; cal.id = 'oftCalBtn'; cal.textContent = 'Calendar of every date';
    cal.onclick = () => oftProject.calendarDialog(() => JSON.parse(serialize()));
    links.prepend(cal);
  }
  const state = oftEl('fileState');
  if (state && state.parentElement) state.parentElement.append(links);
  const dlgs = document.createElement('div');
  dlgs.innerHTML = `<dialog class="oft-dialog" id="oftSettings" aria-labelledby="oftSettingsTitle"><form method="dialog" id="oftSettingsForm">
  <h2 id="oftSettingsTitle">You and this browser</h2>
  <label class="oft-field" for="oftNameInput">Your name</label>
  <input type="text" id="oftNameInput" autocomplete="name" maxlength="60">
  <p class="oft-changed">Kept in this browser only. The tools note it on the records you change, and warn others who open the file while you have it open.</p>
  <h3>Remembered file</h3><p id="oftFileText"></p><p><button type="button" class="btn" id="oftForgetFile">Forget it</button></p>
  <div id="oftFolderBox"><h3>Conflicted copies</h3><p id="oftFolderText">Let the tools look in the project file's folder for conflicted copies made by your sync app.</p><p><button type="button" class="btn" id="oftFolderBtn">Choose the folder</button></p></div>
  <div class="oft-actions"><button type="button" class="btn" id="oftSettingsCancel">Cancel</button><button type="submit" class="btn primary">Save</button></div></form></dialog>
<dialog class="oft-dialog" id="oftVersionsDialog" aria-labelledby="oftVersionsTitle"><h2 id="oftVersionsTitle">Earlier versions</h2><p id="oftVersionsIntro"></p>
  <ol class="oft-versions" id="oftVersionsList"></ol>
  <p class="oft-changed">Copies are kept in this browser only, so also keep the file itself backed up. See <a href="https://github.com/open-filmmaker-toolkit/toolkit/blob/main/docs/backups.md">keeping your project safe</a>.</p>
  <div class="oft-actions"><button type="button" class="btn" id="oftVersionsClose">Close</button></div></dialog>
<dialog class="oft-dialog" id="oftMergeDialog" aria-labelledby="oftMergeTitle"><h2 id="oftMergeTitle">Merge two copies</h2><p id="oftMergeIntro"></p>
  <div class="oft-files" id="oftMergePick"><div><span id="oftMergeA">Not chosen</span><button type="button" class="btn" id="oftMergeABtn">Choose the first copy</button></div><div><span id="oftMergeB">Not chosen</span><button type="button" class="btn" id="oftMergeBBtn">Choose the second copy</button></div></div>
  <input type="file" id="oftMergeFile" accept=".json,application/json" hidden>
  <div id="oftMergeResult" aria-live="polite"></div>
  <div class="oft-actions"><button type="button" class="btn" id="oftMergeCancel">Cancel</button><button type="button" class="btn primary" id="oftMergeSave" disabled>Save the merged file</button></div></dialog>`;
  document.body.append(...dlgs.children);
  oftEl('oftFolderBox').hidden = !window.showDirectoryPicker;
  oftEl('oftNameBtn').onclick = () => { oftEl('oftNameInput').value = oftMe(); oftSettingsText(); oftEl('oftSettings').showModal(); oftEl('oftNameInput').focus(); };
  oftEl('oftSettingsCancel').onclick = () => oftEl('oftSettings').close();
  oftEl('oftSettingsForm').addEventListener('submit', () => { oftStore.set('oft-user-name', oftEl('oftNameInput').value.trim() || null); oftSettingsText(); if (fileHandle && baselineText && !dirty) oftMarkOpen(baselineText, fileHandle); });
  oftEl('oftForgetFile').onclick = oftForget;
  oftEl('oftFolderBtn').onclick = oftPickFolder;
  oftEl('oftMergeBtn').onclick = () => oftOpenMerge('copies');
  oftEl('oftVersionsBtn').onclick = oftOpenVersions;
  oftEl('oftVersionsClose').onclick = () => oftEl('oftVersionsDialog').close();
  oftEl('oftVersionsList').addEventListener('click', ev => { const b = ev.target.closest('[data-restore]'); if (b) oftRestore(Number(b.dataset.restore)); });
  oftEl('oftMergeABtn').onclick = () => oftReadCopy('a');
  oftEl('oftMergeBBtn').onclick = () => oftReadCopy('b');
  oftEl('oftMergeFile').addEventListener('change', async ev => { const f = ev.target.files[0]; if (f) await oftTakeCopy(ev.target.dataset.side || 'b', f.name, await f.text()); });
  oftEl('oftMergeCancel').onclick = () => oftEl('oftMergeDialog').close();
  oftEl('oftMergeSave').onclick = oftSaveMerged;
  oftEl('oftPresenceBtn').onclick = () => { oftEl('oftPresence').hidden = true; };
  oftEl('oftCopiesHide').onclick = () => { oftEl('oftCopies').hidden = true; };
  const cancel = oftEl('conflictCancelBtn');
  if (cancel) { const b = document.createElement('button'); b.type = 'button'; b.className = 'btn primary'; b.id = 'conflictMergeBtn'; b.textContent = 'Merge both'; b.onclick = oftMergeConflict; cancel.parentElement.prepend(b); }
  oftFilmExtras();
  if (!window.showSaveFilePicker && !oftStore.get(OFT_NOTE_DONE)) {
    oftEl('oftBrowserText').innerHTML = oftBrowserNote();
    oftEl('oftBrowser').hidden = false;
    oftEl('oftBrowserBtn').onclick = () => { oftStore.set(OFT_NOTE_DONE, '1'); oftEl('oftBrowser').hidden = true; };
  }
  oftWatchDialogs();
  oftSettingsText();
}
const oftLoadText = loadText;
loadText = function (text, name, handle) {
  const out = oftLoadText.apply(this, arguments);
  if (fileName === name && baselineText === text) oftOpened(text, name, handle || null);
  return out;
};
const oftSaveFile = saveFile;
saveFile = async function () {
  if (fileHandle) {
    if (!(await oftWritable(fileHandle))) { toast(`The browser didn't allow saving to ${fileHandle.name}. Try again and allow it, or open the file again.`, true); return; }
    try {
      const current = await (await fileHandle.getFile()).text();
      if (baselineText != null && current !== baselineText) {
        const a = JSON.parse(current), b = JSON.parse(baselineText);
        const others = oftOpenList(a).filter(p => p.name !== oftMe());
        delete a.openBy; delete b.openBy;
        if (JSON.stringify(a) === JSON.stringify(b)) { baselineText = current; if (others.length) doc.openBy = others; else delete doc.openBy; }
      }
    } catch { /* the tool's own check reports it */ }
  }
  if (doc && Array.isArray(doc.openBy)) { const others = doc.openBy.filter(p => oftFresh(p) && p.name !== oftMe()); if (others.length) doc.openBy = others; else delete doc.openBy; }
  oftStamp();
  const before = baselineText, name = fileName;
  const out = await oftSaveFile.apply(this, arguments);
  // Keep the file as it was before this save, then the saved file, when the save went through.
  if (!dirty && fileName) {
    if (before && name === fileName && !(await oftVersions(fileName)).length) await oftKeep(fileName, before, '');
    await oftKeep(fileName, fileHandle && baselineText ? baselineText : serialize(), typeof TOOL !== 'undefined' ? TOOL : '');
    oftCarry();
  }
  return out;
};
window.addEventListener('pagehide', () => { oftCarry(); oftClearOpen(); });
setTimeout(async () => { oftBuild(); oftRecent(); if (!(await oftArrive(false))) oftOffer(); }, 0);

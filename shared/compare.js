// Saved versions of a tool's record, and two of them side by side. A tool calls
// oftSideBySide.versions(box, spec) to draw a "Versions" list with a name box and Save, where
// spec = { noun, list: () => [...], save: label => void, rows: data => [[part, text]], now: () => data,
//          restore: version => void, remove: version => void, label: version => '' }.
// oftSideBySide.open({ title, options: [{ id, label, data }], a, b, rows }) shows any two side by side, with
// the words that differ marked.
const oftSideBySide = (() => {
  const str = v => (v == null ? '' : String(v));
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  // Words removed from a and added in b, marked with <del> and <ins>.
  function diff(a, b) {
    const A = str(a).split(/(\s+)/), B = str(b).split(/(\s+)/);
    if (A.length * B.length > 4e6) return [e(a), e(b)];
    const n = A.length, m = B.length, L = Array.from({ length: n + 1 }, () => new Uint32Array(m + 1));
    for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) L[i][j] = A[i] === B[j] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
    let i = 0, j = 0, x = '', y = '';
    while (i < n || j < m) {
      if (i < n && j < m && A[i] === B[j]) { x += e(A[i]); y += e(B[j]); i++; j++; }
      else if (j < m && (i >= n || L[i][j + 1] >= L[i + 1][j])) { y += /^\s+$/.test(B[j]) ? e(B[j]) : `<ins>${e(B[j])}</ins>`; j++; }
      else { x += /^\s+$/.test(A[i]) ? e(A[i]) : `<del>${e(A[i])}</del>`; i++; }
    }
    return [x, y];
  }
  function style() {
    if (document.getElementById('oftCompareCss')) return;
    const css = document.createElement('style');
    css.id = 'oftCompareCss';
    css.textContent = `.oft-cmp { width: min(1000px, calc(100vw - 32px)); }
.oft-cmp-pick { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 0 0 10px; }
.oft-cmp-pick label { display: grid; gap: 4px; font-weight: 600; font-size: 14px; }
.oft-cmp-pick select { padding: 6px 8px; border: 1px solid var(--rule); border-radius: 6px; background: var(--paper); color: var(--ink); font: inherit; font-weight: 400; }
.oft-cmp-sum { margin: 0 0 8px; font-size: 14px; }
.oft-cmp-rows { display: grid; gap: 10px; margin: 0 0 12px; max-height: 60vh; overflow-y: auto; }
.oft-cmp-row h3 { margin: 0 0 4px; font-size: 14px; }
.oft-cmp-row h3 span { margin-left: 6px; font-weight: 400; color: var(--ink-2); }
.oft-cmp-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.oft-cmp-cols div { padding: 6px 8px; border: 1px solid var(--rule); border-radius: 6px; white-space: pre-wrap; overflow-wrap: anywhere; font-size: 14px; }
.oft-cmp-row.same .oft-cmp-cols div { color: var(--ink-2); }
.oft-cmp del { background: #f8d7d3; color: #6b1a12; text-decoration: line-through; }
.oft-cmp ins { background: #d6efdf; color: #12462a; text-decoration: none; }
@media (prefers-color-scheme: dark) { .oft-cmp del { background: #4a221d; color: #ffd7d1; } .oft-cmp ins { background: #183a28; color: #cdf3dc; } }
.oft-versions-list { list-style: none; margin: 4px 0 8px; padding: 0; }
.oft-versions-list li { display: flex; flex-wrap: wrap; gap: 4px 8px; align-items: center; padding: 6px 0; font-size: 14px; }
.oft-versions-list li + li { border-top: 1px solid var(--rule); }
.oft-versions-list .nm { flex: 1 1 140px; min-width: 0; overflow-wrap: anywhere; }
.oft-versions-list .when { display: block; font-size: 12.5px; color: var(--ink-2); }
.oft-versions-add { display: flex; gap: 6px; }
.oft-versions-add input { flex: 1; min-width: 0; padding: 6px 8px; border: 1px solid var(--rule); border-radius: 6px; background: var(--paper); color: var(--ink); font: inherit; }
@media (max-width: 640px) { .oft-cmp-cols, .oft-cmp-pick { grid-template-columns: 1fr; } }`;
    document.head.append(css);
  }
  let spec = null;
  function dialog() {
    let dlg = document.getElementById('oftCmpDialog');
    if (dlg) return dlg;
    dlg = document.createElement('dialog');
    dlg.className = 'oft-dialog oft-cmp'; dlg.id = 'oftCmpDialog'; dlg.setAttribute('aria-labelledby', 'oftCmpTitle');
    dlg.innerHTML = `<h2 id="oftCmpTitle"></h2><div class="oft-cmp-pick"><label>On the left<select id="oftCmpA"></select></label><label>On the right<select id="oftCmpB"></select></label></div>
      <p class="oft-cmp-sum" id="oftCmpSum" role="status"></p><div class="oft-cmp-rows" id="oftCmpRows"></div>
      <div class="oft-actions"><button type="button" class="btn" id="oftCmpClose">Close</button></div>`;
    document.body.append(dlg);
    dlg.querySelector('#oftCmpClose').onclick = () => dlg.close();
    dlg.querySelector('#oftCmpA').onchange = draw;
    dlg.querySelector('#oftCmpB').onchange = draw;
    return dlg;
  }
  function draw() {
    const dlg = dialog(), get = id => spec.options.find(o => o.id === id) || spec.options[0];
    const a = get(dlg.querySelector('#oftCmpA').value), b = get(dlg.querySelector('#oftCmpB').value);
    const ra = spec.rows(a.data), rb = spec.rows(b.data);
    const parts = [...new Set([...ra.map(r => r[0]), ...rb.map(r => r[0])])];
    const val = (rows, p) => str((rows.find(r => r[0] === p) || [])[1]);
    let differ = 0;
    dlg.querySelector('#oftCmpRows').innerHTML = parts.map(p => {
      const x = val(ra, p), y = val(rb, p), same = x === y;
      if (!same) differ++;
      const [hx, hy] = same ? [e(x), e(y)] : diff(x, y);
      return `<section class="oft-cmp-row${same ? ' same' : ''}"><h3>${e(p)}<span>${same ? 'The same' : 'Differs'}</span></h3><div class="oft-cmp-cols"><div>${hx || '<i>Empty</i>'}</div><div>${hy || '<i>Empty</i>'}</div></div></section>`;
    }).join('') || '<p>Nothing to compare yet.</p>';
    dlg.querySelector('#oftCmpSum').textContent = `${differ} of ${parts.length} part${parts.length === 1 ? '' : 's'} differ${differ === 1 ? 's' : ''}. Words only on the left are struck through; words only on the right are highlighted.`;
  }
  function open(s) {
    style();
    spec = s;
    const dlg = dialog(), opts = s.options.map(o => `<option value="${e(o.id)}">${e(o.label)}</option>`).join('');
    dlg.querySelector('#oftCmpTitle').textContent = s.title;
    dlg.querySelector('#oftCmpA').innerHTML = opts; dlg.querySelector('#oftCmpB').innerHTML = opts;
    dlg.querySelector('#oftCmpA').value = s.a || s.options[0].id;
    dlg.querySelector('#oftCmpB').value = s.b || s.options[s.options.length - 1].id;
    draw();
    dlg.showModal();
  }
  const when = iso => { const d = new Date(iso); return isNaN(d) ? '' : d.toLocaleDateString(undefined, { dateStyle: 'medium' }); };
  // The Versions list a tool shows in a side card.
  function versions(box, s) {
    style();
    const list = s.list();
    const label = v => (s.label ? s.label(v) : str(v.label) || 'Untitled version');
    const html = `${list.length ? `<ul class="oft-versions-list">${list.map((v, i) => `<li><span class="nm">${e(label(v))}<span class="when">${e(when(v.at))}</span></span>
        <button type="button" class="btn small" data-v-cmp="${i}">Compare</button><button type="button" class="btn small" data-v-restore="${i}">Restore</button><button type="button" class="btn small" data-v-del="${i}" aria-label="Remove ${e(label(v))}">Remove</button></li>`).join('')}</ul>` : `<p class="hint">No versions saved yet.</p>`}
      <div class="oft-versions-add"><input type="text" aria-label="Name for this version" placeholder="${e(s.placeholder || 'Before the spring changes')}" autocomplete="off"><button type="button" class="btn small" data-v-save>Save this version</button></div>`;
    // Only redrawn when the list changes, so a click isn't lost when the page redraws as a field loses focus.
    if (box.dataset.html !== html) { box.innerHTML = html; box.dataset.html = html; }
    box.onclick = ev => {
      const t = ev.target.closest('button');
      if (!t) return;
      const v = list[Number(t.dataset.vCmp ?? t.dataset.vRestore ?? t.dataset.vDel)];
      if (t.hasAttribute('data-v-save')) { const inp = box.querySelector('input'); s.save(inp.value.trim() || `Version ${list.length + 1}`); return; }
      if (t.dataset.vCmp != null) open({ title: `Compare versions of the ${s.noun}`, rows: s.rows, options: [...list.map((x, i) => ({ id: `v${i}`, label: `${label(x)}, ${when(x.at)}`, data: x })), { id: 'now', label: 'Now', data: s.now() }], a: `v${t.dataset.vCmp}`, b: 'now' });
      else if (t.dataset.vRestore != null) s.restore(v);
      else if (t.dataset.vDel != null) s.remove(v);
    };
  }
  return { open, versions, diff };
})();

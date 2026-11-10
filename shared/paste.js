// Paste a list: one person or place per line, from a treatment, a spreadsheet column or an email. Anything after
// a comma, a tab or a dash is the second column (a role, or an address). You see every row before it's added,
// and anything already in the project is unticked, so nothing is added twice. Plain text matching, no AI.
const oftPaste = (() => {
  const clean = s => String(s == null ? '' : s).trim();
  const key = s => clean(s).toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  // "Maria Chen, subject" / "- Maria Chen — subject" / "1. Maria Chen<TAB>subject" all give { name, extra }.
  function parse(text) {
    const seen = new Set();
    return String(text || '').split(/\r?\n/).map(line => line.replace(/^\s*(?:[-*•·▪]|\d+[.)])\s+/, '').trim()).filter(Boolean).map(line => {
      const m = line.match(/^(.*?)(?:\t|,| [–—-] )(.*)$/);
      const name = clean(m ? m[1] : line).replace(/^["']|["']$/g, ''), extra = clean(m ? m[2] : '').replace(/^["']|["']$/g, '');
      const k = key(name);
      const again = seen.has(k);
      seen.add(k);
      return { name, extra, again };
    }).filter(r => r.name);
  }
  // Rows marked against what's already there: { name, extra, have, again }.
  function plan(text, existing) {
    const have = new Set((existing || []).map(key));
    return parse(text).map(r => ({ ...r, have: have.has(key(r.name)) }));
  }
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  // A dialog for a tool: o = { title, intro, placeholder, extraLabel, noun, nouns, existing: () => [names], add: rows => count }.
  let dlg = null, opts = null, rows = [];
  function build() {
    const css = document.createElement('style');
    css.textContent = `.oft-paste textarea { width: 100%; box-sizing: border-box; min-height: 140px; padding: 8px 10px; border: 1px solid var(--rule); border-radius: 6px; background: var(--sheet); color: var(--ink); font: 14px/1.5 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
.oft-paste .oft-paste-rows { list-style: none; margin: 8px 0 0; padding: 0; max-height: 40vh; overflow: auto; }
.oft-paste .oft-paste-rows li { padding: 5px 0; border-bottom: 1px solid var(--rule-soft, var(--rule)); }
.oft-paste .oft-paste-rows label { display: flex; gap: 8px; align-items: flex-start; overflow-wrap: anywhere; }
.oft-paste .oft-paste-rows small { color: var(--ink-3); }
.oft-paste .oft-paste-count { margin: 8px 0 0; color: var(--ink-2); }`;
    document.head.append(css);
    dlg = document.createElement('dialog');
    dlg.className = 'oft-dialog oft-paste';
    dlg.id = 'oftPaste';
    dlg.setAttribute('aria-labelledby', 'oftPasteTitle');
    dlg.innerHTML = `<form method="dialog" id="oftPasteForm"><h2 id="oftPasteTitle"></h2><p id="oftPasteIntro"></p>
      <label class="oft-field" for="oftPasteText">Paste your list</label><textarea id="oftPasteText" spellcheck="false"></textarea>
      <p class="oft-paste-count" id="oftPasteCount" aria-live="polite"></p><ul class="oft-paste-rows" id="oftPasteRows"></ul>
      <div class="oft-actions"><button type="button" class="btn" id="oftPasteCancel">Cancel</button><button type="submit" class="btn primary" id="oftPasteAdd">Add</button></div></form>`;
    document.body.append(dlg);
    const text = dlg.querySelector('#oftPasteText');
    text.addEventListener('input', draw);
    dlg.querySelector('#oftPasteRows').addEventListener('change', count);
    dlg.querySelector('#oftPasteCancel').onclick = () => dlg.close();
    dlg.querySelector('#oftPasteForm').addEventListener('submit', ev => {
      ev.preventDefault();
      const keep = [...dlg.querySelectorAll('#oftPasteRows input:checked')].map(i => rows[+i.value]);
      if (!keep.length) { text.focus(); return; }
      const n = opts.add(keep.map(r => ({ name: r.name, extra: r.extra })));
      dlg.close();
      if (typeof toast === 'function') toast(`Added ${n} ${n === 1 ? opts.noun : opts.nouns}.`);
    });
  }
  function draw() {
    rows = plan(dlg.querySelector('#oftPasteText').value, opts.existing());
    dlg.querySelector('#oftPasteRows').innerHTML = rows.map((r, i) => `<li><label><input type="checkbox" value="${i}"${r.have || r.again ? '' : ' checked'}><span><b>${esc(r.name)}</b>${r.extra ? `, ${esc(r.extra)}` : ''}${r.have ? ` <small>Already in the project</small>` : r.again ? ' <small>Listed twice</small>' : ''}</span></label></li>`).join('');
    count();
  }
  function count() {
    const n = dlg.querySelectorAll('#oftPasteRows input:checked').length;
    dlg.querySelector('#oftPasteCount').textContent = rows.length ? `You'll add ${n} ${n === 1 ? opts.noun : opts.nouns}.` : '';
    const b = dlg.querySelector('#oftPasteAdd');
    b.textContent = n ? `Add ${n} ${n === 1 ? opts.noun : opts.nouns}` : 'Add';
    b.disabled = !n;
  }
  function open(o) {
    opts = o;
    if (!dlg) build();
    dlg.querySelector('#oftPasteTitle').textContent = o.title;
    dlg.querySelector('#oftPasteIntro').textContent = o.intro;
    const text = dlg.querySelector('#oftPasteText');
    text.value = '';
    text.placeholder = o.placeholder || '';
    draw();
    dlg.showModal();
    text.focus();
  }
  return { parse, plan, open, key };
})();

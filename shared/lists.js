// Lists to share between projects: funders and their usual deadlines, festivals, and the like.
// A list is a small JSON file, { format: "oft-list", formatVersion: 1, kind, title, savedAt, items },
// that a team keeps in a shared folder or passes around; nothing is fetched from anywhere.
// A tool describes its list in OFT_LIST = { kind, title, noun, nouns, items: () => [...],
// label: item => '', detail: item => '', has: item => bool, add: items => number }
// and calls oftLists.save() and oftLists.open() from its own buttons.
const oftLists = (() => {
  const str = v => (v == null ? '' : String(v));
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const L = () => OFT_LIST;
  const plural = (n, a, b) => `${n} ${n === 1 ? a : b}`;
  function save() {
    const items = L().items();
    if (!items.length) { toast(`There are no ${L().nouns} to put in a list yet.`); return; }
    const out = { format: 'oft-list', formatVersion: 1, kind: L().kind, title: `${L().title}${doc.project && doc.project.title ? `, from ${doc.project.title}` : ''}`, savedAt: new Date().toISOString(), items };
    const name = `${slug()}-${L().kind}-list.json`;
    download(JSON.stringify(out, null, 2) + '\n', name, 'application/json');
    toast(`Saved ${plural(items.length, L().noun, L().nouns)} to ${name}. Open it from another project to add them there.`);
  }
  function dialog() {
    let dlg = document.getElementById('oftListDialog');
    if (dlg) return dlg;
    dlg = document.createElement('dialog');
    dlg.className = 'oft-dialog'; dlg.id = 'oftListDialog'; dlg.setAttribute('aria-labelledby', 'oftListTitle');
    dlg.innerHTML = `<h2 id="oftListTitle"></h2><p id="oftListIntro"></p>
  <p><button type="button" class="btn small" id="oftListAll">Tick all</button> <button type="button" class="btn small" id="oftListNone">Untick all</button></p>
  <fieldset class="oft-list-items" id="oftListItems"><legend class="oft-vh">Pick what to add</legend></fieldset>
  <div class="oft-actions"><button type="button" class="btn" id="oftListCancel">Cancel</button><button type="button" class="btn primary" id="oftListAdd">Add</button></div>`;
    document.body.append(dlg);
    const css = document.createElement('style');
    css.textContent = '.oft-list-items { border: 0; margin: 0 0 12px; padding: 0; min-width: 0; display: grid; gap: 6px; max-height: 50vh; overflow-y: auto; }\n.oft-list-items label { display: flex; gap: 8px; align-items: flex-start; font-size: 14px; }\n.oft-list-items input { margin-top: 3px; }\n.oft-list-items small { display: block; color: var(--ink-2); }\n.oft-vh { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }';
    document.head.append(css);
    dlg.querySelector('#oftListCancel').onclick = () => dlg.close();
    dlg.querySelector('#oftListAll').onclick = () => dlg.querySelectorAll('#oftListItems input:not(:disabled)').forEach(i => { i.checked = true; });
    dlg.querySelector('#oftListNone').onclick = () => dlg.querySelectorAll('#oftListItems input').forEach(i => { i.checked = false; });
    return dlg;
  }
  function show(list, fileName) {
    const items = (Array.isArray(list.items) ? list.items : []).filter(x => x && typeof x === 'object');
    const dlg = dialog(), $ = q => dlg.querySelector(q);
    $('#oftListTitle').textContent = `Add from ${list.title || fileName}`;
    const fresh = items.filter(i => !L().has(i)).length;
    $('#oftListIntro').textContent = `${plural(items.length, L().noun, L().nouns)} in the list${items.length - fresh ? `, ${items.length - fresh} already in this project` : ''}. Pick the ones to add. Check their dates and details: a shared list is only as current as whoever saved it.`;
    $('#oftListItems').innerHTML = '<legend class="oft-vh">Pick what to add</legend>' + items.map((it, k) => {
      const have = L().has(it);
      return `<label><input type="checkbox" value="${k}"${have ? ' disabled' : ' checked'}><span>${e(L().label(it))}<small>${e(have ? 'Already in this project' : L().detail(it))}</small></span></label>`;
    }).join('');
    $('#oftListAdd').onclick = () => {
      const picked = [...dlg.querySelectorAll('#oftListItems input:checked')].map(i => items[+i.value]);
      if (!picked.length) { dlg.close(); return; }
      const n = L().add(picked);
      dlg.close();
      changed();
      toast(`Added ${plural(n, L().noun, L().nouns)} from the list.`);
    };
    dlg.showModal();
  }
  function open() {
    const input = document.createElement('input');
    input.type = 'file'; input.accept = '.json,application/json'; input.hidden = true;
    document.body.append(input);
    input.onchange = async () => {
      const f = input.files[0];
      input.remove();
      if (!f) return;
      let list;
      try { list = JSON.parse(await f.text()); } catch { toast(`${f.name} isn't a list file this tool can read.`); return; }
      if (!list || list.format !== 'oft-list') { toast(`${f.name} isn't a shared list. Save one with "Save a list" in this tool.`); return; }
      if (list.kind !== L().kind) { toast(`${f.name} is a list of ${str(list.kind) || 'something else'}, not ${L().nouns}.`); return; }
      show(list, f.name);
    };
    input.click();
  }
  return { save, open, show };
})();

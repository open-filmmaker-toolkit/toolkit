// Adding a distributor's delivery schedule: paste the list from their schedule, one item a line,
// and each becomes an item of your own, marked with the distributor's name. A tool defines
// OFT_SCHEDULE = { noun, sections: [[id, label]], guess: line => sectionId, has: (title, distributor) => bool,
// add: (distributor, [{ title, section }]) => number } and calls oftSchedule.open() from its own button.
const oftSchedule = (() => {
  const str = v => (v == null ? '' : String(v));
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const S = () => OFT_SCHEDULE;
  // Lines from a pasted schedule: numbering, bullets and tick boxes taken off, headings and blanks left out.
  function lines(text) {
    return str(text).split(/\r?\n/).map(l => l.replace(/^\s*(?:[-*•▪◦☐□✓✔]|\(?[0-9a-zA-Z]{1,3}[.)]|\[\s?[xX]?\s?\])\s+/, '').replace(/\s+/g, ' ').trim())
      .filter(l => l.length > 2 && !/:$/.test(l) && !/^(delivery schedule|deliverables?|page \d+)/i.test(l));
  }
  function dialog() {
    let dlg = document.getElementById('oftSchedDialog');
    if (dlg) return dlg;
    dlg = document.createElement('dialog');
    dlg.className = 'oft-dialog'; dlg.id = 'oftSchedDialog'; dlg.setAttribute('aria-labelledby', 'oftSchedTitle');
    dlg.innerHTML = `<h2 id="oftSchedTitle">Add a distributor's delivery schedule</h2>
  <p>Copy the list from the distributor's delivery schedule and paste it here, one item a line. Each line becomes an item marked with their name; you can change its section afterwards.</p>
  <p><label for="oftSchedName">Distributor</label><br><input id="oftSchedName" type="text" autocomplete="off" placeholder="The distributor or platform"></p>
  <p><label for="oftSchedText">Their schedule</label><br><textarea id="oftSchedText" rows="8"></textarea></p>
  <p class="oft-sched-note" id="oftSchedNote" role="status"></p>
  <div class="oft-actions"><button type="button" class="btn" id="oftSchedCancel">Cancel</button><button type="button" class="btn primary" id="oftSchedAdd">Add them</button></div>`;
    document.body.append(dlg);
    const css = document.createElement('style');
    css.textContent = '#oftSchedDialog input, #oftSchedDialog textarea { width: 100%; box-sizing: border-box; font: inherit; }\n.oft-sched-note { font-size: 13px; color: var(--ink-2); min-height: 1.2em; }';
    document.head.append(css);
    const note = () => {
      const name = dlg.querySelector('#oftSchedName').value.trim(), ls = lines(dlg.querySelector('#oftSchedText').value);
      const fresh = ls.filter(l => !S().has(l, name));
      dlg.querySelector('#oftSchedNote').textContent = ls.length ? `${fresh.length} ${fresh.length === 1 ? S().noun : S().noun + 's'} to add${ls.length > fresh.length ? `, ${ls.length - fresh.length} already on the list` : ''}.` : '';
    };
    dlg.addEventListener('input', note);
    dlg.querySelector('#oftSchedCancel').onclick = () => dlg.close();
    dlg.querySelector('#oftSchedAdd').onclick = () => {
      const nameEl = dlg.querySelector('#oftSchedName'), textEl = dlg.querySelector('#oftSchedText'), name = nameEl.value.trim();
      if (!name) { nameEl.setCustomValidity('Name the distributor.'); nameEl.reportValidity(); return; }
      const ls = lines(textEl.value).filter(l => !S().has(l, name));
      if (!ls.length) { textEl.setCustomValidity('Paste the items from the schedule.'); textEl.reportValidity(); return; }
      const n = S().add(name, ls.map(title => ({ title, section: S().guess(title) })));
      dlg.close();
      toast(`Added ${n} ${n === 1 ? S().noun : S().noun + 's'} from ${name}'s schedule.`);
    };
    for (const id of ['oftSchedName', 'oftSchedText']) dlg.querySelector('#' + id).addEventListener('input', ev => ev.target.setCustomValidity(''));
    return dlg;
  }
  function open() {
    const dlg = dialog();
    dlg.querySelector('#oftSchedName').value = '';
    dlg.querySelector('#oftSchedText').value = '';
    dlg.querySelector('#oftSchedNote').textContent = '';
    dlg.showModal();
    dlg.querySelector('#oftSchedName').focus();
  }
  return { open, lines };
})();

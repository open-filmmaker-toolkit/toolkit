// Contacts from an address book. Reads the .vcf files Apple Contacts, Google Contacts and Outlook export,
// then lists each contact to pick from before anything is added. A tool describes what a contact becomes in
// OFT_VCARD = { noun, nouns, plan: contact => ({ have, text }), add: contacts => number }, where have means
// it matches one already in the project; ticking one of those fills in what's missing.
const oftVcard = (() => {
  const str = v => (v == null ? '' : String(v));
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const plural = (n, a, b) => `${n} ${n === 1 ? a : b}`;
  function qp(v, charset) {
    const bytes = [];
    for (let i = 0; i < v.length; i++) {
      if (v[i] === '=' && /^[0-9A-F]{2}$/i.test(v.slice(i + 1, i + 3))) { bytes.push(parseInt(v.slice(i + 1, i + 3), 16)); i += 2; }
      else bytes.push(v.charCodeAt(i) & 255);
    }
    try { return new TextDecoder(charset || 'utf-8').decode(new Uint8Array(bytes)); } catch { return new TextDecoder('utf-8').decode(new Uint8Array(bytes)); }
  }
  const unescape = v => v.replace(/\\([,;:\\nN])/g, (m, ch) => (/n/i.test(ch) ? '\n' : ch)).trim();
  const parts = v => v.split(/(?<!\\);/).map(unescape);
  function parse(text) {
    const lines = [];
    for (const l of str(text).replace(/^﻿/, '').replace(/\r\n?/g, '\n').split('\n')) {
      const last = lines[lines.length - 1];
      // A line starting with a space or tab continues the one before; so does one after a quoted-printable "=".
      if (last != null && /^[ \t]/.test(l)) lines[lines.length - 1] += l.slice(1);
      else if (last != null && /=$/.test(last) && /QUOTED-PRINTABLE/i.test(last.split(':')[0])) lines[lines.length - 1] = last.slice(0, -1) + l;
      else lines.push(l);
    }
    const out = [];
    let c = null;
    for (const l of lines) {
      const i = l.indexOf(':');
      if (i < 0) continue;
      const [rawName, ...params] = l.slice(0, i).split(';');
      const name = rawName.replace(/^[^.]*\./, '').toUpperCase();
      let v = l.slice(i + 1);
      if (name === 'BEGIN' && /vcard/i.test(v)) { c = { emails: [], phones: [] }; continue; }
      if (name === 'END' && /vcard/i.test(v)) { if (c) out.push(finish(c)); c = null; continue; }
      if (!c) continue;
      if (params.some(p => /QUOTED-PRINTABLE/i.test(p))) v = qp(v, (params.find(p => /^CHARSET=/i.test(p)) || '').split('=')[1]);
      const pref = params.some(p => /PREF/i.test(p));
      const put = (list, x) => { if (x) { if (pref) list.unshift(x); else list.push(x); } };
      if (name === 'FN') c.fn = unescape(v);
      else if (name === 'N') c.n = parts(v);
      else if (name === 'ORG') c.org = parts(v).filter(Boolean).join(', ');
      else if (name === 'TITLE' || (name === 'ROLE' && !c.title)) c.title = unescape(v);
      else if (name === 'EMAIL') put(c.emails, unescape(v).replace(/^mailto:/i, ''));
      else if (name === 'TEL') put(c.phones, unescape(v).replace(/^tel:/i, ''));
      else if (name === 'URL' && !c.url) c.url = unescape(v);
      else if (name === 'NOTE') c.note = unescape(v);
      else if (name === 'ADR' && !c.address) c.address = parts(v).filter(Boolean).join(', ');
    }
    return out.filter(x => x.name);
  }
  function finish(c) {
    const n = c.n || [];
    const fromN = [n[3], n[1], n[2], n[0], n[4]].filter(Boolean).join(' ');
    const o = { name: c.fn || fromN || c.org || c.emails[0] || '' };
    for (const [k, v] of [['org', c.org], ['title', c.title], ['email', c.emails[0]], ['phone', c.phones[0]], ['url', c.url], ['note', c.note], ['address', c.address]]) if (v) o[k] = v;
    return o;
  }
  function dialog() {
    let dlg = document.getElementById('oftVcardDialog');
    if (dlg) return dlg;
    dlg = document.createElement('dialog');
    dlg.className = 'oft-dialog'; dlg.id = 'oftVcardDialog'; dlg.setAttribute('aria-labelledby', 'oftVcardTitle');
    dlg.innerHTML = `<h2 id="oftVcardTitle">Import from an address book</h2><p id="oftVcardIntro"></p>
  <p><button type="button" class="btn small" id="oftVcardAll">Tick all</button> <button type="button" class="btn small" id="oftVcardNone">Untick all</button></p>
  <fieldset class="oft-vcard-items" id="oftVcardItems"><legend class="oft-vh">Pick the contacts to add</legend></fieldset>
  <div class="oft-actions"><button type="button" class="btn" id="oftVcardCancel">Cancel</button><button type="button" class="btn primary" id="oftVcardAdd">Add</button></div>`;
    document.body.append(dlg);
    const css = document.createElement('style');
    css.textContent = '.oft-vcard-items { border: 0; margin: 0 0 12px; padding: 0; min-width: 0; display: grid; gap: 6px; max-height: 50vh; overflow-y: auto; }\n.oft-vcard-items label { display: flex; gap: 8px; align-items: flex-start; font-size: 14px; }\n.oft-vcard-items input { width: 18px; height: 18px; margin: 2px 0 0; flex: none; }\n.oft-vcard-items small { display: block; color: inherit; opacity: 0.75; font-size: 13px; }';
    document.head.append(css);
    dlg.querySelector('#oftVcardCancel').onclick = () => dlg.close();
    dlg.querySelector('#oftVcardAll').onclick = () => { dlg.querySelectorAll('#oftVcardItems input').forEach(i => { i.checked = true; }); count(dlg); };
    dlg.querySelector('#oftVcardNone').onclick = () => { dlg.querySelectorAll('#oftVcardItems input').forEach(i => { i.checked = false; }); count(dlg); };
    dlg.querySelector('#oftVcardItems').addEventListener('change', () => count(dlg));
    return dlg;
  }
  function count(dlg) {
    const n = dlg.querySelectorAll('#oftVcardItems input:checked').length;
    dlg.querySelector('#oftVcardAdd').textContent = n ? `Add ${plural(n, 'contact', 'contacts')}` : 'Add';
    dlg.querySelector('#oftVcardAdd').disabled = !n;
  }
  function show(cards, fileName) {
    const V = OFT_VCARD, dlg = dialog(), $ = q => dlg.querySelector(q);
    const plans = cards.map(c => V.plan(c));
    const have = plans.filter(p => p.have).length;
    $('#oftVcardIntro').textContent = `${plural(cards.length, 'contact', 'contacts')} in ${fileName}${have ? `, ${have} already in this project` : ''}. Pick the ones to add.${have ? ' Ticking one already here fills in what it\'s missing and changes nothing else.' : ''}`;
    $('#oftVcardItems').innerHTML = '<legend class="oft-vh">Pick the contacts to add</legend>' + cards.map((c, k) =>
      `<label><input type="checkbox" value="${k}"${plans[k].have ? '' : ' checked'}><span>${e(c.name)}<small>${e([c.title, c.org, c.email, c.phone].filter(Boolean).join(' · '))}</small><small>${e(plans[k].text)}</small></span></label>`).join('');
    count(dlg);
    $('#oftVcardAdd').onclick = () => {
      const picked = [...dlg.querySelectorAll('#oftVcardItems input:checked')].map(i => cards[+i.value]);
      if (!picked.length) return;
      const n = V.add(picked);
      dlg.close();
      changed();
      toast(`Added ${plural(n, 'contact', 'contacts')} from ${fileName}.`);
    };
    dlg.showModal();
  }
  function open() {
    const input = document.createElement('input');
    input.type = 'file'; input.accept = '.vcf,.vcard,text/vcard,text/x-vcard'; input.hidden = true; input.id = 'oftVcardInput';
    document.body.append(input);
    input.onchange = async () => {
      const f = input.files[0];
      input.remove();
      if (!f) return;
      const cards = parse(await f.text());
      if (!cards.length) { toast(`Couldn't find any contacts in ${f.name}. Export a .vcf file from your address book and choose that.`); return; }
      show(cards, f.name);
    };
    input.click();
  }
  return { parse, open, show };
})();

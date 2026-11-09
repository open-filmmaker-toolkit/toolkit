// Translations. Each language is a plain spreadsheet in translations/ (English in one column, the translation
// in the next), and .github/scripts/sync_shared.py copies the lines a page uses into OFT_LANGS below this code.
// Text is matched a sentence at a time: a paragraph, heading, button, label or link, with any bold, code or link
// inside it kept, so a translation can move them. The page is translated as it changes, too.
const oftI18n = (() => {
  const LANGS = typeof OFT_LANGS === 'object' && OFT_LANGS ? OFT_LANGS : {};
  const KEY = 'oft-lang';
  const UNIT = new Set(['P', 'LI', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'LABEL', 'BUTTON', 'A', 'TD', 'TH', 'SUMMARY', 'LEGEND', 'OPTION', 'DT', 'DD', 'FIGCAPTION']);
  const INLINE = new Set(['B', 'STRONG', 'I', 'EM', 'CODE', 'A', 'SPAN', 'KBD', 'SMALL', 'ABBR', 'SUP', 'SUB']);
  const ATTRS = ['placeholder', 'aria-label', 'title', 'alt'];
  const esc = t => t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const unesc = t => t.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
  const store = { get() { try { return localStorage.getItem(KEY); } catch { return null; } }, set(v) { try { localStorage.setItem(KEY, v); } catch { /* storage off */ } } };
  const pick = () => { const s = store.get(); if (s === 'en' || LANGS[s]) return s; const b = (navigator.language || '').slice(0, 2).toLowerCase(); return LANGS[b] ? b : 'en'; };
  const lang = pick();
  const table = () => (LANGS[lang] && LANGS[lang].strings) || {};
  // The same key the extractor in sync_shared.py makes: text, with inline elements as bare tags.
  function keyOf(el) {
    let out = '';
    for (const n of el.childNodes) {
      if (n.nodeType === 3) out += esc(n.nodeValue);
      else if (n.nodeType === 1 && INLINE.has(n.tagName) && [...n.childNodes].every(c => c.nodeType === 3)) out += `<${n.tagName.toLowerCase()}>${esc(n.textContent)}</${n.tagName.toLowerCase()}>`;
      else if (n.nodeType !== 8) return null;
    }
    return out.replace(/\s+/g, ' ').trim().replace(/<(\w+)> /g, '<$1>').replace(/ <\/(\w+)>/g, '</$1>');
  }
  // Puts the translation in, reusing the original bold, code and links (with their addresses) in its order.
  function put(el, text) {
    const pool = {};
    for (const n of el.children) (pool[n.tagName.toLowerCase()] = pool[n.tagName.toLowerCase()] || []).push(n);
    const frag = document.createDocumentFragment();
    const parts = text.split(/(<\w+>[^<]*<\/\w+>)/);
    for (const p of parts) {
      const m = p.match(/^<(\w+)>([^<]*)<\/\1>$/);
      if (m) { const orig = (pool[m[1]] || []).shift(); const n = orig ? orig.cloneNode(false) : document.createElement(m[1]); n.textContent = unesc(m[2]); frag.append(n); }
      else if (p) frag.append(document.createTextNode(unesc(p)));
    }
    el.replaceChildren(frag);
    el.dataset.oftT = '1';
  }
  function apply(root) {
    const t = table();
    if (!root || !Object.keys(t).length) return;
    const els = root.nodeType === 1 ? [root, ...root.querySelectorAll('*')] : [...root.querySelectorAll('*')];
    for (const el of els) {
      if (el.closest('script, style, textarea, [contenteditable], [data-no-translate]')) continue;
      for (const a of ATTRS) { const v = el.getAttribute(a); if (v) { const k = v.replace(/\s+/g, ' ').trim(); if (t[k]) el.setAttribute(a, t[k]); } }
      if (UNIT.has(el.tagName) && !el.dataset.oftT) { const k = keyOf(el); if (k && t[k]) put(el, t[k]); }
    }
  }
  // Every page offers the languages there are; English brings the page back by reloading it.
  function picker() {
    const codes = Object.keys(LANGS);
    if (!codes.length) return;
    const home = document.querySelector('.home-link');
    const where = (home && home.parentElement) || document.querySelector('[data-lang-picker]') || document.querySelector('footer');
    if (!where) return;
    const wrap = document.createElement('span');
    wrap.className = 'oft-lang';
    wrap.setAttribute('data-no-translate', '');
    wrap.innerHTML = `<label for="oftLang">${lang === 'en' ? 'Language' : esc((LANGS[lang] && LANGS[lang].label) || 'Language')}</label> <select id="oftLang"><option value="en">English</option>${codes.map(c => `<option value="${c}"${c === lang ? ' selected' : ''}>${esc(LANGS[c].name)}</option>`).join('')}</select>`;
    where.append(' ', wrap);
    const css = document.createElement('style');
    css.textContent = '.oft-lang { display: inline-flex; gap: 6px; align-items: center; margin-left: 10px; font-size: 13px; white-space: nowrap; } .oft-lang select { padding: 2px 4px; border: 1px solid var(--rule); border-radius: 4px; background: var(--sheet, var(--paper)); color: var(--ink); font: inherit; }';
    document.head.append(css);
    wrap.querySelector('select').addEventListener('change', ev => { store.set(ev.target.value); window.location.reload(); });
  }
  function start() {
    if (lang === 'en') { picker(); return; }
    document.documentElement.lang = lang;
    apply(document.body);
    picker();
    if (document.title && table()[document.title]) document.title = table()[document.title];
    // Tools draw much of the page as you work, so new parts are translated as they appear.
    new MutationObserver(list => {
      const seen = new Set();
      for (const m of list) {
        const n = m.type === 'characterData' ? m.target.parentElement : m.target;
        if (!n || seen.has(n)) continue;
        seen.add(n);
        if (m.type === 'childList' && n.dataset && n.dataset.oftT) delete n.dataset.oftT;
        if (m.type === 'childList' || m.type === 'characterData') { const u = n.closest && n.closest('[data-oft-t]'); if (u && u !== n && m.type === 'characterData') delete u.dataset.oftT; }
        apply(n.nodeType === 1 ? n : n.parentElement);
      }
    }).observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS });
  }
  // Text a tool writes into a file or a printout in a chosen language, such as a screening kit.
  const t = (text, code = lang) => { const tb = (LANGS[code] && LANGS[code].strings) || {}; return tb[text] || text; };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else setTimeout(start, 0);
  return { t, lang, langs: () => Object.keys(LANGS).map(c => ({ code: c, name: LANGS[c].name })), apply };
})();

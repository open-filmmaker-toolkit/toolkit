// Reading and joining documents in the browser, with no library: the text of a Word document or a PDF,
// and several PDFs joined into one. PDFs locked with a password, and scans with no text in them, can't be read.
// oftDocs.text(file) resolves to the text, a line for each paragraph or line; oftDocs.merge([ArrayBuffer]) to a Blob.
const oftDocs = (() => {
  const dec = new TextDecoder();
  const latin = u => { let t = ''; for (let i = 0; i < u.length; i += 8192) t += String.fromCharCode.apply(null, u.subarray(i, i + 8192)); return t; };
  const unlatin = s => { const u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i) & 255; return u; };
  const inflate = async (bytes, raw) => new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream(raw ? 'deflate-raw' : 'deflate'))).arrayBuffer());
  const canInflate = () => typeof DecompressionStream !== 'undefined';

  // ---------- Word ----------
  async function docxText(buf) {
    const b = new Uint8Array(buf), dv = new DataView(buf);
    let e = -1;
    for (let i = b.length - 22; i >= Math.max(0, b.length - 66000); i--) if (dv.getUint32(i, true) === 0x06054b50) { e = i; break; }
    if (e < 0) throw new Error("isn't a Word document");
    let p = dv.getUint32(e + 16, true);
    const n = dv.getUint16(e + 10, true);
    for (let k = 0; k < n; k++) {
      if (dv.getUint32(p, true) !== 0x02014b50) break;
      const method = dv.getUint16(p + 10, true), size = dv.getUint32(p + 20, true), nl = dv.getUint16(p + 28, true), xl = dv.getUint16(p + 30, true), cl = dv.getUint16(p + 32, true), off = dv.getUint32(p + 42, true);
      const fname = dec.decode(b.subarray(p + 46, p + 46 + nl));
      p += 46 + nl + xl + cl;
      if (fname !== 'word/document.xml') continue;
      const start = off + 30 + dv.getUint16(off + 26, true) + dv.getUint16(off + 28, true), data = b.subarray(start, start + size);
      let xml;
      if (method === 0) xml = dec.decode(data);
      else if (method === 8 && canInflate()) xml = dec.decode(await inflate(data, true));
      else throw new Error("can't be unpacked in this browser");
      const d = new DOMParser().parseFromString(xml, 'application/xml'), W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main';
      return [...d.getElementsByTagNameNS(W, 'p')].map(par => [...par.getElementsByTagNameNS(W, '*')].map(x => (x.localName === 't' ? x.textContent : x.localName === 'tab' || x.localName === 'br' ? ' ' : '')).join('')).join('\n');
    }
    throw new Error("isn't a Word document");
  }

  // ---------- PDF ----------
  // Every object in the file, by number, with its dictionary as text and its stream as stored.
  // Objects packed into object streams are unpacked; a later copy of an object replaces an earlier one.
  async function parsePdf(buf) {
    const b = new Uint8Array(buf), raw = latin(b);
    if (!raw.startsWith('%PDF')) throw new Error("isn't a PDF");
    if (/\/Encrypt\s/.test(raw)) throw new Error('is locked with a password');
    const objs = new Map(), re = /(\d+)\s+(\d+)\s+obj\b/g;
    let m;
    while ((m = re.exec(raw))) {
      const at = m.index + m[0].length, stop = raw.indexOf('endobj', at);
      let body = raw.slice(at, stop < 0 ? undefined : stop);
      const si = body.search(/\bstream\r?\n/);
      const o = { dict: (si >= 0 ? body.slice(0, si) : body).trim() };
      if (si >= 0) {
        let st = at + si + 6; if (raw[st] === '\r') st++; if (raw[st] === '\n') st++;
        const lm = /\/Length\s+(\d+)(?!\s+\d+\s+R)/.exec(o.dict);
        let end = lm ? st + +lm[1] : -1;
        if (end < 0 || raw.slice(end, end + 30).indexOf('endstream') < 0) { end = raw.indexOf('endstream', st); while (end > st && (raw[end - 1] === '\n' || raw[end - 1] === '\r')) end--; }
        o.raw = b.subarray(st, end);
      }
      objs.set(+m[1], o);
      if (stop > 0) re.lastIndex = stop;
    }
    const data = async o => {
      if (!o.raw) return null;
      if (o.data) return o.data;
      if (/\/FlateDecode/.test(o.dict)) { if (!canInflate()) throw new Error("can't be read in this browser"); try { o.data = await inflate(o.raw); } catch { o.data = new Uint8Array(0); } }
      else o.data = /\/Filter/.test(o.dict) ? new Uint8Array(0) : o.raw;
      return o.data;
    };
    for (const o of [...objs.values()]) if (/\/Type\s*\/ObjStm/.test(o.dict)) {
      const t = latin(await data(o)), n = +(/\/N\s+(\d+)/.exec(o.dict) || [])[1], first = +(/\/First\s+(\d+)/.exec(o.dict) || [])[1];
      const nums = t.slice(0, first).trim().split(/\s+/).map(Number);
      for (let k = 0; k < n; k++) { const from = first + nums[2 * k + 1], to = k + 1 < n ? first + nums[2 * k + 3] : t.length; if (!objs.has(nums[2 * k])) objs.set(nums[2 * k], { dict: t.slice(from, to).trim(), packed: true }); }
    }
    const roots = [...raw.matchAll(/\/Root\s+(\d+)\s+\d+\s+R/g)];
    const root = roots.length ? +roots[roots.length - 1][1] : [...objs].find(([, o]) => /\/Type\s*\/Catalog/.test(o.dict))?.[0];
    return { objs, root, data };
  }
  const ref = (dict, key) => { const m = new RegExp(`/${key}\\s+(\\d+)\\s+\\d+\\s+R`).exec(dict); return m ? +m[1] : null; };
  const refs = (dict, key) => { const m = new RegExp(`/${key}\\s*\\[([^\\]]*)\\]`).exec(dict); return m ? [...m[1].matchAll(/(\d+)\s+\d+\s+R/g)].map(x => +x[1]) : ref(dict, key) != null ? [ref(dict, key)] : []; };
  // The page objects in order, walking the page tree from the catalog.
  function pages(p) {
    const cat = p.objs.get(p.root), out = [], seen = new Set();
    const walk = n => { if (seen.has(n)) return; seen.add(n); const o = p.objs.get(n); if (!o) return; if (/\/Type\s*\/Pages\b/.test(o.dict)) refs(o.dict, 'Kids').forEach(walk); else out.push(n); };
    if (cat) { const r = ref(cat.dict, 'Pages'); if (r != null) walk(r); }
    return out;
  }
  // bfchar and bfrange entries of a ToUnicode map: character codes to text.
  function cmap(t) {
    const map = new Map(), hex = h => { let s = ''; for (let i = 0; i + 4 <= h.length; i += 4) s += String.fromCharCode(parseInt(h.slice(i, i + 4), 16)); return s || String.fromCharCode(parseInt(h, 16)); };
    for (const blk of t.matchAll(/beginbfchar([\s\S]*?)endbfchar/g)) for (const x of blk[1].matchAll(/<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>/g)) map.set(parseInt(x[1], 16), hex(x[2]));
    for (const blk of t.matchAll(/beginbfrange([\s\S]*?)endbfrange/g)) for (const x of blk[1].matchAll(/<([0-9a-fA-F]+)>\s*<([0-9a-fA-F]+)>\s*(<[0-9a-fA-F]+>|\[[^\]]*\])/g)) {
      const a = parseInt(x[1], 16), z = parseInt(x[2], 16);
      if (x[3][0] === '[') [...x[3].matchAll(/<([0-9a-fA-F]+)>/g)].forEach((y, k) => map.set(a + k, hex(y[1])));
      else { const base = x[3].slice(1, -1), lo = parseInt(base.slice(-4), 16), pre = base.length > 4 ? hex(base.slice(0, -4)) : ''; for (let c = a; c <= z && c - a < 65536; c++) map.set(c, pre + String.fromCharCode(lo + c - a)); }
    }
    return map;
  }
  // The fonts a page or form uses, by resource name: how to turn its character codes into text.
  async function fonts(p, dict) {
    const out = new Map();
    let res = dict, r = ref(dict, 'Resources');
    if (r != null && p.objs.get(r)) res = p.objs.get(r).dict;
    let fd = /\/Font\s*<<([\s\S]*?)>>/.exec(res), fdText = fd ? fd[1] : '';
    const fr = ref(res, 'Font'); if (!fd && fr != null && p.objs.get(fr)) fdText = p.objs.get(fr).dict;
    for (const f of fdText.matchAll(/\/([^\s/<>\[\]()]+)\s+(\d+)\s+\d+\s+R/g)) {
      const font = p.objs.get(+f[2]); if (!font) continue;
      const tu = ref(font.dict, 'ToUnicode'), cm = tu != null && p.objs.get(tu);
      out.set(f[1], { map: cm && cm.raw ? cmap(latin(await p.data(cm))) : null, two: /Type0|Identity-H/.test(font.dict) });
    }
    return out;
  }
  // Text shown by a content stream, a new line whenever the text moves down the page.
  function lines(t, fontsOf) {
    const out = []; let line = '', font = null, y = null;
    const flush = () => { if (line.trim()) out.push(line.replace(/\s+/g, ' ').trim()); line = ''; };
    const decode = bytes => { if (!font || !font.map) return bytes.map(c => String.fromCharCode(c)).join(''); const w = font.two ? 2 : 1; let s = ''; for (let i = 0; i + w <= bytes.length; i += w) { const c = w === 2 ? bytes[i] * 256 + bytes[i + 1] : bytes[i]; s += font.map.get(c) || ''; } return s; };
    const lit = s => { const o = []; for (let i = 0; i < s.length; i++) { const c = s[i]; if (c !== '\\') { o.push(c.charCodeAt(0)); continue; } const n = s[++i], esc = { n: 10, r: 13, t: 9, b: 8, f: 12 }[n]; if (esc != null) o.push(esc); else if (/[0-7]/.test(n)) { let d = n; while (d.length < 3 && /[0-7]/.test(s[i + 1])) d += s[++i]; o.push(parseInt(d, 8) & 255); } else if (n === '\r' || n === '\n') { if (n === '\r' && s[i + 1] === '\n') i++; } else if (n != null) o.push(n.charCodeAt(0)); } return o; };
    const hexb = h => { h = h.replace(/\s+/g, ''); if (h.length % 2) h += '0'; const o = []; for (let i = 0; i < h.length; i += 2) o.push(parseInt(h.slice(i, i + 2), 16)); return o; };
    const str1 = k => (k[0] === '(' ? decode(lit(k.slice(1, -1))) : decode(hexb(k.slice(1, -1))));
    const tok = /\((?:\\[\s\S]|[^\\)])*\)|<[0-9a-fA-F\s]*>|\[(?:\((?:\\[\s\S]|[^\\)])*\)|<[0-9a-fA-F\s]*>|[^\]])*\]|\/[^\s/\[\]()<>]+|-?\d*\.?\d+|[A-Za-z'"*]+/g;
    const stack = [];
    let mm;
    while ((mm = tok.exec(t))) {
      const k = mm[0];
      if (!/^[A-Za-z'"*]+$/.test(k)) { stack.push(k); continue; }
      const top = stack[stack.length - 1];
      if (k === 'Tf') font = fontsOf.get(String(stack[stack.length - 2] || '').slice(1)) || null;
      else if (k === 'Tj') { if (top) line += str1(top); }
      else if (k === "'" || k === '"') { flush(); if (top) line += str1(top); }
      else if (k === 'TJ') { for (const part of String(top || '').matchAll(/\((?:\\[\s\S]|[^\\)])*\)|<[0-9a-fA-F\s]*>|-?\d*\.?\d+/g)) { const q = part[0]; if (q[0] === '(' || q[0] === '<') line += str1(q); else if (+q < -200) line += ' '; } }
      else if (k === 'Td' || k === 'TD') { if (+top) flush(); else line += ' '; }
      else if (k === 'Tm') { const ny = +top; if (y == null || Math.abs(ny - y) > 1) flush(); else line += ' '; y = ny; }
      else if (k === 'T*' || k === 'ET') flush();
      stack.length = 0;
    }
    flush();
    return out;
  }
  async function pdfText(buf) {
    const p = await parsePdf(buf), out = [];
    for (const n of pages(p)) {
      const pg = p.objs.get(n), f = await fonts(p, pg.dict);
      for (const c of refs(pg.dict, 'Contents')) { const o = p.objs.get(c); if (o && o.raw) out.push(...lines(latin(await p.data(o)), f)); }
    }
    return out.join('\n');
  }

  // Several PDFs as one: each file's page tree goes under a new one, so pages keep what they inherit.
  async function merge(buffers) {
    const chunks = [], offsets = [];
    let size = 0, next = 3;
    const put = u => { chunks.push(u); size += u.length; };
    const kids = [];
    let count = 0;
    put(unlatin('%PDF-1.7\n%\xe2\xe3\xcf\xd3\n'));
    for (const buf of buffers) {
      const p = await parsePdf(buf), cat = p.objs.get(p.root), pr = cat && ref(cat.dict, 'Pages');
      if (pr == null || !p.objs.get(pr)) throw new Error('has no pages to add');
      const max = Math.max(...p.objs.keys()), off = next;
      const remap = s => s.replace(/(\d+)\s+(\d+)\s+R\b/g, (x, a) => `${+a + off} 0 R`);
      for (const [n, o] of p.objs) {
        if (/\/Type\s*\/(XRef|ObjStm|Catalog)\b/.test(o.dict) || n === p.root) continue;
        let dict = remap(o.dict);
        if (n === pr) dict = dict.replace(/\/Parent\s+\d+\s+0\s+R/, '').replace(/^<</, '<< /Parent 2 0 R');
        if (o.raw) dict = dict.replace(/\/Length\s+\d+(\s+\d+\s+R)?/, `/Length ${o.raw.length}`);
        offsets[n + off] = size;
        put(unlatin(`${n + off} 0 obj\n${dict}\n`));
        if (o.raw) { put(unlatin('stream\n')); put(o.raw); put(unlatin('\nendstream\n')); }
        put(unlatin('endobj\n'));
      }
      kids.push(pr + off);
      count += pages(p).length;
      next = off + max + 1;
    }
    offsets[1] = size; put(unlatin('1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'));
    offsets[2] = size; put(unlatin(`2 0 obj\n<< /Type /Pages /Kids [${kids.map(k => `${k} 0 R`).join(' ')}] /Count ${count} >>\nendobj\n`));
    const xref = size;
    let x = `xref\n0 ${next}\n0000000000 65535 f \n`;
    for (let i = 1; i < next; i++) x += offsets[i] != null ? `${String(offsets[i]).padStart(10, '0')} 00000 n \n` : '0000000000 65535 f \n';
    put(unlatin(`${x}trailer\n<< /Size ${next} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`));
    return { blob: new Blob(chunks, { type: 'application/pdf' }), pages: count };
  }

  const isPdf = f => /\.pdf$/i.test(f.name) || f.type === 'application/pdf';
  const isDocx = f => /\.docx$/i.test(f.name) || f.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
  // The text of a file: Word, PDF, or anything that's already text.
  async function text(file) {
    if (isPdf(file)) { const t = await pdfText(await file.arrayBuffer()); if (!t.trim()) throw new Error("has no text to read. If it's a scan, run it through text recognition first"); return t; }
    if (isDocx(file)) return docxText(await file.arrayBuffer());
    return file.text();
  }
  return { text, merge, pdfText, docxText, isPdf, isDocx };
})();

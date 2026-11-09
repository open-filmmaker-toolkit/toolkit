// Reading transcripts from transcription apps: SRT, WebVTT, text with timestamps, Word documents
// and the HTML noScribe writes.
// Shared by the paper edit and the interview log, which keep transcripts in paperEdit.transcripts.
const oftTranscript = (() => {
  const str = v => (v == null ? '' : String(v));
  const isNum = n => typeof n === 'number' && isFinite(n);
  // A time such as 01:02:03,456, 01:02:03.4, 02:03.456 or 01:02:03, in seconds.
  function secs(s) {
    const m = str(s).trim().match(/^(?:(\d{1,2}):)?(\d{1,2}):(\d{2})(?:[.,](\d{1,3}))?$/);
    if (!m) return null;
    return (Number(m[1] || 0) * 3600) + Number(m[2]) * 60 + Number(m[3]) + (m[4] ? Number(`0.${m[4]}`) : 0);
  }
  const clean = s => str(s).replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&nbsp;/g, ' ').replace(/\s+/g, ' ').trim();
  // A speaker at the start of a line: "Ruth Hammond: ...", "SPEAKER_01: ...", "S01: ...".
  function speakerOf(text) {
    const m = text.match(/^((?:[A-Z][\w'.-]*)(?: [A-Z][\w'.-]*){0,3}|SPEAKER[_ ]?\d+|S\d{1,2}):\s+(.*)$/);
    return m && m[1].length <= 30 ? { speaker: m[1], text: m[2] } : { text };
  }
  function parseCues(text) {
    const segs = [];
    for (const block of text.replace(/\r/g, '').split(/\n\s*\n/)) {
      const lines = block.split('\n').map(l => l.trim()).filter(Boolean);
      const i = lines.findIndex(l => l.includes('-->'));
      if (i < 0) continue;
      const [a, b] = lines[i].split('-->').map(x => x.trim().split(/\s+/)[0]);
      const start = secs(a), end = secs(b);
      if (start == null) continue;
      let raw = lines.slice(i + 1).join(' ');
      let speaker = '';
      const v = raw.match(/<v(?:\.[^ >]*)?\s+([^>]+)>/);
      if (v) speaker = v[1].trim();
      raw = clean(raw);
      if (!raw) continue;
      const sp = speaker ? { speaker, text: raw } : speakerOf(raw);
      segs.push(Object.assign({ start, end: end != null && end > start ? end : start + 2 }, sp));
    }
    return segs;
  }
  // Text with a timestamp at the start of each paragraph, or no timestamps at all.
  function parseText(text) {
    const TS = /^\s*[\[(]?((?:\d{1,2}:)?\d{1,2}:\d{2}(?:[.,]\d{1,3})?)[\])]?(?:\s*(?:-->|–|-)\s*[\[(]?((?:\d{1,2}:)?\d{1,2}:\d{2}(?:[.,]\d{1,3})?)[\])]?)?\s*(.*)$/;
    const lines = text.replace(/\r/g, '').split('\n');
    const segs = [];
    let cur = null, any = false;
    for (const line of lines) {
      const m = line.match(TS);
      if (m && secs(m[1]) != null) {
        any = true;
        if (cur) segs.push(cur);
        cur = { start: secs(m[1]), end: m[2] ? secs(m[2]) : null, text: m[3] || '' };
      } else if (line.trim()) {
        if (!cur || (!any && cur.text)) { if (cur) segs.push(cur); cur = { start: null, end: null, text: '' }; }
        cur.text = `${cur.text} ${line.trim()}`.trim();
      } else if (cur && !any && cur.text) { segs.push(cur); cur = null; }
    }
    if (cur) segs.push(cur);
    const out = segs.map(s => Object.assign(s, speakerOf(clean(s.text)))).filter(s => s.text);
    // Paragraphs without an end run to the start of the next one.
    out.forEach((s, i) => { if (isNum(s.start) && !isNum(s.end)) { const n = out[i + 1]; s.end = n && isNum(n.start) && n.start > s.start ? n.start : s.start + Math.max(2, s.text.split(/\s+/).length / 2.5); } });
    return out;
  }
  // HTML, such as noScribe's: segments it times with anchors named ts_<start ms>_<end ms>_<speaker>
  // when there are any, otherwise each paragraph as a line of text, with its [hh:mm:ss] timestamp.
  function parseHtml(html) {
    const dom = new DOMParser().parseFromString(html, 'text/html');
    const anchors = [...dom.querySelectorAll('a[name^="ts_"]')].map(a => ({ a, m: /^ts_(\d+)_(\d+)(?:_(.*))?$/.exec(a.getAttribute('name')) })).filter(x => x.m);
    if (anchors.length) {
      return anchors.map(({ a, m }) => {
        const sp = speakerOf(clean(a.textContent));
        return Object.assign({ start: +m[1] / 1000, end: +m[2] / 1000 }, m[3] && !sp.speaker ? { speaker: m[3] } : {}, sp);
      }).filter(x => x.text);
    }
    const blocks = [...dom.body.querySelectorAll('p, li, h1, h2, h3')];
    const lines = (blocks.length ? blocks.map(n => n.textContent) : str(dom.body.innerText || dom.body.textContent).split('\n')).map(clean).filter(Boolean);
    return parseText(lines.join('\n\n'));
  }
  // A Word document's paragraphs, read from the zip in the browser: no library, using its own unzip.
  async function docxText(buf) {
    const b = new Uint8Array(buf), dv = new DataView(buf);
    let e = -1;
    for (let i = b.length - 22; i >= Math.max(0, b.length - 66000); i--) if (dv.getUint32(i, true) === 0x06054b50) { e = i; break; }
    if (e < 0) throw new Error("isn't a Word document");
    let p = dv.getUint32(e + 16, true);
    const n = dv.getUint16(e + 10, true), dec = new TextDecoder();
    for (let k = 0; k < n; k++) {
      if (dv.getUint32(p, true) !== 0x02014b50) break;
      const method = dv.getUint16(p + 10, true), size = dv.getUint32(p + 20, true), nl = dv.getUint16(p + 28, true), xl = dv.getUint16(p + 30, true), cl = dv.getUint16(p + 32, true), off = dv.getUint32(p + 42, true);
      const fname = dec.decode(b.subarray(p + 46, p + 46 + nl));
      p += 46 + nl + xl + cl;
      if (fname !== 'word/document.xml') continue;
      const start = off + 30 + dv.getUint16(off + 26, true) + dv.getUint16(off + 28, true), data = b.subarray(start, start + size);
      let xml;
      if (method === 0) xml = dec.decode(data);
      else if (method === 8 && typeof DecompressionStream !== 'undefined') xml = await new Response(new Blob([data]).stream().pipeThrough(new DecompressionStream('deflate-raw'))).text();
      else throw new Error("can't be unpacked in this browser");
      const doc = new DOMParser().parseFromString(xml, 'application/xml'), W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main';
      return [...doc.getElementsByTagNameNS(W, 'p')].map(par => [...par.getElementsByTagNameNS(W, '*')].map(x => (x.localName === 't' ? x.textContent : x.localName === 'tab' ? ' ' : x.localName === 'br' ? ' ' : '')).join('')).join('\n');
    }
    throw new Error("isn't a Word document");
  }
  // The text of a transcript file, whatever kind it is. Word documents come back as one paragraph a line.
  async function read(file) {
    if (/\.docx$/i.test(file.name) || file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return docxText(await file.arrayBuffer());
    return file.text();
  }
  function parse(text, name, newId) {
    if (/\.html?$/i.test(name) || /^\s*(<!doctype html|<html)/i.test(text)) {
      const segs = parseHtml(text).map(s => { const o = { id: newId('seg'), text: s.text }; if (isNum(s.start)) { o.start = Math.round(s.start * 1000) / 1000; o.end = Math.round((isNum(s.end) && s.end > s.start ? s.end : s.start + 2) * 1000) / 1000; } if (s.speaker) o.speaker = s.speaker; return o; });
      return { segments: segs, format: 'html', timed: segs.some(s => isNum(s.start)) };
    }
    const isCue = /-->/.test(text) && (/^﻿?WEBVTT/.test(text) || /\.(srt|vtt)$/i.test(name) || /^\s*\d+\s*\n\s*[\d:,.]+\s*-->/m.test(text));
    const segs = (isCue ? parseCues(text) : parseText(text)).map(s => { const o = { id: newId('seg'), text: s.text }; if (isNum(s.start)) { o.start = Math.round(s.start * 1000) / 1000; o.end = Math.round(s.end * 1000) / 1000; } if (s.speaker) o.speaker = s.speaker; return o; });
    return { segments: segs, format: isCue ? (/WEBVTT/.test(text) ? 'vtt' : 'srt') : 'text', timed: segs.some(s => isNum(s.start)) };
  }
  // Seconds as hours, minutes and seconds, such as 00:03:12.
  const hms = s => { s = Math.max(0, Math.floor(s)); return [Math.floor(s / 3600), Math.floor(s / 60) % 60, s % 60].map(n => String(n).padStart(2, '0')).join(':'); };
  return { parse, read, secs, hms };
})();

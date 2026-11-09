// Reading transcripts from transcription apps: SRT, WebVTT, text with timestamps and the HTML noScribe writes,
// and Word documents and PDFs, which need the docs block (shared/docs.js) on the page too.
// Shared by the paper edit and the interview log, which keep transcripts in paperEdit.transcripts,
// and the clearance report, which reads scripts.
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
  // The text of a transcript file, whatever kind it is. Word documents and PDFs, read by oftDocs, come back a paragraph or line at a time.
  const read = file => oftDocs.text(file);
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

// Files for editing apps, written from the project: timecode with drop frame, FCPXML for Final Cut Pro and
// DaVinci Resolve, Final Cut Pro 7 XML for Premiere Pro, CMX 3600 edit lists, Avid ALE bin files, and marker
// lists for Resolve, Avid and Final Cut. Media comes in offline, named as in the project, ready to relink.
const oftEdit = (() => {
  const str = v => (v == null ? '' : String(v));
  const x = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' })[c]);
  const RATES = { '23.976': [24000, 1001], '24': [2400, 100], '25': [2500, 100], '29.97': [30000, 1001], '30': [3000, 100], '50': [5000, 100], '59.94': [60000, 1001], '60': [6000, 100] };
  const rateOf = fps => RATES[str(fps)] || RATES[String(Number(fps))] || RATES['23.976'];
  const base = fps => Math.round(rateOf(fps)[0] / rateOf(fps)[1]);
  const ntsc = fps => rateOf(fps)[1] === 1001;
  // Drop frame only exists at 29.97 and 59.94: two (or four) frame numbers are skipped each minute, except every tenth.
  const canDrop = fps => ['29.97', '59.94'].includes(str(fps));
  function frames(tc, fps, drop) {
    const m = str(tc).trim().match(/^(\d{1,2})[:;.](\d{2})[:;.](\d{2})[:;.](\d{2})$/);
    if (!m) return null;
    const b = base(fps), [h, mi, s, f] = m.slice(1).map(Number);
    if (mi > 59 || s > 59 || f >= b) return null;
    let n = ((h * 60 + mi) * 60 + s) * b + f;
    if (drop && canDrop(fps)) { const d = b / 15, mins = h * 60 + mi; n -= d * (mins - Math.floor(mins / 10)); }
    return n;
  }
  function tc(n, fps, drop) {
    const b = base(fps);
    n = Math.max(0, Math.round(n));
    if (drop && canDrop(fps)) {
      const d = b / 15, per10 = b * 600 - d * 9, per1 = b * 60 - d;
      const tens = Math.floor(n / per10), rem = n % per10;
      n += d * 9 * tens + (rem > d ? d * Math.floor((rem - d) / per1) : 0);
    }
    const parts = [Math.floor(n / (b * 3600)) % 24, Math.floor(n / (b * 60)) % 60, Math.floor(n / b) % 60, n % b].map(v => String(v).padStart(2, '0'));
    return `${parts[0]}:${parts[1]}:${parts[2]}${drop && canDrop(fps) ? ';' : ':'}${parts[3]}`;
  }
  // FCPXML times are rational seconds: frames times the frame duration.
  const t = (n, fps) => { const [den, num] = rateOf(fps); return n ? `${n * num}/${den}s` : '0s'; };
  const frameDuration = fps => { const [den, num] = rateOf(fps); return `${num}/${den}s`; };
  const fileUrl = p => 'file:///' + str(p).replace(/\\/g, '/').replace(/^\/+/, '').split('/').map(encodeURIComponent).join('/');
  const head = '<?xml version="1.0" encoding="UTF-8"?>\n';

  // Clips: [{ name, file, path, reel, srcIn, srcOut, start, note, track }], all in frames; start is where the
  // source media's own timecode begins. audio: 'together', or 'separate' to put the sound on its own tracks, one
  // for each value of clip.track (a speaker, say), numbered in the order they come.
  function sources(clips) {
    const by = new Map();
    for (const c of clips) {
      const k = c.file || c.name;
      const s = by.get(k) || { file: k, path: c.path || k, start: c.start != null ? c.start : c.srcIn, end: c.srcOut };
      s.start = Math.min(s.start, c.start != null ? c.start : c.srcIn); s.end = Math.max(s.end, c.srcOut);
      by.set(k, s);
    }
    [...by.values()].forEach((s, i) => { s.id = `r${i + 2}`; s.n = i + 1; });
    return by;
  }
  const trackNames = clips => [...new Set(clips.map(c => str(c.track) || 'Audio'))];

  function fcpxml({ title, fps, drop, clips, recStart = 0, audio = 'together', markers = [] }) {
    const src = sources(clips), tracks = trackNames(clips), dur = clips.reduce((n, c) => n + (c.srcOut - c.srcIn), 0);
    const fmt = drop && canDrop(fps) ? 'DF' : 'NDF';
    const res = [`<format id="r1" frameDuration="${frameDuration(fps)}" width="1920" height="1080"/>`,
      ...[...src.values()].map(s => `<asset id="${s.id}" name="${x(s.file.replace(/\.[^.]+$/, ''))}" start="${t(s.start, fps)}" duration="${t(s.end - s.start, fps)}" hasVideo="1" hasAudio="1" format="r1" audioSources="1" audioChannels="2"><media-rep kind="original-media" src="${x(fileUrl(s.path))}"/></asset>`)];
    let at = recStart;
    const mk = (m, off) => `<marker start="${t(off, fps)}" duration="${frameDuration(fps)}" value="${x(m.text)}"/>`;
    const spine = clips.map(c => {
      const s = src.get(c.file || c.name), len = c.srcOut - c.srcIn, lane = tracks.indexOf(str(c.track) || 'Audio') + 1;
      const notes = c.note ? mk({ text: c.note }, c.srcIn) : '';
      const body = audio === 'separate'
        ? `<asset-clip ref="${s.id}" offset="${t(at, fps)}" name="${x(c.name)}" start="${t(c.srcIn, fps)}" duration="${t(len, fps)}" tcFormat="${fmt}" srcEnable="video">${notes}<asset-clip ref="${s.id}" lane="-${lane}" offset="${t(c.srcIn, fps)}" name="${x(c.name)}" start="${t(c.srcIn, fps)}" duration="${t(len, fps)}" srcEnable="audio" audioRole="dialogue.${x(tracks[lane - 1]).replace(/[^\w-]/g, '-')}"/></asset-clip>`
        : `<asset-clip ref="${s.id}" offset="${t(at, fps)}" name="${x(c.name)}" start="${t(c.srcIn, fps)}" duration="${t(len, fps)}" tcFormat="${fmt}" audioRole="dialogue">${notes}</asset-clip>`;
      at += len;
      return body;
    });
    let gap = 0;
    if (markers.length) {
      const end = Math.max(...markers.map(m => m.at + (m.len || 1))) - recStart;
      gap = Math.max(1, end);
      spine.push(`<gap name="Markers" offset="${t(at, fps)}" start="${t(recStart, fps)}" duration="${t(Math.max(1, end), fps)}">${markers.map(m => mk(m, m.at)).join('')}</gap>`);
    }
    return `${head}<!DOCTYPE fcpxml>\n<fcpxml version="1.9">\n<resources>\n${res.join('\n')}\n</resources>\n<library>\n<event name="${x(title)}">\n<project name="${x(title)}">\n<sequence format="r1" tcStart="${t(recStart, fps)}" tcFormat="${fmt}" duration="${t(dur + gap, fps)}" audioLayout="stereo" audioRate="48k">\n<spine>\n${spine.join('\n')}\n</spine>\n</sequence>\n</project>\n</event>\n</library>\n</fcpxml>\n`;
  }

  // Final Cut Pro 7 XML, which Premiere Pro imports: picture on V1 and the sound on A1 and A2, or a pair of
  // tracks for each speaker when the audio is separate.
  function xmeml({ title, fps, drop, clips, recStart = 0, audio = 'together' }) {
    const src = sources(clips), tracks = audio === 'separate' ? trackNames(clips) : ['Audio'];
    const rate = `<rate><timebase>${base(fps)}</timebase><ntsc>${ntsc(fps) ? 'TRUE' : 'FALSE'}</ntsc></rate>`;
    const tcx = n => `<timecode>${rate}<string>${tc(n, fps, drop)}</string><frame>${n}</frame><displayformat>${drop && canDrop(fps) ? 'DF' : 'NDF'}</displayformat></timecode>`;
    const seen = new Set();
    const file = s => { if (seen.has(s.id)) return `<file id="file-${s.n}"/>`; seen.add(s.id); return `<file id="file-${s.n}"><name>${x(s.file)}</name><pathurl>${x(fileUrl(s.path))}</pathurl>${rate}<duration>${s.end - s.start}</duration>${tcx(s.start)}<media><video><samplecharacteristics><width>1920</width><height>1080</height></samplecharacteristics></video><audio><channelcount>2</channelcount></audio></media></file>`; };
    let at = 0;
    const placed = clips.map((c, i) => { const s = src.get(c.file || c.name), len = c.srcOut - c.srcIn, p = { c, s, i, start: at, end: at + len, in: c.srcIn - s.start, out: c.srcOut - s.start }; at += len; return p; });
    const item = (p, kind, idx) => `<clipitem id="clipitem-${kind}${idx}-${p.i + 1}"><name>${x(p.c.name)}</name><duration>${p.s.end - p.s.start}</duration>${rate}<start>${p.start}</start><end>${p.end}</end><in>${p.in}</in><out>${p.out}</out>${file(p.s)}${kind === 'a' ? `<sourcetrack><mediatype>audio</mediatype><trackindex>${idx}</trackindex></sourcetrack>` : ''}${p.c.note && kind === 'v' ? `<comments><mastercomment1>${x(p.c.note)}</mastercomment1></comments>` : ''}</clipitem>`;
    const video = `<video><track>${placed.map(p => item(p, 'v', 1)).join('')}</track></video>`;
    const atracks = [];
    tracks.forEach(name => [1, 2].forEach(ch => atracks.push(`<track>${placed.filter(p => audio !== 'separate' || (str(p.c.track) || 'Audio') === name).map(p => item(p, 'a', ch)).join('')}</track>`)));
    return `${head}<!DOCTYPE xmeml>\n<xmeml version="4">\n<sequence id="sequence-1"><name>${x(title)}</name><duration>${at}</duration>${rate}${tcx(recStart)}<media>${video}<audio>${atracks.join('')}</audio></media></sequence>\n</xmeml>\n`;
  }

  // A CMX 3600 edit list. Separate audio puts each event's sound on its own line, on A for the first speaker,
  // A2 for the second, and so on up to A4.
  function edl({ title, fps, drop, clips, recStart = 0, audio = 'together' }) {
    const tracks = trackNames(clips);
    const lines = [`TITLE: ${str(title).replace(/[^\x20-\x7e]/g, '').slice(0, 70)}`, `FCM: ${drop && canDrop(fps) ? 'DROP FRAME' : 'NON-DROP FRAME'}`, ''];
    let at = recStart, n = 0;
    const ev = (reel, tr, c, rin) => `${String(++n).padStart(3, '0')}  ${reel.padEnd(8)} ${tr.padEnd(5)} C        ${tc(c.srcIn, fps, drop)} ${tc(c.srcOut, fps, drop)} ${tc(rin, fps, drop)} ${tc(rin + c.srcOut - c.srcIn, fps, drop)}`;
    for (const c of clips) {
      const reel = (str(c.reel) || 'AX').replace(/[^A-Za-z0-9_]/g, '').slice(0, 8) || 'AX';
      const k = Math.min(3, tracks.indexOf(str(c.track) || 'Audio'));
      const rows = audio === 'separate' ? [ev(reel, 'V', c, at), ev(reel, k ? `A${k + 1}` : 'A', c, at)] : [ev(reel, 'AA/V', c, at)];
      for (const r of rows) {
        lines.push(r);
        if (c.file || c.name) lines.push(`* FROM CLIP NAME: ${str(c.file || c.name).replace(/[^\x20-\x7e]/g, '')}`);
        if (c.note) lines.push(`* COMMENT: ${str(c.note).replace(/[^\x20-\x7e]/g, '').slice(0, 70)}`);
        lines.push('');
      }
      at += c.srcOut - c.srcIn;
    }
    return lines.join('\r\n');
  }

  // An Avid bin file: one row for each clip, with its source timecodes and any other columns.
  function ale({ fps, clips, columns = [] }) {
    const cols = ['Name', 'Tracks', 'Start', 'End', 'Tape', 'Source File', ...columns];
    const clean = v => str(v).replace(/[\t\r\n]+/g, ' ').trim();
    const rows = clips.map(c => [c.name, c.tracks || 'VA1A2', tc(c.start, fps, c.drop), tc(c.end, fps, c.drop), c.tape, c.file, ...columns.map(k => (c.extra || {})[k])].map(clean).join('\t'));
    return ['Heading', 'FIELD_DELIM\tTABS', 'VIDEO_FORMAT\t1080', 'AUDIO_FORMAT\t48khz', `FPS\t${str(fps)}`, '', 'Column', cols.join('\t'), '', 'Data', ...rows, ''].join('\r\n');
  }

  // Markers: [{ at (frames), len, text, color, user }]. Resolve reads them as an EDL; Avid as tab-separated text.
  const RESOLVE = { red: 'Red', yellow: 'Yellow', blue: 'Blue', green: 'Green', cyan: 'Cyan', purple: 'Purple' };
  function resolveMarkers({ title, fps, drop, markers }) {
    const lines = [`TITLE: ${str(title).replace(/[^\x20-\x7e]/g, '').slice(0, 70)}`, `FCM: ${drop && canDrop(fps) ? 'DROP FRAME' : 'NON-DROP FRAME'}`, ''];
    markers.forEach((m, i) => {
      const a = tc(m.at, fps, drop), b = tc(m.at + 1, fps, drop);
      lines.push(`${String(i + 1).padStart(3, '0')}  001      V     C        ${a} ${b} ${a} ${b}  `);
      lines.push(` |C:ResolveColor${RESOLVE[m.color] || 'Blue'} |M:${str(m.text).replace(/[|\r\n]+/g, ' ').trim()} |D:${Math.max(1, m.len || 1)}`);
      lines.push('');
    });
    return lines.join('\r\n');
  }
  function avidMarkers({ fps, drop, markers }) {
    return markers.map(m => [str(m.user) || 'QC', tc(m.at, fps, drop), 'V1', m.color || 'red', str(m.text).replace(/[\t\r\n]+/g, ' ').trim(), Math.max(1, m.len || 1)].join('\t')).join('\n') + '\n';
  }

  // Titles for supers: each { at, len, lines: [name, title] } becomes a Basic Title clip connected above an
  // empty timeline, which Final Cut Pro and Resolve keep as editable text.
  function fcpxmlTitles({ title, fps, drop, recStart = 0, titles }) {
    const fmt = drop && canDrop(fps) ? 'DF' : 'NDF';
    const end = Math.max(1, ...titles.map(s => s.at + s.len)) - recStart;
    const effect = '<effect id="r2" name="Basic Title" uid=".../Titles.localized/Bumper:Opener.localized/Basic Title.localized/Basic Title.moti"/>';
    const clips = titles.map((s, i) => `<title ref="r2" lane="1" offset="${t(s.at, fps)}" name="${x(s.lines[0])}" start="0s" duration="${t(s.len, fps)}"><text><text-style ref="ts${i + 1}">${x(s.lines.filter(Boolean).join('\n'))}</text-style></text><text-style-def id="ts${i + 1}"><text-style font="Helvetica" fontSize="60" fontColor="1 1 1 1" alignment="left"/></text-style-def></title>`);
    return `${head}<!DOCTYPE fcpxml>\n<fcpxml version="1.9">\n<resources>\n<format id="r1" frameDuration="${frameDuration(fps)}" width="1920" height="1080"/>\n${effect}\n</resources>\n<library>\n<event name="${x(title)}">\n<project name="${x(title)}">\n<sequence format="r1" tcStart="${t(recStart, fps)}" tcFormat="${fmt}" duration="${t(end, fps)}">\n<spine>\n<gap name="Supers" offset="${t(recStart, fps)}" start="${t(recStart, fps)}" duration="${t(end, fps)}">\n${clips.join('\n')}\n</gap>\n</spine>\n</sequence>\n</project>\n</event>\n</library>\n</fcpxml>\n`;
  }
  // Subtitles: SRT and WebVTT, which most editing and titling apps read as timed text.
  function srt(items, fps, recStart = 0) {
    const s = n => { const ms = Math.max(0, Math.round(((n - recStart) * rateOf(fps)[1] / rateOf(fps)[0]) * 1000)); return `${String(Math.floor(ms / 3600000)).padStart(2, '0')}:${String(Math.floor(ms / 60000) % 60).padStart(2, '0')}:${String(Math.floor(ms / 1000) % 60).padStart(2, '0')},${String(ms % 1000).padStart(3, '0')}`; };
    return items.map((it, i) => `${i + 1}\r\n${s(it.at)} --> ${s(it.at + it.len)}\r\n${it.lines.filter(Boolean).join('\r\n')}\r\n`).join('\r\n');
  }
  function vtt(items, fps, recStart = 0) {
    return 'WEBVTT\r\n\r\n' + srt(items, fps, recStart).replace(/(\d\d:\d\d:\d\d),(\d\d\d)/g, '$1.$2').replace(/^\d+\r\n(?=\d\d:)/gm, '');
  }
  return { RATES, frames, tc, canDrop, base, fcpxml, xmeml, edl, ale, resolveMarkers, avidMarkers, fcpxmlTitles, srt, vtt };
})();

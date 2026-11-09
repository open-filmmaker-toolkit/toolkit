// Word and PowerPoint files, written in the browser with no libraries: the Office Open XML parts, zipped by
// shared/zip.js. Keynote, Pages, Google Slides and Docs, and LibreOffice open them too.
// oftOffice.docx(blocks, { title }) and oftOffice.pptx(slides, { title, size, colors, fonts }) return Blobs.
// A block is { type: 'title' | 'h1' | 'h2' | 'p' | 'small' | 'list' | 'table', text, items, head, rows, widths }.
// A slide is { title, lines, kind: 'title' | 'text' | 'grid' | 'full' | 'split', left, images: [{ data, w, h, alt }], note }.
const oftOffice = (() => {
  const str = v => (v == null ? '' : String(v));
  // XML text: escaped, and without the control characters XML can't hold.
  const x = s => str(s).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const XML = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n';
  const NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships';
  const REL = t => `http://schemas.openxmlformats.org/officeDocument/2006/relationships/${t}`;
  const rels = list => `${XML}<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${list.map(([id, type, target]) => `<Relationship Id="${id}" Type="${type.startsWith('http') ? type : REL(type)}" Target="${x(target)}"/>`).join('')}</Relationships>`;
  const core = title => `${XML}<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${x(title)}</dc:title><dc:creator>Open Filmmaker Toolkit</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}</dcterms:created></cp:coreProperties>`;
  const app = name => `${XML}<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>${x(name)}</Application></Properties>`;
  const pkgRels = main => rels([['rId1', 'officeDocument', main], ['rId2', 'http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties', 'docProps/core.xml'], ['rId3', 'extended-properties', 'docProps/app.xml']]);
  const types = (overrides, images) => `${XML}<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>${images ? '<Default Extension="jpeg" ContentType="image/jpeg"/><Default Extension="png" ContentType="image/png"/><Default Extension="gif" ContentType="image/gif"/>' : ''}${overrides.map(([p, t]) => `<Override PartName="${p}" ContentType="${t}"/>`).join('')}<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>`;
  const hex = c => (/^#?[0-9a-f]{6}$/i.test(str(c)) ? str(c).replace('#', '').toUpperCase() : null);

  // ---------- Word ----------
  const W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="' + NS_R + '"';
  const run = (t, props = '') => str(t).split('\n').map((line, i) => `${i ? '<w:r><w:br/></w:r>' : ''}<w:r>${props ? `<w:rPr>${props}</w:rPr>` : ''}<w:t xml:space="preserve">${x(line)}</w:t></w:r>`).join('');
  const para = (t, style, props) => `<w:p>${style ? `<w:pPr><w:pStyle w:val="${style}"/></w:pPr>` : ''}${run(t, props)}</w:p>`;
  function table(b) {
    const cols = Math.max(1, ...[b.head || [], ...(b.rows || [])].map(r => r.length));
    const total = 9360, widths = b.widths && b.widths.length === cols ? b.widths.map(w => Math.round(total * w / b.widths.reduce((a, c) => a + c, 0))) : Array(cols).fill(Math.round(total / cols));
    const border = '<w:top w:val="single" w:sz="4" w:color="999999"/><w:left w:val="single" w:sz="4" w:color="999999"/><w:bottom w:val="single" w:sz="4" w:color="999999"/><w:right w:val="single" w:sz="4" w:color="999999"/><w:insideH w:val="single" w:sz="4" w:color="999999"/><w:insideV w:val="single" w:sz="4" w:color="999999"/>';
    const cell = (v, i, headRow) => `<w:tc><w:tcPr><w:tcW w:w="${widths[i]}" w:type="dxa"/>${headRow ? '<w:shd w:val="clear" w:color="auto" w:fill="EEEEEE"/>' : ''}</w:tcPr><w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>${run(v, headRow ? '<w:b/>' : '')}</w:p></w:tc>`;
    const row = (r, headRow) => `<w:tr>${headRow ? '<w:trPr><w:tblHeader/></w:trPr>' : ''}${Array.from({ length: cols }, (_, i) => cell(r[i], i, headRow)).join('')}</w:tr>`;
    return `<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/><w:tblBorders>${border}</w:tblBorders><w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>${widths.map(w => `<w:gridCol w:w="${w}"/>`).join('')}</w:tblGrid>${b.head ? row(b.head, true) : ''}${(b.rows || []).map(r => row(r, false)).join('')}</w:tbl><w:p/>`;
  }
  function docx(blocks, { title = 'Document' } = {}) {
    const body = blocks.map(b => {
      if (b.type === 'title') return para(b.text, 'Title');
      if (b.type === 'h1') return para(b.text, 'Heading1');
      if (b.type === 'h2') return para(b.text, 'Heading2');
      if (b.type === 'small') return para(b.text, 'Small');
      if (b.type === 'list') return (b.items || []).map(t => `<w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr>${run(`• ${str(t)}`)}</w:p>`).join('');
      if (b.type === 'table') return table(b);
      return para(b.text);
    }).join('');
    const doc = `${XML}<w:document ${W}><w:body>${body}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>`;
    const style = (id, name, ppr, rpr, extra = '') => `<w:style w:type="paragraph"${id === 'Normal' ? ' w:default="1"' : ''} w:styleId="${id}"><w:name w:val="${name}"/>${id === 'Normal' ? '' : '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'}${extra}<w:qFormat/>${ppr ? `<w:pPr>${ppr}</w:pPr>` : ''}${rpr ? `<w:rPr>${rpr}</w:rPr>` : ''}</w:style>`;
    const styles = `${XML}<w:styles ${W}><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
${style('Normal', 'Normal')}${style('Title', 'Title', '<w:spacing w:after="200"/>', '<w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:sz w:val="48"/><w:szCs w:val="48"/>')}${style('Heading1', 'heading 1', '<w:keepNext/><w:spacing w:before="280" w:after="100"/><w:outlineLvl w:val="0"/>', '<w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:b/><w:sz w:val="30"/><w:szCs w:val="30"/>')}${style('Heading2', 'heading 2', '<w:keepNext/><w:spacing w:before="200" w:after="80"/><w:outlineLvl w:val="1"/>', '<w:b/><w:sz w:val="24"/><w:szCs w:val="24"/>')}${style('Small', 'Small text', '', '<w:color w:val="555555"/><w:sz w:val="18"/><w:szCs w:val="18"/>')}${style('ListBullet', 'List Bullet', '<w:spacing w:after="60"/><w:ind w:left="360" w:hanging="200"/>')}</w:styles>`;
    return oftZip.make([
      { name: '[Content_Types].xml', data: types([['/word/document.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'], ['/word/styles.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml']]) },
      { name: '_rels/.rels', data: pkgRels('word/document.xml') },
      { name: 'docProps/core.xml', data: core(title) }, { name: 'docProps/app.xml', data: app('Open Filmmaker Toolkit') },
      { name: 'word/_rels/document.xml.rels', data: rels([['rId1', 'styles', 'styles.xml']]) },
      { name: 'word/document.xml', data: doc }, { name: 'word/styles.xml', data: styles },
    ]);
  }

  // ---------- PowerPoint ----------
  const P = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="' + NS_R + '" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"';
  const EMU = 914400;
  const SIZE = { widescreen: [12192000, 6858000], letter: [10058400, 7772400] };
  const group = '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>';
  const theme = (c, f) => `${XML}<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Toolkit"><a:themeElements><a:clrScheme name="Toolkit"><a:dk1><a:srgbClr val="${c.ink}"/></a:dk1><a:lt1><a:srgbClr val="${c.bg}"/></a:lt1><a:dk2><a:srgbClr val="${c.dark}"/></a:dk2><a:lt2><a:srgbClr val="EEEEEE"/></a:lt2><a:accent1><a:srgbClr val="${c.accent}"/></a:accent1><a:accent2><a:srgbClr val="4472C4"/></a:accent2><a:accent3><a:srgbClr val="A5A5A5"/></a:accent3><a:accent4><a:srgbClr val="FFC000"/></a:accent4><a:accent5><a:srgbClr val="5B9BD5"/></a:accent5><a:accent6><a:srgbClr val="70AD47"/></a:accent6><a:hlink><a:srgbClr val="0563C1"/></a:hlink><a:folHlink><a:srgbClr val="954F72"/></a:folHlink></a:clrScheme><a:fontScheme name="Toolkit"><a:majorFont><a:latin typeface="${x(f.head)}"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="${x(f.text)}"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="Toolkit"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>`;
  function textBox(id, name, [l, t, w, h], paras, { anchor = 't', align = 'l' } = {}) {
    const ps = paras.map(p => `<a:p><a:pPr algn="${p.align || align}"><a:spcAft><a:spcPts val="${p.after == null ? 600 : p.after}"/></a:spcAft></a:pPr><a:r><a:rPr lang="en-US" sz="${p.size}" dirty="0"${p.bold ? ' b="1"' : ''}><a:solidFill><a:srgbClr val="${p.color}"/></a:solidFill><a:latin typeface="${x(p.font)}"/></a:rPr><a:t>${x(p.text)}</a:t></a:r></a:p>`).join('') || '<a:p><a:endParaRPr lang="en-US"/></a:p>';
    return `<p:sp><p:nvSpPr><p:cNvPr id="${id}" name="${x(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="${Math.round(l)}" y="${Math.round(t)}"/><a:ext cx="${Math.round(w)}" cy="${Math.round(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="${anchor}"><a:normAutofit/></a:bodyPr><a:lstStyle/>${ps}</p:txBody></p:sp>`;
  }
  // A picture that fills its box, cropped to keep its shape, like CSS object-fit: cover.
  function picture(id, rid, img, [l, t, w, h], dim) {
    const ir = img.w && img.h ? img.w / img.h : w / h, br = w / h;
    let crop = '';
    if (ir > br) { const c = Math.round((1 - br / ir) / 2 * 100000); crop = `<a:srcRect l="${c}" r="${c}"/>`; }
    else if (ir < br) { const c = Math.round((1 - ir / br) / 2 * 100000); crop = `<a:srcRect t="${c}" b="${c}"/>`; }
    return `<p:pic><p:nvPicPr><p:cNvPr id="${id}" name="Picture ${id}" descr="${x(img.alt)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="${rid}">${dim ? '<a:lum bright="-30000"/>' : ''}</a:blip>${crop}<a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="${Math.round(l)}" y="${Math.round(t)}"/><a:ext cx="${Math.round(w)}" cy="${Math.round(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>`;
  }
  const imgExt = d => (d[0] === 0x89 && d[1] === 0x50 ? 'png' : d[0] === 0x47 && d[1] === 0x49 ? 'gif' : 'jpeg');
  function pptx(slides, { title = 'Presentation', size = 'widescreen', colors = {}, fonts = {} } = {}) {
    const [W0, H0] = SIZE[size] || SIZE.widescreen;
    const c = { bg: hex(colors.bg) || 'FFFFFF', ink: hex(colors.ink) || '222222', accent: hex(colors.accent) || '2F6F5E', dark: hex(colors.dark) || '1F2421', darkInk: hex(colors.darkInk) || 'FFFFFF', muted: hex(colors.muted) || '666666' };
    const f = { head: fonts.head || 'Georgia', text: fonts.text || 'Calibri' };
    const files = [], media = [];
    const m = W0 * 0.06;
    slides.forEach((s, k) => {
      const n = k + 1, shapes = [], srels = [['rId1', 'slideLayout', '../slideLayouts/slideLayout1.xml']];
      let id = 2;
      const addImg = (img, box, dim) => {
        if (!img || !img.data) return;
        const name = `image${media.length + 1}.${imgExt(img.data)}`;
        media.push({ name: `ppt/media/${name}`, data: img.data });
        const rid = `rId${srels.length + 1}`;
        srels.push([rid, 'image', `../media/${name}`]);
        shapes.push(picture(id++, rid, img, box, dim));
      };
      const head = (t, color, sz = 3200) => ({ text: t, size: sz, bold: true, color, font: f.head, after: 900 });
      const lines = (arr, color, sz = 2400) => arr.filter(t => str(t).trim()).map(t => ({ text: t, size: sz, color, font: f.text }));
      const imgs = s.images || [];
      let bg = c.bg, ink = c.ink;
      if (s.kind === 'title') {
        if (imgs[0]) { addImg(imgs[0], [0, 0, W0, H0], true); ink = 'FFFFFF'; }
        shapes.push(textBox(id++, 'Title', [m, H0 * 0.55, W0 - 2 * m, H0 * 0.38], [head(s.title, ink, 5400), ...lines(s.lines || [], ink, 2200)], { anchor: 'b' }));
      } else if (s.kind === 'full') {
        addImg(imgs[0], [0, 0, W0, H0]);
        if ((s.lines || []).length) shapes.push(textBox(id++, 'Caption', [m, H0 * 0.84, W0 - 2 * m, H0 * 0.12], lines(s.lines, 'FFFFFF', 1800), { anchor: 'b' }));
      } else if (s.kind === 'grid') {
        shapes.push(textBox(id++, 'Title', [m, m * 0.8, W0 - 2 * m, H0 * 0.14], [head(s.title, ink)]));
        const shown = imgs.slice(0, 6), cols = shown.length <= 2 ? Math.max(shown.length, 1) : 3, rows = Math.ceil(shown.length / cols) || 1, gap = W0 * 0.012;
        const top = H0 * 0.24, avail = H0 * ((s.lines || []).length ? 0.56 : 0.68), cw = (W0 - 2 * m - gap * (cols - 1)) / cols, ch = (avail - gap * (rows - 1)) / rows;
        shown.forEach((img, i) => addImg(img, [m + (i % cols) * (cw + gap), top + Math.floor(i / cols) * (ch + gap), cw, ch]));
        if ((s.lines || []).length) shapes.push(textBox(id++, 'Text', [m, top + avail + gap * 2, W0 - 2 * m, H0 - top - avail - m], lines(s.lines, ink, 1800)));
      } else if (s.kind === 'split' && imgs[0]) {
        const half = W0 / 2;
        addImg(imgs[0], [s.left ? 0 : half, 0, half, H0]);
        const x0 = s.left ? half + m : m;
        shapes.push(textBox(id++, 'Title', [x0, m, half - 2 * m, H0 * 0.18], [head(s.title, ink)]));
        shapes.push(textBox(id++, 'Text', [x0, m + H0 * 0.2, half - 2 * m, H0 - 2 * m - H0 * 0.2], lines(s.lines || [], ink)));
      } else {
        shapes.push(textBox(id++, 'Title', [m, m, W0 - 2 * m, H0 * 0.18], [head(s.title, ink)]));
        shapes.push(textBox(id++, 'Text', [m, m + H0 * 0.2, W0 - 2 * m, H0 - 2 * m - H0 * 0.2], lines(s.lines || [], ink)));
      }
      if (s.note) shapes.push(textBox(id++, 'Note', [m, H0 - m * 0.9, W0 - 2 * m, m * 0.6], [{ text: s.note, size: 1100, color: c.muted, font: f.text }], { anchor: 'b' }));
      files.push({ name: `ppt/slides/slide${n}.xml`, data: `${XML}<p:sld ${P}><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="${bg}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg><p:spTree>${group}${shapes.join('')}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>` });
      files.push({ name: `ppt/slides/_rels/slide${n}.xml.rels`, data: rels(srels) });
    });
    const presentation = `${XML}<p:presentation ${P} saveSubsetFonts="1"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>${slides.map((_, k) => `<p:sldId id="${256 + k}" r:id="rId${k + 3}"/>`).join('')}</p:sldIdLst><p:sldSz cx="${W0}" cy="${H0}"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>`;
    const master = `${XML}<p:sldMaster ${P}><p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg><p:spTree>${group}</p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>`;
    const layout = `${XML}<p:sldLayout ${P} type="blank" preserve="1"><p:cSld name="Blank"><p:spTree>${group}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>`;
    const PT = 'application/vnd.openxmlformats-officedocument.presentationml.';
    return oftZip.make([
      { name: '[Content_Types].xml', data: types([['/ppt/presentation.xml', PT + 'presentation.main+xml'], ['/ppt/slideMasters/slideMaster1.xml', PT + 'slideMaster+xml'], ['/ppt/slideLayouts/slideLayout1.xml', PT + 'slideLayout+xml'], ['/ppt/theme/theme1.xml', 'application/vnd.openxmlformats-officedocument.theme+xml'], ...slides.map((_, k) => [`/ppt/slides/slide${k + 1}.xml`, PT + 'slide+xml'])], true) },
      { name: '_rels/.rels', data: pkgRels('ppt/presentation.xml') },
      { name: 'docProps/core.xml', data: core(title) }, { name: 'docProps/app.xml', data: app('Open Filmmaker Toolkit') },
      { name: 'ppt/presentation.xml', data: presentation },
      { name: 'ppt/_rels/presentation.xml.rels', data: rels([['rId1', 'slideMaster', 'slideMasters/slideMaster1.xml'], ['rId2', 'theme', 'theme/theme1.xml'], ...slides.map((_, k) => [`rId${k + 3}`, 'slide', `slides/slide${k + 1}.xml`])]) },
      { name: 'ppt/slideMasters/slideMaster1.xml', data: master },
      { name: 'ppt/slideMasters/_rels/slideMaster1.xml.rels', data: rels([['rId1', 'slideLayout', '../slideLayouts/slideLayout1.xml'], ['rId2', 'theme', '../theme/theme1.xml']]) },
      { name: 'ppt/slideLayouts/slideLayout1.xml', data: layout },
      { name: 'ppt/slideLayouts/_rels/slideLayout1.xml.rels', data: rels([['rId1', 'slideMaster', '../slideMasters/slideMaster1.xml']]) },
      { name: 'ppt/theme/theme1.xml', data: theme(c, f) },
      ...files, ...media,
    ]);
  }
  // Bytes from a data: URL, for images kept in the project file.
  function dataBytes(url) {
    const m = /^data:[^;,]*(;base64)?,(.*)$/s.exec(str(url));
    if (!m) return null;
    if (!m[1]) return new TextEncoder().encode(decodeURIComponent(m[2]));
    const b = atob(m[2]), out = new Uint8Array(b.length);
    for (let i = 0; i < b.length; i++) out[i] = b.charCodeAt(i);
    return out;
  }
  // Blocks from a printed page in the tool: headings, paragraphs, lists and tables, in order. Anything hidden
  // from print, and pictures, are left out.
  function blocksFrom(root) {
    const out = [];
    // Text with line breaks where the page has them, whether or not the page is showing.
    const flat = n => n.nodeType === 3 ? n.nodeValue.replace(/\s+/g, ' ') : n.nodeType !== 1 ? '' : n.tagName === 'BR' ? '\n'
      : (n.tagName === 'SPAN' ? ' ' : '') + [...n.childNodes].map(flat).join('') + (/^(DIV|P|LI|TR|H[1-6])$/.test(n.tagName) ? '\n' : /^(TD|TH|SPAN)$/.test(n.tagName) ? ' ' : '');
    const text = el => flat(el).replace(/ {2,}/g, ' ').replace(/ *\n */g, '\n').replace(/\n{3,}/g, '\n\n').trim();
    const walk = el => {
      for (const n of el.children) {
        if (n.hidden || n.getAttribute('aria-hidden') === 'true' && n !== root) continue;
        const tag = n.tagName.toLowerCase();
        if (tag === 'h1') out.push({ type: out.some(b => b.type === 'title') ? 'h1' : 'title', text: text(n) });
        else if (tag === 'h2') out.push({ type: 'h1', text: text(n) });
        else if (/^h[3-6]$/.test(tag)) out.push({ type: 'h2', text: text(n) });
        else if (tag === 'p') { const t = text(n); if (t) out.push({ type: /note|meta|legal|small|sub/.test(n.className) ? 'small' : 'p', text: t }); }
        else if (tag === 'ul' || tag === 'ol') out.push({ type: 'list', items: [...n.children].map(text).filter(Boolean) });
        else if (tag === 'table') {
          const rows = [...n.querySelectorAll('tr')].map(tr => [...tr.children].map(text));
          const head = n.querySelector('thead tr') ? rows.shift() : null;
          if (rows.length || head) out.push({ type: 'table', head, rows });
        } else if (tag === 'dl') out.push({ type: 'table', rows: [...n.querySelectorAll('dt')].map(dt => [text(dt), dt.nextElementSibling ? text(dt.nextElementSibling) : '']) });
        else if (['img', 'svg', 'canvas', 'script', 'style', 'figure', 'button'].includes(tag)) continue;
        else if (n.children.length) walk(n);
        else { const t = text(n); if (t) out.push({ type: 'p', text: t }); }
      }
    };
    walk(root);
    return out;
  }
  return { docx, pptx, dataBytes, blocksFrom, EMU };
})();

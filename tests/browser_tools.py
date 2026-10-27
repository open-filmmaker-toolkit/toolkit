"""Real-browser checks for every tool.

Run: pip install playwright pypdf && playwright install chromium
     python tests/browser_tools.py [chromium|chromium-fallback|firefox|webkit]   (default: chromium)

CI runs chromium and chromium-fallback. chromium-fallback is Chromium with the file
picker API removed, so it takes the download/upload path Firefox and Safari use.
Firefox and WebKit still work locally (playwright install firefox webkit).

Checks, per tool: opening the sample, saving, all CSV exports, phone width, dark
mode and print layout. Chromium also covers the save-conflict warning (it has the
file picker API; its handles are faked in memory) and renders a real PDF.
chromium-fallback, Firefox and WebKit (Safari's engine) use the download/upload fallback instead.
The call sheet, release tracker, credits builder, name supers list, subject tracker, research and archival log, comps tracker, treatment builder and pitch deck builder also get end-to-end checks
of their own, and the spreadsheet templates are checked against the tools' exports.
"""
import csv, io, json, os, pathlib, sys
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parents[1]
sample = (root / 'samples/the-river-keeps.oft.json').read_text()
TOOLS = ['clearance-log', 'music-cue-sheet', 'call-sheet', 'release-tracker', 'credits-builder', 'name-supers', 'subject-tracker', 'research-log', 'comps-tracker', 'treatment-builder', 'pitch-deck']
COLLECTIONS = ['project', 'people', 'locations', 'thirdPartyElements', 'contracts', 'assets', 'musicCueSheet', 'callSheets']
PRINT_BTN = {'clearance-log': '#printBtn', 'music-cue-sheet': '#printBtn', 'call-sheet': '#printAllBtn', 'release-tracker': '#printBtn',
             'credits-builder': '#printBtn', 'name-supers': '#printBtn', 'subject-tracker': '#printBtn', 'research-log': '#printBtn', 'comps-tracker': '#printBtn', 'treatment-builder': '#printBtn', 'pitch-deck': '#printBtn'}
PHONE = {'width': 390, 'height': 844}
# The button that opens each tool's main dialog, for the phone-width check. Most tools use #addBtn.
DIALOG_BTN = {'treatment-builder': '[data-compare]'}

STUB_PRINT = 'window.print = () => { window.__printed = true; };'
NO_PICKERS = 'delete window.showOpenFilePicker; delete window.showSaveFilePicker; delete window.showDirectoryPicker;'
FALLBACK = False
FAKE_PICKERS = """
window.__file = {name:'proj.oft.json', text: %s};
window.__writes = 0;
const mk = () => ({name: window.__file.name,
  getFile: async () => ({text: async () => window.__file.text, name: window.__file.name}),
  createWritable: async () => { let buf=''; return {write: async d => {buf += d;}, close: async () => {window.__file.text = buf; window.__writes++;}}; },
  queryPermission: async()=>'granted', requestPermission: async()=>'granted'});
window.showOpenFilePicker = async () => [mk()];
window.showSaveFilePicker = async () => mk();
""" % json.dumps(sample)

fails = []
def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok:
        fails.append(msg)

def luminance(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(rgb[0]) + 0.7152 * ch(rgb[1]) + 0.0722 * ch(rgb[2])

def contrast(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)

# Resolves real text and background colors, walking up through transparent layers.
COLORS_JS = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const rgb = v => { c.clearRect(0,0,1,1); c.fillStyle = '#000'; c.fillStyle = v; c.fillRect(0,0,1,1); const d = c.getImageData(0,0,1,1).data; return [d[0],d[1],d[2],d[3]/255]; };
  const bg = el => { for (let e = el; e; e = e.parentElement) { const v = rgb(getComputedStyle(e).backgroundColor); if (v[3] > 0.99) return v.slice(0,3); } return [255,255,255]; };
  const pairs = {};
  for (const [k, sel] of Object.entries({page: 'body', heading: 'h1', button: '.btn:not(.primary):not(.danger)', primary: '.btn.primary'})) {
    const el = document.querySelector(sel);
    if (el && (sel === 'body' || el.offsetParent !== null)) pairs[k] = [rgb(getComputedStyle(el).color).slice(0,3), bg(el)];
  }
  return pairs;
}"""

def new_page(browser, name, fake, extra='', **ctx):
    context = browser.new_context(accept_downloads=True, **ctx)
    page = context.new_page()
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.add_init_script(STUB_PRINT + (NO_PICKERS if FALLBACK else '') + (FAKE_PICKERS if fake else '') + extra)
    page.goto('file://%s/tools/%s/index.html' % (root, name))
    page.wait_for_load_state('networkidle')
    return context, page, errs

def open_sample(page, fake):
    if fake:
        page.click('#openBtn')
    else:
        page.set_input_files('#fileInput', files=[{'name': 'proj.oft.json', 'mimeType': 'application/json', 'buffer': sample.encode()}])
    page.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")

def horizontal_overflow(page):
    return page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')

def test_core(browser, name, fake):
    ctx, pg, errs = new_page(browser, name, fake)
    open_sample(pg, fake)
    check('River' in pg.inner_text('#filmTitle'), 'sample opens')
    for col in COLLECTIONS:
        pg.click('#projectCsvBtn')
        pg.select_option('#projectCsvCollection', col)
        with pg.expect_download() as d:
            pg.click('#projectCsvForm button[type=submit]')
        text = open(d.value.path(), encoding='utf-8-sig').read()
        check(d.value.suggested_filename.endswith('-%s.csv' % col) and len(list(csv.reader(io.StringIO(text)))) >= 1, 'csv export %s' % col)
    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        check(pg.evaluate('window.__writes') == 1 and not pg.is_visible('#conflictDialog'), 'clean save writes, no conflict')
        ext = json.loads(pg.evaluate('window.__file.text')); ext['project']['title'] = 'CHANGED EXTERNALLY'
        pg.evaluate('t => window.__file.text = t', json.dumps(ext))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        check(pg.is_visible('#conflictDialog') and 'CHANGED EXTERNALLY' in pg.evaluate('window.__file.text'), 'conflict warns and leaves the file alone')
        pg.click('#conflictCancelBtn')
        check(not pg.is_visible('#conflictDialog'), 'keep editing closes the dialog')
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        writes = pg.evaluate('window.__writes')
        pg.click('#conflictOverwriteBtn'); pg.wait_for_timeout(300)
        check(pg.evaluate('window.__writes') == writes + 1 and 'CHANGED EXTERNALLY' not in pg.evaluate('window.__file.text'), 'overwrite replaces the file')
        pg.evaluate('t => window.__file.text = t', json.dumps(ext))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        pg.click('#conflictReloadBtn'); pg.wait_for_timeout(300)
        check('CHANGED EXTERNALLY' in pg.content(), 'reload latest shows the newer file')
        pg.evaluate('t => window.__file.text = t', json.dumps(dict(ext, project=dict(ext['project'], title='AGAIN'))))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        with pg.expect_download() as d:
            pg.click('#conflictCopyBtn')
        check(d.value.suggested_filename.endswith('.json'), 'save a copy downloads')
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        saved = json.loads(open(d.value.path(), encoding='utf-8').read())
        check(saved.get('project', {}).get('title') == 'The River Keeps', 'save downloads the project file')
        pg.set_input_files('#fileInput', files=[{'name': 'again.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(saved).encode()}])
        pg.wait_for_timeout(300)
        check('River' in pg.inner_text('#filmTitle'), 'saved file reopens')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_phone(browser, name, fake):
    ctx, pg, errs = new_page(browser, name, fake, viewport=PHONE)
    check(horizontal_overflow(pg) <= 1, 'phone: empty state does not scroll sideways')
    open_sample(pg, fake)
    check(horizontal_overflow(pg) <= 1, 'phone: loaded project does not scroll sideways (%spx over)' % horizontal_overflow(pg))
    for sel in ['#saveBtn', '#openBtn']:
        box = pg.locator(sel).bounding_box()
        check(box is not None and box['x'] >= 0 and box['x'] + box['width'] <= PHONE['width'] + 1, 'phone: %s fits on screen' % sel)
    pg.locator(DIALOG_BTN.get(name, '#addBtn')).first.click(); pg.wait_for_timeout(300)
    box = pg.locator('dialog[open]').first.bounding_box()
    check(box is not None and box['x'] >= 0 and box['x'] + box['width'] <= PHONE['width'] + 1, 'phone: editor fits on screen')
    check(horizontal_overflow(pg) <= 1, 'phone: editor does not scroll the page sideways')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_dark(browser, name, fake):
    for scheme in ['light', 'dark']:
        ctx, pg, errs = new_page(browser, name, fake, color_scheme=scheme)
        open_sample(pg, fake)
        pairs = pg.evaluate(COLORS_JS)
        page_bg = pairs['page'][1]
        if scheme == 'dark':
            check(luminance(page_bg) < 0.2, 'dark mode: page background is dark %s' % page_bg)
        else:
            check(luminance(page_bg) > 0.6, 'light mode: page background is light %s' % page_bg)
        for k, (fg, bg) in pairs.items():
            ratio = contrast(fg, bg)
            check(ratio >= 4.5, '%s mode: %s text contrast %.1f:1' % (scheme, k, ratio))
        ctx.close()

def test_print(browser, name, fake, can_pdf):
    ctx, pg, errs = new_page(browser, name, fake)
    open_sample(pg, fake)
    pg.click(PRINT_BTN[name]); pg.wait_for_timeout(300)
    check(pg.evaluate('window.__printed === true'), 'print dialog is requested')
    pg.emulate_media(media='print')
    check(pg.is_visible('#report') and not pg.is_visible('.page'), 'print view shows only the report')
    check('The River Keeps' in pg.inner_text('#report'), 'report names the film')
    if can_pdf:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pg.pdf(prefer_css_page_size=True)))
        pdf_text = ' '.join(p.extract_text() or '' for p in reader.pages)
        check(len(reader.pages) >= 1 and 'The River Keeps' in pdf_text, 'PDF renders %d page(s) with the film title' % len(reader.pages))
        if name == 'call-sheet':
            days = len(json.loads(sample)['callSheets'])
            check(len(reader.pages) == days, 'PDF has one page per shoot day (%d)' % days)
            check('General call' in pdf_text and '7:00' in pdf_text, 'PDF has the call time')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_call_sheet_export(browser, fake):
    ctx, pg, errs = new_page(browser, 'call-sheet', fake)
    open_sample(pg, fake)
    with pg.expect_download() as d:
        pg.click('#sheetCsvBtn')
    txt = open(d.value.path(), encoding='utf-8-sig').read()
    check(txt.startswith('CALL SHEET') and 'CREW AND CAST' in txt, 'all-days spreadsheet export')
    template = (root / 'templates/call-sheet-template.csv').read_text()
    keep = ('CALL SHEET', 'SCHEDULE', 'CREW AND CAST', 'NOTES', 'Film', 'General call', 'Nearest hospital', 'Time', 'Name', 'Prepared by')
    skeleton = lambda t: [r[0] for r in csv.reader(io.StringIO(t)) if r and r[0] in keep]
    check(skeleton(template) == skeleton(txt), 'export layout matches the blank template')
    pg.locator('[data-id]').first.click(); pg.wait_for_timeout(200)
    with pg.expect_download() as d:
        pg.click('#sheetCsvDayBtn')
    check('-call-sheet-' in d.value.suggested_filename, 'single-day spreadsheet export')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

# A project folder in memory, for the release tracker's "Connect project folder" (Chromium only).
FAKE_DIR = """
window.__dir = {'proj.oft.json': ''};
const fsFile = path => ({name: path.split('/').pop(), isSameEntry: async () => true,
  getFile: async () => new File([window.__dir[path]], path.split('/').pop()),
  createWritable: async () => { const parts = []; return {write: async d => { parts.push(d); }, close: async () => { window.__dir[path] = await new Blob(parts).text(); }}; }});
const fsDir = (prefix, name) => ({name,
  getDirectoryHandle: async n => fsDir(prefix + n + '/', n),
  getFileHandle: async (n, o) => { const path = prefix + n; if (!(path in window.__dir)) { if (o && o.create) window.__dir[path] = ''; else throw new DOMException('Not found', 'NotFoundError'); } return fsFile(path); }});
window.showDirectoryPicker = async () => fsDir('', 'River Keeps');
"""

def test_release_tracker(browser, fake):
    ctx, pg, errs = new_page(browser, 'release-tracker', fake, extra=FAKE_DIR if fake else '')
    open_sample(pg, fake)
    check(pg.inner_text('#covHeadline') == '2 of 7 covered', 'coverage counts the sample (%s)' % pg.inner_text('#covHeadline'))
    missing = pg.locator('.cov-line.is-missing').all_inner_texts()
    check(any('Marcus Bell' in t for t in missing) and any('Riverside levee' in t for t in missing), 'flags a person and a location with no release on file')
    check('Riverside levee' in pg.inner_text('#placesCov'), 'a location on a call sheet counts as filmed')

    # Start a release from a flagged person, sign it and attach a scan.
    pg.click('#peopleCov .is-missing:has-text("Marcus Bell") .cov-sig')
    check(pg.is_visible('#editor') and pg.input_value('#f-type') == 'appearance release', 'flagged person opens a new appearance release')
    check(pg.eval_on_selector_all('#peopleList input:checked', 'els => els.map(e => e.value)') == ['person-marcus-bell'], 'the flagged person is already checked')
    pg.select_option('#f-status', 'signed')
    check(len(pg.input_value('#f-signedDate')) == 10, 'marking it signed fills in today')
    if fake:
        pg.click('#connectFolderBtn'); pg.wait_for_timeout(200)
        check('River Keeps' in pg.inner_text('#folderNote'), 'project folder connects')
    pg.set_input_files('#scanInput', files=[{'name': 'marcus-release.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4 fake'}])
    check('marcus-release.pdf' in pg.inner_text('#scanList'), 'attached scan is listed')
    pg.click('#editorSubmit'); pg.wait_for_timeout(300)
    check(not pg.is_visible('#editor'), 'saving closes the editor')
    check('is-covered' in pg.get_attribute('#peopleCov .cov-line:has-text("Marcus Bell")', 'class'), 'person is now covered')
    if fake:
        check(pg.evaluate("window.__dir['releases/marcus-release.pdf']") == '%PDF-1.4 fake', 'scan is copied into the releases folder')

    # Decline a pending release.
    pg.click('#peopleCov .cov-line:has-text("Leon Pryor") .cov-sig')
    pg.select_option('#f-status', 'declined')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('is-declined' in pg.get_attribute('#peopleCov .cov-line:has-text("Leon Pryor")', 'class'), 'declined release is flagged')

    # Take someone off camera.
    pg.click('#onCameraBtn')
    pg.uncheck('#ocPeople input[value="person-daniel-okafor"]')
    pg.click('#onCameraForm button[type=submit]'); pg.wait_for_timeout(200)
    check('Daniel Okafor' not in pg.inner_text('#peopleCov'), 'unchecked person leaves the on-camera list')

    # A materials release links to clearance log items, and deleting it unlinks them.
    pg.click('#addBtn')
    pg.select_option('#f-type', 'materials release')
    pg.fill('#f-title', 'Temporary materials release')
    pg.check('#elementsList input[value="sample-01"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.select_option('#statusFilter', 'pending')
    check(pg.locator('#rows tr[data-id]').count() >= 1, 'status filter shows matching releases')
    pg.select_option('#statusFilter', 'all')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rel_csv = open(d.value.path(), encoding='utf-8-sig').read()
    check('Marcus Bell' in rel_csv and 'Temporary materials release' in rel_csv, 'releases CSV lists the new releases')

    def saved_project():
        if fake:
            pg.click('#saveBtn'); pg.wait_for_timeout(300)
            return json.loads(pg.evaluate('window.__file.text'))
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        return json.loads(open(d.value.path(), encoding='utf-8').read())

    data = saved_project()
    temp = next(c for c in data['contracts'] if c['title'] == 'Temporary materials release')
    el = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-01')
    check(temp['id'] in el.get('contractIds', []), 'materials release is recorded on the clearance log item')
    marcus = next(c for c in data['contracts'] if 'person-marcus-bell' in c.get('personIds', []))
    scan = next(a for a in data['assets'] if a['id'] in marcus.get('assetIds', []))
    check(marcus['status'] == 'signed' and scan['type'] == 'release scan' and scan['relativePath'] == 'releases/marcus-release.pdf', 'saved release has its scan as an asset')
    people = {p['id']: p for p in data['people']}
    check(people['person-daniel-okafor'].get('onCamera') is False and people['person-marcus-bell'].get('onCamera') is True, 'on-camera choices are saved')
    original = json.loads(sample)
    music = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-03')
    check(music.get('music') == next(e for e in original['thirdPartyElements'] if e['id'] == 'sample-03')['music']
          and data.get('callSheets') == original['callSheets'] and data.get('musicCueSheet') == original['musicCueSheet'], 'other tools\' data is unchanged')

    pg.click('#rows tr:has-text("Temporary materials release") .el-name')
    pg.once('dialog', lambda dlg: dlg.accept())
    pg.click('#deleteBtn'); pg.wait_for_timeout(300)
    data = saved_project()
    el = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-01')
    before = next(e for e in original['thirdPartyElements'] if e['id'] == 'sample-01')
    check(not any(c['title'] == 'Temporary materials release' for c in data['contracts']) and el.get('contractIds') == before.get('contractIds'),
          'deleting a release unlinks its clearance log items and keeps their other contracts')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_credits_builder(browser, fake):
    ctx, pg, errs = new_page(browser, 'credits-builder', fake)
    open_sample(pg, fake)
    check(pg.inner_text('#reqCount') == '1 of 2 in the credits', 'flags the required credit that is missing (%s)' % pg.inner_text('#reqCount'))
    crawl = pg.inner_text('#crawl')
    check('Lena Ward' in crawl and 'Muddy Water Hymn' in crawl and 'levee at night' not in crawl.lower(), 'crawl shows people and songs, without excluded score cues')

    pg.click('#reqs [data-addreq="contract-rchs-license"]'); pg.wait_for_timeout(200)
    check(pg.inner_text('#reqCount') == '2 of 2 in the credits', 'adding the required wording meets it')

    pg.click('#exportBtn')
    text = pg.inner_text('#exportPreview')
    check('Directed by\nLena Ward' in text and 'Written by Earl Whitaker and June Whitaker' in text and 'Published by Delta Song Publishing (BMI)' in text,
          'text export has credits and music lines')
    check('Riverside County Historical Society' in text and 'Riverside Courier' not in text, 'text export lists archival sources, without excluded ones')
    pg.check('input[name=layout][value=columns]')
    check('Directed by\tLena Ward' in pg.inner_text('#exportPreview'), 'two-column layout uses a tab')
    with pg.expect_download() as d:
        pg.click('#downloadTxtBtn')
    check(d.value.suggested_filename.endswith('-end-credits-two-columns.txt') and 'Directed by\tLena Ward' in open(d.value.path(), encoding='utf-8').read(),
          'text file downloads')
    check(not pg.is_visible('#exportDialog'), 'export dialog closes after download')

    pg.click('#addBtn'); pg.fill('#f-role', 'Gaffer'); pg.fill('#f-names', 'Jo Park')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Jo Park' in pg.inner_text('#crawl'), 'new credit shows in the crawl')
    rows = pg.locator('#entries .entry')
    last = rows.count() - 1
    pg.click('[data-up="%d"]' % last); pg.wait_for_timeout(100)
    check('Gaffer' in rows.nth(last - 1).inner_text(), 'moving a credit up reorders it')

    pg.click('[data-edit="credit-post-supervisor"]')
    pg.click('#deleteBtn'); pg.wait_for_timeout(200)
    check('Sam Okafor' in pg.inner_text('#uncredited'), 'removing a credit lists the person as not credited')
    pg.click('#uncredited [data-skip="person-sam-okafor"]'); pg.wait_for_timeout(200)
    check('Sam Okafor' not in pg.inner_text('#uncredited'), 'marking someone not credited takes them off the list')

    pg.click('#addReqBtn')
    pg.select_option('#r-contract', '')
    pg.fill('#r-title', 'Test archive license')
    pg.select_option('#r-element', 'sample-07')
    pg.fill('#r-text', 'Courtesy of the Test Archive')
    pg.click('#reqForm button[type=submit]'); pg.wait_for_timeout(200)
    check(pg.inner_text('#reqCount') == '2 of 3 in the credits', 'a new requirement is flagged until the credits include it')

    pg.click('#playBtn')
    check('is-playing' in pg.get_attribute('#screen', 'class'), 'play crawl starts the roll')
    pg.click('#playBtn')
    check('is-playing' not in pg.get_attribute('#screen', 'class'), 'stop crawl ends it')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    entries = data['credits']['entries']
    check(any(e.get('role') == 'Gaffer' and e.get('names') == ['Jo Park'] for e in entries) and data['credits'].get('notCredited') == ['person-sam-okafor'],
          'credits and not-credited choices are saved')
    lic = next((c for c in data['contracts'] if c.get('title') == 'Test archive license'), {})
    el = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-07')
    check(lic.get('requiredCredit') == 'Courtesy of the Test Archive' and lic.get('thirdPartyElementIds') == ['sample-07'] and lic.get('id') in el.get('contractIds', []),
          'new license is saved and linked to its clearance log item')
    original = json.loads(sample)
    song = lambda d: next(e for e in d['thirdPartyElements'] if e['id'] == 'sample-03').get('music')
    check(data['people'] == original['people'] and data.get('callSheets') == original['callSheets'] and data.get('musicCueSheet') == original['musicCueSheet']
          and song(data) == song(original), "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

    # Drafting from the project, on the sample with its credits taken out.
    ctx, pg, errs = new_page(browser, 'credits-builder', False)
    bare = json.loads(sample); bare.pop('credits')
    pg.set_input_files('#fileInput', files=[{'name': 'bare.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(bare).encode()}])
    pg.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")
    check(pg.is_visible('#fillBtn'), 'a project without credits offers a draft')
    pg.click('#fillBtn'); pg.wait_for_timeout(200)
    roles = [t.split('\n')[0] for t in pg.locator('#entries .entry .what').all_inner_texts()]
    check(roles[:6] == ['Director', 'Producer', 'Editor', 'Director of photography', 'Composer', 'Featuring'], 'draft puts key creatives first, then featuring %s' % roles[:6])
    crawl = pg.inner_text('#crawl')
    check('Daniel Okafor' in crawl and 'Muddy Water Hymn' in crawl and 'All rights reserved' in crawl, 'draft has people, music and a copyright line')
    check(pg.inner_text('#reqCount') == '2 of 2 in the credits', 'draft includes the required wording')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

# Each spreadsheet template's columns must appear in its tool's CSV export, in the same order.
TEMPLATE_EXPORTS = [('clearance-log', 'clearance-log-template.csv'), ('release-tracker', 'release-log-template.csv'),
                    ('music-cue-sheet', 'music-cue-sheet-template.csv'), ('name-supers', 'name-supers-template.csv'),
                    ('subject-tracker', 'subject-tracker-template.csv'), ('research-log', 'research-log-template.csv'),
                    ('comps-tracker', 'comps-tracker-template.csv')]

def test_name_supers(browser, fake):
    ctx, pg, errs = new_page(browser, 'name-supers', fake)
    open_sample(pg, fake)
    rows = pg.inner_text('#rows')
    check('Close to Marcus Bell in the project' in rows, 'flags a typed name close to someone in the project')
    check('Changed: title was "Levee board member"' in rows and 'New since export' in rows, 'flags changes since the last export')
    check('Marcus Bell' in pg.inner_text('#missing'), 'lists people on camera without a super')
    pg.click('[data-link="super-foreman"]'); pg.wait_for_timeout(200)
    check('Close to Marcus Bell' not in pg.inner_text('#rows') and 'Everyone on camera has a super' in pg.inner_text('#missing'), 'using the project spelling links the super')

    pg.click('[data-edit="super-ruth"]')
    pg.fill('#f-name', 'Ruth A. Hammond'); pg.fill('#f-tc', '1:02'); pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a badly formed timecode is refused')
    pg.fill('#f-tc', '01:00:30:00'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .nm').first.inner_text() == 'Ruth A. Hammond', 'supers sort by timecode, with the fixed spelling')

    pg.click('#addBtn'); pg.select_option('#f-person', ''); pg.fill('#f-name', 'Archival narrator'); pg.fill('#f-title', 'Voice, 1965 newsreel')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Archival narrator' in pg.inner_text('#rows'), 'adds a super for someone not in the project')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    lines = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(lines[0] == ['First appears', 'Name', 'Title', 'Notes', 'Since last export'] and lines[1][:2] == ['01:00:30:00', 'Ruth A. Hammond'] and lines[1][4].startswith('Changed'),
          'export lists supers in order with what changed')
    check('No changes since then' in pg.inner_text('#since') and 'New since export' not in pg.inner_text('#rows'), 'export resets the change flags')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    people = {p['id']: p for p in data['people']}
    foreman = next(e for e in data['supers']['entries'] if e['id'] == 'super-foreman')
    check(people['person-ruth-hammond']['name'] == 'Ruth A. Hammond' and foreman.get('personId') == 'person-marcus-bell' and 'name' not in foreman,
          'spelling fixes and links are saved to the project')
    check(len(data['supers']['lastExport']['entries']) == 5, 'the export snapshot is saved')
    original = json.loads(sample)
    check(data.get('credits') == original['credits'] and data.get('callSheets') == original['callSheets'] and data['contracts'] == original['contracts'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_subject_tracker(browser, fake):
    ctx, pg, errs = new_page(browser, 'subject-tracker', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 5 and 'Agreed 2' in pg.inner_text('#filters'), 'lists subjects with counts by access')
    pg.click('[data-filter="declined"]')
    check(pg.locator('#rows .row').count() == 1 and 'Office of the mayor' in pg.inner_text('#rows'), 'filters by access status')
    pg.click('[data-filter="all"]'); pg.fill('#search', 'diary')
    check(pg.locator('#rows .row').count() == 1, 'search finds subjects by notes')
    pg.fill('#search', '')

    pg.click('#addBtn'); pg.fill('#f-name', 'Ida Fenn'); pg.fill('#f-about', 'Ran the sandbag line in 1993')
    pg.select_option('#f-status', 'in-conversation'); pg.fill('#f-next', '2020-01-02'); pg.fill('#f-nextNote', 'Send the release')
    pg.fill('#logNote', 'Met at the library'); pg.click('#logAddBtn')
    check('Met at the library' in pg.inner_text('#log'), 'logs a contact in the editor')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    first = pg.locator('#rows .row').first.inner_text()
    check('Ida Fenn' in first and 'overdue' in first and 'Ida Fenn' in pg.inner_text('#dueList'), 'an overdue follow-up comes first and is listed as due')

    pg.click('[data-edit="subject-clerk"]'); pg.select_option('#f-status', 'agreed'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Agreed, not in the project yet' in pg.inner_text('#rows'), 'flags agreed subjects not in the project')
    pg.click('[data-person="subject-clerk"]'); pg.wait_for_timeout(200)
    check('Agreed, not in the project yet' not in pg.inner_text('#rows'), 'adds an agreed subject to the project')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    lines = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(lines[1][0] == 'Ida Fenn' and len(lines) == 7, 'CSV lists subjects, follow-ups first')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    doris = next(p for p in data['people'] if p['name'] == 'Doris Kemp')
    clerk = next(s for s in data['subjects'] if s['id'] == 'subject-clerk')
    ida = next(s for s in data['subjects'] if s['name'] == 'Ida Fenn')
    check(clerk['personId'] == doris['id'] and doris.get('onCamera') is True and doris.get('phone') == '555-0142' and doris.get('roles') == ['Interview subject'],
          'the new person is saved with their contact details, on camera')
    check(ida.get('log') == [{'date': ida['lastContact'], 'note': 'Met at the library'}] and ida['nextFollowUp'] == '2020-01-02', 'the contact log and follow-up are saved')
    original = json.loads(sample)
    check(data.get('credits') == original['credits'] and data.get('supers') == original['supers'] and data['contracts'] == original['contracts'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_research_log(browser, fake):
    ctx, pg, errs = new_page(browser, 'research-log', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 4 and 'Research sources 2' in pg.inner_text('#tab-research'), 'shows archival leads, with research sources on their own tab')
    check('In the clearance log: Licensed' in pg.inner_text('#rows'), "shows a linked lead's clearance status")
    pg.click('#tab-research')
    check('Corps of Engineers' in pg.inner_text('#rows') and 'Flood of 1965' not in pg.inner_text('#rows'), 'switches to research sources')
    pg.click('#tab-archival')
    pg.select_option('#statusFilter', 'screener-received')
    check(pg.locator('#rows .row').count() == 1, 'filters by status')
    pg.select_option('#statusFilter', '')

    pg.click('[data-edit="source-sandbag"]'); pg.select_option('#f-status', 'ready-to-license'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Ready, not in the clearance log yet' in pg.inner_text('#rows'), 'flags a ready lead not in the clearance log')
    pg.click('[data-send="source-sandbag"]'); pg.wait_for_timeout(200)
    check('Ready, not in the clearance log yet' not in pg.inner_text('#rows') and pg.inner_text('#rows').count('In the clearance log') == 3, 'sends a lead to the clearance log')

    pg.click('#addBtn'); pg.fill('#f-title', 'Levee construction stills'); pg.fill('#f-cost', '-5'); pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a negative cost is refused')
    pg.fill('#f-cost', '200'); pg.select_option('#f-type', 'Archival still'); pg.fill('#f-archive', 'State archives'); pg.click('#sendBtn'); pg.wait_for_timeout(200)
    check('Levee construction stills' in pg.inner_text('#rows') and '4 sent to the clearance log' in pg.inner_text('#totals'), 'a new source can be sent straight from the editor')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    lines = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(len(lines) == 8 and lines[0][0] == 'Log' and any(r[1] == 'Levee construction stills' and r[13] == 'Not started' for r in lines), 'CSV lists every source with its clearance status')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    sandbag = next(s for s in data['sources'] if s['id'] == 'source-sandbag')
    el = next(e for e in data['thirdPartyElements'] if e['id'] == sandbag.get('elementId'))
    check(el['description'] == 'Sandbag line on Front Street, 1993' and el['type'] == 'Archival still' and el['status'] == 'not-started'
          and el['rightsHolder'] == 'Riverside Public Library' and el['cost'] == 75 and 'Box 31, folder 7' in el['source'], 'the sent element carries the lead\'s details')
    new = next(s for s in data['sources'] if s.get('title') == 'Levee construction stills')
    check(new.get('cost') == 200 and new.get('status') == 'ready-to-license' and new.get('elementId'), 'the new source is saved, linked and ready')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data.get('credits') == original['credits'] and data['contracts'] == original['contracts']
          and [e for e in data['thirdPartyElements'] if e['id'].startswith('sample-')] == original['thirdPartyElements'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_comps_tracker(browser, fake):
    ctx, pg, errs = new_page(browser, 'comps-tracker', fake)
    open_sample(pg, fake)
    rows = pg.inner_text('#rows')
    check(pg.locator('#rows .row').count() == 3 and rows.count('No source') == 1, 'lists comps and flags a figure without a source')
    pg.click('[data-tag="subjectTags:floods"]')
    check(pg.locator('#rows .row').count() == 2, 'filters by tag')
    pg.click('[data-tag="subjectTags:floods"]')
    check('Fewer than three comps' in pg.inner_text('#checks') and 'without a source' in pg.inner_text('#checks'), 'checks the comps page before the pitch')
    pg.check('[data-pitch="comp-ledger"]'); pg.wait_for_timeout(100)
    check('Fewer than three' not in pg.inner_text('#checks') and 'more than seven years old' in pg.inner_text('#checks'), 'picking a comp updates the checks')

    pg.click('[data-edit="comp-seawall"]')
    pg.locator('#figRows .fig-source').first.fill('Fictional box office tracker, 2022')
    pg.click('#addFigBtn'); pg.locator('#figRows .fig-label').last.fill('Budget'); pg.locator('#figRows .fig-amount').last.fill('$600,000')
    pg.fill('#f-style', 'archival-led, essay')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.inner_text('#rows').count('No source') == 1 and 'Style: essay' in pg.inner_text('#rows'), 'adds a figure and a tag; the new unsourced figure is flagged')

    pg.click('#printBtn'); pg.wait_for_timeout(200)
    report = pg.inner_text('#report')
    check('$210,000' in report and 'Fictional box office tracker, 2022' in report and '$600,000' not in report and 'Ledger of the Low Water' in report, 'the comps page lists picked comps with sourced figures only')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    lines = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(lines[1][0] == 'Backwater Hymnal' and 'Budget: $600,000 (no source)' in lines[2][7], 'CSV lists comps newest first with their figures')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    seawall = next(c for c in data['comps'] if c['id'] == 'comp-seawall')
    ledger = next(c for c in data['comps'] if c['id'] == 'comp-ledger')
    check(seawall['figures'][1] == {'label': 'Budget', 'amount': '$600,000'} and seawall['styleTags'] == ['archival-led', 'essay'] and ledger.get('inPitch') is True, 'comps are saved')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data.get('sources') == original['sources'] and data['thirdPartyElements'] == original['thirdPartyElements'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_treatment_builder(browser, fake):
    ctx, pg, errs = new_page(browser, 'treatment-builder', fake)
    open_sample(pg, fake)
    check(pg.input_value('#t-logline').startswith('When the river') and '25 / 50' in pg.inner_text('#outline'), 'opens the treatment with word counts')
    pg.fill('#t-logline', ' '.join(['word'] * 55)); pg.wait_for_timeout(100)
    check('5 over' in pg.inner_text('#wc-logline') and 'over' in pg.get_attribute('#wc-logline', 'class'), 'flags a section over its target')
    pg.fill('[data-target="logline"]', '60'); pg.wait_for_timeout(100)
    check('55 of 60 words' in pg.inner_text('#wc-logline'), 'targets can be changed')

    pg.click('[data-insert="team"]'); pg.wait_for_timeout(100)
    team = pg.input_value('#t-team')
    check('Director: Lena Ward' in team and 'Ruth Hammond' not in team, 'adds the crew, not the subjects, to the team section')
    pg.click('[data-insert="subjects"]'); pg.wait_for_timeout(100)
    subj = pg.input_value('#t-subjects')
    check('Daniel Okafor' in subj and 'Marcus Bell' in subj and 'Doris Kemp' in subj and subj.count('Ruth Hammond') == 1, 'adds missing subjects from the project and subject tracker, without repeats')

    pg.click('[data-compare="version-grant-draft"]'); pg.wait_for_timeout(200)
    body = pg.inner_html('#compareBody')
    check('<del>' in body and '<ins>' in body and 'Empty in both.' in pg.inner_text('#compareBody'), 'compares the current text with a saved version')
    pg.click('#compareClose')
    pg.fill('#versionLabel', 'Before the edit'); pg.click('#saveVersionBtn'); pg.wait_for_timeout(100)
    pg.fill('#t-access', 'Changed access text.'); pg.wait_for_timeout(100)
    pg.click('[data-compare]')
    check('Changes since "Before the edit"' in pg.inner_text('#compareTitle') and '1 section changed' in pg.inner_text('#compareLead'), 'a new version compares against later edits')
    pg.once('dialog', lambda d: d.accept())
    pg.click('#restoreVersionBtn'); pg.wait_for_timeout(200)
    check(pg.input_value('#t-access').startswith('Ruth has agreed'), 'goes back to a saved version')

    with pg.expect_download() as d:
        pg.click('#mdBtn')
    md = open(d.value.path(), encoding='utf-8').read()
    check(md.startswith('# The River Keeps') and '## Team' in md and '## Long synopsis' not in md, 'Markdown export has filled sections only')
    with pg.expect_download() as d:
        pg.click('#txtBtn')
    check('ACCESS\n\nRuth has agreed' in open(d.value.path(), encoding='utf-8').read(), 'plain text export')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    t = data['treatment']
    check(t['targets'] == {'shortSynopsis': 100, 'logline': 60} and len(t['versions']) == 2 and 'Lena Ward' in t['sections']['team'], 'sections, targets and versions are saved')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data.get('subjects') == original['subjects'] and data.get('credits') == original['credits'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_pitch_deck(browser, fake):
    import base64
    ctx, pg, errs = new_page(browser, 'pitch-deck', fake)
    open_sample(pg, fake)
    check(pg.locator('#deck .slide-wrap').count() == 8 and '7 slides, 1 left out' in pg.inner_text('#count'), 'opens the deck, with one slide left out')
    deck = pg.inner_text('#deck')
    check('Lena Ward' in deck and 'Backwater Hymnal' in deck and 'Fictional trade report' in deck, 'team and comps slides come from the project')

    png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAFklEQVR4nGP8z8DAwMDAxMDAwMDAAAANHQEDK+mmyAAAAABJRU5ErkJggg==')
    pg.set_input_files('#imgInput', files=[{'name': 'still.png', 'mimeType': 'image/png', 'buffer': png}])
    pg.wait_for_function("document.querySelectorAll('#imgs figure').length === 4")
    check(pg.locator('#imgs figure').count() == 4, 'adds an image from the computer')

    pg.click('#addBtn'); pg.select_option('#f-kind', 'image'); pg.fill('#f-body', 'The levee at dawn')
    pg.locator('#pickImgs input').nth(0).check(); pg.locator('#pickImgs input').nth(1).check()
    pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor') and 'one image' in pg.inner_text('#pickHint'), 'a full-page image slide takes one image')
    pg.locator('#pickImgs input').nth(0).uncheck(); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#deck .slide-wrap').count() == 9 and 'The levee at dawn' in pg.inner_text('#deck'), 'adds a full-page image slide')
    pg.click('[data-up="8"]'); pg.wait_for_timeout(100)
    check('Full-page image' in pg.locator('#deck .slide-wrap').nth(7).inner_text(), 'moves a slide')

    pg.check('input[name=size][value=letter]'); pg.click('#printBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#report .slide').count() == 8 and '11in 8.5in' in pg.inner_text('#pageSize'), 'prints the slides that aren\'t left out, at letter size')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    d = data['pitchDeck']
    new = d['images'][-1]
    check(d['size'] == 'letter' and new['name'] == 'still.png' and new['data'].startswith('data:image/jpeg;base64,') and d['slides'][7]['kind'] == 'image' and d['slides'][7]['imageIds'] == [d['images'][1]['id']],
          'size, images and slides are saved')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data.get('comps') == original['comps'] and data.get('treatment') == original['treatment'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

    # Starting from the project, on the sample without a deck.
    ctx, pg, errs = new_page(browser, 'pitch-deck', False)
    bare = json.loads(sample); bare.pop('pitchDeck')
    pg.set_input_files('#fileInput', files=[{'name': 'bare.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(bare).encode()}])
    pg.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")
    pg.click('#draftBtn'); pg.wait_for_timeout(200)
    deck = pg.inner_text('#deck')
    check(pg.locator('#deck .slide-wrap').count() == 8 and 'flood diary' in deck and 'Riverside has flooded' in deck and '[What you' in deck, 'drafts slides from the treatment and project')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_template_columns(browser, fake):
    for name, template in TEMPLATE_EXPORTS:
        ctx, pg, errs = new_page(browser, name, fake)
        open_sample(pg, fake)
        with pg.expect_download() as d:
            pg.click('#csvBtn')
        exported = next(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
        wanted = next(csv.reader(io.StringIO((root / 'templates' / template).read_text(encoding='utf-8-sig'))))
        remaining = iter(exported)
        check(all(col in remaining for col in wanted), '%s: template columns appear in the export, in order' % template)
        check(not errs, 'no page errors %s' % errs)
        ctx.close()

def main():
    global FALLBACK
    mode = sys.argv[1] if len(sys.argv) > 1 else 'chromium'
    FALLBACK = mode == 'chromium-fallback'
    engine = 'chromium' if FALLBACK else mode
    fake = mode == 'chromium'
    with sync_playwright() as p:
        # PLAYWRIGHT_CHANNEL=chrome uses an installed Google Chrome instead of Playwright's own Chromium (CI does this).
        channel = os.environ.get('PLAYWRIGHT_CHANNEL') if engine == 'chromium' else None
        browser = getattr(p, engine).launch(headless=True, **({'channel': channel} if channel else {}))
        print('#### %s %s' % (mode, browser.version))
        for name in TOOLS:
            for label, fn in [('core', lambda: test_core(browser, name, fake)), ('phone', lambda: test_phone(browser, name, fake)),
                              ('dark mode', lambda: test_dark(browser, name, fake)), ('print', lambda: test_print(browser, name, fake, fake))]:
                print('== %s / %s' % (name, label))
                fn()
        print('== call-sheet / spreadsheet export')
        test_call_sheet_export(browser, fake)
        print('== release-tracker / releases, coverage and scans')
        test_release_tracker(browser, fake)
        print('== credits-builder / credits, requirements and export')
        test_credits_builder(browser, fake)
        print('== name-supers / flags, spelling and export')
        test_name_supers(browser, fake)
        print('== subject-tracker / filters, follow-ups and adding people')
        test_subject_tracker(browser, fake)
        print('== research-log / tabs, statuses and sending to the clearance log')
        test_research_log(browser, fake)
        print('== comps-tracker / sources, tags and the comps page')
        test_comps_tracker(browser, fake)
        print('== treatment-builder / counts, project lines and versions')
        test_treatment_builder(browser, fake)
        print('== pitch-deck / slides, images and print sizes')
        test_pitch_deck(browser, fake)
        print('== templates / columns match the tools\' exports')
        test_template_columns(browser, fake)
        browser.close()
    print('FAILS', fails)
    sys.exit(1 if fails else 0)

main()

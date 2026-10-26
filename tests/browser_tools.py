"""Real-browser checks for every tool.

Run: pip install playwright pypdf && playwright install chromium firefox webkit
     python tests/browser_tools.py [chromium|firefox|webkit]   (default: chromium)

Checks, per tool: opening the sample, saving, all CSV exports, phone width, dark
mode and print layout. Chromium also covers the save-conflict warning (it has the
file picker API; its handles are faked in memory) and renders a real PDF.
Firefox and WebKit (Safari's engine) use the download/upload fallback instead.
The call sheet, release tracker and credits builder also get end-to-end checks
of their own, and the spreadsheet templates are checked against the tools' exports.
"""
import csv, io, json, pathlib, sys
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parents[1]
sample = (root / 'samples/the-river-keeps.oft.json').read_text()
TOOLS = ['clearance-log', 'music-cue-sheet', 'call-sheet', 'release-tracker', 'credits-builder']
COLLECTIONS = ['project', 'people', 'locations', 'thirdPartyElements', 'contracts', 'assets', 'musicCueSheet', 'callSheets']
PRINT_BTN = {'clearance-log': '#printBtn', 'music-cue-sheet': '#printBtn', 'call-sheet': '#printAllBtn', 'release-tracker': '#printBtn',
             'credits-builder': '#printBtn'}
PHONE = {'width': 390, 'height': 844}

STUB_PRINT = 'window.print = () => { window.__printed = true; };'
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
    page.add_init_script(STUB_PRINT + (FAKE_PICKERS if fake else '') + extra)
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
    pg.click('#addBtn'); pg.wait_for_timeout(300)
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
                    ('music-cue-sheet', 'music-cue-sheet-template.csv')]

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
    engine = sys.argv[1] if len(sys.argv) > 1 else 'chromium'
    fake = engine == 'chromium'
    with sync_playwright() as p:
        browser = getattr(p, engine).launch(headless=True)
        print('#### %s %s' % (engine, browser.version))
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
        print('== templates / columns match the tools\' exports')
        test_template_columns(browser, fake)
        browser.close()
    print('FAILS', fails)
    sys.exit(1 if fails else 0)

main()

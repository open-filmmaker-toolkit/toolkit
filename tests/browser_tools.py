"""Real-browser checks for project CSV export and the save-conflict warning.

Run: pip install playwright && playwright install chromium && python tests/browser_tools.py
File picker handles are faked in memory; everything else is the shipped page.
"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parents[1]
sample = (root/'samples/the-river-keeps.oft.json').read_text()
INIT = """
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
def check(c, m):
    print(('PASS ' if c else 'FAIL ') + m)
    if not c: fails.append(m)
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for tool in ['clearance-log','music-cue-sheet','call-sheet']:
        print('==', tool)
        ctx = b.new_context(accept_downloads=True)
        pg = ctx.new_page(); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.add_init_script(INIT)
        pg.goto('file://%s/tools/%s/index.html' % (root, tool)); pg.wait_for_load_state('networkidle')
        pg.click('#openBtn'); pg.wait_for_timeout(300)
        # CSV export for each collection
        for col in ['project','people','locations','thirdPartyElements','contracts','assets','musicCueSheet','callSheets']:
            pg.click('#projectCsvBtn'); pg.select_option('#projectCsvCollection', col)
            with pg.expect_download() as d:
                pg.click('#projectCsvForm button[type=submit]')
            dl = d.value; txt = open(dl.path()).read()
            check(dl.suggested_filename.endswith('-%s.csv' % col) and len(txt) > 0, 'csv %s -> %s (%d bytes)' % (col, dl.suggested_filename, len(txt)))
        # clean save
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        check(pg.evaluate('window.__writes') == 1, 'clean save writes')
        check(not pg.is_visible('#conflictDialog'), 'no conflict on clean save')
        # external change -> conflict
        orig = pg.evaluate('window.__file.text')
        ext = json.loads(orig); ext['project']['title'] = 'CHANGED EXTERNALLY'
        pg.evaluate('t => window.__file.text = t', json.dumps(ext))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        check(pg.is_visible('#conflictDialog'), 'conflict dialog shown')
        check('CHANGED EXTERNALLY' in pg.evaluate('window.__file.text'), 'file untouched while warning')
        pg.click('#conflictCancelBtn'); check(not pg.is_visible('#conflictDialog'), 'keep editing closes')
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        w = pg.evaluate('window.__writes')
        pg.click('#conflictOverwriteBtn'); pg.wait_for_timeout(300)
        check(pg.evaluate('window.__writes') == w+1 and 'CHANGED EXTERNALLY' not in pg.evaluate('window.__file.text'), 'overwrite replaces file')
        pg.evaluate('t => window.__file.text = t', json.dumps(ext))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        pg.click('#conflictReloadBtn'); pg.wait_for_timeout(300)
        check('CHANGED EXTERNALLY' in pg.content() , 'reload latest shows external title')
        pg.evaluate('t => window.__file.text = t', json.dumps(dict(ext, project=dict(ext['project'], title='AGAIN'))))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        with pg.expect_download() as d:
            pg.click('#conflictCopyBtn')
        check(True, 'save a copy downloads: ' + d.value.suggested_filename)
        check(not errs, 'no page errors %s' % errs)
        ctx.close()
    print('== call-sheet spreadsheet export and print')
    ctx = b.new_context(accept_downloads=True)
    pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script(INIT + 'window.print = () => { window.__printed = true; };')
    pg.goto('file://%s/tools/call-sheet/index.html' % root); pg.wait_for_load_state('networkidle')
    pg.click('#openBtn'); pg.wait_for_timeout(300)
    with pg.expect_download() as d:
        pg.click('#sheetCsvBtn')
    txt = open(d.value.path(), encoding='utf-8-sig').read()
    check(d.value.suggested_filename.endswith('.csv') and txt.startswith('CALL SHEET') and 'CREW AND CAST' in txt and 'General call,' in txt, 'all-days spreadsheet export: ' + d.value.suggested_filename)
    template = (root/'templates/call-sheet-template.csv').read_text()
    import csv, io
    labels = lambda t: [r[0] for r in csv.reader(io.StringIO(t)) if r]
    def skeleton(t):
        rows = [r for r in csv.reader(io.StringIO(t)) if r and r[0]]
        return [r[0] for r in rows if r[0] in ('CALL SHEET', 'SCHEDULE', 'CREW AND CAST', 'NOTES', 'Film', 'General call', 'Nearest hospital', 'Time', 'Name', 'Prepared by')]
    check(skeleton(template) == skeleton(txt), 'export layout matches blank template')
    pg.click('#printAllBtn'); pg.wait_for_timeout(200)
    check(pg.evaluate('window.__printed === true') and pg.locator('.sheet-page').count() >= 1, 'print builds sheet pages')
    pg.emulate_media(media='print')
    check(pg.is_visible('.sheet-page') and not pg.is_visible('.page'), 'print view shows only the sheet')
    pg.emulate_media(media='screen')
    pg.locator('#list [data-id], [data-id]').first.click(); pg.wait_for_timeout(200)
    with pg.expect_download() as d:
        pg.click('#sheetCsvDayBtn')
    check('-call-sheet-' in d.value.suggested_filename, 'single-day export: ' + d.value.suggested_filename)
    check(not errs, 'no page errors %s' % errs)
    ctx.close()
    b.close()
print('FAILS', fails); sys.exit(1 if fails else 0)

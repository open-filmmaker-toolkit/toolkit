"""Copy shared code into the tools and the home page.

Each tool is one self-contained HTML file, so code that several pages need lives in
shared/ and is copied into each page between marker comments:

    /* oft-shared:tool begin. Copied from shared/tool.js by .github/scripts/sync_shared.py; edit it there. */
    ...
    /* oft-shared:tool end */

Edit the file in shared/, then run: python3 .github/scripts/sync_shared.py
The repository check (validate_repo.py) fails if a page's copy is out of date.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BEGIN = '/* oft-shared:%s begin. Copied from shared/%s.js by .github/scripts/sync_shared.py; edit it there. */'
END = '/* oft-shared:%s end */'


def pages():
    return sorted(ROOT.glob('tools/*/index.html')) + [ROOT / 'index.html']


# Translations: each language in translations/ is copied into a page's i18n block, but only the lines
# that page uses, so a page carries no more than it needs.
def languages():
    import csv
    langs = {}
    folder = ROOT / 'translations'
    names = folder / 'languages.csv'
    if not names.is_file():
        return langs
    for row in csv.DictReader(names.read_text(encoding='utf-8-sig').splitlines()):
        code = (row.get('Code') or '').strip()
        f = folder / ('%s.csv' % code)
        if not code or not f.is_file():
            continue
        strings = {}
        for r in csv.reader(f.read_text(encoding='utf-8-sig').splitlines()[1:]):
            if len(r) >= 2 and r[0].strip() and r[1].strip():
                strings[r[0].strip()] = r[1].strip()
        langs[code] = {'name': row.get('Name', code).strip(), 'label': (row.get('Label') or 'Language').strip(), 'strings': strings}
    return langs


def i18n_data(page_text):
    import json
    src = re.sub(r'/\* oft-shared:i18n begin.*?oft-shared:i18n end \*/', '', page_text, flags=re.S)
    unesc = lambda t: t.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    used = lambda k: all(unesc(seg).strip() in src for seg in re.split(r'</?\w+>', k) if seg.strip())
    out = {}
    for code, lang in sorted(languages().items()):
        out[code] = {'name': lang['name'], 'label': lang['label'], 'strings': {k: v for k, v in sorted(lang['strings'].items()) if used(k)}}
    return 'const OFT_LANGS = ' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';'


def block(name, indent, page_text=''):
    code = (ROOT / 'shared' / ('%s.js' % name)).read_text(encoding='utf-8').rstrip('\n')
    if name == 'i18n':
        code = i18n_data(page_text) + '\n' + code
    lines = [BEGIN % (name, name)] + code.split('\n') + [END % name]
    return '\n'.join((indent + l) if l else '' for l in lines)


def blocks_in(text):
    return re.findall(r'/\* oft-shared:([a-z0-9-]+) begin\.', text)


def sync(text):
    for name in blocks_in(text):
        pat = re.compile(r'^([ \t]*)' + re.escape(BEGIN % (name, name)) + r'.*?' + re.escape(END % name), re.S | re.M)
        text = pat.sub(lambda m, t=text: block(name, m.group(1), t), text, count=1)
    return text


# The service worker (sw.js) keeps a copy of every page, so the toolkit works offline once installed.
SW = ROOT / 'sw.js'
PAGES_RE = re.compile(r'(// oft-pages begin).*?(\n[ \t]*// oft-pages end)', re.S)


def sw_pages():
    files = ['./', 'index.html', 'manifest.webmanifest', 'docs/assets/icon.svg', 'docs/assets/icon-192.png', 'docs/assets/icon-512.png']
    files += [p.relative_to(ROOT).as_posix() for p in sorted(ROOT.glob('tools/*/index.html'))]
    files += [p.relative_to(ROOT).as_posix() for p in sorted(ROOT.glob('samples/*')) if p.is_file()]
    return files


def sync_sw(text):
    return PAGES_RE.sub(lambda m: m.group(1) + ''.join("\n  '%s'," % f for f in sw_pages()) + m.group(2), text, count=1)


def check():
    """Returns a list of pages whose shared code differs from shared/."""
    bad = []
    for p in pages():
        text = p.read_text(encoding='utf-8')
        if blocks_in(text) and sync(text) != text:
            bad.append(str(p.relative_to(ROOT)))
    if SW.is_file() and sync_sw(SW.read_text(encoding='utf-8')) != SW.read_text(encoding='utf-8'):
        bad.append('sw.js')
    return bad


if __name__ == '__main__':
    if '--check' in sys.argv:
        bad = check()
        print('\n'.join('Out of date: %s' % b for b in bad) or 'Shared code is up to date.')
        sys.exit(1 if bad else 0)
    for p in pages():
        text = p.read_text(encoding='utf-8')
        new = sync(text)
        if new != text:
            p.write_text(new, encoding='utf-8')
            print('Updated', p.relative_to(ROOT))
    if SW.is_file():
        text = SW.read_text(encoding='utf-8')
        if sync_sw(text) != text:
            SW.write_text(sync_sw(text), encoding='utf-8')

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


def block(name, indent):
    code = (ROOT / 'shared' / ('%s.js' % name)).read_text(encoding='utf-8').rstrip('\n')
    lines = [BEGIN % (name, name)] + code.split('\n') + [END % name]
    return '\n'.join((indent + l) if l else '' for l in lines)


def blocks_in(text):
    return re.findall(r'/\* oft-shared:([a-z-]+) begin\.', text)


def sync(text):
    for name in blocks_in(text):
        pat = re.compile(r'^([ \t]*)' + re.escape(BEGIN % (name, name)) + r'.*?' + re.escape(END % name), re.S | re.M)
        text = pat.sub(lambda m: block(name, m.group(1)), text, count=1)
    return text


def check():
    """Returns a list of pages whose shared code differs from shared/."""
    bad = []
    for p in pages():
        text = p.read_text(encoding='utf-8')
        if blocks_in(text) and sync(text) != text:
            bad.append(str(p.relative_to(ROOT)))
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

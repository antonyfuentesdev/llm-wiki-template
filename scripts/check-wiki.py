#!/usr/bin/env python3
"""Mechanical wiki checks from lint.md. Run from anywhere: python3 scripts/check-wiki.py
Prints file:line: message for each finding and exits 1 if there are any."""
import functools, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, 'wiki')
SKIP_TOP = {'.git', '_templates', 'examples', 'tmp', 'inbox', 'scripts', '.obsidian'}
TYPES = {'source', 'entity', 'concept', 'topic', 'question', 'workflow', 'index'}
PAGE_KEYS = ['type', 'partition', 'created', 'updated', 'sources', 'tags', 'status']
LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)\)')
PLACEHOLDER = re.compile(r'<(?![a-z]+://)[A-Za-z/][^<>]*>')
findings = []

def report(path, line, msg):
    findings.append(f'{os.path.relpath(path, ROOT)}:{line}: {msg}')

def prose(path):
    """Yield (line number, text without inline code, raw text) outside fenced code blocks."""
    fence = None
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        s = line.strip()
        if fence:
            fence = None if s and set(s) == {fence[0]} and len(s) >= len(fence) else fence
            continue
        m = re.match(r'(`{3,}|~{3,})', s)
        if m:
            fence = m.group(1)
            continue
        yield n, re.sub(r'`[^`]*`', '', line.rstrip('\n')), line

def frontmatter(path):
    m = re.match(r'---\n(.*?)\n---\n', open(path, encoding='utf-8').read(), re.S)
    pairs = [l.split(':', 1) for l in m.group(1).split('\n') if ':' in l and l[0] != ' '] if m else []
    return {k.strip(): v.strip() for k, v in pairs}

@functools.lru_cache(maxsize=None)
def anchors(path):
    """GitHub-style heading slugs; repeated headings get -1, -2 suffixes."""
    seen, out = {}, set()
    for _, _, raw in prose(path):
        m = re.match(r'#{1,6}\s+(.+)', raw)
        if m:
            a = re.sub(r'[^\w\- ]', '', m.group(1).strip().lower()).replace(' ', '-')
            out.add(a if a not in seen else f'{a}-{seen[a]}')
            seen[a] = seen.get(a, 0) + 1
    return out

is_raw = lambda p: f'{os.sep}raw{os.sep}' in p
files = []
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if not (dp == ROOT and d in SKIP_TOP) and d != '.git']
    files += [os.path.join(dp, f) for f in fns if f.endswith('.md')]
fms = {p: frontmatter(p) for p in files}
pages = [p for p in files if p.startswith(WIKI + os.sep) and not is_raw(p)]
inbound, listed = {}, {}

for p in files:
    if is_raw(p):
        continue
    fm, wiki_page = fms[p], p in pages
    refs, defs, cited = set(), set(), set()
    for n, text, raw in prose(p):
        if wiki_page and ('<!--' in text or PLACEHOLDER.search(text)):
            report(p, n, 'leftover template comment or <placeholder>')
        for k in re.findall(r'\[\^(\d+)\]', text):
            report(p, n, f'numbered footnote [^{k}]; use a key (AGENTS.md §7)')
        refs.update(re.findall(r'\[\^([^\]]+)\](?!:)', text))
        d = re.match(r'\[\^([^\]]+)\]:', raw)
        defs.update([d.group(1)] if d else [])
        for m in LINK.finditer(text):
            target, _, anchor = m.group(1).partition('#')
            if '://' in target or target.startswith('mailto:'):
                continue
            dest = os.path.normpath(os.path.join(os.path.dirname(p), target)) if target else p
            if not os.path.exists(dest):
                report(p, n, f'broken link {m.group(1)}')
                continue
            if anchor and dest.endswith('.md') and anchor not in anchors(dest):
                report(p, n, f'missing anchor {m.group(1)}')
            if is_raw(dest):
                cited.add(os.path.relpath(dest, ROOT))
                q = re.search(r'\s—\s"([^"]+)"\s*$', raw) if d else None
                body = ' '.join(open(dest, encoding='utf-8').read().split()).lower() if q else ''
                if q and ' '.join(q.group(1).split()).lower() not in body:
                    report(p, n, f'quote not found in {os.path.relpath(dest, ROOT)}')
            if dest != p:
                (listed if fm.get('type') == 'index' else inbound).setdefault(dest, set()).add(p)
    for k in sorted(refs - defs):
        report(p, 1, f'footnote [^{k}] has no definition')
    if not wiki_page:
        continue
    kind = fm.get('type')
    keys = ['type', 'created', 'updated'] if kind == 'index' else PAGE_KEYS
    missing = [k for k in keys if k not in fm]
    if kind == 'index' and 'partition' not in fm and 'scope' not in fm:
        missing.append('partition or scope')
    if missing:
        report(p, 1, f'missing frontmatter: {", ".join(missing)}')
    if kind not in TYPES:
        report(p, 1, f'unknown type: {kind}')
    if kind in ('index', 'workflow') or 'sources' not in fm:
        continue
    declared = set(re.findall(r'[^\[\],\s]+', fm['sources']))
    for s in sorted(cited - declared):
        report(p, 1, f'cites {s} but sources: omits it')
    for s in sorted(declared - cited):
        report(p, 1, f'sources: lists {s} but the page never cites it')

for p in pages:
    if fms[p].get('type') == 'index':
        continue
    if not inbound.get(p):
        report(p, 1, 'orphan: no inbound link from a non-index page')
    index = os.path.join(WIKI, os.path.relpath(p, WIKI).split(os.sep)[0], 'index.md')
    if index not in listed.get(p, set()):
        report(p, 1, f'not listed in {os.path.relpath(index, ROOT)}')

git = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=MDR', 'HEAD', '--',
                      'wiki/*/raw/*'], cwd=ROOT, capture_output=True, text=True)
if git.returncode == 0:
    for f in git.stdout.split():
        report(os.path.join(ROOT, f), 1, 'raw file modified, deleted, or renamed (AGENTS.md §1)')

print('\n'.join(findings) or 'check-wiki: no findings')
sys.exit(1 if findings else 0)

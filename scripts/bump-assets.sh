#!/usr/bin/env bash
# Stamp every local asset reference with ?v=<hash of THAT FILE>.
#
# GitHub Pages serves assets with cache-control: max-age=600, which is long enough
# for someone to load a new page against a cached style.css or nav.js and see, say,
# a menu missing its newest link. The query string changes exactly when the file
# changes, so the browser refetches then and only then.
#
# Per file, deliberately. This used to be one hash of every asset concatenated, which
# meant editing one byte of lead.js handed all 1,628 references on the site a new URL:
# every visitor lost their whole cache, and Googlebot had to re-download all 119 KB of
# JS and CSS for every page it looked at. Crawl stats showed the damage — 62% of a
# 90-day budget of 80 crawl requests went on "page resource load", 66% of it
# JavaScript, while 244 pages sat undiscovered. On a site Google already crawls
# grudgingly, spending the budget re-fetching unchanged assets is the one part of that
# we control.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import hashlib, pathlib, re

root = pathlib.Path('.')

# hash each asset once: assets/nav.js -> 8 hex chars of its own content
digests = {}
for f in sorted(root.glob('assets/*')):
    if f.is_file() and f.suffix in ('.js', '.css', '.json'):
        digests[f.as_posix()] = hashlib.sha1(f.read_bytes()).hexdigest()[:8]

ref = re.compile(r'(?P<a>(?:src|href)=")(?P<up>(?:\.\./)*)(?P<p>assets/[^"?]+)(?:\?v=[^"]*)?"')

def stamp(m):
    d = digests.get(m.group('p'))
    tail = f'?v={d}' if d else ''          # unknown file: leave it unstamped
    return f'{m.group("a")}{m.group("up")}{m.group("p")}{tail}"'

pages = changed = 0
for f in root.rglob('*.html'):
    if '.git' in f.parts:
        continue
    pages += 1
    s = f.read_text()
    new = ref.sub(stamp, s)
    if new != s:
        f.write_text(new)
        changed += 1

print(f'stamped {changed} of {pages} pages · {len(digests)} assets hashed individually')
PY

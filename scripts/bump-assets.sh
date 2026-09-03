#!/usr/bin/env bash
# Stamp every local asset reference with ?v=<hash of the assets themselves>.
#
# GitHub Pages serves assets with cache-control: max-age=600, which is long enough
# for someone to load a new page against a cached style.css or nav.js and see, say,
# a menu missing its newest link.
#
# The version is a hash of assets/ CONTENT, not the git sha — a sha isn't knowable
# until after the commit, and content hashing means the query string changes exactly
# when the assets change and not otherwise.
set -euo pipefail
cd "$(dirname "$0")/.."
V=$(cat assets/*.css assets/*.js | shasum | cut -c1-8)
python3 - "$V" <<'PY'
import sys, pathlib, re
v = sys.argv[1]; n = 0
for f in pathlib.Path('.').glob('*.html'):
    s = f.read_text(); orig = s
    s = re.sub(r'(?P<a>(?:src|href)=")(?P<p>assets/[^"?]+)(?:\?v=[^"]*)?"',
               lambda m: f'{m.group("a")}{m.group("p")}?v={v}"', s)
    if s != orig:
        f.write_text(s); n += 1
print(f'stamped {n} pages with ?v={v}')
PY

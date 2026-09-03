#!/usr/bin/env bash
# Stamp every local asset reference with ?v=<git-sha>, so a deploy can never be
# half-applied by a browser holding a cached style.css or nav.js.
# GitHub Pages serves assets with cache-control: max-age=600, which is otherwise
# long enough for people to see a new page with the old menu.
set -euo pipefail
cd "$(dirname "$0")/.."
V=$(git rev-parse --short HEAD 2>/dev/null || date +%s)
python3 - "$V" <<'PY'
import sys, pathlib, re
v = sys.argv[1]
n = 0
for f in pathlib.Path('.').glob('*.html'):
    s = f.read_text(); orig = s
    # src="assets/x.js" or href="assets/x.css", with or without an existing ?v=
    s = re.sub(r'(?P<a>(?:src|href)=")(?P<p>assets/[^"?]+)(?:\?v=[^"]*)?"',
               lambda m: f'{m.group("a")}{m.group("p")}?v={v}"', s)
    if s != orig:
        f.write_text(s); n += 1
print(f'stamped {n} pages with ?v={v}')
PY

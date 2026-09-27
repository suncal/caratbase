#!/usr/bin/env python3
"""Syntax-check every inline script and JSON-LD block in the generated site.

A broken inline script fails silently: the page renders, the console error is
invisible unless you look, and the calculator on it simply never runs. That is
exactly how a stray apostrophe shipped a dead class-ring page — the generator was
happy, the HTML was valid, and only the tool was broken.

Run after the generators, before bump-assets. Exits non-zero on the first problem so
it can gate a build.
"""
import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
INLINE = re.compile(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', re.S)


def main():
    pages = sorted(p for p in ROOT.rglob('*.html')
                   if '.git' not in p.parts and 'node_modules' not in p.parts)
    js_ok = js_bad = ld_ok = ld_bad = 0
    problems = []

    with tempfile.TemporaryDirectory() as tmp:
        scratch = pathlib.Path(tmp) / 'block.js'
        for page in pages:
            rel = page.relative_to(ROOT)
            html = page.read_text(encoding='utf-8', errors='replace')
            for attrs, body in INLINE.findall(html):
                if not body.strip():
                    continue
                if 'ld+json' in attrs:
                    try:
                        json.loads(body)
                        ld_ok += 1
                    except Exception as e:
                        ld_bad += 1
                        problems.append('%s  JSON-LD: %s' % (rel, e))
                    continue
                scratch.write_text(body, encoding='utf-8')
                r = subprocess.run(['node', '--check', str(scratch)],
                                   capture_output=True, text=True)
                if r.returncode == 0:
                    js_ok += 1
                else:
                    js_bad += 1
                    detail = [ln for ln in r.stderr.splitlines() if 'Error' in ln]
                    problems.append('%s  JS: %s' % (rel, detail[0] if detail else 'syntax error'))

    print('pages %d · inline JS %d ok / %d bad · JSON-LD %d ok / %d bad'
          % (len(pages), js_ok, js_bad, ld_ok, ld_bad))
    for p in problems:
        print('  FAIL', p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())

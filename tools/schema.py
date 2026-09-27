#!/usr/bin/env python3
"""Structured data for the hand-written static pages.

Pages built by tools/design/pages.py get their schema from shell(); the long-tail
pages get theirs from genpages.write(). The remaining root pages are hand-written
HTML that nothing regenerates, so this injects their JSON-LD instead.

Writes one marked block per page and replaces it on re-run, so it is idempotent and
never touches schema that was authored by hand (index.html's WebSite/Organization
block, for example, is left exactly as it is).

Run after pages.py and before bump-assets.sh.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://caratbase.com'
MARK = 'data-cb="auto"'

# name -> (breadcrumb label, is it an interactive tool)
PAGES = {
    'value.html':      ('Diamond & jewelry valuation', True),
    'gemstone.html':   ('Gemstone values', True),
    'metals.html':     ('Gold & metal prices', True),
    'budget.html':     ('Diamond budget calculator', True),
    'stamp.html':      ('Hallmark lookup', True),
    'size.html':       ('Diamond size chart', True),
    'ring-size.html':  ('Ring size converter', True),
    'measure.html':    ('Measure from a photo', True),
    'vault.html':      ('My vault', True),
    'widgets.html':    ('Free jewelry widgets', False),
    'methodology.html': ('How we value', False),
    'privacy.html':    ('Privacy', False),
    'terms.html':      ('Terms', False),
    'disclaimer.html': ('Disclaimer', False),
}


def meta(html, attr, key):
    m = re.search(r'<meta ' + attr + r'="' + key + r'" content="(.*?)">', html, re.S)
    return m.group(1) if m else ''


def build(name, label, is_tool, html):
    graph = [{
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": label, "item": BASE + "/" + name},
        ]}]
    if is_tool:
        graph.append({
            "@context": "https://schema.org", "@type": "WebApplication",
            "name": label,
            "url": BASE + "/" + name,
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript",
            "description": meta(html, 'name', 'description'),
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "publisher": {"@type": "Organization", "name": "CaratBase", "url": BASE + "/"},
        })
    return ('<script type="application/ld+json" ' + MARK + '>'
            + json.dumps(graph, separators=(',', ':')) + '</script>')


def main():
    check = '--check' in sys.argv
    changed = 0
    for name, (label, is_tool) in PAGES.items():
        p = ROOT / name
        if not p.exists():
            print('missing:', name)
            continue
        html = p.read_text(encoding='utf-8')
        block = build(name, label, is_tool, html)

        existing = re.search(r'<script type="application/ld\+json" ' + re.escape(MARK) + r'>.*?</script>',
                             html, re.S)
        if existing:
            if existing.group(0) == block:
                continue
            new = html.replace(existing.group(0), block, 1)
        else:
            if '</head>' not in html:
                print('no </head>:', name)
                continue
            new = html.replace('</head>', block + '\n</head>', 1)

        changed += 1
        print(('would update ' if check else 'updated ') + name)
        if not check:
            p.write_text(new, encoding='utf-8')
    print('schema:', changed, 'page(s)', '(check only)' if check else 'written')
    return 0


if __name__ == '__main__':
    sys.exit(main())

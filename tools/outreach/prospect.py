#!/usr/bin/env python3
"""Find link prospects: resource pages that already link to jewelry tools.

The site's bottleneck is referring domains, not content. The cheapest links to earn
are on pages that have already decided to link to calculators like ours — resource
lists, jeweler "useful links" pages, wedding-planning guides. Two angles:

  BROKEN  the page links to a tool that now 404s. Highest conversion rate in link
          building, because you are fixing their page, not asking for a favor.
  LIVE    the page links to working competitor tools. Lower hit rate, but these are
          pages whose owner has already shown they link out to this exact category.

Politeness: one request at a time with a delay, a real User-Agent, robots.txt
respected per host, and a hard cap on pages fetched. This is prospecting at the scale
of an afternoon's manual research, not crawling.

    python3 tools/outreach/prospect.py --max 60 --out prospects.csv
"""
import argparse
import csv
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import pathlib
import urllib.robotparser
from html.parser import HTMLParser

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/125 Safari/537.36')
DELAY = 1.5

# The searches that produced the shipped candidate list. Kept so the list can be
# regrown later with a real search tool.
SEED_QUERIES = [
    'jewelry "useful links" ring size chart',
    'jeweler resources page "ring size" converter link',
    '"diamond education" resources links page jeweler',
    'wedding planning resources "ring size chart" link',
    '"helpful links" jewelry appraisal calculator',
    'jewelry blog "resources" "gold calculator" link',
    '"ring sizer" "print" resources page links',
    'gemology resources links "price guide" tools',
    '"links we like" jewelry OR diamond OR gemstone',
    'antique jewelry "useful resources" hallmark links',
]

# Tool-ish destinations: a page linking to these is in our category.
CATEGORY = re.compile(
    r'(ring.?siz|carat|diamond|gemston|hallmark|gold.?(price|calc)|jewel|melt.?value|'
    r'birthstone|apprais|pennyweight|karat)', re.I)

SKIP_HOST = re.compile(
    r'(facebook|twitter|x\.com|instagram|pinterest|linkedin|youtube|tiktok|reddit|'
    r'google|bing|duckduckgo|amazon|etsy|ebay|wikipedia|archive\.org|caratbase)', re.I)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.title = ''
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for k, v in attrs:
                if k == 'href' and v:
                    self.hrefs.append(v)
        elif tag == 'title':
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and len(self.title) < 200:
            self.title += data.strip()


def get(url, timeout=20, method='GET'):
    req = urllib.request.Request(url, headers={'User-Agent': UA}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = b'' if method == 'HEAD' else r.read(400_000)
        return r.status, r.geturl(), body


_robots = {}


def allowed(url):
    """Honor robots.txt per host. A host we cannot read robots for is treated as
    allowed, which matches what a browser would do."""
    p = urllib.parse.urlparse(url)
    root = p.scheme + '://' + p.netloc
    if root not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(root + '/robots.txt')
        try:
            rp.read()
        except Exception:
            rp = None
        _robots[root] = rp
    rp = _robots[root]
    if rp is None:
        return True
    try:
        return rp.can_fetch(UA, url)
    except Exception:
        return True


def candidates(path):
    """Candidate URLs, one per line, '#' for comments.

    Discovery deliberately lives outside this script: DuckDuckGo's HTML endpoint
    serves an anti-bot page to anything without a browser, and hammering a search
    engine is both rude and fragile. Collect candidates with a real search tool,
    paste them into a file, and let this do the link analysis."""
    out = []
    for line in pathlib.Path(path).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#') and line.startswith('http'):
            if not SKIP_HOST.search(line):
                out.append(line)
    return out


def _status(url, method):
    try:
        st, _, _ = get(url, timeout=12, method=method)
        return st
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0                            # unreachable: not evidence of a dead link


def link_status(url):
    """Status of an outbound link, conservative about calling anything dead.

    We are going to write to a stranger and tell them a link on their page is
    broken, so a false positive costs credibility. Two rules earn that confidence:
    a HEAD 404 is always re-checked with a GET (plenty of hosts 404 HEAD and serve
    the page fine), and 403 is never treated as broken — that is a bot block, and
    the link works perfectly for the humans reading their page."""
    st = _status(url, 'HEAD')
    if st in (403, 405, 0) or st in (404, 410):
        st = _status(url, 'GET')            # confirm with a real request
        time.sleep(0.3)
    return st


def examine(page_url, checked, budget):
    """Fetch one candidate page and report category links, broken ones first."""
    if not allowed(page_url):
        return None
    try:
        st, final, body = get(page_url)
    except Exception:
        return None
    if st != 200:
        return None

    p = Links()
    try:
        p.feed(body.decode('utf-8', 'replace'))
    except Exception:
        pass

    host = urllib.parse.urlparse(final).netloc
    cat, broken = [], []
    for href in p.hrefs:
        full = urllib.parse.urljoin(final, href)
        if not full.startswith('http'):
            continue
        h = urllib.parse.urlparse(full).netloc
        if h == host or SKIP_HOST.search(full):
            continue
        if not CATEGORY.search(full):
            continue
        cat.append(full)

    # Only spend link checks where there is something to find.
    for link in cat[:budget]:
        if link in checked:
            st = checked[link]
        else:
            st = link_status(link)
            checked[link] = st
            time.sleep(0.4)
        if st in (404, 410):            # confirmed by GET in link_status
            broken.append(link)

    if not cat:
        return None
    return {
        'url': final,
        'domain': host,
        'title': p.title[:120],
        'category_links': len(cat),
        'broken_links': len(broken),
        'broken_example': broken[0] if broken else '',
        'angle': 'BROKEN — offer ours as the replacement' if broken
                 else 'LIVE — already links to tools in our category',
        'pitch_page': ('https://caratbase.com/ring-size.html' if re.search(r'ring.?siz', ' '.join(cat), re.I)
                       else 'https://caratbase.com/scrap-gold-calculator.html' if re.search(r'gold|melt|karat', ' '.join(cat), re.I)
                       else 'https://caratbase.com/value.html'),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--urls', required=True, help='file of candidate URLs, one per line')
    ap.add_argument('--max', type=int, default=60, help='max candidate pages to fetch')
    ap.add_argument('--link-budget', type=int, default=8, help='links to status-check per page')
    ap.add_argument('--out', default='tools/outreach/prospects.csv')
    a = ap.parse_args()

    seen, rows, checked = set(), [], {}
    for url in candidates(a.urls):
        if len(seen) >= a.max:
            break
        key = urllib.parse.urlparse(url).netloc + urllib.parse.urlparse(url).path
        if key in seen:
            continue
        seen.add(key)
        r = examine(url, checked, a.link_budget)
        if r:
            rows.append(r)
            print('  [%s] %-34s %d category links, %d broken' % (
                'BROKEN' if r['broken_links'] else ' live ',
                r['domain'], r['category_links'], r['broken_links']), file=sys.stderr)
        else:
            print('  [  --  ] %-34s no category links / not fetchable' % (
                urllib.parse.urlparse(url).netloc,), file=sys.stderr)
        time.sleep(DELAY)

    # Broken-link targets first: those are the ones worth writing to by hand.
    rows.sort(key=lambda r: (-r['broken_links'], -r['category_links']))
    if rows:
        with open(a.out, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    print('\n%d prospects -> %s  (%d with broken links)' % (
        len(rows), a.out, sum(1 for r in rows if r['broken_links'])))
    return 0


if __name__ == '__main__':
    sys.exit(main())

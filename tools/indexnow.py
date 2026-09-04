#!/usr/bin/env python3
"""
Submit every URL to IndexNow.

Google does not support IndexNow, but Bing, Yandex, Seznam and Naver do — and Bing is what
powers DuckDuckGo and ChatGPT's search. Those engines will crawl a submitted URL within hours
instead of waiting weeks to discover it, which makes this the only genuinely fast indexing
lever available without spending anything.

Run after every deploy. Submitting unchanged URLs repeatedly is discouraged, so this only
sends what the sitemap says changed today.
"""
import json, pathlib, re, sys, urllib.request, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = 'caratbase.com'
ENDPOINT = 'https://api.indexnow.org/IndexNow'

keys = list(ROOT.glob('*.txt'))
keys = [k for k in keys if re.fullmatch(r'[0-9a-f]{32}', k.stem)]
if not keys:
    sys.exit('No IndexNow key file found in the site root.')
KEY = keys[0].stem

sitemap = (ROOT / 'sitemap.xml').read_text()
urls = re.findall(r'<loc>([^<]+)</loc>', sitemap)

only_changed = '--all' not in sys.argv
if only_changed:
    today = datetime.date.today().isoformat()
    blocks = re.findall(r'<url>.*?</url>', sitemap, re.S)
    urls = [re.search(r'<loc>([^<]+)</loc>', b).group(1) for b in blocks
            if today in b] or urls

payload = {'host': HOST, 'key': KEY,
           'keyLocation': f'https://{HOST}/{KEY}.txt',
           'urlList': urls[:10000]}

req = urllib.request.Request(ENDPOINT, method='POST',
    data=json.dumps(payload).encode(),
    headers={'Content-Type': 'application/json; charset=utf-8'})
try:
    with urllib.request.urlopen(req, timeout=45) as r:
        print(f'IndexNow: submitted {len(payload["urlList"])} URLs — HTTP {r.status}')
        print('  200 accepted · 202 accepted, key validating · 4xx see docs')
except urllib.error.HTTPError as e:
    print(f'IndexNow: HTTP {e.code} — {e.read()[:300].decode(errors="replace")}')
    sys.exit(1 if e.code >= 500 else 0)

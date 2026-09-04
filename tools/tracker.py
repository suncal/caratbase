#!/usr/bin/env python3
"""
Competitive tracker.

Watches the sites that currently rank for our keywords and records what changes: page size,
word count, and — the part that actually matters — which ad networks and affiliate programmes
they wire in. Today not one of them monetises beyond AdSense, which is the whole basis of our
revenue advantage. This exists so we find out the week that stops being true, rather than a
year later.

  python3 tools/tracker.py            # check and append to tools/tracker-history.json
  python3 tools/tracker.py --diff     # ...and print what changed since last run
"""
import json, pathlib, re, ssl, sys, urllib.request, datetime

ROOT = pathlib.Path(__file__).resolve().parent
HIST = ROOT / 'tracker-history.json'
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/120.0 Safari/537.36'}

SITES = [
    ('goldpricez',    'https://goldpricez.com/us/gram'),
    ('meltvalue',     'https://meltvalue.com/gold-price-per-gram'),
    ('goldtoolkit',   'https://goldtoolkit.com/calculators/gold-calculator/'),
    ('ringsizes.biz', 'https://www.ringsizes.biz/'),
    ('ringsize.org',  'https://www.ringsize.org/'),
    ('omnicalculator','https://www.omnicalculator.com/everyday-life/ring-size'),
]

SIGNALS = {
    'adsense':        r'adsbygoogle|googlesyndication|ca-pub-\d+',
    'ad_manager':     r'securepubads|googletagservices',
    'ezoic':          r'ezoic|ezojs',
    'mediavine':      r'mediavine',
    'raptive':        r'adthrive|raptive',
    'amazon_affil':   r'amzn\.to|tag=[a-z0-9\-]+-20|amazon-adsystem',
    'cj_impact_awin': r'awin1\.com|anrdoezrs|dpbolvw|jdoqocy|prf\.hn|impact-ad',
    'shareasale':     r'shareasale',
    'email_capture':  r'type=["\']email["\']',
    'camera_input':   r'getUserMedia|mediaDevices|capture=',
    'photo_upload':   r'type=["\']file["\']',
    'canvas':         r'<canvas',
    'localstorage':   r'localStorage',
    'schema':         r'application/ld\+json',
}

def fetch(url):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=30, context=CTX
    ).read().decode('utf-8', 'replace')

def snapshot():
    out = {}
    for name, url in SITES:
        try:
            html = fetch(url)
        except Exception as e:
            out[name] = {'error': str(e)[:80]}
            continue
        text = re.sub(r'<[^>]+>', ' ',
               re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S | re.I))
        out[name] = {
            'kb': len(html) // 1024,
            'words': len(text.split()),
            'inputs': len(re.findall(r'<input', html, re.I)),
            'signals': sorted(k for k, p in SIGNALS.items() if re.search(p, html, re.I)),
            'adsense_id': (re.search(r'ca-pub-(\d+)', html) or [None, None])[1],
        }
    return {'date': datetime.date.today().isoformat(), 'sites': out}

def main():
    hist = json.loads(HIST.read_text()) if HIST.exists() else []
    snap = snapshot()

    if '--diff' in sys.argv and hist:
        prev = hist[-1]['sites']
        print(f"Changes since {hist[-1]['date']}:\n")
        any_change = False
        for name, cur in snap['sites'].items():
            old = prev.get(name, {})
            if 'error' in cur or 'error' in old:
                continue
            gained = set(cur['signals']) - set(old.get('signals', []))
            lost   = set(old.get('signals', [])) - set(cur['signals'])
            dw = cur['words'] - old.get('words', cur['words'])
            bits = []
            if gained: bits.append('ADDED ' + ', '.join(sorted(gained)))
            if lost:   bits.append('removed ' + ', '.join(sorted(lost)))
            if abs(dw) > 150: bits.append(f'{dw:+d} words')
            if bits:
                any_change = True
                print(f'  {name:<16} {" · ".join(bits)}')
        if not any_change:
            print('  nothing material changed')
        print()

    for name, d in snap['sites'].items():
        if 'error' in d:
            print(f'  {name:<16} unreachable ({d["error"][:40]})'); continue
        mon = [s for s in d['signals'] if s in
               ('adsense','ad_manager','ezoic','mediavine','raptive',
                'amazon_affil','cj_impact_awin','shareasale')]
        print(f'  {name:<16} {d["kb"]:>4}KB {d["words"]:>6}w  inputs:{d["inputs"]:<3} '
              f'money:{",".join(mon) if mon else "NONE"}')

    hist.append(snap)
    HIST.write_text(json.dumps(hist[-60:], indent=1))
    print(f'\n  recorded {snap["date"]} — {len(hist)} snapshots on file')

if __name__ == '__main__':
    main()

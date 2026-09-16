#!/usr/bin/env python3
"""
Create the CaratBase jeweller-widget campaign in Instantly (v2 API).

    INSTANTLY_API_KEY=... python3 tools/outreach/instantly_load.py            # create, paused
    INSTANTLY_API_KEY=... python3 tools/outreach/instantly_load.py --leads leads.csv

Creates the 3-step sequence from jeweler-widget-sequence.md, attached to ONE warmed inbox at
40 sends/day, stop-on-reply, open/link tracking off (plain-text look). The campaign is left
PAUSED — activate it from the Instantly UI once leads are loaded and you have eyeballed one.

leads.csv columns: email, first_name, company_name, website, platform, personal
  personal = the one specific thing noticed on their site (a collection, a ring). Required —
  the first line of email 1 is built on it, and a blank one reads as spam.
"""
import csv, json, os, sys, urllib.request

KEY = os.environ.get('INSTANTLY_API_KEY') or sys.exit('set INSTANTLY_API_KEY')
API = 'https://api.instantly.ai/api/v2'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
INBOX = os.environ.get('INSTANTLY_INBOX', 'david@veloexa.org')
NAME = 'CaratBase — jeweller widgets'

def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization': 'Bearer ' + KEY, 'User-Agent': UA, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{method} {path} -> HTTP {e.code}: {e.read().decode()[:300]}')

def html(text):
    return ''.join(f'<div>{line or "<br>"}</div>' for line in text.strip('\n').split('\n'))

STEPS = [
  (0, 'ring sizer for {{website}}', """Hi {{first_name}},

I was on {{website}} looking at {{personal}} and noticed there's no ring size finder on the site. Every jeweller I talk to says "what size am I?" is their most common email.

I built a free one. It converts US/UK/EU/Indian sizes, finds a size from a ring's inside diameter or a finger measurement, and matches your brand colour. It's two lines of code:

https://caratbase.com/widgets.html

No sign-up, nothing to pay, and it doesn't collect anything about your visitors. The only thing it asks is a small "powered by" line underneath.

If you'd like it on the site and don't have someone to paste the code, reply and I'll tell you exactly where it goes for {{platform}}.

Sunny
CaratBase"""),
  (4, 're: ring sizer for {{website}}', """{{first_name}} — one more thing on this, then I'll leave you alone.

There's also a diamond size chart (any carat in any shape, drawn true to scale on a finger) and a live gold calculator for "we buy gold" pages. Same two lines, same terms: free, no sign-up.

https://caratbase.com/widgets.html

If a ring sizer isn't useful to you, no need to reply.

Sunny"""),
  (6, 'last one', """Hi {{first_name}} — closing the loop. If you ever want the free ring sizer for {{website}}, the code is at caratbase.com/widgets.html and it takes about a minute.

All the best with the shop.

Sunny"""),
]

def main():
    existing = [c for c in call('GET', '/campaigns?limit=100').get('items', []) if c['name'] == NAME]
    if existing:
        cid = existing[0]['id']; print('campaign exists:', cid)
    else:
        body = {
          'name': NAME,
          'email_list': [INBOX],
          'daily_limit': 40,
          'stop_on_reply': True,
          'stop_on_auto_reply': True,
          'open_tracking': False,
          'link_tracking': False,
          'text_only': True,
          'campaign_schedule': {'schedules': [{
              'name': 'Business hours', 'timing': {'from': '09:00', 'to': '17:00'},
              'days': {'1': True, '2': True, '3': True, '4': True, '5': True},
              'timezone': 'America/New_York'}]},
          'sequences': [{'steps': [
              {'type': 'email', 'delay': delay,
               'variants': [{'subject': subj, 'body': html(text)}]}
              for delay, subj, text in STEPS]}],
        }
        c = call('POST', '/campaigns', body); cid = c['id']
        print('created campaign:', cid, '(paused)')

    if '--leads' in sys.argv:
        path = sys.argv[sys.argv.index('--leads') + 1]
        rows = list(csv.DictReader(open(path)))
        need = {'email', 'first_name', 'company_name', 'website', 'platform', 'personal'}
        missing = need - set(rows[0].keys()) if rows else need
        if missing: sys.exit(f'leads.csv missing columns: {sorted(missing)}')
        bad = [r['email'] for r in rows if not r['personal'].strip()]
        if bad: sys.exit(f'{len(bad)} leads have an empty "personal" field — fill them or drop them: {bad[:5]}')
        n = 0
        for r in rows:
            call('POST', '/leads', {
              'campaign': cid, 'email': r['email'].strip(), 'first_name': r['first_name'].strip(),
              'company_name': r['company_name'].strip(), 'website': r['website'].strip(),
              'custom_variables': {'platform': r['platform'].strip(), 'personal': r['personal'].strip()},
              'skip_if_in_workspace': True})
            n += 1
        print(f'added {n} leads')
    print('Next: open the campaign in Instantly, send yourself one test, then Activate.')

if __name__ == '__main__':
    main()

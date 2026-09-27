#!/usr/bin/env python3
"""Issue, list and revoke widget licenses.

Minting is a deliberate manual step. There is no payment provider wired up, so the honest
flow is: money arrives however it arrives, then you issue a key. When a provider does
exist, its webhook can call the same admin endpoint and this script stops being the only
way in.

The admin key is never passed on the command line — it would land in your shell history.
Put it in the environment or in a file this repo ignores:

    export CARATBASE_DASH_KEY=...          # or
    echo '...' > ~/.caratbase_dash_key

Usage:
    python3 tools/licenses.py new  --domain ringsmith.co.uk --email hi@ringsmith.co.uk
    python3 tools/licenses.py new  --domain x.com --plan pro --days 365 --notes "paid 1yr"
    python3 tools/licenses.py list
    python3 tools/licenses.py revoke --key cb_live_...
    python3 tools/licenses.py check --key cb_live_... --domain ringsmith.co.uk
"""
import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = os.environ.get('CARATBASE_API',
                     'https://caratbase-analytics.sunnyatlanta20.workers.dev')
UA = {'User-Agent': 'caratbase-licenses/1.0', 'content-type': 'application/json'}


def dash_key():
    k = os.environ.get('CARATBASE_DASH_KEY')
    if k:
        return k.strip()
    f = pathlib.Path.home() / '.caratbase_dash_key'
    if f.exists():
        return f.read_text().strip()
    sys.exit('No admin key. Set CARATBASE_DASH_KEY or write ~/.caratbase_dash_key')


def post(payload):
    url = API + '/api/licenses?key=' + urllib.parse.quote(dash_key())
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=UA,
                                 method='POST')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')[:200]
        sys.exit('HTTP %s from the worker: %s' % (e.code, body))
    except Exception as e:
        sys.exit('Could not reach the worker: %s' % e)


def cmd_new(a):
    payload = {'action': 'create', 'domain': a.domain, 'plan': a.plan}
    if a.email:
        payload['email'] = a.email
    if a.notes:
        payload['notes'] = a.notes
    if a.days:
        payload['expires'] = int(time.time() * 1000) + a.days * 86400 * 1000
    d = post(payload)
    if not d.get('ok'):
        sys.exit('Refused: %s' % d.get('reason', d))
    print('key     ', d['key'])
    print('domain  ', d['domain'])
    print('plan    ', d['plan'])
    if a.days:
        print('expires  in %d days' % a.days)
    print()
    print('Give them this, and tell them to add it to the widget div:')
    print('  <div class="caratbase-widget" data-widget="ring-size" data-key="%s"></div>' % d['key'])


def cmd_list(_a):
    rows = post({'action': 'list'})
    if not rows:
        print('no licenses issued yet')
        return
    print('%-34s %-26s %-6s %-8s %s' % ('key', 'domain', 'plan', 'status', 'issued'))
    for r in rows:
        issued = time.strftime('%Y-%m-%d', time.gmtime((r.get('created') or 0) / 1000))
        exp = r.get('expires')
        if exp and exp < time.time() * 1000:
            r['status'] = r['status'] + '/exp'
        print('%-34s %-26s %-6s %-8s %s' % (
            r['key'], r['domain'][:26], r['plan'], r['status'], issued))
    print('\n%d license(s)' % len(rows))


def cmd_state(a, action):
    d = post({'action': action, 'key': a.key})
    print(json.dumps(d))


def cmd_check(a):
    """Resolve a key exactly as the widget would — no admin key needed."""
    url = (API + '/api/license?key=' + urllib.parse.quote(a.key) +
           '&domain=' + urllib.parse.quote(a.domain))
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        d = json.loads(r.read().decode())
    print(json.dumps(d, indent=2))
    print('\n' + ('licensed — badge removed' if d.get('ok')
                  else 'resolves to FREE (badge stays)%s' %
                       (' — ' + d['reason'] if d.get('reason') else '')))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)

    n = sub.add_parser('new', help='issue a key for one domain')
    n.add_argument('--domain', required=True)
    n.add_argument('--plan', default='pro')
    n.add_argument('--email')
    n.add_argument('--notes')
    n.add_argument('--days', type=int, help='expire after N days (default: never)')

    sub.add_parser('list', help='every key issued')

    for name in ('revoke', 'pause', 'activate'):
        s = sub.add_parser(name)
        s.add_argument('--key', required=True)

    c = sub.add_parser('check', help='resolve a key the way the widget does')
    c.add_argument('--key', required=True)
    c.add_argument('--domain', required=True)

    a = ap.parse_args()
    if a.cmd == 'new':
        cmd_new(a)
    elif a.cmd == 'list':
        cmd_list(a)
    elif a.cmd == 'check':
        cmd_check(a)
    else:
        cmd_state(a, a.cmd)


if __name__ == '__main__':
    main()

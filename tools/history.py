#!/usr/bin/env python3
"""Append today's spot prices to assets/history.json.

A price index is only worth citing once it has history, and we have none: metals.json
keeps today and yesterday and throws the rest away. This starts the series. Run daily
from the metals workflow, right after metals.json is rewritten.

One record per day, keyed by UTC date, so re-running is a no-op and a backfilled or
corrected day overwrites cleanly rather than duplicating.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'assets/metals.json'
DST = ROOT / 'assets/history.json'
METALS = ('gold', 'silver', 'platinum', 'palladium')


def main():
    cur = json.loads(SRC.read_text())
    day = cur['updated'][:10]
    row = {m: round(v, 4) for m, v in cur['perGram'].items() if m in METALS and v}

    if DST.exists():
        hist = json.loads(DST.read_text())
    else:
        hist = {'unit': 'USD per gram',
                'source': 'api.gold-api.com spot, Yahoo Finance futures fallback',
                'license': 'CC BY 4.0 — free to reuse with attribution to CaratBase',
                'days': {}}

    existed = hist['days'].get(day)
    hist['days'][day] = row
    hist['updated'] = cur['updated']
    hist['days'] = dict(sorted(hist['days'].items()))
    hist['count'] = len(hist['days'])
    first, last = next(iter(hist['days'])), day
    hist['range'] = {'from': first, 'to': last}

    DST.write_text(json.dumps(hist, indent=1, sort_keys=False) + '\n')

    # A flat CSV alongside it: people who cite data want to open it in a spreadsheet,
    # and "download the CSV" is a much easier ask than "parse our JSON".
    lines = ['date,' + ','.join(METALS)]
    for d, r in hist['days'].items():
        lines.append(d + ',' + ','.join(str(r.get(m, '')) for m in METALS))
    (ROOT / 'assets/history.csv').write_text('\n'.join(lines) + '\n')

    print(('updated ' if existed else 'appended ') + day + ': ' +
          ', '.join(m + ' $' + str(row[m]) for m in METALS if m in row))
    print('history now spans ' + first + ' to ' + last + ' (' + str(len(hist['days'])) + ' days)')
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Align the data.js spot seeds with assets/metals.json.

spot.js replaces METAL_SPOT at runtime from the Worker (or from metals.json as a
fallback), so these constants only ever show for the moment before that fetch
resolves. They still need to be roughly right: a seed left untouched for weeks
flashes a price several percent off, and the ticker uses it as its fallback if
both live sources fail.

Run after refreshing metals.json, before regenerating pages. Idempotent.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'assets/data.js'


def main() -> int:
    spot = json.loads((ROOT / 'assets/metals.json').read_text())['perGram']
    gold, silver, plat = (round(spot[k], 2) for k in ('gold', 'silver', 'platinum'))

    src = DATA.read_text(encoding='utf-8')
    before = src

    src = re.sub(r'(const GOLD_SPOT_PER_G = )[\d.]+(;)',
                 lambda m: f'{m.group(1)}{gold}{m.group(2)}', src, count=1)
    src = re.sub(r'(const METAL_SPOT = \{gold:)[\d.]+(, platinum:)[\d.]+(, silver:)[\d.]+(\})',
                 lambda m: f'{m.group(1)}{gold}{m.group(2)}{plat}{m.group(3)}{silver}{m.group(4)}',
                 src, count=1)

    if f'{gold}' not in src:
        print('sync_prices: could not find the spot constants in data.js', file=sys.stderr)
        return 1

    if src == before:
        print(f'sync_prices: already current (gold ${gold}/g)')
        return 0

    DATA.write_text(src, encoding='utf-8')
    print(f'sync_prices: seeds set to gold ${gold}, platinum ${plat}, silver ${silver} per gram')
    return 0


if __name__ == '__main__':
    sys.exit(main())

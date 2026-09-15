#!/usr/bin/env python3
"""
Turn the Blue Nile product feed into per-page stone picks.

    python3 tools/feed/build_picks.py <feed.csv|feed.xml|feed.json>   -> assets/picks.json

Heath's brief: point each page at 2–3 specific stones, a mix of natural and lab. For every
carat × shape page this selects, from stones matching the page's grade (G colour or better,
VS2 or better, Very Good cut or better, carat from 5% under to 10% over):
  - the 2 cheapest natural stones
  - the 1 cheapest lab-grown stone
Cheapest-that-qualifies is the honest pick — it is the stone the page's own price range says
is good value, and a reader can see for themselves why it was chosen.

FIELD MAPPING: the feed's column names are unknown until Blake sends it. Edit FIELDS below
to map them; everything else stays the same. Values are normalised (shape names, grades,
'lab'/'natural') so the mapping is the only thing that should ever need touching.
"""
import csv, json, pathlib, re, sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT = ROOT / 'assets' / 'picks.json'

# feed column -> our field. Left side gets edited when the real feed arrives.
FIELDS = {
    'id':      ['id', 'product_id', 'sku', 'stock_id'],
    'shape':   ['shape', 'diamond_shape'],
    'carat':   ['carat', 'carat_weight', 'weight'],
    'color':   ['color', 'colour'],
    'clarity': ['clarity'],
    'cut':     ['cut', 'cut_grade'],
    'price':   ['price', 'sale_price', 'retail_price'],
    'url':     ['url', 'link', 'product_url', 'deeplink'],
    'image':   ['image', 'image_url', 'imageurl', 'thumbnail'],
    'lab':     ['lab_grown', 'labgrown', 'type', 'origin', 'category'],
    'cert':    ['lab', 'certificate', 'grading_lab', 'report'],
}
CTS    = [0.25,0.5,0.75,1,1.25,1.5,2,2.5,3,4,5]
SHAPES = ['Round','Oval','Princess','Cushion','Emerald','Pear','Marquise','Radiant','Asscher','Heart']
COLORS  = ['K','J','I','H','G','F','E','D']
CLARITY = ['SI2','SI1','VS2','VS1','VVS2','VVS1','IF','FL']
CUTS    = ['good','very good','ideal','excellent','astor','true hearts']

def load(path):
    p = pathlib.Path(path); t = p.suffix.lower()
    if t == '.json':
        d = json.loads(p.read_text()); return d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list))
    if t == '.xml':
        root = ET.parse(p).getroot()
        items = root.findall('.//item') or root.findall('.//product') or list(root)
        return [{c.tag.split('}')[-1].lower(): (c.text or '').strip() for c in it} for it in items]
    with p.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter='\t' if t == '.tsv' else ','))

def pick(row, key):
    low = {k.lower().strip(): v for k, v in row.items() if k}
    for name in FIELDS[key]:
        if name in low and str(low[name]).strip(): return str(low[name]).strip()
    return ''

def norm_shape(s):
    s = s.lower()
    for sh in SHAPES:
        if sh.lower() in s: return sh
    return None

def normalise(row):
    shape = norm_shape(pick(row, 'shape'))
    try: carat = float(re.sub(r'[^\d.]', '', pick(row, 'carat')))
    except ValueError: carat = None
    try: price = float(re.sub(r'[^\d.]', '', pick(row, 'price')))
    except ValueError: price = None
    color = pick(row, 'color').upper()[:1]
    clarity = pick(row, 'clarity').upper().replace(' ', '')
    cut = pick(row, 'cut').lower()
    labv = pick(row, 'lab').lower()
    lab = any(w in labv for w in ('lab', 'created', 'grown', 'synthetic'))
    if not (shape and carat and price and pick(row, 'url')): return None
    return dict(id=pick(row, 'id'), shape=shape, carat=carat, color=color, clarity=clarity,
                cut=cut, price=price, url=pick(row, 'url'), image=pick(row, 'image'),
                lab=lab, cert=pick(row, 'cert'))

def qualifies(s, ct):
    return (ct * 0.95 <= s['carat'] <= ct * 1.10
            and s['color'] in COLORS and COLORS.index(s['color']) >= COLORS.index('G')
            and s['clarity'] in CLARITY and CLARITY.index(s['clarity']) >= CLARITY.index('VS2')
            and (not s['cut'] or any(c in s['cut'] for c in CUTS[1:])))

def main(path):
    raw = load(path)
    stones = [x for x in (normalise(r) for r in raw) if x]
    print(f'{len(raw)} rows in feed, {len(stones)} usable stones')
    picks = {}
    for ct in CTS:
        for sh in SHAPES:
            pool = [s for s in stones if s['shape'] == sh and qualifies(s, ct)]
            nat = sorted([s for s in pool if not s['lab']], key=lambda s: s['price'])[:2]
            lab = sorted([s for s in pool if s['lab']], key=lambda s: s['price'])[:1]
            key = f"{ct:g}-carat-{sh.lower()}".replace('.', '-')
            picks[key] = nat + lab
    filled = sum(1 for v in picks.values() if v)
    print(f'{filled}/{len(picks)} pages have picks')
    OUT.write_text(json.dumps({'generated': __import__('datetime').date.today().isoformat(),
                               'pages': picks}, separators=(',', ':')))
    print('wrote', OUT.relative_to(ROOT))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__))

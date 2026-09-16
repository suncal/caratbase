"""Per-page photography via LUMEN cloud. Idempotent: skips files that exist, stops at the
daily budget guard. Re-run tomorrow to finish. Style rules for the whole set: one subject,
warm ivory linen, soft daylight, macro, no text, no hands, no logo — so the pages read as one
collection rather than a stock-photo mix."""
import json, pathlib, subprocess, sys, urllib.request
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
def get(url, timeout=60): return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=timeout)
ROOT = pathlib.Path(__file__).resolve().parents[2]
KEYF = pathlib.Path('/Users/priyankarchakraborty/Trading/lumen/cloud/.owner_key.json')
d = json.loads(KEYF.read_text()); KEY = d.get('key') or list(d.values())[0]
API = 'https://lumen-cloud.sunnyatlanta20.workers.dev'
STYLE = ' Warm ivory linen surface, soft diffused daylight from the left, shallow depth of field, calm cream and warm-gray palette, refined luxury still life, macro lens, no text, no hands, no logo, nothing else in frame.'

GEMS = {
 'ruby': 'a single loose cushion-cut ruby, vivid pigeon-blood red with deep saturation',
 'blue-sapphire': 'a single loose cushion-cut blue sapphire, rich royal blue with velvety saturation',
 'pink-sapphire': 'a single loose oval pink sapphire, clear vivid pink',
 'yellow-sapphire': 'a single loose cushion-cut yellow sapphire, clean bright canary yellow',
 'emerald': 'a single loose emerald-cut emerald, deep vivid green with a soft garden of inclusions',
 'alexandrite': 'a single loose oval alexandrite showing its color change, teal green with a hint of purple-red at the edge',
 'spinel': 'a single loose cushion-cut red spinel, bright cherry red, very clean',
 'paraiba-tourmaline': 'a single loose oval paraiba tourmaline, electric neon turquoise blue glowing from within',
 'tanzanite': 'a single loose cushion-cut tanzanite, deep violet-blue',
 'aquamarine': 'a single loose emerald-cut aquamarine, pale clear sea blue',
 'tourmaline': 'a single loose elongated tourmaline crystal cut, vivid green shading to pink at one end, watermelon coloring',
 'tsavorite-garnet': 'a single loose cushion-cut tsavorite garnet, vivid grass green',
 'garnet': 'a single loose round rhodolite garnet, deep wine red with a purple flash',
 'peridot': 'a single loose oval peridot, bright olive green',
 'amethyst': 'a single loose cushion-cut amethyst, deep royal purple',
 'citrine': 'a single loose oval citrine, warm honey orange-yellow',
 'blue-topaz': 'a single loose emerald-cut swiss blue topaz, clear bright sky blue',
 'imperial-topaz': 'a single loose oval imperial topaz, peachy golden orange',
 'opal-black': 'a single polished black opal cabochon, dark body with vivid red, green and blue play of color',
 'opal-white': 'a single polished white opal cabochon, milky body with soft pastel play of color',
 'jade-jadeite': 'a single polished oval jadeite cabochon, translucent vivid imperial green',
}
SHAPES = {s: f'a single loose {s} cut white diamond, colorless and brilliant, facets catching soft light, standing on its pavilion tip' for s in
          ['round','oval','princess','cushion','emerald','pear','marquise','radiant','asscher','heart']}
SHAPES['round'] = 'a single loose round brilliant cut white diamond, colorless, facets catching soft light, viewed face-up at a slight angle'
KARAT = {
 '24k': 'a small stack of pure 24 karat gold coins and a smooth bar, deep saturated butter-yellow gold',
 '22k': 'two traditional 22 karat gold bangles, rich warm deep yellow gold',
 '18k': 'a classic 18 karat yellow gold wedding band and a slim chain, warm yellow gold',
 '14k': 'a 14 karat gold ring and a delicate chain, slightly paler warm yellow gold',
 '10k': 'a 10 karat gold class ring and a chain, pale yellow gold with a cooler tone',
 '9k':  'a 9 karat gold signet ring and a fine chain, pale light yellow gold',
}
JOBS = [('stones', k, v) for k, v in GEMS.items()] + [('shapes', k, v) for k, v in SHAPES.items()] + [('karat', k, v) for k, v in KARAT.items()]

def gen(prompt):
    req = urllib.request.Request(API + '/generate', data=json.dumps({'prompt': prompt + STYLE, 'mode': 'full'}).encode(),
                                 headers={'Content-Type': 'application/json', 'x-api-key': KEY, 'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=240) as r: return json.load(r)

def main():
    made = 0
    for folder, name, prompt in JOBS:
        out = ROOT / 'assets/img' / folder / f'{name}.jpg'
        if out.exists(): continue
        h = json.load(get(API + '/health', 20))
        if h['fal_spend_today_cents'] + 6 > h['fal_daily_cap_cents']:
            print(f'budget guard reached ({h["fal_spend_today_cents"]}c) — re-run tomorrow'); break
        try:
            r = gen(prompt)
        except Exception as e:
            print(name, 'failed:', str(e)[:80]); continue
        url = r.get('image_url')
        if not url: print(name, 'no image:', r); continue
        raw = get(url, 120).read()
        tmp = out.with_suffix('.raw.jpg'); tmp.write_bytes(raw)
        from PIL import Image
        im = Image.open(tmp).convert('RGB').resize((1000, 1000), Image.LANCZOS)
        im.save(out, quality=82, optimize=True, progressive=True); im.save(out.with_suffix('.webp'), quality=76, method=6)
        tmp.unlink(); made += 1; print(f'{folder}/{name}: ok')
    print(f'{made} images made; {sum(1 for f,n,_ in JOBS if not (ROOT/"assets/img"/f/(n+".jpg")).exists())} remaining')

if __name__ == '__main__': main()

#!/usr/bin/env python3
"""
CaratBase — programmatic long-tail page generator.

The strategy this implements: head terms like "diamond price" are held by retailers with
enormous authority and are not winnable from a new domain. But the specific questions
underneath them — "what is US ring size 7 in UK", "what does 925 mean", "14k gold price per
gram", "how big is a 1.5 carat oval" — are held by thin pages on small sites, and each one
is winnable on its own.

The rule every page here obeys: it must answer its exact question in the first sentence,
with a real number produced by our own engines, and then give the visitor the live tool.
A page that merely restates the question with a keyword swapped is the thing Google's
helpful-content system exists to remove, and building 400 of those would be worse than
building none.
"""
import json, math, pathlib, re, subprocess, shutil, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIRS = ['ring-size', 'hallmark', 'gold-price', 'diamond', 'gemstone']
BASE = 'https://caratbase.com'
TODAY = datetime.date.today().isoformat()

# ---------------------------------------------------------------- data via node
def node_eval(expr, *files):
    """Run an expression against our real engines so pages carry real numbers."""
    src = '\n'.join((ROOT / f).read_text() for f in files)
    src += f'\nconsole.log(JSON.stringify({expr}));\n'
    tmp = ROOT / 'tools' / '_tmp.js'
    tmp.write_text(src)
    out = subprocess.run(['node', str(tmp)], capture_output=True, text=True)
    tmp.unlink(missing_ok=True)
    if out.returncode:
        raise SystemExit('node failed:\n' + out.stderr[:2000])
    return json.loads(out.stdout)

HL = ' style="background:var(--gold-dim);font-weight:600"'

# ---------------------------------------------------------------- table helpers
# A cell or header that starts with '#' is numeric and right-aligned.
NUM = ' class="num"'
def _cell(tag, c):
    c = str(c)
    return f'<{tag}{NUM if c.startswith("#") else ""}>{c.lstrip("#")}</{tag}>'
def tr(cells, hl=False):
    return f'<tr{HL if hl else ""}>' + ''.join(_cell('td', c) for c in cells) + '</tr>'
def tbl(head, rows):
    return ('<div class="table-scroll"><table><thead><tr>'
            + ''.join(_cell('th', h) for h in head)
            + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
def mid(v, lo='retailLow', hi='retailHigh'):
    return (v[lo] + v[hi]) / 2
def pct(a, b):
    return round((a / b - 1) * 100)

# Weight units people actually weigh gold in. Grams per unit.
UNITS = [('gram', 1), ('pennyweight (dwt)', 1.5552), ('tola', 11.6638),
         ('ounce (avoirdupois)', 28.3495), ('troy ounce', 31.1035), ('baht', 15.244),
         ('100 g', 100), ('kilogram', 1000)]

def money(n):
    return '$' + format(int(round(n)), ',')

# ---------------------------------------------------------------- page shell
SHELL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}/{url}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{base}/{url}">
<link rel="stylesheet" href="{up}assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 28 28'><polygon points='19.32,18.72 14,20.32 8.68,18.72 6.32,13.84 8.68,8.96 14,7.36 19.32,8.96 21.68,13.84' fill='%23C9A961' fill-opacity='.2' stroke='%23C9A961' stroke-width='1.4'/><polygon points='16.42,15.06 14,15.79 11.58,15.06 10.5,12.84 11.58,10.62 14,9.89 16.42,10.62 17.5,12.84' fill='%23C9A961' stroke='%238A6420'/></svg>">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<header class="site-head"><div class="wrap head-in">
  <a href="{up}index.html" class="logo"></a><nav class="nav"></nav>
</div></header>
<main class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb">
    <a href="{up}index.html">Home</a> <span>›</span> <a href="{up}{hub}">{hubname}</a>
    <span>›</span> <span>{crumb}</span>
  </nav>
  <div class="tool-hero legal">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
  </div>

  <div class="answer-box">{answer}</div>

  <div class="legal">{body}</div>

  <section class="section" style="padding-top:26px">
    <h2 style="font-size:24px;margin-bottom:6px">{cta_h}</h2>
    <p class="small" style="margin-bottom:16px">{cta_p}</p>
    <a href="{up}{cta_url}" class="btn btn-gold btn-lg">{cta_label}</a>
  </section>

  {related}
</main>
<footer class="site-foot"><div class="wrap foot-in">
  <div>&copy; <span id="yr"></span> CaratBase &mdash; independent jewellery valuation reference.</div>
  <div style="display:flex;gap:20px;flex-wrap:wrap">
    <a href="{up}methodology.html">How we value</a><a href="{up}disclaimer.html">Disclaimer</a>
    <a href="{up}privacy.html">Privacy</a><a href="{up}terms.html">Terms</a></div>
</div><div class="wrap"><p class="disclaimer">{footnote}</p></div></footer>
<script src="{up}assets/data.js"></script>
<script src="{up}assets/analytics.js"></script>
<script src="{up}assets/logo.js"></script>
<script src="{up}assets/nav.js"></script>
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</body></html>
'''

def related_block(title, links, up):
    if not links: return ''
    items = ''.join(
        f'<a href="{up}{u}" class="rel-link">{t}</a>' for t, u in links)
    return (f'<section class="section" style="padding-top:10px">'
            f'<h2 style="font-size:22px;margin-bottom:14px">{title}</h2>'
            f'<div class="rel-grid">{items}</div></section>')

def write(url, **kw):
    p = ROOT / url
    p.parent.mkdir(parents=True, exist_ok=True)
    depth = url.count('/')
    kw.setdefault('up', '../' * depth)
    kw.setdefault('base', BASE)
    # canonical + og:url must match the sitemap, which serves directories as
    # '/slug/' not '/slug/index.html'. Two URLs, one page, one canonical.
    kw['url'] = url.replace('/index.html', '/')
    p.write_text(SHELL.format(**kw))
    return url

# ================================================================ RING SIZES
def _ring_common(rows, r, all_us):
    """Everything computed for one size, shared by the US-number and UK-letter pages."""
    us = float(r['us'])
    spot = json.loads((ROOT / 'assets/metals.json').read_text())['perGram']
    # a window of neighbours, not the whole chart: the full chart lives on the hub
    win = [x for x in rows if abs(float(x['us']) - us) <= 1.5]
    win_rows = [tr([x['us'], x['uk'], x['eu'], x['jp'] or '—', f"#{x['dia']} mm", f"#{x['circ']} mm"],
                   hl=(x['us'] == r['us'])) for x in win]
    byus = {float(x['us']): x for x in rows}
    def at(delta):
        return byus.get(round((us + delta) * 4) / 4)
    up_h, dn_h = at(0.5), at(-0.5)
    step_up = round(up_h['circ'] - r['circ'], 2) if up_h else None
    step_dn = round(r['circ'] - dn_h['circ'], 2) if dn_h else None
    # fit adjustments by band width
    fit_rows = []
    for label, delta in [('Narrow band, under 4 mm', 0), ('Medium band, 4–6 mm', 0.25),
                         ('Wide band, 6 mm and over', 0.5), ('Comfort-fit (domed inside)', -0.25)]:
        x = at(delta)
        if x: fit_rows.append(tr([label, f"US {x['us']}", f"UK {x['uk']}", f"EU {x['eu']}"], hl=(delta == 0)))
    # what a plain band at this size weighs and is worth
    wt = node_eval('[' + ','.join(
        f"{{w:{w},k:{k!r},b:bandWeight({r['dia']},{w},1.6,{k!r})}}"
        for w in [2, 4, 6] for k in ['14K', '18K', 'Platinum']) + ']', 'assets/data.js')
    def metal_val(k, g):
        return g * (spot['platinum'] * 0.95 if k == 'Platinum' else spot['gold'] * {'14K':0.585,'18K':0.75}[k])
    wt_rows = [tr([f"{x['w']} mm {x['k']}", f"#{x['b']['grams']} g", '#' + money(metal_val(x['k'], x['b']['grams']))])
               for x in wt]
    inch_d = r['dia'] / 25.4; inch_c = r['circ'] / 25.4
    # where this size sits
    if us <= 4.5:     place = 'a small size — common for a child, a pinky ring, or a very slim hand'
    elif us <= 7.5:   place = 'in the most common range for women\'s rings; US 6 to 7 covers roughly half of all women'
    elif us <= 9:     place = 'at the upper end of women\'s sizes and the lower end of men\'s; common for a woman\'s thumb or a slim man\'s ring finger'
    elif us <= 11.5:  place = 'in the most common range for men\'s rings; US 9 to 10½ covers most men'
    else:             place = 'a large size, usually a man\'s ring finger or a thumb ring'
    return dict(win_rows=win_rows, fit_rows=fit_rows, wt_rows=wt_rows, step_up=step_up,
                step_dn=step_dn, inch_d=inch_d, inch_c=inch_c, place=place,
                up_h=up_h, dn_h=dn_h, spot=spot)

def _ring_body(r, name, c):
    """The computed sections shared by both page types. `name` is how this page names the size."""
    step = ''
    if c['up_h'] and c['dn_h']:
        step = (f"<p>One half size is a very small step: going up to {c['up_h']['us']} (UK {c['up_h']['uk']}) adds "
                f"{c['step_up']} mm of circumference, and down to {c['dn_h']['us']} (UK {c['dn_h']['uk']}) removes "
                f"{c['step_dn']} mm. Quarter sizes exist and a good jeweller will make one; if you sit "
                f"between two half sizes, choose the smaller for a narrow band and the larger for a wide one.</p>")
    return f"""
    <h2>How to check this is your size</h2>
    <p>The surest way is to measure a ring that already fits the right finger. Lay it flat and
    measure straight across the <strong>inside</strong> of the band. If it reads about
    <strong>{r['dia']} mm</strong> ({c['inch_d']:.3f} in), you are a {name}.</p>
    <p>If you have no ring to hand, wrap a strip of paper around the base of the finger, mark
    where it overlaps, and measure the length. About <strong>{r['circ']} mm</strong> ({c['inch_c']:.2f} in)
    means {name}. Measure at the end of the day, when fingers are at their largest — a ring sized
    on a cold morning will feel tight by evening.</p>
    <p>{name} is {c['place']}.</p>

    <h2>{name} and its neighbours</h2>
    {tbl(['US', 'UK / AU', 'Europe', 'India / Japan', '#Diameter', '#Circumference'], c['win_rows'])}
    {step}
    <p>The <a href="../">full chart</a> covers every size from US 3 to US 16 in all five systems.</p>

    <h2>Adjusting for the band</h2>
    <p>A wide band touches more of the finger and feels tighter at the same measurement, and a
    comfort-fit band (domed on the inside) feels looser. For a finger that measures {r['circ']} mm:</p>
    {tbl(['Band', 'Order', '', ''], c['fit_rows'])}

    <h2>What a plain band in this size weighs</h2>
    <p>Useful if you are buying by weight or checking a quote. A solid band 1.6 mm thick at
    {name}, with the metal alone valued at today's spot price:</p>
    {tbl(['Band', '#Weight', '#Metal value today'], c['wt_rows'])}
    <p>A jeweller's price is well above the metal value — it carries the making, the finish and the
    margin — but the metal figure is the floor the piece can never fall below, and the number a
    scrap buyer starts from.</p>"""

def build_ring_sizes():
    rows = node_eval('RING_SIZES', 'assets/ringdata.js')
    urls = []
    # every size, halves included: 'ring size 6.5 in uk' is searched as often as whole sizes
    all_us = [r for r in rows if (float(r['us'])*2) == int(float(r['us'])*2)]

    for r in all_us:
        us, uk, eu, jp = r['us'], r['uk'], r['eu'], r['jp']
        dia, circ = r['dia'], r['circ']
        slug = f"ring-size/us-{str(us).replace('.','-')}/index.html"
        c = _ring_common(rows, r, all_us)
        near = [x for x in all_us if abs(float(x['us'])-float(us)) <= 2 and x['us'] != us][:6]
        urls.append(write(slug,
          title=f"US Ring Size {us} in UK, EU &amp; India — {uk}, {eu}, {dia}mm | CaratBase",
          desc=f"US ring size {us} is UK size {uk}, EU {eu} and Indian/Japanese size {jp or '—'}. "
               f"Inside diameter {dia}mm, circumference {circ}mm. Band-width adjustments, what a "
               f"band this size weighs, and a true-to-scale sizer.",
          eyebrow='Ring size conversion',
          h1=f"US ring size {us} in UK, Europe and India",
          crumb=f"US {us}", hub='ring-size/', hubname='Ring sizes',
          answer=f"<p><strong>US ring size {us}</strong> is <strong>UK size {uk}</strong>, "
                 f"<strong>European (ISO) size {eu}</strong>"
                 + (f" and <strong>Indian/Japanese size {jp}</strong>" if jp else "")
                 + f". That is an inside diameter of <strong>{dia}&nbsp;mm</strong> and an inside "
                   f"circumference of <strong>{circ}&nbsp;mm</strong>.</p>",
          body=_ring_body(r, f"US {us}", c),
          cta_h='Measure it yourself, right now',
          cta_p='Lay a ring on your screen and match it against circles drawn true to life, '
                'calibrated against any bank card.',
          cta_url='ring-size.html', cta_label='Open the ring sizer',
          related=related_block('Nearby sizes',
            [(f"US size {x['us']} → UK {x['uk']}", f"ring-size/us-{str(x['us']).replace('.','-')}/")
             for x in near], '../../'),
          footnote='Conversions follow the standard published charts and ISO 8653. Individual '
                   'jewellers vary slightly; for an expensive ring, confirm in person. Band weights '
                   f'assume a 1.6 mm thick solid band; metal valued at ${c["spot"]["gold"]:,.2f}/g gold spot.',
          schema=json.dumps({
            "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"What is US ring size {us} in UK sizes?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"US ring size {us} is UK size {uk}. The inside diameter is {dia} mm and the "
                 f"inside circumference is {circ} mm."}},
              {"@type":"Question","name":f"What is the diameter of a US size {us} ring?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"A US size {us} ring has an inside diameter of {dia} mm ({c['inch_d']:.3f} inches)."}},
              {"@type":"Question","name":f"What size should I order for a wide band if I am a US {us}?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"For a band 6 mm or wider, order about half a size up from US {us}. For a 4 to 6 mm "
                 f"band, a quarter size up."}}]})))
    # UK letter pages — the same conversion approached from the other direction
    seen=set()
    for r in rows:
        uk=r['uk']
        if uk in seen: continue
        seen.add(uk)
        slug_uk=re.sub(r'[^a-z0-9]+','-',uk.lower().replace('½','-half')).strip('-')
        c = _ring_common(rows, r, all_us)
        near=[x for x in rows if abs(float(x['us'])-float(r['us']))<=1.5 and x['uk']!=uk][:6]
        urls.append(write(f"ring-size/uk-{slug_uk}/index.html",
          title=f"UK Ring Size {uk} in US &amp; EU — US {r['us']}, {r['dia']}mm | CaratBase",
          desc=f"UK ring size {uk} is US size {r['us']} and European size {r['eu']}. "
               f"Inside diameter {r['dia']}mm. Band-width adjustments, what a band this size "
               f"weighs, and a true-to-scale ring sizer.",
          eyebrow='Ring size conversion',
          h1=f"UK ring size {uk} in US and European sizes",
          crumb=f"UK {uk}", hub='ring-size/', hubname='Ring sizes',
          answer=f"<p><strong>UK ring size {uk}</strong> is <strong>US size {r['us']}</strong> and "
                 f"<strong>European (ISO) size {r['eu']}</strong>. The inside diameter is "
                 f"<strong>{r['dia']}&nbsp;mm</strong> and the circumference "
                 f"<strong>{r['circ']}&nbsp;mm</strong>.</p>"
                 f"<p style=\"margin-top:10px\">The UK, Ireland, Australia and New Zealand share this "
                 f"letter scale. Europe uses the circumference in millimetres directly, which is why "
                 f"the European size and the circumference are the same figure.</p>",
          body=_ring_body(r, f"UK {uk}", c),
          cta_h='Measure it on your screen',
          cta_p='Lay a ring against circles drawn true to life, calibrated with any bank card.',
          cta_url='ring-size.html', cta_label='Open the ring sizer',
          related=related_block('Nearby sizes',
            [(f"UK {x['uk']} → US {x['us']}",
              f"ring-size/uk-{re.sub(r'[^a-z0-9]+','-',x['uk'].lower().replace('½','-half')).strip('-')}/")
             for x in near], '../../'),
          footnote='Conversions follow ISO 8653 and the standard published charts. Band weights '
                   f'assume a 1.6 mm thick solid band; metal valued at ${c["spot"]["gold"]:,.2f}/g gold spot.',
          schema=json.dumps({
            "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"What is UK ring size {uk} in US sizes?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"UK ring size {uk} is US size {r['us']} and European size {r['eu']}, an inside "
                 f"diameter of {r['dia']} mm."}},
              {"@type":"Question","name":f"What is the diameter of a UK size {uk} ring?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"A UK size {uk} ring has an inside diameter of {r['dia']} mm ({c['inch_d']:.3f} inches) "
                 f"and a circumference of {r['circ']} mm."}}]})))
    return urls

# ================================================================ HALLMARKS
def _purity_fraction(s):
    """Pull the metal fraction out of a purity string like '9K · 37.5% gold' or '95% platinum'."""
    m = re.search(r'(\d+(?:\.\d+)?)\s*%', s['purity'])
    if m: return float(m.group(1)) / 100
    m = re.match(r'^(\d{3})$', s['code'])
    return int(m.group(1)) / 1000 if m else None

def build_hallmarks():
    stamps = node_eval('STAMPS', 'assets/data.js')
    spot = json.loads((ROOT / 'assets/metals.json').read_text())['perGram']
    urls = []
    for s in stamps:
        code = s['code']
        slug_code = re.sub(r'[^a-z0-9]+', '-', code.lower()).strip('-')
        slug = f"hallmark/{slug_code}/index.html"
        others = [x for x in stamps if x['code'] != code][:8]
        worth_flag = {'solid':'Solid precious metal','filled':'Partial — low value',
                      'plated':'Plated — no metal value','lab':'Real diamond, weak resale',
                      'none':'No precious metal'}.get(s['value'], '')
        # metal value by weight — only where the stamp states a purity of a metal we price
        metal_key = ('gold' if 'gold' in s['metal'].lower() and s['metal'] != 'Gold or fine silver'
                     else 'silver' if 'silver' in s['metal'].lower()
                     else 'platinum' if 'platinum' in s['metal'].lower() else None)
        frac = _purity_fraction(s) if s['value'] == 'solid' else None
        value_section = ''
        per_g = None
        if metal_key and frac and metal_key in spot and code not in ('BIS', 'LION', 'KP'):
            per_g = spot[metal_key] * frac
            rows = [tr([f"{w} g", '#' + money(per_g*w), f"#{money(per_g*w*0.7)} – {money(per_g*w*0.9)}"])
                    for w in [1, 3, 5, 10, 20, 50]]
            value_section = f"""
    <h2>What {code} is worth by weight, today</h2>
    <p>A piece stamped {code} is {frac*100:.1f}% {metal_key}, so at today's spot price the metal in
    it is worth <strong>${per_g:,.2f} per gram</strong>. A buyer will offer 70–90% of that — they
    carry the refining cost and take a margin — and anything below about 60% is a poor offer.</p>
    {tbl(['Weight', '#Metal value', '#Likely offer'], rows)}
    <p>Weigh the piece without stones if you can. A typical ring is 3–6 g, a 45 cm chain 8–15 g,
    a bangle 15–30 g. Stones, solder and springs add weight that is not {metal_key}.</p>"""
        elif code == '999':
            g999, s999 = spot['gold'] * 0.999, spot['silver'] * 0.999
            value_section = f"""
    <h2>Worth by weight — but which metal?</h2>
    <p>999 is used on both fine gold and fine silver, and the two are worth very different
    amounts: <strong>${g999:,.2f} per gram</strong> if it is gold, <strong>${s999:,.2f} per gram</strong>
    if it is silver. Colour usually settles it; if not, a magnet test rules out neither, but a
    density check or an acid test does.</p>
    {tbl(['Weight', '#If gold', '#If silver'], [tr([f"{w} g", '#' + money(g999*w), '#' + money(s999*w)]) for w in [1,5,10,20,50]])}"""
        elif s['value'] in ('plated', 'none'):
            value_section = f"""
    <h2>What {code} is worth by weight</h2>
    <p>Nothing, as metal. A plated or base-metal piece carries a layer of precious metal measured
    in microns — far too little to recover — and a refiner will not buy it. Whatever value it has
    is as a finished piece of jewellery, a brand, or an antique, not as scrap.</p>"""
        elif s['value'] == 'filled':
            value_section = f"""
    <h2>What {code} is worth by weight</h2>
    <p>A little, but rarely enough to sell. Gold-filled pieces are 5% gold by weight at most,
    bonded to a brass core; a 10 g piece holds perhaps half a gram of gold, and most refiners
    set a minimum batch well above that. Vermeil is sterling silver underneath, which is worth
    scrap silver — about ${spot['silver']*0.925:,.2f} per gram today.</p>"""
        aliases = [a for a in s.get('alias', []) if a.lower() != code.lower()]
        alias_p = (f"<p>You may also see it written as <strong>{'</strong>, <strong>'.join(aliases)}</strong>. "
                   f"They all mean the same thing.</p>") if aliases else ''
        # marks in the same metal family that get confused with this one
        family = [x for x in stamps if x['code'] != code and x['metal'] == s['metal']]
        confuse = ''
        if family:
            confuse = ("<h2>Marks often confused with " + code + "</h2>" +
                       tbl(['Mark', 'Means', 'Worth'], [tr([
                           f"<a href=\"../{re.sub(r'[^a-z0-9]+','-',x['code'].lower()).strip('-')}/\">{x['code']}</a>",
                           x['purity'], {'solid':'Solid metal','filled':'Partial','plated':'Plated only','lab':'Lab diamond','none':'No metal value'}.get(x['value'],'')])
                           for x in family[:8]]))
        urls.append(write(slug,
          title=f"What Does {code} Mean on Jewellery? {s['metal']} — {s['purity']} | CaratBase",
          desc=f"{code} means {s['purity']}. {s['worth'][:100]} "
               + (f"Worth ${per_g:,.2f} per gram today." if per_g else "What it is, and what it is worth."),
          eyebrow='Hallmark meaning',
          h1=f"What does {code} mean on jewellery?",
          crumb=code, hub='hallmark/', hubname='Hallmarks',
          answer=f"<p><strong>{code}</strong> means <strong>{s['purity']}</strong> "
                 f"({s['metal']}). <span class=\"pill\">{worth_flag}</span></p>"
                 f"<p style=\"margin-top:10px\">{s['worth']}"
                 + (f" At today's price the metal is worth about <strong>${per_g:,.2f} per gram</strong>." if per_g else "")
                 + "</p>",
          body=f"""
    <h2>What the mark tells you</h2>
    <p>{s['note']}</p>
    {alias_p}
    {value_section}

    <h2>Is it worth anything?</h2>
    <p>{s['worth']}</p>

    {confuse}

    <h2>Where to find it</h2>
    <p>On a ring the mark is almost always inside the band. On a chain or bracelet look at the
    clasp or the tag beside it; on earrings check the post or the back. Marks are tiny and often
    worn — a phone camera zoomed all the way in usually reads one better than your eye does.</p>

    <h2>A stamp is evidence, not proof</h2>
    <p>Marks wear down, are struck only partially, and are occasionally forged outright. If a
    piece is valuable enough to matter, have the metal tested rather than relying on the stamp
    alone. Equally, an absent stamp does not always mean an absent metal: older and handmade
    jewellery is frequently unmarked.</p>""",
          cta_h='Found something real? Value it',
          cta_p='If the piece is solid metal or holds a stone, see what it is actually worth — '
                'both at retail and what you would genuinely be offered for it.',
          cta_url='value.html', cta_label='Value my jewellery',
          related=related_block('Other marks',
            [(f"What does {x['code']} mean?",
              f"hallmark/{re.sub(r'[^a-z0-9]+','-',x['code'].lower()).strip('-')}/")
             for x in others], '../../'),
          footnote='Hallmark information is general guidance. For a valuable piece, have it '
                   f'verified by a jeweller. Metal prices: gold ${spot["gold"]:,.2f}/g, silver '
                   f'${spot["silver"]:,.2f}/g, platinum ${spot["platinum"]:,.2f}/g, refreshed daily.',
          schema=json.dumps({
            "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"What does {code} mean on jewellery?",
               "acceptedAnswer":{"@type":"Answer","text":f"{code} means {s['purity']}. {s['note']}"}},
              {"@type":"Question","name":f"Is {code} jewellery worth anything?",
               "acceptedAnswer":{"@type":"Answer","text":s['worth'] +
                 (f" At today's price the metal is worth about ${per_g:,.2f} per gram." if per_g else "")}}]})))
    return urls

# ================================================================ GOLD BY KARAT
def build_gold():
    spot = json.loads((ROOT / 'assets/metals.json').read_text())['perGram']
    karats = [('24K',0.999),('22K',0.916),('18K',0.750),('14K',0.585),('10K',0.417),('9K',0.375)]
    alloy_note = {
      '24K': 'Pure gold. Too soft for daily-wear jewellery, so it is mostly coins, bars and Asian bridal pieces.',
      '22K': 'The standard for Indian, Middle Eastern and much East Asian jewellery. Rich colour, but soft — stones are rarely set in it.',
      '18K': 'The usual fine-jewellery standard in Europe and for luxury brands worldwide. The best balance of colour and durability.',
      '14K': 'The dominant standard in the United States. Harder-wearing than 18K and noticeably cheaper per gram.',
      '10K': 'The lowest purity that can legally be called gold in the US. Common in class rings, mass-market chain and men\'s jewellery.',
      '9K':  'The UK and Commonwealth entry-level standard, not legally "gold" in the US. Pale in colour and very hard-wearing.',
    }
    items = [('Thin wedding band', 3), ('Heavy wedding band', 7), ('Signet ring', 9),
             ('45 cm chain, light', 8), ('45 cm chain, heavy', 20), ('Bangle', 25),
             ('Pair of hoop earrings', 5), ('Charm bracelet, loaded', 35)]
    urls = []
    for k, pur in karats:
        per_g = spot['gold'] * pur
        rows = [tr([kk, f"#{pp*100:.1f}%", f"#${spot['gold']*pp:,.2f}", f"#${spot['gold']*pp*10:,.0f}",
                    f"#{pp/pur*100:.0f}%"], hl=(kk == k)) for kk, pp in karats]
        weights = [tr([f"{w} g", '#' + money(per_g*w), f"#{money(per_g*w*0.7)} – {money(per_g*w*0.9)}"])
                   for w in [1,2,3,5,8,10,15,20,25,30,50,75,100]]
        units = [tr([u, f"#{g:g} g", '#' + money(per_g*g)]) for u, g in UNITS]
        item_rows = [tr([n, f"#~{g} g", '#' + money(per_g*g), f"#{money(per_g*g*0.7)} – {money(per_g*g*0.9)}"])
                     for n, g in items]
        alloy_g = round((1 - pur) * 10, 2)
        urls.append(write(f"gold-price/{k.lower()}/index.html",
          title=f"{k} Gold Price Per Gram Today — ${per_g:,.2f} | CaratBase",
          desc=f"{k} gold is worth ${per_g:,.2f} per gram today ({pur*100:.1f}% pure). Price per "
               f"tola, pennyweight and ounce, what common pieces are worth, and what a buyer will "
               f"really pay.",
          eyebrow='Live gold price',
          h1=f"{k} gold price per gram today",
          crumb=k, hub='gold-price/', hubname='Gold price',
          answer=f"<p><strong>{k} gold is worth about ${per_g:,.2f} per gram</strong> at today's "
                 f"spot price. {k} is {pur*100:.1f}% pure gold, so a gram of it contains "
                 f"{pur:.3f}&nbsp;g of gold and the rest is alloy.</p>"
                 f"<p style=\"margin-top:10px\">A scrap buyer will realistically offer "
                 f"<strong>${per_g*0.7:,.2f}–${per_g*0.9:,.2f} per gram</strong>, because they "
                 f"carry the cost of refining and take a margin.</p>",
          body=f"""
    <h2>What {k} is</h2>
    <p>{alloy_note[k]} In 10 g of {k} there is {pur*10:.2f} g of gold and {alloy_g} g of alloy —
    usually copper and silver, which is what sets the colour: more copper reads rose, more silver
    reads pale, and white gold is {k.lower()} gold alloyed with palladium or nickel and plated with rhodium.</p>

    <h2>{k} by the units gold is actually weighed in</h2>
    {tbl(['Unit', '#Grams', '#' + k + ' value'], units)}
    <p>Indian and Pakistani jewellers quote by the tola; American buyers and pawn shops by the
    pennyweight; bullion by the troy ounce. They are all the same gold at the same price — the
    unit is only a way to make a quote harder to compare. Convert to grams and it is one number.</p>

    <h2>What your piece is worth by weight</h2>
    {tbl(['Weight', '#Metal value', '#Likely offer'], weights)}

    <h2>What common {k} pieces are worth</h2>
    <p>Typical weights, without stones. Weigh yours if you can — a kitchen scale reading to 1 g is enough.</p>
    {tbl(['Piece', '#Weight', '#Metal value', '#Likely offer'], item_rows)}

    <h2>Every karat at today's price</h2>
    {tbl(['Karat', '#Pure gold', '#Per gram', '#Per 10 g', '#vs ' + k], rows)}

    <h2>Why a buyer pays less than this</h2>
    <p>The figure above is the metal content at spot. Spot is the price of pure, refined gold
    traded in bulk; your ring is an alloy, often with stones and solder in it. A buyer refines
    it, carries that cost, and takes a margin. An offer of 70–90% of the calculated value is
    normal. Below about 60%, walk away.</p>

    <h2>Scrap value is the floor, not the answer</h2>
    <p>If the piece holds a diamond, carries a maker's mark, or has any antique interest, scrap
    is the worst price it can fetch. Melting an Art Deco setting for its metal destroys most of
    what it was worth.</p>""",
          cta_h='Weigh it and find out exactly',
          cta_p=f'Enter the weight in grams, ounces, pennyweight or tola and get the {k} value '
                f'at the live price — or estimate the weight from the ring size if you have no scales.',
          cta_url='metals.html', cta_label='Open the gold calculator',
          related=related_block('Other purities',
            [(f"{kk} gold price per gram", f"gold-price/{kk.lower()}/")
             for kk, _ in karats if kk != k], '../../'),
          footnote=f'Spot price used: ${spot["gold"]:,.2f} per gram, refreshed daily. Indicative '
                   f'only, not an offer to buy or sell.',
          schema=json.dumps({
            "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"What is {k} gold worth per gram?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"{k} gold is worth about ${per_g:,.2f} per gram, being {pur*100:.1f}% pure gold. "
                 f"A scrap buyer typically offers 70 to 90 percent of that."}},
              {"@type":"Question","name":f"What is {k} gold worth per tola?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"One tola is 11.664 grams, so {k} gold is worth about {money(per_g*11.6638)} per tola today."}},
              {"@type":"Question","name":f"How pure is {k} gold?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"{k} gold is {pur*100:.1f}% pure gold by weight. The rest is alloy, usually copper and silver."}}]})))
    return urls

# ================================================================ DIAMOND CARAT x SHAPE
def build_diamonds():
    cts = [0.25,0.5,0.75,1,1.25,1.5,2,2.5,3,4,5]
    shapes = ['Round','Oval','Princess','Cushion','Emerald','Pear','Marquise','Radiant','Asscher','Heart']
    colors = ['D','F','G','H','I','J']
    clars  = ['VVS1','VS1','VS2','SI1','SI2']
    base = "cut:'Very Good',origin:'Natural',cert:'GIA'"
    # One node round-trip computes every number on every page: the headline value, the
    # 30-cell colour x clarity grid, the lab-grown twin, the price just under this weight,
    # and what the same money buys elsewhere.
    expr = ('[' + ','.join(
        f"{{ct:{c},shape:'{s}',"
        f"v:valueDiamond({{carat:{c},shape:'{s}',color:'G',clarity:'VS2',{base}}}),"
        f"lab:valueDiamond({{carat:{c},shape:'{s}',color:'G',clarity:'VS2',cut:'Very Good',origin:'Lab-grown',cert:'IGI'}}),"
        f"under:valueDiamond({{carat:{round(c-0.05,2)},shape:'{s}',color:'G',clarity:'VS2',{base}}}),"
        f"d:shapeDims('{s}',{c}),"
        f"grid:[{','.join(f'valueDiamond({{carat:{c},shape:{s!r},color:{co!r},clarity:{cl!r},{base}}})' for co in colors for cl in clars)}]"
        f"}}" for c in cts for s in shapes) + ']')
    data = node_eval(expr, 'assets/data.js', 'assets/shapes.js')
    by = {(d['ct'], d['shape']): d for d in data}
    # "same money" alternatives need the budget first, so a second pass
    expr2 = ('[' + ','.join(
        f"{{ct:{d['ct']},shape:'{d['shape']}',"
        f"bigger:caratForBudget({mid(d['v'])},{{shape:'Round',color:'J',clarity:'SI1',{base}}}),"
        f"labct:caratForBudget({mid(d['v'])},{{shape:'{d['shape']}',color:'G',clarity:'VS2',cut:'Very Good',origin:'Lab-grown',cert:'IGI'}})}}"
        for d in data) + ']')
    for a in node_eval(expr2, 'assets/data.js'):
        by[(a['ct'], a['shape'])].update(bigger=a['bigger'], labct=a['labct'])

    urls = []
    for c in cts:
        for s in shapes:
            d = by[(c, s)]; v = d['v']; dim = d['d']; lab = d['lab']; under = d['under']
            ctxt = f"{c:g}"
            slug = f"diamond/{ctxt.replace('.','-')}-carat-{s.lower()}/index.html"
            def durl(cc, ss): return f"diamond/{('%g'%cc).replace('.','-')}-carat-{ss.lower()}/"
            sib = [(f"{c:g} ct {x.lower()}", durl(c, x)) for x in shapes if x != s][:6]
            other_ct = [(f"{cc:g} ct {s.lower()}", durl(cc, s)) for cc in cts if cc != c][:6]
            keep = round(v['resaleHigh']/v['retailHigh']*100)
            area = dim['l'] * dim['w']
            rd = by[(c, 'Round')]['d']; round_area = rd['l'] * rd['w']
            spread = pct(area, round_area)
            g = d['grid']; gi = lambda co, cl: g[colors.index(co)*len(clars)+clars.index(cl)]

            # colour x clarity grid, this weight and shape only
            grid_rows = [tr([co] + ['#' + money(mid(gi(co, cl))) for cl in clars],
                            hl=(co == 'G')) for co in colors]
            cheapest = mid(gi('J','SI2')); dearest = mid(gi('D','VVS1'))

            # every shape at this weight; every weight in this shape
            shape_rows = [tr([x, f"#{by[(c,x)]['d']['l']} × {by[(c,x)]['d']['w']}",
                              f"#{by[(c,x)]['d']['l']*by[(c,x)]['d']['w']:.0f}",
                              '#' + money(mid(by[(c,x)]['v']))], hl=(x == s)) for x in shapes]
            ct_rows = [tr([f"{cc:g} ct", f"#{by[(cc,s)]['d']['l']} × {by[(cc,s)]['d']['w']}",
                           '#' + money(mid(by[(cc,s)]['v'])),
                           '#' + money(mid(by[(cc,s)]['v'],'resaleLow','resaleHigh'))],
                          hl=(cc == c)) for cc in cts]

            # the price step just under this weight
            u_ct = round(c - 0.05, 2)
            u_mid = mid(under); this_mid = mid(v)
            saving = pct(u_mid, this_mid)   # negative number
            size_loss = round((1 - (u_ct / c) ** (1/3)) * 100, 1)
            if saving <= -8:
                cliff = (f"<p>A <strong>{u_ct:g} carat</strong> {s.lower()} of the same grade costs about "
                         f"<strong>{money(u_mid)}</strong> — <strong>{-saving}% less</strong> than this stone — "
                         f"and is only {size_loss}% shorter across, a difference no one can see on a "
                         f"finger. Weights just under a round number are priced in a lower bracket "
                         f"because the round number itself is what buyers ask for.</p>")
            else:
                cliff = (f"<p>There is no useful saving just below this weight: a {u_ct:g} carat "
                         f"{s.lower()} costs about {money(u_mid)}, only {-saving}% less, and the next "
                         f"price bracket does not begin until further down.</p>")

            # same money, other choices
            bg = d['bigger']; lc = d['labct']
            alt_rows = [tr([f"This stone — {ctxt} ct {s.lower()}, G / VS2, natural", '#' + money(this_mid),
                            f"#{dim['l']} × {dim['w']} mm"], hl=True)]
            if bg and bg['carat'] > c:
                alt_rows.append(tr([f"A {bg['carat']:g} ct round, J / SI1, natural",
                                    '#' + money(mid(bg)), f"#about {(bg['carat']/c)**(1/3)*dim['l']:.1f} mm long"]))
            if lc and lc['carat'] > c:
                alt_rows.append(tr([f"A {lc['carat']:g} ct lab-grown {s.lower()}, G / VS2",
                                    '#' + money(mid(lc)), f"#about {(lc['carat']/c)**(1/3)*dim['l']:.1f} mm long"]))
            alt_rows.append(tr([f"Lab-grown twin — {ctxt} ct {s.lower()}, G / VS2",
                                '#' + money(mid(lab)), f"#{dim['l']} × {dim['w']} mm"]))

            urls.append(write(slug,
              title=f"{ctxt} Carat {s} Diamond — Size in MM, Price &amp; Resale Value | CaratBase",
              desc=f"A {ctxt} carat {s.lower()} diamond measures {dim['l']}×{dim['w']}mm and costs "
                   f"{money(v['retailLow'])}–{money(v['retailHigh'])} at retail. Real resale value "
                   f"{money(v['resaleLow'])}–{money(v['resaleHigh'])}. Price by colour and clarity, "
                   f"lab-grown equivalent, and every shape at this weight.",
              eyebrow='Diamond size and price',
              h1=f"{ctxt} carat {s.lower()} diamond: size, price and what it really resells for",
              crumb=f"{ctxt} ct {s.lower()}", hub='diamond/', hubname='Diamonds',
              answer=f"<p>A <strong>{ctxt} carat {s.lower()} diamond</strong> measures about "
                     f"<strong>{dim['l']} × {dim['w']} mm</strong> face-up and costs roughly "
                     f"<strong>{money(v['retailLow'])}–{money(v['retailHigh'])}</strong> at retail "
                     f"for a G colour, VS2, well-cut stone.</p>"
                     f"<p style=\"margin-top:10px\">If you sold it, you would realistically be "
                     f"offered <strong>{money(v['resaleLow'])}–{money(v['resaleHigh'])}</strong> "
                     f"— about {keep}% of what it cost. A lab-grown stone of the same size and grade "
                     f"costs about <strong>{money(mid(lab))}</strong>.</p>",
              body=f"""
    <h2>How big it actually looks</h2>
    <p>{dim['l']} × {dim['w']} mm is the face-up measurement — what sits above the finger — giving
    a visible area of about <strong>{area:.0f} mm²</strong>. {dim['note']}
    {"That is " + str(abs(spread)) + "% " + ("more" if spread > 0 else "less") + " face-up area than a round of the same weight." if s != 'Round' else "Round is the reference shape: every other cut is measured against it."}</p>
    <p>Carat is a measure of <em>weight</em>, not size, and weight rises with the cube of the
    length. Doubling the carat makes a stone only about {(2**(1/3)):.2f} times longer, so a
    {c*2:g} carat {s.lower()} would be roughly {dim['l']*2**(1/3):.1f} mm across, not {dim['l']*2:.1f}.</p>

    <h2>Price by colour and clarity, {ctxt} carat {s.lower()}</h2>
    <p>Retail mid-point for each grade, Very Good cut, GIA-graded, natural. The range on this page
    runs from <strong>{money(cheapest)}</strong> (J colour, SI2) to <strong>{money(dearest)}</strong>
    (D colour, VVS1) — a {pct(dearest, cheapest)}% spread for stones that are the same size to the
    tenth of a millimetre.</p>
    {tbl(['Colour'] + ['#' + cl for cl in clars], grid_rows)}
    <p>Above about G colour and VS2 clarity, almost nothing you pay for is visible without a loupe.
    Cut is the one grade worth protecting: a badly cut {s.lower()} looks dull whatever else is true of it.</p>

    <h2>The price step just below {ctxt} carat</h2>
    {cliff}

    <h2>The same money, spent differently</h2>
    <p>At about {money(this_mid)}, these are the honest alternatives to this exact stone.</p>
    {tbl(['Option', '#Price', '#Size'], alt_rows)}
    <p>The lab-grown figure is not a typo. Lab-grown prices fell by roughly 85% between 2022 and
    2025 and resale is 5–12% of retail, so the saving is real at the counter and is gone the day
    after. Buy lab-grown to wear it; never as a store of value.</p>

    <h2>Price and the resale gap</h2>
    {tbl(['Where you sell', '#Typical offer', '#Share of retail'], [
        tr(['Pawn shop or "we buy gold" counter', '#' + money(v['resaleLow']), f"#{round(v['resaleLow']/mid(v)*100)}%"]),
        tr(['Online diamond buyer (mail-in)', '#' + money(mid(v,'resaleLow','resaleHigh')), f"#{round(mid(v,'resaleLow','resaleHigh')/mid(v)*100)}%"]),
        tr(['Private sale or consignment', '#' + money(v['resaleHigh']), f"#{round(v['resaleHigh']/mid(v)*100)}%"]),
    ])}
    <p>The gap is not a criticism of buying jewellery — it is simply the number nobody mentions
    at the counter. A jeweller's price carries rent, staff, insurance and margin, and none of
    that comes back to you when you sell.</p>

    <h2>{ctxt} carat in every shape</h2>
    {tbl(['Shape', '#Face-up mm', '#Area mm²', '#Retail (G / VS2)'], shape_rows)}

    <h2>Every weight in {s.lower()}</h2>
    {tbl(['Weight', '#Face-up mm', '#Retail (G / VS2)', '#Resale'], ct_rows)}""",
              cta_h='Value your own stone',
              cta_p='Enter your exact specification — including side stones and the metal it is '
                    'set in — and get both numbers for your piece rather than this example.',
              cta_url='value.html', cta_label='Value my diamond',
              related=(related_block(f'The same weight in other shapes', sib, '../../') +
                       related_block(f'Other weights in {s.lower()}', other_ct, '../../')),
              footnote='Estimates for a G colour, VS2 clarity, Very Good cut, GIA-graded natural '
                       'stone unless stated. Individual stones vary. Lab-grown figures assume IGI grading.',
              schema=json.dumps({
                "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                  {"@type":"Question","name":f"How big is a {ctxt} carat {s.lower()} diamond?",
                   "acceptedAnswer":{"@type":"Answer","text":
                     f"A {ctxt} carat {s.lower()} diamond measures about {dim['l']} by {dim['w']} "
                     f"millimetres face-up, a visible area of about {area:.0f} square millimetres."}},
                  {"@type":"Question","name":f"How much does a {ctxt} carat {s.lower()} diamond cost?",
                   "acceptedAnswer":{"@type":"Answer","text":
                     f"About {money(v['retailLow'])} to {money(v['retailHigh'])} at retail for a "
                     f"G colour, VS2 clarity, well-cut stone. Across grades it runs from about "
                     f"{money(cheapest)} for J/SI2 to {money(dearest)} for D/VVS1. Resale is typically "
                     f"{money(v['resaleLow'])} to {money(v['resaleHigh'])}."}},
                  {"@type":"Question","name":f"How much is a lab-grown {ctxt} carat {s.lower()} diamond?",
                   "acceptedAnswer":{"@type":"Answer","text":
                     f"About {money(mid(lab))} for a G colour, VS2 lab-grown {s.lower()} of {ctxt} carat, "
                     f"with resale of only {money(lab['resaleLow'])} to {money(lab['resaleHigh'])}."}}]})))
    return urls

# ================================================================ GEMSTONES
def build_gems():
    names = node_eval('Object.keys(GEMS)', 'assets/gems.js')
    gems = node_eval('GEMS', 'assets/gems.js')
    treatments = node_eval('GEM_TREATMENTS', 'assets/gems.js')
    tiers = ['Commercial', 'Good', 'Fine', 'Exceptional']
    ladder_ct = [0.5, 1, 2, 3, 5]
    def treats_for(n):
        nl = n.lower()
        t = ['Not treated (lab certified)', 'Heated (standard)']
        if 'emerald' in nl: t = ['Not treated (lab certified)', 'Oiled — minor (emerald)',
                                 'Oiled — moderate (emerald)', 'Oiled — significant (emerald)']
        if 'ruby' in nl: t += ['Fracture filled — glass']
        if 'sapphire' in nl: t += ['Diffusion treated']
        if 'topaz' in nl: t += ['Irradiated']
        if 'opal' in nl or 'jade' in nl or 'garnet' in nl or 'peridot' in nl or 'spinel' in nl: t += ['Dyed']
        return t + ['Unknown']
    std = {n: 'Oiled — minor (emerald)' if 'emerald' in n.lower() else 'Heated (standard)' for n in names}
    def q(n, ct, tier, treat, origin):
        return (f"valueGem({{type:{json.dumps(n)},carat:{ct},tier:{json.dumps(tier)},"
                f"treatment:{json.dumps(treat)},origin:{json.dumps(origin)}}})")
    expr = ('[' + ','.join(
        f"{{t:{json.dumps(n)},"
        f"v:{q(n,2,'Fine',std[n],list(gems[n]['origins'])[-1])},"
        f"cts:[{','.join(q(n,c,'Fine',std[n],list(gems[n]['origins'])[-1]) for c in ladder_ct)}],"
        f"tiers:[{','.join(q(n,2,t,std[n],list(gems[n]['origins'])[-1]) for t in tiers)}],"
        f"treats:[{','.join(q(n,2,'Fine',t,list(gems[n]['origins'])[-1]) for t in treats_for(n))}],"
        f"origins:[{','.join(q(n,2,'Fine',std[n],o) for o in gems[n]['origins'])}]"
        f"}}" for n in names) + ']')
    data = node_eval(expr, 'assets/gems.js')
    urls = []
    for d in data:
        n = d['t']; v = d['v']
        slug_n = re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
        origins = list(gems[n]['origins'])
        prem = [o for o in origins if 'Unknown' not in o]
        ct_rows = [tr([f"{c:g} ct", '#' + money(x['ppc']), f"#{money(x['retailLow'])} – {money(x['retailHigh'])}",
                       f"#{money(x['resaleLow'])} – {money(x['resaleHigh'])}"], hl=(c == 2))
                   for c, x in zip(ladder_ct, d['cts'])]
        tier_rows = [tr([t, '#' + money(x['ppc']), f"#{money(x['retailLow'])} – {money(x['retailHigh'])}"], hl=(t == 'Fine'))
                     for t, x in zip(tiers, d['tiers'])]
        tl = treats_for(n)
        treat_rows = [tr([t.replace(' (emerald)', ''), f"#{treatments[t]['mult']:g}×", f"#{money(x['retailLow'])} – {money(x['retailHigh'])}"],
                         hl=(t == std[n])) for t, x in zip(tl, d['treats'])]
        orig_rows = [tr([o, f"#{gems[n]['origins'][o]:g}×", f"#{money(x['retailLow'])} – {money(x['retailHigh'])}"],
                        hl=(o == origins[-1])) for o, x in zip(origins, d['origins'])]
        best = d['treats'][0]; worst = min(d['treats'], key=lambda x: x['retailLow'])
        worst_name = tl[d['treats'].index(worst)].replace(' (emerald)', '')
        ratio = round(mid(best) / max(1, mid(worst)))
        ppc5 = d['cts'][-1]['ppc']; ppc1 = d['cts'][1]['ppc']
        per_ct_climb = round(ppc5 / ppc1, 1)
        urls.append(write(f"gemstone/{slug_n}/index.html",
          title=f"{n} Value — What Is a 2 Carat {n} Worth? | CaratBase",
          desc=f"A fine 2 carat {n.lower()} is worth {money(v['retailLow'])}–{money(v['retailHigh'])} "
               f"at retail. Value by carat, quality, treatment and origin — treatment changes it "
               f"more than size does.",
          eyebrow='Coloured stone value',
          h1=f"What is a {n.lower()} worth?",
          crumb=n, hub='gemstone/', hubname='Gemstones',
          answer=f"<p>A <strong>fine 2 carat {n.lower()}</strong>, {std[n].split(' (')[0].lower()} and without certified "
                 f"origin, is worth roughly <strong>{money(v['retailLow'])}–{money(v['retailHigh'])}</strong> "
                 f"at retail — about {money(v['ppc'])} per carat.</p>"
                 f"<p style=\"margin-top:10px\">Resale is far lower: "
                 f"<strong>{money(v['resaleLow'])}–{money(v['resaleHigh'])}</strong>. Coloured "
                 f"stones have no universal grading standard, so a buyer carries more risk and "
                 f"prices for it.</p>",
          body=f"""
    <h2>{n} value by carat</h2>
    <p>Price per carat climbs with size far faster than it does for diamonds, because large clean
    {n.lower()} is much rarer than small. A 5 carat stone of this quality is priced at about
    <strong>{per_ct_climb}× the per-carat rate</strong> of a 1 carat one.</p>
    {tbl(['Weight', '#Per carat', '#Retail', '#Resale'], ct_rows)}

    <h2>{n} value by quality, 2 carat</h2>
    <p>Colour is most of it: saturation, hue and how evenly it holds across the stone. Then
    clarity, then cut. The tiers below are the trade's working bands; two respected dealers can
    put the same stone in neighbouring tiers.</p>
    {tbl(['Quality', '#Per carat', '#Retail, 2 ct'], tier_rows)}

    <h2>Treatment matters more than size</h2>
    <p>This is the single most important thing about {n.lower()} value, and the thing owners
    least often know about their own stone. For a fine 2 carat {n.lower()}, the same stone runs
    from about <strong>{money(mid(worst))}</strong> ({worst_name.lower()}) to
    <strong>{money(mid(best))}</strong> (untreated, lab certified) — a factor of roughly
    <strong>{ratio}×</strong> — while looking much the same across a counter.</p>
    {tbl(['Treatment', '#Multiplier', '#Retail, fine 2 ct'], treat_rows)}
    <p>{treatments[std[n]]['note']} Assume any stone is treated unless a report says otherwise.</p>

    <h2>Origin, but only if certified</h2>
    <p>{'For ' + n.lower() + ', the sources that command a premium are ' + ', '.join(prem[:3]) + '.' if prem else 'Origin has little effect on this stone.'}
    A premium applies only when a recognised laboratory has certified the origin in writing.
    A seller's claim on its own is worth nothing.</p>
    {tbl(['Origin', '#Multiplier', '#Retail, fine 2 ct'], orig_rows) if len(origins) > 1 else ''}

    <h2>Why the range is wide</h2>
    <p>Diamonds have the 4Cs and a dominant grading authority. Coloured stones have neither.
    Colour quality — which drives most of the value — is judged by eye, and two respected labs
    can describe the same stone differently. Any honest estimate for a {n.lower()} is a broader
    range than a diamond estimate, and ours is.</p>

    <h2>When a report pays for itself</h2>
    <p>If your stone might be worth more than about $2,000, a laboratory report on treatment
    and origin usually returns several times its cost. Without one a buyer must assume the
    least favourable case and price for that risk.</p>""",
          cta_h=f'Value your own {n.lower()}',
          cta_p='Enter the carat weight, quality, treatment and origin and get a figure matched '
                'to your stone rather than this example.',
          cta_url='gemstone.html', cta_label='Open the gemstone calculator',
          related=related_block('Other stones',
            [(f"What is a {x['t'].lower()} worth?",
              f"gemstone/{re.sub(r'[^a-z0-9]+','-',x['t'].lower()).strip('-')}/")
             for x in data if x['t'] != n][:8], '../../'),
          footnote='Coloured stone valuation is far less standardised than diamond valuation and '
                   'ranges are correspondingly wide. Not an appraisal.',
          schema=json.dumps({
            "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"How much is a 2 carat {n.lower()} worth?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"A fine 2 carat {n.lower()} is worth roughly {money(v['retailLow'])} to "
                 f"{money(v['retailHigh'])} at retail, or about {money(v['ppc'])} per carat. "
                 f"Treatment affects this more than size does."}},
              {"@type":"Question","name":f"How much is a 1 carat {n.lower()} worth?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"A fine 1 carat {n.lower()} is worth roughly {money(d['cts'][1]['retailLow'])} to "
                 f"{money(d['cts'][1]['retailHigh'])} at retail."}},
              {"@type":"Question","name":f"Does treatment affect {n.lower()} value?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"Enormously. A fine 2 carat {n.lower()} runs from about {money(mid(worst))} if "
                 f"{worst_name.lower()} to {money(mid(best))} if untreated and lab certified."}}]})))
    return urls


# ================================================================ CATEGORY HUBS
def build_hubs(built):
    """A parent page for each generated directory.

    Two jobs. Crawlers try the parent of every URL they find, and five 404s at the top of
    our biggest directories is both a wasted crawl and a bad signal. And with no hub, the
    222 leaf pages were reachable only through the sitemap — no internal links meant no
    path for authority to reach them from the home page.
    """
    HUBS = {
      'ring-size': dict(
        title='Ring Size Conversion Charts — US, UK, EU, India &amp; Japan | CaratBase',
        desc='Every ring size converted between US, UK, European and Indian/Japanese systems, '
             'with inside diameter and circumference in millimetres.',
        h1='Ring size conversion charts',
        lead='Every size, converted between all five systems used around the world, with the '
             'inside diameter and circumference in millimetres. Pick your size, or '
             '<a href="../ring-size.html">measure it with the sizer</a>.',
        tool='ring-size.html', tool_label='Open the ring sizer'),
      'hallmark': dict(
        title='Jewellery Hallmarks Explained — What Every Stamp Means | CaratBase',
        desc='What the mark inside your jewellery means. 925, 750, 585, 417, GF, EPNS and more '
             '— the metal, the purity, and whether the piece is worth anything.',
        h1='Jewellery hallmarks, explained',
        lead='Nearly every real piece carries a stamp. Here is what each one means, what metal '
             'it is, and — the part that matters — whether it is worth anything by weight.',
        tool='stamp.html', tool_label='Look up a stamp'),
      'gold-price': dict(
        title='Gold Price Per Gram by Karat — 24K, 22K, 18K, 14K, 10K, 9K | CaratBase',
        desc='Live gold price per gram for every karat, and what a scrap buyer will '
             'realistically pay for each.',
        h1='Gold price per gram, by karat',
        lead='What each purity is worth per gram at today\'s price, and the offer a buyer is '
             'likely to actually make.',
        tool='metals.html', tool_label='Open the gold calculator'),
      'diamond': dict(
        title='Diamond Sizes &amp; Prices by Carat and Shape | CaratBase',
        desc='How big each carat weight looks in millimetres across ten diamond shapes, what it '
             'costs at retail, and the far smaller figure it resells for.',
        h1='Diamond sizes and prices, by carat and shape',
        lead='Carat is weight, not size — and the same weight looks very different across '
             'shapes. Every combination below gives the true face-up size in millimetres, the '
             'retail price, and the resale figure nobody else publishes.',
        tool='value.html', tool_label='Value your own diamond'),
      'gemstone': dict(
        title='Gemstone Values — Ruby, Sapphire, Emerald &amp; More | CaratBase',
        desc='What each coloured stone is worth, and why treatment affects the value far more '
             'than size does.',
        h1='What coloured stones are worth',
        lead='Coloured stones do not price like diamonds. There is no universal grading '
             'standard, and treatment usually matters more than size — often by a factor of '
             'thousands.',
        tool='gemstone.html', tool_label='Value a gemstone'),
    }
    # A data table per hub. Google crawled /hallmark/ at 214 words of link list and declined to
    # index it; a hub that is itself the best single page on its topic is a different thing.
    spot = json.loads((ROOT / 'assets/metals.json').read_text())['perGram']
    rows = node_eval('RING_SIZES', 'assets/ringdata.js')
    stamps = node_eval('STAMPS', 'assets/data.js')
    cts = [0.25,0.5,0.75,1,1.25,1.5,2,2.5,3,4,5]
    shapes = ['Round','Oval','Princess','Cushion','Emerald','Pear','Marquise','Radiant','Asscher','Heart']
    dims = node_eval('[' + ','.join(f"shapeDims('{sh}',{c})" for c in cts for sh in shapes) + ']',
                     'assets/data.js', 'assets/shapes.js')
    gems = node_eval('Object.entries(GEMS).map(([t,g])=>({t, o:Object.keys(g.origins)[0], '
                     'v:valueGem({type:t,carat:2,tier:"Fine",treatment:t=="Emerald"?"Oiled — minor (emerald)":"Heated (standard)",'
                     'origin:Object.keys(g.origins).slice(-1)[0]})}))', 'assets/gems.js')
    karats = [('24K',0.999),('22K',0.916),('18K',0.750),('14K',0.585),('10K',0.417),('9K',0.375)]
    def slug_of(code): return re.sub(r'[^a-z0-9]+','-',code.lower()).strip('-')
    TABLES = {
      'ring-size': '<h2>Every size, every system</h2>' + tbl(
          ['US', 'UK / AU', 'Europe', 'India / Japan', '#Diameter', '#Circumference'],
          [tr([f'<a href="us-{str(x["us"]).replace(".","-")}/">{x["us"]}</a>' if (float(x['us'])*2)==int(float(x['us'])*2) else x['us'],
               x['uk'], x['eu'], x['jp'] or '—', f"#{x['dia']} mm", f"#{x['circ']} mm"]) for x in rows]),
      'hallmark': '<h2>Every mark at a glance</h2>' + tbl(
          ['Mark', 'Metal', 'Means', 'Worth as metal'],
          [tr([f'<a href="{slug_of(x["code"])}/">{x["code"]}</a>', x['metal'], x['purity'],
               {'solid':'Yes — solid','filled':'Very little','plated':'No','lab':'Diamond, not metal','none':'No'}.get(x['value'],'')])
           for x in stamps]),
      'gold-price': '<h2>Every karat, per gram, today</h2>' + tbl(
          ['Karat', '#Pure gold', '#Per gram', '#Per tola', '#Per troy oz', '#Likely scrap offer / g'],
          [tr([f'<a href="{k.lower()}/">{k}</a>', f"#{pp*100:.1f}%", f"#${spot['gold']*pp:,.2f}",
               '#' + money(spot['gold']*pp*11.6638), '#' + money(spot['gold']*pp*31.1035),
               f"#${spot['gold']*pp*0.7:,.2f} – ${spot['gold']*pp*0.9:,.2f}"]) for k, pp in karats])
          + f'<p class="small">Gold spot ${spot["gold"]:,.2f} per gram, refreshed daily.</p>'
          + '<h2>Reading a karat</h2>'
          + '<p>Karat is purity in twenty-fourths: 24K is pure, 18K is eighteen parts gold in twenty-four '
            '(75%), 14K is fourteen (58.5%). Most of the world stamps the purity as a three-digit '
            'fraction of a thousand instead — 750, 585, 417 — which is the same information, and the '
            '<a href="../hallmark/">hallmark pages</a> decode every one. The karat sets the value of the '
            'metal exactly; it says nothing about the value of the piece, which can be far higher if it '
            'carries a stone, a maker\'s name, or age.</p>'
          + '<h2>Pure gold by the units it is quoted in</h2>'
          + tbl(['Unit', '#Grams', '#24K value today'],
                [tr([u, f"#{g:g} g", '#' + money(spot['gold']*0.999*g)]) for u, g in UNITS])
          + '<p>Every unit is the same gold at the same price. Convert a quote to grams before comparing it '
            'with another, and be suspicious of anyone who will not.</p>',
      'diamond': '<h2>Face-up size in millimetres, every weight and shape</h2>' + tbl(
          ['Carat'] + ['#' + sh for sh in shapes],
          [tr([f'<a href="{("%g"%c).replace(".","-")}-carat-round/">{c:g} ct</a>'] +
              [f'#<a href="{("%g"%c).replace(".","-")}-carat-{sh.lower()}/">{dims[i*len(shapes)+j]["l"]}×{dims[i*len(shapes)+j]["w"]}</a>'
               for j, sh in enumerate(shapes)]) for i, c in enumerate(cts)]),
      'gemstone': '<h2>What a fine 2 carat stone is worth</h2>' + tbl(
          ['Stone', '#Per carat', '#Retail, 2 ct', '#Resale', 'Premium origin'],
          [tr([f'<a href="{slug_of(g["t"])}/">{g["t"]}</a>', '#' + money(g['v']['ppc']),
               f"#{money(g['v']['retailLow'])} – {money(g['v']['retailHigh'])}",
               f"#{money(g['v']['resaleLow'])} – {money(g['v']['resaleHigh'])}",
               g['o'] if 'Unknown' not in g['o'] else '—'])
           for g in sorted(gems, key=lambda g: -g['v']['ppc'])]),
    }
    urls=[]
    for d, cfg in HUBS.items():
        kids = sorted(u for u in built if u.startswith(d + '/'))
        links = []
        for u in kids:
            slug = u.split('/')[1]
            label = slug.replace('-', ' ')
            if d == 'ring-size':
                label = ('US size ' + slug[3:].replace('-', '.')) if slug.startswith('us-') \
                        else ('UK size ' + slug[3:].replace('-half', '\u00bd').upper())
            elif d == 'gold-price':  label = slug.upper() + ' gold price per gram'
            elif d == 'diamond':     label = label.replace('carat', 'ct').replace(' ct ', ' carat ')
            elif d == 'hallmark':    label = 'What does ' + slug.upper() + ' mean?'
            else:                    label = label.title()
            links.append((label, f'{d}/{slug}/'))
        body = (f'<p class="lede" style="margin-bottom:26px">{cfg["lead"]}</p>'
                + TABLES[d]
                + related_block(f'All {len(links)} pages', links, '../'))
        urls.append(write(f'{d}/index.html',
          title=cfg['title'], desc=cfg['desc'], eyebrow='Reference',
          h1=cfg['h1'], crumb=cfg['h1'], hub=cfg['tool'], hubname='Tools',
          answer=f'<p>{cfg["lead"]}</p>',
          body=body,
          cta_h='Work out your own',
          cta_p='These pages are worked examples. Put your own details in and get a figure '
                'matched to your piece.',
          cta_url=cfg['tool'], cta_label=cfg['tool_label'],
          related='',
          footnote='Estimates for information only. See our '
                   '<a href="../methodology.html">methodology</a>.',
          schema=json.dumps({"@context":"https://schema.org","@type":"CollectionPage",
                             "name":cfg['h1'],"url":f"{BASE}/{d}/"})))
    return urls

# ================================================================ MAIN
def main():
    for d in OUT_DIRS:
        shutil.rmtree(ROOT / d, ignore_errors=True)
    urls = []
    for name, fn in [('ring sizes', build_ring_sizes), ('hallmarks', build_hallmarks),
                     ('gold karats', build_gold), ('diamonds', build_diamonds),
                     ('gemstones', build_gems)]:
        got = fn()
        print(f'  {len(got):>4}  {name}')
        urls += got
    hubs = build_hubs(urls)
    print(f'  {len(hubs):>4}  category hubs')
    urls += hubs

    # Sitemaps: one per section plus an index at the old URL, so Search Console reports
    # indexing per section and the existing submission keeps working unchanged.
    core = ['', 'value.html','gemstone.html','budget.html','metals.html','stamp.html',
            'size.html','ring-size.html','measure.html','vault.html','methodology.html',
            'disclaimer.html','privacy.html','terms.html']
    def entry(u, pri, freq):
        loc = f'{BASE}/{u}'.replace('/index.html','/')
        return (f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
                f'<changefreq>{freq}</changefreq><priority>{pri}</priority></url>')
    def urlset(entries):
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + '\n'.join(entries) + '\n</urlset>\n')
    files = {}
    files['sitemap-core.xml'] = [entry('', '1.0', 'daily')] + [
        entry(u, '0.3' if u in ('privacy.html','terms.html') else '0.9', 'weekly') for u in core[1:]]
    for d in OUT_DIRS:
        kids = [u for u in urls if u.startswith(d + '/')]
        files[f'sitemap-{d}.xml'] = [entry(u, '0.8' if u == f'{d}/index.html' else '0.7', 'monthly')
                                     for u in kids]
    for name, entries in files.items():
        (ROOT / name).write_text(urlset(entries))
    (ROOT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(f'  <sitemap><loc>{BASE}/{n}</loc><lastmod>{TODAY}</lastmod></sitemap>' for n in files)
        + '\n</sitemapindex>\n')
    print(f'\n  sitemap index: {len(files)} sitemaps, {sum(len(e) for e in files.values())} URLs')
    return urls

if __name__ == '__main__':
    print('Generating long-tail pages...\n')
    main()

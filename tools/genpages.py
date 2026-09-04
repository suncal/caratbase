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
def build_ring_sizes():
    rows = node_eval('RING_SIZES', 'assets/ringdata.js')
    urls = []
    # every size, halves included: 'ring size 6.5 in uk' is searched as often as whole sizes
    all_us = [r for r in rows if (float(r['us'])*2) == int(float(r['us'])*2)]

    for r in all_us:
        us, uk, eu, jp = r['us'], r['uk'], r['eu'], r['jp']
        dia, circ = r['dia'], r['circ']
        slug = f"ring-size/us-{str(us).replace('.','-')}/index.html"
        table = ''.join(
            f"<tr{HL if x['us']==us else ''}>"
            f"<td>{x['us']}</td><td>{x['uk']}</td><td>{x['eu']}</td>"
            f"<td>{x['jp'] if x['jp'] else '—'}</td><td class='num'>{x['dia']} mm</td>"
            f"<td class='num'>{x['circ']} mm</td></tr>"
            for x in rows)
        near = [x for x in all_us if abs(float(x['us'])-float(us)) <= 2 and x['us'] != us][:6]
        urls.append(write(slug,
          title=f"US Ring Size {us} in UK, EU &amp; India — {uk}, {eu}, {dia}mm | CaratBase",
          desc=f"US ring size {us} is UK size {uk}, EU {eu} and Indian/Japanese size {jp or '—'}. "
               f"Inside diameter {dia}mm, circumference {circ}mm. Free converter and true-to-scale sizer.",
          eyebrow='Ring size conversion',
          h1=f"US ring size {us} in UK, Europe and India",
          crumb=f"US {us}", hub='ring-size.html', hubname='Ring size',
          answer=f"<p><strong>US ring size {us}</strong> is <strong>UK size {uk}</strong>, "
                 f"<strong>European (ISO) size {eu}</strong>"
                 + (f" and <strong>Indian/Japanese size {jp}</strong>" if jp else "")
                 + f". That is an inside diameter of <strong>{dia}&nbsp;mm</strong> and an inside "
                   f"circumference of <strong>{circ}&nbsp;mm</strong>.</p>",
          body=f"""
    <h2>How to check this is your size</h2>
    <p>The surest way is to measure a ring that already fits the right finger. Lay it flat and
    measure straight across the <strong>inside</strong> of the band. If it reads about
    {dia}&nbsp;mm, you are a US {us}.</p>
    <p>If you have no ring to hand, wrap a strip of paper around the base of the finger, mark
    where it overlaps, and measure the length. About {circ}&nbsp;mm means US {us}. Measure at the
    end of the day, when fingers are at their largest — a ring sized on a cold morning will feel
    tight by evening.</p>

    <h2>Full conversion chart</h2>
    <div class="table-scroll"><table>
      <thead><tr><th>US</th><th>UK / AU</th><th>Europe</th><th>India / Japan</th>
        <th class="num">Diameter</th><th class="num">Circumference</th></tr></thead>
      <tbody>{table}</tbody></table></div>

    <h2>A note on wide bands</h2>
    <p>A band wider than about 6&nbsp;mm sits against more of your finger and feels tighter at
    the same measurement. Most jewellers suggest going up a quarter to a half size, so a US {us}
    in a narrow band is often a {float(us)+0.5:g} in a wide one.</p>""",
          cta_h='Measure it yourself, right now',
          cta_p='Lay a ring on your screen and match it against circles drawn true to life, '
                'calibrated against any bank card.',
          cta_url='ring-size.html', cta_label='Open the ring sizer',
          related=related_block('Nearby sizes',
            [(f"US size {x['us']} → UK {x['uk']}", f"ring-size/us-{str(x['us']).replace('.','-')}/")
             for x in near], '../../'),
          footnote='Conversions follow the standard published charts and ISO 8653. Individual '
                   'jewellers vary slightly; for an expensive ring, confirm in person.',
          schema=json.dumps({
            "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"What is US ring size {us} in UK sizes?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"US ring size {us} is UK size {uk}. The inside diameter is {dia} mm and the "
                 f"inside circumference is {circ} mm."}},
              {"@type":"Question","name":f"What is the diameter of a US size {us} ring?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"A US size {us} ring has an inside diameter of {dia} mm."}}]})))
    # UK letter pages — the same conversion approached from the other direction
    seen=set()
    for r in rows:
        uk=r['uk']
        if uk in seen: continue
        seen.add(uk)
        slug_uk=re.sub(r'[^a-z0-9]+','-',uk.lower().replace('½','-half')).strip('-')
        near=[x for x in rows if abs(float(x['us'])-float(r['us']))<=1.5 and x['uk']!=uk][:6]
        urls.append(write(f"ring-size/uk-{slug_uk}/index.html",
          title=f"UK Ring Size {uk} in US &amp; EU — US {r['us']}, {r['dia']}mm | CaratBase",
          desc=f"UK ring size {uk} is US size {r['us']} and European size {r['eu']}. "
               f"Inside diameter {r['dia']}mm. Free converter and true-to-scale ring sizer.",
          eyebrow='Ring size conversion',
          h1=f"UK ring size {uk} in US and European sizes",
          crumb=f"UK {uk}", hub='ring-size.html', hubname='Ring size',
          answer=f"<p><strong>UK ring size {uk}</strong> is <strong>US size {r['us']}</strong> and "
                 f"<strong>European (ISO) size {r['eu']}</strong>. The inside diameter is "
                 f"<strong>{r['dia']}&nbsp;mm</strong> and the circumference "
                 f"<strong>{r['circ']}&nbsp;mm</strong>.</p>",
          body=f"""
    <h2>Checking it yourself</h2>
    <p>Measure straight across the inside of a ring that already fits. About {r['dia']}&nbsp;mm
    means UK {uk}. Or wrap paper around the finger and measure the length — about
    {r['circ']}&nbsp;mm is the same size.</p>
    <p>The UK, Ireland and Australia share this letter system, sometimes called the Wheat Sheaf
    scale. The US uses numbers, and Europe uses the circumference in millimetres directly, which
    is why the European size and the circumference above are the same figure.</p>

    <h2>Full conversion chart</h2>
    <div class="table-scroll"><table>
      <thead><tr><th>UK / AU</th><th>US</th><th>Europe</th><th>India / Japan</th>
        <th class="num">Diameter</th></tr></thead>
      <tbody>{''.join(f"<tr{HL if x['uk']==uk else ''}><td>{x['uk']}</td><td>{x['us']}</td><td>{x['eu']}</td><td>{x['jp'] if x['jp'] else '—'}</td><td class='num'>{x['dia']} mm</td></tr>" for x in rows)}</tbody></table></div>""",
          cta_h='Measure it on your screen',
          cta_p='Lay a ring against circles drawn true to life, calibrated with any bank card.',
          cta_url='ring-size.html', cta_label='Open the ring sizer',
          related=related_block('Nearby sizes',
            [(f"UK {x['uk']} → US {x['us']}",
              f"ring-size/uk-{re.sub(r'[^a-z0-9]+','-',x['uk'].lower().replace('½','-half')).strip('-')}/")
             for x in near], '../../'),
          footnote='Conversions follow ISO 8653 and the standard published charts.',
          schema=json.dumps({
            "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"What is UK ring size {uk} in US sizes?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"UK ring size {uk} is US size {r['us']}, with an inside diameter of {r['dia']} mm."}}]})))
    return urls

# ================================================================ HALLMARKS
def build_hallmarks():
    stamps = node_eval('STAMPS', 'assets/data.js')
    urls = []
    for s in stamps:
        code = s['code']
        slug_code = re.sub(r'[^a-z0-9]+', '-', code.lower()).strip('-')
        slug = f"hallmark/{slug_code}/index.html"
        others = [x for x in stamps if x['code'] != code][:8]
        worth_flag = {'solid':'Solid precious metal','filled':'Partial — low value',
                      'plated':'Plated — no metal value','lab':'Real diamond, weak resale',
                      'none':'No precious metal'}.get(s['value'], '')
        urls.append(write(slug,
          title=f"What Does {code} Mean on Jewellery? {s['metal']} — {s['purity']} | CaratBase",
          desc=f"{code} means {s['purity']}. {s['worth'][:110]}",
          eyebrow='Hallmark meaning',
          h1=f"What does {code} mean on jewellery?",
          crumb=code, hub='stamp.html', hubname='Hallmarks',
          answer=f"<p><strong>{code}</strong> means <strong>{s['purity']}</strong> "
                 f"({s['metal']}). <span class=\"pill\">{worth_flag}</span></p>"
                 f"<p style=\"margin-top:10px\">{s['worth']}</p>",
          body=f"""
    <h2>What the mark tells you</h2>
    <p>{s['note']}</p>

    <h2>Is it worth anything?</h2>
    <p>{s['worth']}</p>

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
                   'verified by a jeweller.',
          schema=json.dumps({
            "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
              {"@type":"Question","name":f"What does {code} mean on jewellery?",
               "acceptedAnswer":{"@type":"Answer","text":f"{code} means {s['purity']}. {s['note']}"}},
              {"@type":"Question","name":f"Is {code} jewellery worth anything?",
               "acceptedAnswer":{"@type":"Answer","text":s['worth']}}]})))
    return urls

# ================================================================ GOLD BY KARAT
def build_gold():
    spot = json.loads((ROOT / 'assets/metals.json').read_text())['perGram']
    karats = [('24K',0.999),('22K',0.916),('18K',0.750),('14K',0.585),('10K',0.417),('9K',0.375)]
    urls = []
    for k, pur in karats:
        per_g = spot['gold'] * pur
        rows = ''.join(
            f"<tr{HL if kk==k else ''}>"
            f"<td>{kk}</td><td class='num'>{pp*100:.1f}%</td>"
            f"<td class='num'>${spot['gold']*pp:,.2f}</td>"
            f"<td class='num'>${spot['gold']*pp*10:,.0f}</td></tr>" for kk, pp in karats)
        weights = ''.join(
            f"<tr><td>{w} g</td><td class='num'>${per_g*w:,.2f}</td>"
            f"<td class='num'>${per_g*w*0.7:,.0f} – ${per_g*w*0.9:,.0f}</td></tr>"
            for w in [1,2,5,10,20,50,100])
        urls.append(write(f"gold-price/{k.lower()}/index.html",
          title=f"{k} Gold Price Per Gram Today — ${per_g:,.2f} | CaratBase",
          desc=f"{k} gold is worth ${per_g:,.2f} per gram today ({pur*100:.1f}% pure). "
               f"Live prices, what a buyer will really pay, and a free calculator.",
          eyebrow='Live gold price',
          h1=f"{k} gold price per gram today",
          crumb=k, hub='metals.html', hubname='Metal prices',
          answer=f"<p><strong>{k} gold is worth about ${per_g:,.2f} per gram</strong> at today's "
                 f"spot price. {k} is {pur*100:.1f}% pure gold, so a gram of it contains "
                 f"{pur:.3f}&nbsp;g of gold and the rest is alloy.</p>"
                 f"<p style=\"margin-top:10px\">A scrap buyer will realistically offer "
                 f"<strong>${per_g*0.7:,.2f}–${per_g*0.9:,.2f} per gram</strong>, because they "
                 f"carry the cost of refining and take a margin.</p>",
          body=f"""
    <h2>What your piece is worth by weight</h2>
    <div class="table-scroll"><table>
      <thead><tr><th>Weight</th><th class="num">Metal value</th>
        <th class="num">Likely offer</th></tr></thead><tbody>{weights}</tbody></table></div>

    <h2>Every karat at today's price</h2>
    <div class="table-scroll"><table>
      <thead><tr><th>Karat</th><th class="num">Pure gold</th><th class="num">Per gram</th>
        <th class="num">Per 10 g</th></tr></thead><tbody>{rows}</tbody></table></div>

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
              {"@type":"Question","name":f"How pure is {k} gold?",
               "acceptedAnswer":{"@type":"Answer","text":
                 f"{k} gold is {pur*100:.1f}% pure gold by weight."}}]})))
    return urls

# ================================================================ DIAMOND CARAT x SHAPE
def build_diamonds():
    cts = [0.25,0.5,0.75,1,1.25,1.5,2,2.5,3,4,5]
    shapes = ['Round','Oval','Princess','Cushion','Emerald','Pear','Marquise','Radiant','Asscher','Heart']
    spec = "{color:'G',clarity:'VS2',cut:'Very Good',origin:'Natural',cert:'GIA'}"
    expr = ('[' + ','.join(
        f"{{ct:{c},shape:'{s}',v:valueDiamond(Object.assign({{carat:{c},shape:'{s}'}},{spec})),"
        f"d:shapeDims('{s}',{c})}}" for c in cts for s in shapes) + ']')
    data = node_eval(expr, 'assets/data.js', 'assets/shapes.js')
    by = {(d['ct'], d['shape']): d for d in data}
    urls = []
    for c in cts:
        for s in shapes:
            d = by[(c, s)]; v = d['v']; dim = d['d']
            ctxt = f"{c:g}"
            slug = f"diamond/{ctxt.replace('.','-')}-carat-{s.lower()}/index.html"
            sib = [(f"{c:g} ct {x.lower()}", f"diamond/{ctxt.replace('.','-')}-carat-{x.lower()}/")
                   for x in shapes if x != s][:6]
            other_ct = [(f"{cc:g} ct {s.lower()}", f"diamond/{('%g'%cc).replace('.','-')}-carat-{s.lower()}/")
                        for cc in cts if cc != c][:6]
            keep = round(v['resaleHigh']/v['retailHigh']*100)
            urls.append(write(slug,
              title=f"{ctxt} Carat {s} Diamond — Size in MM, Price &amp; Resale Value | CaratBase",
              desc=f"A {ctxt} carat {s.lower()} diamond measures {dim['l']}×{dim['w']}mm and costs "
                   f"{money(v['retailLow'])}–{money(v['retailHigh'])} at retail. Real resale value "
                   f"{money(v['resaleLow'])}–{money(v['resaleHigh'])}.",
              eyebrow='Diamond size and price',
              h1=f"{ctxt} carat {s.lower()} diamond: size, price and what it really resells for",
              crumb=f"{ctxt} ct {s.lower()}", hub='size.html', hubname='Diamonds',
              answer=f"<p>A <strong>{ctxt} carat {s.lower()} diamond</strong> measures about "
                     f"<strong>{dim['l']} × {dim['w']} mm</strong> face-up and costs roughly "
                     f"<strong>{money(v['retailLow'])}–{money(v['retailHigh'])}</strong> at retail "
                     f"for a G colour, VS2, well-cut stone.</p>"
                     f"<p style=\"margin-top:10px\">If you sold it, you would realistically be "
                     f"offered <strong>{money(v['resaleLow'])}–{money(v['resaleHigh'])}</strong> "
                     f"— about {keep}% of what it cost.</p>",
              body=f"""
    <h2>How big it actually looks</h2>
    <p>{dim['l']} × {dim['w']} mm is the face-up measurement — what sits above the finger. {dim['note']}</p>
    <p>Carat is a measure of <em>weight</em>, not size, and weight rises with the cube of the
    diameter. That is why doubling the carat does not come close to doubling how big a stone
    looks: a {c*2:g} carat stone is only about {(2**(1/3)):.2f} times longer than this one.</p>

    <h2>Price and the resale gap</h2>
    <div class="table-scroll"><table>
      <thead><tr><th></th><th class="num">Retail</th><th class="num">Resale</th></tr></thead>
      <tbody>
        <tr><td>{ctxt} ct {s.lower()}, G / VS2</td>
          <td class="num">{money(v['retailLow'])}–{money(v['retailHigh'])}</td>
          <td class="num" style="color:var(--bad)">{money(v['resaleLow'])}–{money(v['resaleHigh'])}</td></tr>
      </tbody></table></div>
    <p>The gap is not a criticism of buying jewellery — it is simply the number nobody mentions
    at the counter. A jeweller's price carries rent, staff, insurance and margin, and none of
    that comes back to you when you sell.</p>

    <h2>What changes this figure</h2>
    <p>Colour and clarity move it most. Dropping from G to J colour and VS2 to SI2 buys a
    noticeably larger stone for the same money, and above about G and VS2 almost nothing you
    pay for is visible without a loupe. Cut is the exception and the one grade worth
    protecting: a badly cut diamond looks dull whatever else is true of it.</p>""",
              cta_h='Value your own stone',
              cta_p='Enter your exact specification — including side stones and the metal it is '
                    'set in — and get both numbers for your piece rather than this example.',
              cta_url='value.html', cta_label='Value my diamond',
              related=(related_block(f'The same weight in other shapes', sib, '../../') +
                       related_block(f'Other weights in {s.lower()}', other_ct, '../../')),
              footnote='Estimates for a G colour, VS2 clarity, Very Good cut, GIA-graded natural '
                       'stone. Individual stones vary.',
              schema=json.dumps({
                "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                  {"@type":"Question","name":f"How big is a {ctxt} carat {s.lower()} diamond?",
                   "acceptedAnswer":{"@type":"Answer","text":
                     f"A {ctxt} carat {s.lower()} diamond measures about {dim['l']} by {dim['w']} "
                     f"millimetres face-up."}},
                  {"@type":"Question","name":f"How much does a {ctxt} carat {s.lower()} diamond cost?",
                   "acceptedAnswer":{"@type":"Answer","text":
                     f"About {money(v['retailLow'])} to {money(v['retailHigh'])} at retail for a "
                     f"G colour, VS2 clarity, well-cut stone. Resale is typically "
                     f"{money(v['resaleLow'])} to {money(v['resaleHigh'])}."}}]})))
    return urls

# ================================================================ GEMSTONES
def build_gems():
    names = node_eval('Object.keys(GEMS)', 'assets/gems.js')
    expr = ('[' + ','.join(
        f"{{t:{json.dumps(n)},v:valueGem({{type:{json.dumps(n)},carat:2,tier:'Fine',"
        f"treatment:'Heated (standard)',origin:Object.keys(GEMS[{json.dumps(n)}].origins).slice(-1)[0]}}),"
        f"origins:Object.keys(GEMS[{json.dumps(n)}].origins)}}" for n in names) + ']')
    data = node_eval(expr, 'assets/gems.js')
    urls = []
    for d in data:
        n = d['t']; v = d['v']
        slug_n = re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
        prem = [o for o in d['origins'] if 'Unknown' not in o]
        urls.append(write(f"gemstone/{slug_n}/index.html",
          title=f"{n} Value — What Is a 2 Carat {n} Worth? | CaratBase",
          desc=f"A fine 2 carat {n.lower()} is worth {money(v['retailLow'])}–{money(v['retailHigh'])} "
               f"at retail. Treatment changes this more than size does. Free valuation calculator.",
          eyebrow='Coloured stone value',
          h1=f"What is a {n.lower()} worth?",
          crumb=n, hub='gemstone.html', hubname='Gemstones',
          answer=f"<p>A <strong>fine 2 carat {n.lower()}</strong>, heated and without certified "
                 f"origin, is worth roughly <strong>{money(v['retailLow'])}–{money(v['retailHigh'])}</strong> "
                 f"at retail — about {money(v['ppc'])} per carat.</p>"
                 f"<p style=\"margin-top:10px\">Resale is far lower: "
                 f"<strong>{money(v['resaleLow'])}–{money(v['resaleHigh'])}</strong>. Coloured "
                 f"stones have no universal grading standard, so a buyer carries more risk and "
                 f"prices for it.</p>",
          body=f"""
    <h2>Treatment matters more than size</h2>
    <p>This is the single most important thing about {n.lower()} value, and the thing owners
    least often know about their own stone. An untreated stone with a laboratory report can be
    worth several times a heated one, and a fracture-filled or dyed stone can be worth a tiny
    fraction of either — while looking much the same across a counter.</p>
    <p>Heating is routine, permanent and accepted throughout the trade. Assume any stone is
    heated unless a report says otherwise.</p>

    <h2>Origin, but only if certified</h2>
    <p>{'For ' + n.lower() + ', the sources that command a premium are ' + ', '.join(prem[:3]) + '.' if prem else 'Origin has little effect on this stone.'}
    A premium applies only when a recognised laboratory has certified the origin in writing.
    A seller's claim on its own is worth nothing.</p>

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
                 f"Treatment affects this more than size does."}}]})))
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

    # sitemap: hand-built pages first, then everything generated
    core = ['', 'value.html','gemstone.html','budget.html','metals.html','stamp.html',
            'size.html','ring-size.html','measure.html','vault.html','methodology.html',
            'disclaimer.html','privacy.html','terms.html']
    def entry(u, pri, freq):
        loc = f'{BASE}/{u}'.rstrip('/') + ('/' if u.endswith('/index.html') or u=='' else '')
        loc = f'{BASE}/{u}'.replace('/index.html','/')
        return (f'  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
                f'<changefreq>{freq}</changefreq><priority>{pri}</priority></url>')
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines.append(entry('', '1.0', 'daily'))
    for u in core[1:]:
        pri = '0.3' if u in ('privacy.html','terms.html') else '0.9'
        lines.append(entry(u, pri, 'weekly'))
    for u in urls:
        lines.append(entry(u, '0.7', 'monthly'))
    lines.append('</urlset>')
    (ROOT/'sitemap.xml').write_text('\n'.join(lines) + '\n')
    print(f'\n  sitemap: {len(urls)+len(core)} URLs')
    return urls

if __name__ == '__main__':
    print('Generating long-tail pages...\n')
    main()

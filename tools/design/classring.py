"""The class ring page.

14 queries in the harvest and all of them the same question asked in different words.
It fits the scrap cluster rather than diluting it: a class ring is the archetypal piece
of old gold someone wants to sell, and the honest answer — melt value and nothing more
— is exactly the kind of number this site exists to print.

Two traps to expose, and they are the whole page:

  1. Half of all class rings are not precious metal at all. Valadium, Lustrium,
     Siladium, Celestrium, Ultrium and Lazon are trade names for stainless-steel-family
     alloys, chosen to sound like something. Scrap value: nothing.
  2. The stone is a synthetic or a piece of glass, and people assume it is a ruby.

Merged into PAGES by tools/design/pages.py.
"""

# Stamp -> (purity as a fraction of pure gold, label, what it actually is)
# Base-metal trade names are the reason this page exists.
METALS = [
    ('10K',  0.417, '10K gold',        'The most common class ring metal by far. 41.7% gold.'),
    ('14K',  0.585, '14K gold',        'Less common on class rings, and worth about 40% more per gram than 10K.'),
    ('18K',  0.750, '18K gold',        'Rare on class rings. Usually a custom or much older piece.'),
    ('925',  None,  'Sterling silver', 'Real precious metal, but silver is cheap by weight. A heavy ring is still only a few tens of dollars.'),
    ('VAL',  0.0,   'Valadium',        'Base metal. A stainless-steel-family alloy, not gold.'),
    ('LTM',  0.0,   'Lustrium',        'Base metal. Trade name, no precious content.'),
    ('SIL',  0.0,   'Siladium',        'Base metal despite the name. Contains no silver.'),
    ('CELE', 0.0,   'Celestrium',      'Base metal. A Jostens trade name.'),
    ('ULT',  0.0,   'Ultrium',         'Base metal. No scrap value.'),
    ('LZN',  0.0,   'Lazon',           'Base metal. No scrap value.'),
]

BASE_NAMES = [m for m in METALS if m[1] == 0.0]

WEIGHTS = [
    ("Men's, heavy / traditional", '18–25 g'),
    ("Men's, standard", '14–18 g'),
    ("Women's, standard", '7–12 g'),
    ("Women's, slim or petite", '4–8 g'),
]


def _base_table():
    head = ('<table class="tbl"><thead><tr><th>Stamped inside</th><th>Sold as</th>'
            '<th>What it is</th><th class="num">Scrap value</th></tr></thead><tbody>')
    rows = []
    for code, _p, label, note in BASE_NAMES:
        rows.append('<tr><td><strong>' + code + '</strong></td><td>' + label + '</td>'
                    '<td>' + note + '</td><td class="num">None</td></tr>')
    return head + ''.join(rows) + '</tbody></table>'


def _weight_table():
    head = '<table class="tbl"><thead><tr><th>Ring</th><th class="num">Typical weight</th></tr></thead><tbody>'
    rows = ['<tr><td>' + a + '</td><td class="num">' + b + '</td></tr>' for a, b in WEIGHTS]
    return head + ''.join(rows) + '</tbody></table>'


BODY = '''
  <section class="console">
    <div class="console-head"><span class="name"><span class="dot"></span> Class ring</span><span class="status">metal &middot; weight &middot; what you get</span></div>
    <div class="console-body">
      <div class="console-in">
        <h3>What is stamped inside the band</h3>
        <div class="field"><label>Stamp or metal</label><select id="cMetal"></select></div>
        <div class="grid g2" style="gap:12px">
          <div class="field"><label>Weight in grams</label><input type="number" id="cW" value="16" step="0.1" min="0"></div>
          <div class="field"><label>Not sure of the weight?</label><select id="cGuess">
            <option value="">Use my number</option>
            <option value="21">Men's, heavy</option>
            <option value="16">Men's, standard</option>
            <option value="9.5">Women's, standard</option>
            <option value="6">Women's, slim</option>
          </select></div>
        </div>
        <p class="small">Kitchen scales that read to 1 g are accurate enough here; a jeweler will weigh it properly before making an offer. Do not deduct for the stone &mdash; it weighs almost nothing and is worth nothing.</p>
      </div>
      <div class="console-out" id="cOut"><div class="lab">Waiting for input</div></div>
    </div>
  </section>

  <div id="cVerdict" style="margin-top:22px"></div>

  <section class="section narrow" style="padding-top:44px">
    <h2>First, check it is actually gold</h2>
    <p>This is where most of the disappointment lives. Class ring makers sold enormous numbers of rings in alloys with invented names that sound precious and are not. If the inside of your band carries one of these, the ring is a stainless-steel-family alloy and has no scrap value at all.</p>
    ''' + _base_table() + '''
    <p style="margin-top:14px">A real gold ring is stamped with its karat &mdash; <strong>10K</strong>, <strong>14K</strong>, occasionally <strong>18K</strong>, sometimes written 417, 585 or 750. Sterling is stamped <strong>925</strong>. Anything else is a trade name, and a trade name means base metal. Our <a href="stamp.html">hallmark lookup</a> will decode anything not on this list.</p>
    <p>If there is no stamp at all, a jeweler can test it in under a minute with acid or an XRF gun, usually free while you wait.</p>
  </section>

  <section class="section narrow">
    <h2>The stone is not a ruby</h2>
    <p>Class ring stones are synthetic corundum, synthetic spinel, cubic zirconia or plain colored glass. They were manufactured to look like a birthstone, not to be one. There is no meaningful resale value in the stone, and no buyer will pay extra for it.</p>
    <p>That is worth knowing before you pay anyone to remove it, or turn down an offer because you think the stone is carrying value it is not. If you have a piece where the stone genuinely might matter, <a href="value.html">value it as jewelry instead</a>.</p>
  </section>

  <section class="section narrow">
    <h2>Why melt value is the whole price</h2>
    <p>A class ring is the hardest kind of jewelry to resell intact. It carries someone else's school, someone else's year and frequently someone else's initials, so the second-hand market for it is almost exactly nobody. Antique and estate buyers who would pay a premium for a signed period piece have no interest in a 1998 high school ring.</p>
    <p>So the metal is the price. That is not a bad outcome &mdash; class rings are unusually heavy for their size, and a men's 10K ring at 16&nbsp;g carries real weight compared with a modern hollow chain. It just means the number is set by the scale and the karat, not by sentiment or by what it cost new.</p>
    ''' + _weight_table() + '''
    <p style="margin-top:14px">Once you know the melt figure, who you sell to decides the rest: a refiner pays 85&ndash;95% of it, a pawn shop 40&ndash;70%. The difference on a single ring is often a hundred dollars or more. The <a href="scrap-gold-calculator.html">scrap gold page</a> has the full payout ladder and a checker for any offer you are given.</p>
  </section>

  <section class="section narrow">
    <h2>Before you sell it</h2>
    <p><strong>Consider not selling it.</strong> This is the one piece of jewelry people most often regret scrapping, because the money is modest and the object is not replaceable. A men's 10K ring is a few hundred dollars. If that is not the difference between anything, the ring may be worth more to you in a drawer.</p>
    <p><strong>If it is a family ring, photograph it first.</strong> The engraving inside &mdash; school, year, initials &mdash; is the part nobody can get back once it is melted.</p>
    <p><strong>Get three quotes.</strong> Class rings are a staple of the cash-for-gold trade and are routinely bought at the low end of the range, because the seller rarely knows the melt figure. Walk in with the number above.</p>
  </section>
'''

SCRIPT = r'''
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var METALS = __METALS__;;

  $('cMetal').innerHTML = METALS.map(function(m, i){
    return '<option value="' + i + '"' + (m[0] === '10K' ? ' selected' : '') + '>' +
           m[2] + ' (' + m[0] + ')</option>';
  }).join('');

  function perGram(m){
    if(m[0] === '925') return METAL_SPOT.silver * 0.925;
    return METAL_SPOT.gold * (m[1] || 0);
  }

  function calc(){
    var m = METALS[parseInt($('cMetal').value, 10)] || METALS[0];
    var g = parseFloat($('cW').value) || 0;
    var melt = g * perGram(m);
    var isBase = (m[1] === 0);

    if(isBase){
      $('cOut').innerHTML =
        '<div class="lab">Scrap value</div>' +
        '<div class="big">$0</div>' +
        '<div class="sub">' + m[2] + ' is a base metal alloy — no gold, no silver</div>' +
        '<div class="note">Nobody buys this for scrap, at any weight. If the ring matters to you, keep it; ' +
        'if it does not, it is not worth a trip.</div>';
      $('cVerdict').innerHTML =
        '<div class="panel"><span class="pill">Not precious metal</span>' +
        '<h3 style="margin:10px 0 6px;font-size:19px">' + m[2] + ' has no scrap value</h3>' +
        '<p class="small">It is a stainless-steel-family alloy with a trade name chosen to sound like ' +
        'something. This is the single most common surprise on this page, and it is worth ' +
        'double-checking the stamp before you write the ring off — a real gold ring says 10K, 14K, ' +
        '18K, 417, 585 or 750.</p></div>';
      if(window.cbTrack) cbTrack('tool_use', {tool:'class_ring', metal:m[0], base:true});
      return;
    }

    if(!melt){ $('cOut').innerHTML = '<div class="lab">Enter a weight</div>'; $('cVerdict').innerHTML=''; return; }

    /* Same payout ladder as the scrap page — a class ring is scrap. */
    var refiner = [melt*0.85, melt*0.95], pawn = [melt*0.40, melt*0.70];

    $('cOut').innerHTML =
      '<div class="lab">Melt value — the metal in the ring</div>' +
      '<div class="big">' + fmt(melt) + '</div>' +
      '<div class="sub">' + g.toFixed(1) + ' g of ' + m[2] + ' · ' + fmt(perGram(m)) + ' per gram</div>' +
      '<div class="split">' +
        '<div><div class="lab">A refiner pays</div><div class="v">' + fmt(refiner[0]) + '–' + fmt(refiner[1]) + '</div></div>' +
        '<div><div class="lab">A pawn shop pays</div><div class="v">' + fmt(pawn[0]) + '–' + fmt(pawn[1]) + '</div></div>' +
      '</div>' +
      '<div class="note">The stone adds nothing. Who you sell to is worth ' +
      fmt(refiner[1] - pawn[0]) + ' on this ring.</div>';

    $('cVerdict').innerHTML =
      '<div class="grid g2">' +
      '<div class="panel"><span class="pill pill-ice">Melt is the price</span>' +
      '<h3 style="margin:10px 0 6px;font-size:19px">There is no collector premium</h3>' +
      '<p class="small">A class ring carries someone else&rsquo;s school, year and initials, so almost nobody ' +
      'wants it intact. Estate buyers who pay a premium for signed period pieces have no interest. ' +
      'The scale and the karat set the price.</p></div>' +
      '<div class="panel"><span class="pill">Worth knowing</span>' +
      '<h3 style="margin:10px 0 6px;font-size:19px">Three quotes, not one</h3>' +
      '<p class="small">Class rings are a staple of the cash-for-gold trade and are routinely bought at ' +
      'the bottom of the range, because the seller rarely knows the melt figure. You now do: ' +
      fmt(melt) + '.</p></div></div>';

    if(window.cbTrack) cbTrack('tool_use', {tool:'class_ring', metal:m[0], grams:g});
  }

  $('cGuess').addEventListener('change', function(){
    if(this.value){ $('cW').value = this.value; calc(); }
  });
  ['cMetal','cW'].forEach(function(id){ $(id).addEventListener('input', calc); });
  document.addEventListener('cb:spot', calc);
  calc();
})();
'''

# Substituted after the fact so SCRIPT stays a single raw string end to end. Building it
# as r'''...''' + repr(...) + '''...''' makes only the first segment raw, and a \' in a
# later segment quietly loses its backslash — which broke this page's JS once already.
SCRIPT = SCRIPT.replace(
    '__METALS__',
    repr([[c, p, l] for c, p, l, _n in METALS]).replace('None', 'null'))


def page(faq):
    return dict(
        title='Class Ring Value Calculator — What Yours Is Really Worth',
        desc='What a 10K, 14K or sterling class ring is worth as scrap, what a refiner pays '
             'against a pawn shop, and how to tell if yours is gold or a base metal alloy.',
        eyebrow='Class rings',
        h1='What is your class ring worth?',
        lede='Almost always its melt value and nothing more — and for about half of all class '
             'rings, nothing at all, because they were made in base metal alloys with names chosen '
             'to sound precious. Check the stamp, weigh it, and see the real number before anyone '
             'makes you an offer.',
        schema=faq([
            ('How much is a 10K gold class ring worth?',
             'Its melt value, which is the weight multiplied by 41.7% (the gold content of 10K) '
             'multiplied by the current gold price per gram. A men’s class ring typically '
             'weighs 14–25 g, so most come to a few hundred dollars. What you are actually '
             'paid is a share of that: roughly 85–95% from a refiner, 60–80% from a local '
             'jeweler and 40–70% from a pawn shop.'),
            ('What does VAL, LTM or Siladium mean on a class ring?',
             'They are trade names for base metal. Valadium (VAL), Lustrium (LTM), Siladium (SIL), '
             'Celestrium (CELE), Ultrium (ULT) and Lazon (LZN) are stainless-steel-family alloys '
             'containing no gold or silver, whatever the name suggests — Siladium contains no '
             'silver at all. Rings stamped with any of them have no scrap value. A genuine gold '
             'class ring is stamped 10K, 14K, 18K, 417, 585 or 750.'),
            ('Is the stone in a class ring worth anything?',
             'No. Class ring stones are synthetic corundum, synthetic spinel, cubic zirconia or '
             'colored glass, manufactured to resemble a birthstone rather than to be one. No buyer '
             'pays extra for it, and it is not worth paying to have it removed before selling.'),
            ('Can I sell a class ring for more than scrap value?',
             'Very rarely. A class ring carries a specific school, year and usually initials, so the '
             'second-hand market is effectively nobody, and the estate buyers who pay premiums for '
             'signed period jewelry have no interest in one. Melt value is the realistic price. The '
             'exception is a genuinely antique ring or one from a notable institution, which is '
             'worth having looked at before scrapping.'),
        ]),
        body=BODY,
        script=SCRIPT,
    )

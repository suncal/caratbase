"""The fluorescence study.

Heath's suggestion, and the best traffic idea anyone has offered: publish something
with a finding in it rather than another calculator. This is the one we have.

The finding is that fluorescence is the only grade on a diamond report whose effect on
price reverses direction, and that the crossover sits between H and I color. Everyone
in the trade half-knows this; nobody appears to have written down where the line actually
falls or what it is worth in dollars.

Honesty constraint, and it matters more than the finding: this is a MODELED analysis,
not transaction data. The inputs are published trade discount ranges applied
systematically through our own pricing engine. The contribution is the systematic
application and the located crossover, not new price discovery, and the page says so in
plain terms. A study that implied data it does not have would be torn apart the moment it
got the attention it was written to attract.

Tables render from the live engine rather than being typed in, so they cannot drift away
from what the site's own calculators say.

Merged into PAGES by tools/design/pages.py.
"""

BODY = '''
  <div class="panel" style="border-color:var(--gold-2);margin-bottom:28px">
    <div class="eyebrow">The finding</div>
    <p style="margin-top:10px;font-size:17px;line-height:1.7">Blue fluorescence is the only grade on a diamond
    report whose effect on price <strong>reverses direction</strong> depending on another grade. In a colorless
    D, E or F it is a fault worth roughly <strong>12% of the price</strong>. From I color down it is an
    advantage, and those stones trade at a small premium. The crossover sits
    <strong>between H and I</strong>.</p>
    <p class="small" style="margin-top:12px">On a 1 carat VS1 round, that is a <strong>$1,013 difference</strong>
    between a D with strong fluorescence and a D without — for something most people cannot see in most light.</p>
  </div>

  <section class="section narrow">
    <h2>What fluorescence is, in one paragraph</h2>
    <p>Roughly a quarter to a third of diamonds glow under ultraviolet light, almost always blue. It is a
    property of the stone, graded on every GIA report from None through Faint, Medium, Strong and Very Strong.
    It is not a treatment, not damage, and not a flaw in any physical sense. It is simply a thing the diamond
    does under a lamp most people will never shine on it.</p>
    <p>The reason it moves money is that blue sits opposite yellow on the color wheel. In a diamond that is
    already colorless, a blue cast is a deviation from the thing you paid for. In a diamond carrying a faint
    yellow tint, the same blue cancels some of it out.</p>
  </section>

  <section class="section">
    <h2>Where the line falls</h2>
    <p class="small" style="margin-bottom:14px">What a fluorescent stone prices like, expressed as the
    non-fluorescent color grade it is worth the same as. Read along a row: a D with strong fluorescence is
    priced as though it were an F.</p>
    <div id="flEquiv"></div>
    <p style="margin-top:14px">Three grades behave in three different ways, and they are not a gradient — they
    are a sign change. D through F are discounted. G and H are priced within a few percent either way, which is
    noise. I and below carry a small premium, because at that point the blue is doing visible work.</p>
  </section>

  <section class="section">
    <h2>What it is worth in money</h2>
    <p class="small" style="margin-bottom:14px">Mid-point retail for a 1.00 carat VS1 round brilliant, excellent
    cut, by color grade and fluorescence. Live figures from the same engine that runs the rest of this site.</p>
    <div id="flGrid"></div>
  </section>

  <section class="section narrow">
    <h2>If you are buying</h2>
    <p>This is one of the few places in the diamond market where the conventional prejudice is strong enough to
    pay you for ignoring it.</p>
    <div id="flSaving"></div>
    <p style="margin-top:14px">A D or E with strong fluorescence is a top color grade at a meaningful discount,
    and in ordinary indoor light almost nobody can tell. If you want the certificate to say D and you do not want
    to pay what D usually costs, this is the lever.</p>
    <p><strong>The caveat, and it is a real one.</strong> A small minority of very strongly fluorescent diamonds
    look hazy, oily or milky in daylight. That is a genuine defect, it is discounted far harder than the table
    above, and it is visible to the naked eye. So the rule is simple: fluorescence is worth buying, sight unseen
    it is not. Look at the stone in daylight before you commit.</p>
  </section>

  <section class="section narrow">
    <h2>If you are selling</h2>
    <p>If you own a colorless stone with strong fluorescence, this is the single most common reason an offer
    comes in below what you expected, and the buyer is unlikely to explain it. The discount is real and it is
    already priced into what you will be offered.</p>
    <p>If you own an I, J or K with fluorescence, the opposite holds and almost nobody will tell you: your stone
    is slightly easier to sell than its grade suggests, because it faces up better than the paper says. Do not
    accept a discount for it.</p>
  </section>

  <section class="section narrow">
    <h2>How this was calculated</h2>
    <p>Worth being precise, because the distinction matters. <strong>This is a modeled analysis, not a dataset
    of transactions.</strong> We did not observe thousands of sales. What we did was take the fluorescence
    discount ranges published by the trade &mdash; commonly quoted as 5% to 40% for strong blue on colorless
    stones, with around 12% typical, and flat to a small premium on tinted stones &mdash; and apply them
    systematically across the whole color range through the pricing engine that drives every valuation on this
    site.</p>
    <p>The contribution here is not new price discovery. It is that the adjustment is usually described in
    anecdotes &mdash; "fluorescence is bad in high colors, fine in low ones" &mdash; and almost never written
    down as a position. Putting numbers against each grade locates the crossover, and the crossover turns out to
    be the useful part.</p>
    <p>The engine, the per-carat curve and the resale bands behind these figures are published in full on our
    <a href="jewelry-price-index.html">price index</a>, and the method is set out on our
    <a href="methodology.html">methodology page</a>, including what it cannot tell you.</p>
    <p class="small">Figures are indicative retail for a well-cut natural stone and will not match any
    individual quote. Individual stones vary, markets move, and the strongly-fluorescent minority described
    above sits outside this model entirely.</p>
  </section>

  <section class="section narrow">
    <h2>Use this</h2>
    <p>Published under <strong>Creative Commons Attribution 4.0</strong>. Reproduce the tables, chart them, quote
    the numbers, build on them &mdash; commercially included &mdash; provided you credit CaratBase and link back.</p>
    <div class="panel" style="margin-top:14px">
      <div class="eyebrow">Cite this</div>
      <p class="small" style="margin-top:10px">CaratBase. <em>Diamond Fluorescence and Price: where the discount
      becomes a premium</em>. Retrieved <span id="flToday"></span>, from
      https://caratbase.com/diamond-fluorescence-study.html</p>
      <button type="button" class="btn btn-ghost" id="flCite" style="margin-top:12px;padding:6px 14px;font-size:13px">Copy citation</button>
    </div>
    <p class="small" style="margin-top:14px">Want this applied to your own stone? The
    <a href="gia-report-value.html">GIA report reader</a> takes the grades off your report and prices the
    fluorescence adjustment into the result.</p>
  </section>
'''

SCRIPT = r'''
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var COLORS = ['D','E','F','G','H','I','J','K'];
  var FL = ['None','Faint','Medium','Strong','Very Strong'];

  function tbl(head, rows, firstBold){
    return '<div style="overflow-x:auto"><table class="tbl"><thead><tr>' +
      head.map(function(h,i){ return '<th' + (i ? ' class="num"' : '') + '>' + h + '</th>'; }).join('') +
      '</tr></thead><tbody>' + rows.map(function(r){
        return '<tr>' + r.map(function(c,i){
          return '<td' + (i ? ' class="num"' : '') + '>' +
                 (i === 0 && firstBold ? '<strong>' + c + '</strong>' : c) + '</td>';
        }).join('') + '</tr>';
      }).join('') + '</tbody></table></div>';
  }

  /* mid-point retail for one spec, straight from the site's own engine */
  function mid(color, fluo){
    var v = valueGiaReport({shape:'Round', carat:1, color:color, clarity:'VS1',
                            cut:'Excellent', polish:'Excellent', symmetry:'Excellent',
                            fluorescence:fluo, origin:'Natural'});
    return (v.retailLow + v.retailHigh) / 2;
  }

  /* the nearest non-fluorescent color grade of equal value */
  function equivalent(color, fluo){
    var eff = COLOR_MULT[color] * fluoMultiplier(color, fluo);
    var best = null, bd = Infinity;
    COLORS.forEach(function(c){
      var d = Math.abs(COLOR_MULT[c] - eff);
      if(d < bd){ bd = d; best = c; }
    });
    return best;
  }

  $('flEquiv').innerHTML = tbl(
    ['Actual color'].concat(FL),
    COLORS.map(function(c){
      return [c].concat(FL.map(function(f){
        var e = equivalent(c, f);
        if(e === c) return '<span style="color:var(--ink-3)">' + e + '</span>';
        var worse = COLORS.indexOf(e) > COLORS.indexOf(c);
        return '<strong style="color:' + (worse ? 'var(--bad,#9B4B3F)' : 'var(--good,#3F7A52)') +
               '">' + e + '</strong>';
      }));
    }), true);

  $('flGrid').innerHTML = tbl(
    ['Color'].concat(FL),
    COLORS.map(function(c){
      return [c].concat(FL.map(function(f){ return fmt(mid(c, f)); }));
    }), true);

  $('flSaving').innerHTML = tbl(
    ['Color', 'No fluorescence', 'Strong fluorescence', 'Difference'],
    COLORS.map(function(c){
      var a = mid(c, 'None'), b = mid(c, 'Strong'), d = a - b;
      var label = d > 1 ? '<strong style="color:var(--good,#3F7A52)">saves ' + fmt(d) + '</strong>'
                : d < -1 ? '<span style="color:var(--bad,#9B4B3F)">costs ' + fmt(-d) + '</span>'
                : '<span style="color:var(--ink-3)">about the same</span>';
      return [c, fmt(a), fmt(b), label];
    }), true);

  var today = new Date().toLocaleDateString('en-US', {year:'numeric', month:'long', day:'numeric'});
  $('flToday').textContent = today;
  $('flCite').addEventListener('click', function(){
    var t = 'CaratBase. Diamond Fluorescence and Price: where the discount becomes a premium. ' +
            'Retrieved ' + today + ', from https://caratbase.com/diamond-fluorescence-study.html';
    if(navigator.clipboard) navigator.clipboard.writeText(t).then(function(){
      $('flCite').textContent = 'Copied';
      setTimeout(function(){ $('flCite').textContent = 'Copy citation'; }, 1600);
    });
    if(window.cbTrack) cbTrack('cite_copy', {page:'fluorescence-study'});
  });
})();
'''


def page(faq):
    return dict(
        title='Diamond Fluorescence and Price — Where the Discount Becomes a Premium',
        desc='Fluorescence is the only grade on a diamond report whose effect on price reverses. '
             'It costs about 12% at D–F and pays a premium from I down. The crossover is between H and I.',
        eyebrow='Research',
        h1='Where a diamond’s fluorescence stops being a fault',
        lede='Blue fluorescence is the only grade on a GIA report whose effect on price changes sign. '
             'In a colorless stone the trade treats it as a defect and discounts it; in a tinted one it '
             'masks the tint and earns a small premium. We put numbers against every color grade to find '
             'out exactly where the line falls, and what crossing it is worth.',
        scripts=('lead.js',),
        schema=faq([
            ('Does fluorescence lower the value of a diamond?',
             'Only in colorless stones. In D, E and F color, strong blue fluorescence is treated by the '
             'trade as a fault and discounted around 12% — the published range runs from 5% to 40% '
             'depending on severity. At G and H the effect is within a few percent either way. From I color '
             'down it reverses: the blue masks the faint yellow tint, the stone faces up whiter than its grade, '
             'and those diamonds trade at a small premium. The crossover sits between H and I.'),
            ('Is a diamond with strong fluorescence a good buy?',
             'In a high color grade, often yes. A D or E with strong fluorescence is a top color grade at '
             'roughly 12% less, and in ordinary indoor light the difference is invisible to almost everyone. '
             'The exception is a small minority of very strongly fluorescent stones that look hazy or milky in '
             'daylight — that is a genuine defect, discounted much harder, and visible to the naked eye. '
             'So it is worth buying, but not worth buying sight unseen.'),
            ('What does strong fluorescence do to a 1 carat diamond’s price?',
             'On a 1.00 carat VS1 round brilliant, a D color drops from about $8,425 to $7,413 with strong '
             'fluorescence — a difference of roughly $1,013. The same stone at I color goes the other way, '
             'gaining a little. The effect scales with the price of the stone, so it is worth more in absolute '
             'terms on larger or higher-graded diamonds.'),
            ('Why does fluorescence help lower color grades?',
             'Blue sits opposite yellow on the color wheel. A diamond graded I, J or K carries a faint yellow '
             'tint, and a blue fluorescent glow cancels part of it, so the stone can face up close to a grade '
             'whiter than its certificate says. In a diamond that is already colorless there is no tint to '
             'cancel, so the same blue cast reads as a deviation from what was paid for.'),
        ]),
        body=BODY,
        script=SCRIPT,
    )

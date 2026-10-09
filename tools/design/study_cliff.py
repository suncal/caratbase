"""The carat cliff study.

Second research piece, same treatment as the fluorescence one: a finding, computed from
the site's own engine, published CC BY with a citation.

The finding most people have half-heard is "buy just under a round number". What nobody
seems to have written down is that the saving is large enough to buy two color grades —
so a 0.99 ct E costs LESS than a 1.00 ct G, is two grades better, and faces up the same
size. That is the piece.

Precision note that matters: the site's mm table rounds to one decimal, which makes the
0.99/1.00 difference look like exactly zero. It is not. Diameter scales with the cube
root of weight, so the real gap is about 0.02 mm. The page says 0.02 mm, not zero —
overclaiming a number that is checkable in ten seconds would undo the whole point of
publishing research.

Merged into PAGES by tools/design/pages.py.
"""

BODY = '''
  <div class="panel" style="border-color:var(--gold-2);margin-bottom:28px">
    <div class="eyebrow">The finding</div>
    <p style="margin-top:10px;font-size:17px;line-height:1.7">Diamond prices do not rise smoothly with weight.
    They step, sharply, at the round numbers &mdash; and the step is big enough that
    <strong>a 0.99 carat E color costs less than a 1.00 carat G</strong>, is two color grades better, and
    faces up about <strong>two hundredths of a millimeter</strong> smaller.</p>
    <p class="small" style="margin-top:12px">That is not a rounding artifact or a quirk of one retailer. It
    happens at every magic weight, and the largest step of all is at half a carat, where crossing the line
    costs <strong>44%</strong>.</p>
  </div>

  <section class="section narrow">
    <h2>Why the steps exist</h2>
    <p>Diamonds are priced per carat, and the price <em>per carat</em> itself jumps at weights people ask for by
    name. Nobody walks into a shop asking for a 0.94. They ask for a half carat, or a one carat, so that is
    where demand concentrates and where the per-carat rate resets upward.</p>
    <p>A cutter faces the same incentive from the other side. Given rough that could yield a beautifully
    proportioned 0.96 or a slightly deep 1.01, the 1.01 is worth materially more, so that is frequently what
    gets cut &mdash; which is also why stones just over a round number are sometimes cut a little deep, hiding
    weight in the pavilion where it does not show.</p>
    <p>The result is a market where the hundredth of a carat either side of a round number is the most
    expensive hundredth you will ever buy.</p>
  </section>

  <section class="section">
    <h2>Every cliff, measured</h2>
    <p class="small" style="margin-bottom:14px">Mid-point retail for a well-cut round brilliant at G color and
    VS2 clarity, one hundredth under each magic weight against the weight itself. Face-up diameter from the
    cube-root relationship between weight and width.</p>
    <div id="clGrid"></div>
    <p style="margin-top:14px">The half-carat step is the steepest in proportional terms and the one that
    matters most to the people least able to absorb it. At the top end the percentages settle around a third,
    but a third of a large number is a lot of money.</p>
  </section>

  <section class="section">
    <h2>What stepping back buys you</h2>
    <p class="small" style="margin-bottom:14px">At the one carat line, the saving from dropping to 0.99
    compared against what the same money buys in color on the smaller stone.</p>
    <div id="clTrade"></div>
    <p style="margin-top:14px">This is the part worth sitting with. The saving does not just cover an upgrade
    &mdash; it overshoots it. You can move two color grades, from G to E, and still be <strong>$275 better
    off</strong> than the 1.00 carat G you were originally looking at. The stones are visually the same size.
    One has noticeably better color and a smaller number on the certificate.</p>
  </section>

  <section class="section">
    <h2>The saving by color grade</h2>
    <p class="small" style="margin-bottom:14px">What you keep by buying 0.99 instead of 1.00, at each color
    grade. The better the stone, the more the hundredth of a carat costs.</p>
    <div id="clByColor"></div>
  </section>

  <section class="section narrow">
    <h2>When not to do this</h2>
    <p>Two honest caveats, because the strategy is not free.</p>
    <p><strong>If the number matters to you, the number matters.</strong> Some people want a certificate that
    says one carat, and there is nothing irrational about that &mdash; it is the thing being bought. This
    analysis prices the trade-off; it does not tell you the trade-off is wrong.</p>
    <p><strong>Resale inherits the same cliff.</strong> A 0.99 is harder to sell than a 1.00 for exactly the
    reason it was cheaper, so the discount you enjoyed going in is a discount you concede coming out. Since
    diamonds resell at <a href="jewelry-price-index.html">25&ndash;40% of retail</a> regardless, this matters
    less than it sounds &mdash; but it is not nothing, and anyone presenting the just-under stone as free money
    is not being straight with you.</p>
    <p>It also stacks with the other direction-reversing grade on a certificate: see
    <a href="diamond-fluorescence-study.html">where a diamond&rsquo;s fluorescence stops being a fault</a>.</p>
  </section>

  <section class="section narrow">
    <h2>How this was calculated</h2>
    <p>Same basis as everything else here, and the same caveat. <strong>This is a modeled analysis, not a
    dataset of transactions.</strong> The per-carat curve, the color and clarity multipliers and the bracket
    boundaries are our own pricing model, published in full on the
    <a href="jewelry-price-index.html">price index</a> and explained on the
    <a href="methodology.html">methodology page</a>.</p>
    <p>Face-up diameter is computed from the cube-root relationship between weight and linear dimension, which
    is why the difference across a cliff is around two hundredths of a millimeter rather than zero. Our size
    charts round to one decimal place and would show the two stones as identical; they are not quite, and the
    honest figure is the one above.</p>
    <p class="small">Figures are indicative retail for a well-cut natural stone and will not match any
    individual quote. Real cliffs are a little softer than modeled ones, because a 0.995 exists and gets
    rounded on the certificate.</p>
  </section>

  <section class="section narrow">
    <h2>Use this</h2>
    <p>Published under <strong>Creative Commons Attribution 4.0</strong>. Reproduce the tables, chart them,
    quote the numbers &mdash; commercially included &mdash; provided you credit CaratBase and link back.</p>
    <div class="panel" style="margin-top:14px">
      <div class="eyebrow">Cite this</div>
      <p class="small" style="margin-top:10px">CaratBase. <em>The Carat Cliff: what a hundredth of a carat
      costs</em>. Retrieved <span id="clToday"></span>, from
      https://caratbase.com/carat-cliff-study.html</p>
      <button type="button" class="btn btn-ghost" id="clCite" style="margin-top:12px;padding:6px 14px;font-size:13px">Copy citation</button>
    </div>
    <p class="small" style="margin-top:14px">To price your own weight against the cliff either side of it, use
    the <a href="diamond-price-per-carat.html">price per carat chart</a> or the
    <a href="value.html">valuation tool</a>.</p>
  </section>
'''

SCRIPT = r'''
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var EDGES = [0.50, 0.70, 0.90, 1.00, 1.50, 2.00, 3.00];

  function tbl(head, rows){
    return '<div style="overflow-x:auto"><table class="tbl"><thead><tr>' +
      head.map(function(h,i){ return '<th' + (i ? ' class="num"' : '') + '>' + h + '</th>'; }).join('') +
      '</tr></thead><tbody>' + rows.map(function(r){
        return '<tr>' + r.map(function(c,i){
          return '<td' + (i ? ' class="num"' : '') + '>' + (i === 0 ? '<strong>' + c + '</strong>' : c) + '</td>';
        }).join('') + '</tr>';
      }).join('') + '</tbody></table></div>';
  }

  function mid(o){
    var v = valueDiamond({carat:o.carat, color:o.color || 'G', clarity:'VS2',
                          cut:'Excellent', shape:'Round', origin:'Natural'});
    return (v.retailLow + v.retailHigh) / 2;
  }

  /* Diameter goes with the cube root of weight. Our mm chart rounds to one decimal and
     would call these identical; at this scale the honest figure needs two more places. */
  function dia(ct){ return 6.5 * Math.pow(ct / 1.0, 1 / 3); }

  $('clGrid').innerHTML = tbl(
    ['Magic weight', 'Just under', 'At the weight', 'Step', 'Face-up under', 'Face-up at', 'Difference'],
    EDGES.map(function(e){
      var u = +(e - 0.01).toFixed(2);
      var mu = mid({carat:u}), me = mid({carat:e});
      return [e.toFixed(2) + ' ct', fmt(mu), fmt(me),
              '<strong style="color:var(--bad,#9B4B3F)">+' + Math.round((me - mu) / mu * 100) + '%</strong>',
              dia(u).toFixed(2) + ' mm', dia(e).toFixed(2) + ' mm',
              (dia(e) - dia(u)).toFixed(2) + ' mm'];
    }));

  var base99 = mid({carat:0.99, color:'G'}), base100 = mid({carat:1.00, color:'G'});
  var saving = base100 - base99;
  $('clTrade').innerHTML = tbl(
    ['Stone', 'Price', 'Against the 1.00 ct G', 'Color'],
    [['1.00 ct G', fmt(base100), '&mdash;', 'baseline'],
     ['0.99 ct G', fmt(base99),
      '<strong style="color:var(--good,#3F7A52)">' + fmt(saving) + ' cheaper</strong>', 'same'],
     ['0.99 ct F', fmt(mid({carat:0.99, color:'F'})),
      '<strong style="color:var(--good,#3F7A52)">' + fmt(base100 - mid({carat:0.99, color:'F'})) + ' cheaper</strong>',
      'one grade better'],
     ['0.99 ct E', fmt(mid({carat:0.99, color:'E'})),
      '<strong style="color:var(--good,#3F7A52)">' + fmt(base100 - mid({carat:0.99, color:'E'})) + ' cheaper</strong>',
      'two grades better'],
     ['0.99 ct D', fmt(mid({carat:0.99, color:'D'})),
      (base100 - mid({carat:0.99, color:'D'}) >= 0
        ? '<strong style="color:var(--good,#3F7A52)">' + fmt(base100 - mid({carat:0.99, color:'D'})) + ' cheaper</strong>'
        : '<span style="color:var(--ink-3)">' + fmt(mid({carat:0.99, color:'D'}) - base100) + ' more</span>'),
      'three grades better']]);

  $('clByColor').innerHTML = tbl(
    ['Color', '0.99 ct', '1.00 ct', 'You keep'],
    ['D','E','F','G','H','I','J'].map(function(c){
      var u = mid({carat:0.99, color:c}), e = mid({carat:1.00, color:c});
      return [c, fmt(u), fmt(e),
              '<strong style="color:var(--good,#3F7A52)">' + fmt(e - u) + '</strong>'];
    }));

  var today = new Date().toLocaleDateString('en-US', {year:'numeric', month:'long', day:'numeric'});
  $('clToday').textContent = today;
  $('clCite').addEventListener('click', function(){
    var t = 'CaratBase. The Carat Cliff: what a hundredth of a carat costs. Retrieved ' +
            today + ', from https://caratbase.com/carat-cliff-study.html';
    if(navigator.clipboard) navigator.clipboard.writeText(t).then(function(){
      $('clCite').textContent = 'Copied';
      setTimeout(function(){ $('clCite').textContent = 'Copy citation'; }, 1600);
    });
    if(window.cbTrack) cbTrack('cite_copy', {page:'carat-cliff-study'});
  });
})();
'''


def page(faq):
    return dict(
        title='The Carat Cliff — What a Hundredth of a Carat Actually Costs',
        desc='Diamond prices step at the round numbers. A 0.99 carat E costs less than a 1.00 '
             'carat G, is two color grades better, and faces up 0.02 mm smaller. Every cliff, measured.',
        eyebrow='Research',
        h1='The carat cliff',
        lede='Diamond prices do not rise smoothly with weight — they step, hard, at the weights people '
             'ask for by name. We measured every step, and the one at a carat is large enough to buy two '
             'color grades and leave change.',
        scripts=('lead.js',),
        schema=faq([
            ('Is it cheaper to buy a 0.99 carat diamond than a 1 carat?',
             'Substantially. On a well-cut round at G color and VS2 clarity the 1.00 carat runs about 31% more '
             'per stone than the 0.99, for a face-up difference of roughly 0.02 mm — about two hundredths '
             'of a millimeter, which nobody can see. The saving is large enough to move up two color grades: a '
             '0.99 carat E actually costs less than a 1.00 carat G and looks the same size.'),
            ('Why do diamond prices jump at round carat weights?',
             'Because demand concentrates there. People ask for a half carat or a one carat by name, almost '
             'nobody asks for a 0.94, so the price per carat itself resets upward at those weights. Cutters '
             'face the matching incentive: given rough that could yield a well-proportioned 0.96 or a slightly '
             'deep 1.01, the 1.01 is worth more, which is why stones just over a round number are sometimes '
             'cut deep with the extra weight hidden in the pavilion.'),
            ('Which carat weight has the biggest price jump?',
             'Half a carat, in proportional terms — crossing from 0.49 to 0.50 costs about 44%, the '
             'steepest step on the curve, and it lands on the buyers least able to absorb it. The one carat '
             'and two carat lines are around 31% each, and three carat about 36%. In absolute dollars the '
             'larger cliffs cost far more, but the half carat is the sharpest.'),
            ('Is there a downside to buying just under a round carat weight?',
             'Yes, and it is the mirror of the saving: a 0.99 is harder to resell than a 1.00 for exactly the '
             'reason it was cheaper, so the discount you took going in is one you concede coming out. Since '
             'diamonds resell at 25–40% of retail regardless of weight, it matters less than it sounds, '
             'but anyone presenting the just-under stone as free money is not being straight with you. And if '
             'you specifically want a certificate that says one carat, that is the thing being bought.'),
        ]),
        body=BODY,
        script=SCRIPT,
    )

"""The GIA report page.

A GIA report is the most trusted document in the diamond trade and, by policy, it
never mentions money. That gap is the whole product: we take the grades a report
already gives you and say what they are worth, plus which of them are quietly
costing you and which are working in your favor.

Deliberately NOT a Report Check clone. GIA owns "gia report check" and always
will; competing for it is pointless. We complement it — and we link to it, because
verification should happen at the source.

Merged into PAGES by tools/design/pages.py.
"""

FLUO_ROWS = [
    ('D&nbsp;E&nbsp;F', 'Colorless', 'Discount', '&minus;1%', '&minus;5%', '&minus;12%', '&minus;18%',
     'Blue fluorescence reads as a fault in a stone that is already colorless. Trade discounts run 5&ndash;40% depending on severity and whether the stone faces up milky.'),
    ('G&nbsp;H', 'Near-colorless', 'Roughly neutral', '0%', '&minus;1%', '&minus;3%', '&minus;6%',
     'The crossover band. Priced at a few percent at most &mdash; do not let anyone value your stone as though it were a serious fault.'),
    ('I&nbsp;J&nbsp;K', 'Faint tint', 'Flat to a small premium', '0%', '+1%', '+2%', '+1%',
     'Blue is the complement of yellow, so here the fluorescence masks the tint and the diamond can face up close to a grade whiter. A strongly fluorescent I prices about like a non-fluorescent J.'),
]

LINE_ROWS = [
    ('Carat weight', 'Very large', 'Price per carat steps up at 0.50, 0.70, 0.90, 1.00, 1.50 and 2.00 ct. A 0.96 ct and a 1.00 ct differ by a tenth of a millimeter face-up and thousands of dollars.'),
    ('Color grade', 'Large', 'D to K spans roughly a 2.5&times; price range on an otherwise identical stone. Most of the difference is invisible once the diamond is set in a warm metal.'),
    ('Clarity grade', 'Large', 'FL to I1 spans more than 3&times;. Everything from VS2 upwards is eye-clean, so above VS1 you are paying for a grade only a loupe can see.'),
    ('Cut grade', 'Large &mdash; if it is there', 'Only round brilliants get one. It is the grade that most affects how the diamond actually looks, and fancy shapes do not have it.'),
    ('Fluorescence', 'Medium, and it flips sign', 'The only grade whose effect on price reverses depending on your color grade. Explained in full below.'),
    ('Polish and symmetry', 'Small above Good', 'Finish grades, not cut quality. Below Good they start to show and the stone gets harder to resell.'),
    ('Measurements and proportions', 'Medium', 'Table and depth percentages reveal a badly proportioned stone that still carries good grades &mdash; and on fancy shapes they are most of what you have to go on.'),
    ('Laser inscription', 'None directly', 'Lets you match the physical stone to the report. Worth confirming before you buy second-hand.'),
]


def _fluo_table():
    head = ('<table class="tbl"><thead><tr><th>Your color grade</th><th>Effect on price</th>'
            '<th class="num">Faint</th><th class="num">Medium</th><th class="num">Strong</th>'
            '<th class="num">Very Strong</th></tr></thead><tbody>')
    rows = []
    for grades, band, effect, faint, med, strong, vstrong, _note in FLUO_ROWS:
        rows.append(
            '<tr><td><strong>' + grades + '</strong><br><span class="small">' + band + '</span></td>'
            '<td>' + effect + '</td><td class="num">' + faint + '</td><td class="num">' + med +
            '</td><td class="num">' + strong + '</td><td class="num">' + vstrong + '</td></tr>')
    return head + ''.join(rows) + '</tbody></table>'


def _line_table():
    head = ('<table class="tbl"><thead><tr><th>Line on your report</th><th>Effect on value</th>'
            '<th>What it actually means</th></tr></thead><tbody>')
    rows = ['<tr><td><strong>' + a + '</strong></td><td>' + b + '</td><td>' + c + '</td></tr>'
            for a, b, c in LINE_ROWS]
    return head + ''.join(rows) + '</tbody></table>'


BODY = '''
  <section class="console">
    <div class="console-head"><span class="name"><span class="dot"></span> GIA report</span><span class="status">grades in &middot; value out</span></div>
    <div class="console-body">
      <div class="console-in">
        <h3>Copy the grades from your report</h3>
        <div class="grid g2" style="gap:12px">
          <div class="field"><label>Shape and cutting style</label><select id="gShape"></select></div>
          <div class="field"><label>Carat weight</label><input type="number" id="gCt" value="1.00" step="0.01" min="0.05"></div>
          <div class="field"><label>Color grade</label><select id="gColor"></select></div>
          <div class="field"><label>Clarity grade</label><select id="gClarity"></select></div>
          <div class="field"><label>Cut grade <span class="small" id="gCutNote"></span></label><select id="gCut"></select></div>
          <div class="field"><label>Fluorescence</label><select id="gFluo"></select></div>
          <div class="field"><label>Polish</label><select id="gPolish"></select></div>
          <div class="field"><label>Symmetry</label><select id="gSym"></select></div>
        </div>
        <div class="field"><label>Report type</label><select id="gOrigin"><option>Natural</option><option>Lab-grown</option></select></div>
        <div class="field"><label>Report number <span class="small">optional &mdash; used only to build your verification link</span></label><input type="text" id="gNum" placeholder="e.g. 2141438171" inputmode="numeric" autocomplete="off"></div>
        <div id="gVerify"></div>
      </div>
      <div class="console-out" id="gOut"><div class="lab">Waiting for input</div></div>
    </div>
  </section>

  <div id="gNotes" style="margin-top:22px"></div>
  <div id="gPartner" style="margin-top:22px"></div>
  <div id="gBuyers" style="margin-top:22px"></div>

  <section class="section narrow" style="padding-top:44px">
    <h2>What a GIA report will not do</h2>
    <p>It will not give you a value. That is a deliberate policy, not an oversight &mdash; GIA grades stones and stays out of the business of pricing them, which is exactly why the trade trusts the grades. The consequence is that the most authoritative document about your diamond is silent on the only question most owners actually have.</p>
    <p>It also will not tell you which of your grades were worth paying for. A report lists eleven or twelve facts with equal visual weight. In price terms they are nothing like equal, and two of them commonly move money in directions people do not expect.</p>
    ''' + _line_table() + '''
  </section>

  <section class="section narrow">
    <h2>Fluorescence: the one grade that changes the price without changing the diamond</h2>
    <p>Roughly a third of diamonds fluoresce, almost always blue, under ultraviolet light. It is the single most misunderstood line on a GIA report, because its effect on price <em>reverses</em> depending on your color grade.</p>
    <p>In a colorless D, E or F, the trade treats blue fluorescence as a defect and discounts it &mdash; commonly 5% to 40%, with about 12% typical for Strong. But blue is the complement of yellow. In an I, J or K, the same fluorescence masks the faint tint and the stone can face up close to a grade whiter, so those stones trade flat to a slight premium.</p>
    ''' + _fluo_table() + '''
    <p class="small" style="margin-top:14px">Effects above are typical retail adjustments on an otherwise identical stone, and the calculator applies them. Individual stones vary: a small minority of very strongly fluorescent diamonds look hazy or oily in daylight, which is discounted much harder than the table suggests. That is visible to the eye, so look at the stone.</p>
    <div class="panel" style="margin-top:20px">
      <div class="eyebrow">The number worth remembering</div>
      <p style="margin-top:8px">A D color with strong blue fluorescence can price like a non-fluorescent stone several grades lower. If you are buying, that is the cheapest way to own a top color grade. If you are selling, it is the most common reason an offer comes in under what you expected.</p>
    </div>
  </section>

  <section class="section narrow">
    <h2>Why your fancy shape has no cut grade</h2>
    <p>GIA grades cut for round brilliants and nothing else. An oval, pear, cushion, emerald or princess report carries Polish and Symmetry but no overall cut grade, because facet patterns and light behavior vary too widely between fancy shapes for one standard to cover them.</p>
    <p>This causes a specific and expensive misreading. Shoppers see <em>Excellent Polish, Excellent Symmetry</em> and read it as a verdict on cut quality. It is not. Those are finish grades &mdash; how cleanly the facets were polished and how well they line up. Cut quality is about how the stone handles light, and on a fancy shape GIA has not graded it at all. Two ovals with identical reports can look completely different in the hand.</p>
    <p>So on a fancy shape, judge with your eyes and the proportions, not the grades. GIA has said it will begin grading cut on marquise, oval and pear shapes in 2027, which will close part of this gap.</p>
  </section>

  <section class="section narrow">
    <h2>GIA, IGI and the rest &mdash; why the lab on the report matters to the price</h2>
    <p>Grading is a judgement, and different labs judge differently. GIA is the strictest of the major labs and the trade prices accordingly: the same physical stone graded by a softer lab will often carry a better-looking report and a lower price. That is not a conspiracy, it is just calibration, and it is why a report is only as meaningful as the name on it.</p>
    <p>In practice a stone graded by a lab known to run softer needs to be discounted against the GIA equivalent before you compare prices &mdash; our valuation applies roughly 7% for that, and more for an ungraded stone. The gap is widest on lab-grown diamonds, where a large share of stones are graded outside GIA and color and clarity grades commonly read one to two grades better than a GIA equivalent would.</p>
    <p>The practical rule: compare like with like. A G VS1 from one lab is not automatically a G VS1 from another, and if you are paying a premium for a grade, the lab that assigned it is part of what you are paying for. If you are buying second-hand, check the <a href="#verify">laser inscription against the report</a> before anything else.</p>
  </section>

  <section class="section narrow" id="verify">
    <h2>Verifying a report, and what to do if you have lost yours</h2>
    <p><strong>Verify it at the source.</strong> GIA runs Report Check free for anyone &mdash; you do not need to be the client who submitted the stone. Enter the report number and you get the grades as GIA issued them. Always do this before buying a second-hand stone: it confirms the report is real and that the numbers on the paper in front of you have not been altered.</p>
    <p><strong>Match the stone to the paper.</strong> Most GIA-graded diamonds carry the report number laser-inscribed on the girdle. A jeweler can read it under magnification in seconds. A report that verifies correctly proves the <em>report</em> is genuine; the inscription is what ties it to the stone in your hand.</p>
    <p><strong>If you have lost the report</strong>, the stone has not lost its grades. If it is inscribed, the number is on the diamond and Report Check will return the full grading &mdash; a lost certificate is a paperwork problem, not a value problem. If there is no inscription and no number, the stone has to be re-submitted to be graded again. Either way, you can get a working value from the tool above using what a jeweler can tell you in a few minutes with a loupe and a scale.</p>
    <a class="btn btn-ghost" href="https://www.gia.edu/report-check" target="_blank" rel="noopener">Open GIA Report Check &rarr;</a>
    <p class="small" style="margin-top:12px">Report Check is GIA's own free service and opens on gia.edu. CaratBase is independent of GIA and is not affiliated with, endorsed by or authorized by it. The grades are theirs; the valuation is ours.</p>
  </section>
'''

SCRIPT = r'''
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var SHAPES = ['Round','Oval','Cushion','Princess','Emerald','Pear','Marquise','Radiant','Asscher','Heart'];
  var COLORS = ['D','E','F','G','H','I','J','K'];
  var CLARITIES = ['FL','IF','VVS1','VVS2','VS1','VS2','SI1','SI2','I1'];
  var CUTS = ['Excellent','Very Good','Good','Fair'];
  var FINISH = ['Excellent','Very Good','Good','Fair','Poor'];

  function fill(el, arr, sel){
    el.innerHTML = arr.map(function(v){
      return '<option'+(v===sel?' selected':'')+'>'+v+'</option>'; }).join('');
  }
  fill($('gShape'), SHAPES, 'Round');
  fill($('gColor'), COLORS, 'G');
  fill($('gClarity'), CLARITIES, 'VS2');
  fill($('gCut'), CUTS, 'Excellent');
  fill($('gFluo'), FLUO_GRADES, 'None');
  fill($('gPolish'), FINISH, 'Excellent');
  fill($('gSym'), FINISH, 'Excellent');

  var KIND = {
    cost:   {label:'Costing you money', cls:'pill'},
    good:   {label:'In your favor',    cls:'pill pill-ice'},
    watch:  {label:'Worth knowing',     cls:'pill'},
    neutral:{label:'Barely matters',    cls:'pill'}
  };

  function calc(){
    var shape = $('gShape').value;
    var isRound = (GIA_CUT_GRADED_SHAPES.indexOf(shape) !== -1);

    /* GIA issues no cut grade on fancy shapes, so do not invite a number that
       does not exist on the report. */
    $('gCut').disabled = !isRound;
    $('gCutNote').textContent = isRound ? '' : '— not graded on ' + shape.toLowerCase() + 's';

    var o = {
      shape: shape,
      carat: parseFloat($('gCt').value) || 0,
      color: $('gColor').value,
      clarity: $('gClarity').value,
      cut: isRound ? $('gCut').value : '',
      polish: $('gPolish').value,
      symmetry: $('gSym').value,
      fluorescence: $('gFluo').value,
      origin: $('gOrigin').value
    };
    var v = valueGiaReport(o);
    if(!v){ $('gOut').innerHTML = '<div class="lab">Enter a carat weight</div>'; return; }

    var fluoPct = Math.round((1 - v.fluoMultiplier) * 100);
    var fluoLine = fluoPct === 0
      ? (o.fluorescence === 'None'
          ? 'No fluorescence — nothing on this report is moving the price either way'
          : o.fluorescence + ' fluorescence has no material effect at ' + o.color + ' color')
      : (fluoPct > 0
          ? o.fluorescence + ' fluorescence is holding this about ' + fluoPct + '% below an equivalent non-fluorescent stone'
          : o.fluorescence + ' fluorescence is worth about ' + Math.abs(fluoPct) + '% in your favor at ' + o.color + ' color');

    $('gOut').innerHTML =
      '<div class="lab">Retail, a stone graded like yours</div>' +
      '<div class="big">' + fmt(v.retailLow) + '–' + fmt(v.retailHigh) + '</div>' +
      '<div class="sub">' + (+o.carat).toFixed(2) + ' ct ' + shape.toLowerCase() + ' · ' + o.color + ' · ' + o.clarity +
        (isRound ? ' · ' + o.cut + ' cut' : ' · no GIA cut grade') + '</div>' +
      '<div class="split">' +
        '<div><div class="lab">What it resells for</div><div class="v">' + fmt(v.resaleLow) + '–' + fmt(v.resaleHigh) + '</div></div>' +
        '<div><div class="lab">Fluorescence effect</div><div class="v">' + (fluoPct === 0 ? 'none' : (fluoPct > 0 ? '−' : '+') + Math.abs(fluoPct) + '%') + '</div></div>' +
      '</div>' +
      '<div class="note">' + fluoLine + '</div>';

    $('gNotes').innerHTML = v.notes.length
      ? '<h2 style="font-size:24px;margin-bottom:14px">What your report is telling you</h2><div class="grid g2">' +
        v.notes.map(function(n){
          var k = KIND[n.kind] || KIND.watch;
          return '<div class="panel"><span class="' + k.cls + '">' + k.label + '</span>' +
                 '<h3 style="margin:10px 0 6px;font-size:19px">' + n.head + '</h3>' +
                 '<p class="small">' + n.body + '</p></div>';
        }).join('') + '</div>'
      : '';

    /* Verification link — GIA documents no query parameter for Report Check, so
       send them to it and put the number on the clipboard instead of guessing at
       a deep link that could break silently. */
    var num = ($('gNum').value || '').replace(/[^0-9]/g, '');
    $('gVerify').innerHTML = num.length >= 6
      ? '<p class="small" style="margin-top:4px">Report <strong>' + num + '</strong> — ' +
        '<a href="https://www.gia.edu/report-check" target="_blank" rel="noopener" id="gGo">verify it free at GIA</a>' +
        ' <button type="button" class="btn btn-ghost" id="gCopy" style="padding:4px 10px;font-size:12px;margin-left:6px">Copy number</button></p>'
      : '';
    var copy = $('gCopy');
    if(copy) copy.addEventListener('click', function(){
      if(navigator.clipboard) navigator.clipboard.writeText(num).then(function(){
        copy.textContent = 'Copied'; setTimeout(function(){ copy.textContent = 'Copy number'; }, 1600);
      });
      if(window.cbTrack) cbTrack('gia_verify', {n: num.length});
    });

    if(typeof BLUE_NILE !== 'undefined' && BLUE_NILE.active()){
      $('gPartner').innerHTML = BLUE_NILE.card(
        {carat: o.carat, shape: shape, color: o.color, clarity: o.clarity},
        {title: 'What this specification costs today',
         sub: 'Your report describes one stone. This is the live market for stones graded like it — useful whether you are checking what you paid or what to ask for.'});
    }
    if(typeof Partners !== 'undefined' && !$('gBuyers').innerHTML){
      Partners.mount('gBuyers', 'buyers', {
        title: 'If you are selling rather than checking',
        intro: 'A GIA report is the single thing that makes a diamond easy to sell, because the '
             + 'buyer does not have to take your word for the grades. Approach all three — the '
             + 'spread between them on an identical stone is routinely thousands.',
        footer: 'Whatever you are offered, compare it against the resale range above rather than '
              + 'against what the stone cost.'});
    }
    if(window.cbTrack) cbTrack('tool_use', {tool:'gia_report', shape:shape, fluo:o.fluorescence});
  }

  ['gShape','gCt','gColor','gClarity','gCut','gFluo','gPolish','gSym','gOrigin','gNum']
    .forEach(function(id){ $(id).addEventListener('input', calc); });
  calc();
})();
'''


def page(faq):
    return dict(
        title='GIA Report Value Calculator — What Your Diamond Is Worth',
        desc='Your GIA report says what your diamond is, never what it is worth. '
             'Enter the grades for retail and honest resale value, and what each grade costs you.',
        eyebrow='GIA report',
        h1='What your GIA report doesn’t tell you',
        lede='A GIA report is the most trusted document in the diamond trade, and by policy it never '
             'mentions money. Enter the grades exactly as they appear on yours: you get a retail range, '
             'the honest resale figure, and the specific grades that are quietly costing you — or '
             'quietly working in your favor.',
        schema=faq([
            ('Does a GIA report tell you what a diamond is worth?',
             'No. GIA grades diamonds and does not appraise them, and no GIA report states a value. '
             'That separation is why the trade trusts the grades. To get a value you take the grades '
             'from the report and price them against the current market, which is what the calculator '
             'on this page does — including the honest resale figure, which is typically 25–40% '
             'of retail for a natural diamond and far less for lab-grown.'),
            ('Does fluorescence lower the value of a diamond?',
             'It depends entirely on the color grade. In a colorless D, E or F, blue fluorescence is '
             'treated as a fault and discounted — commonly 5% to 40%, with around 12% typical for '
             'Strong. In an I, J or K it masks the faint yellow tint and the stone can face up close to '
             'a grade whiter, so those diamonds trade flat to a slight premium. At G and H the effect is '
             'a few percent at most.'),
            ('Why is there no cut grade on my GIA report?',
             'Because GIA grades cut for round brilliants only. Fancy shapes — oval, pear, cushion, '
             'princess, emerald, marquise — receive Polish and Symmetry but no overall cut grade, as '
             'their facet patterns vary too widely for a single standard. Excellent Polish and Excellent '
             'Symmetry describe the finish, not how well the stone handles light. GIA has said it will '
             'begin grading cut on marquise, oval and pear shapes in 2027.'),
            ('How do I check whether a GIA report is genuine?',
             'Use GIA Report Check at gia.edu, which is free and open to anyone — you do not have to '
             'be the client who submitted the stone. Enter the report number and compare what GIA returns '
             'against the document in front of you. Then have a jeweler read the laser inscription on the '
             'girdle: verifying the number proves the report is real, while the inscription is what ties '
             'that report to the specific diamond you are holding.'),
            ('I lost my GIA certificate — is my diamond worth less?',
             'No. The grades belong to the stone, not the paper. If the diamond is laser-inscribed with '
             'its report number, a jeweler can read it and GIA Report Check will return the full grading '
             'for free, so a lost certificate is a paperwork problem rather than a value problem. If there '
             'is no inscription and no record of the number, the stone would have to be submitted for '
             'grading again.'),
        ]),
        body=BODY,
        script=SCRIPT,
    )

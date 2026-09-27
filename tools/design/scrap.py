"""The scrap gold page.

Biggest untargeted cluster in the keyword harvest (63 queries) and the highest
intent on the site: someone with a "scrap gold calculator" query is selling today,
not browsing. metals.html answers "what is my gold worth"; this answers "what will
someone actually hand me, and is the offer in front of me fair".

The differentiator is the offer checker. US buyers quote in pennyweight, which is
1.55517 g, and a per-dwt number looks about 55% larger than the same money per
gram. Nothing requires a buyer to quote in a unit you understand, so the single
most useful thing we can do is convert their offer back into a percentage of melt.

Merged into PAGES by tools/design/pages.py.
"""

# Consensus of trade and buyer sources: refiners pay most, pawn shops least.
# Ranges kept conservative where sources disagreed.
CHANNELS = [
    ('Refiner, direct', 0.85, 0.95,
     'Best rate, and the one most sellers never try. Refiners want volume, so small '
     'lots may be refused or charged a lot fee. Worth it once you are into several '
     'ounces.'),
    ('Reputable mail-in buyer', 0.75, 0.88,
     'Low overhead, so rates beat the high street. You post the gold and wait a few '
     'days. Use one that shows you the assay and returns the lot free if you decline.'),
    ('Local gold buyer or jeweler', 0.60, 0.80,
     'Instant money and you watch the scale. The spread pays for the shopfront. This '
     'is where the pennyweight quote below is most likely to appear.'),
    ('Pawn shop', 0.40, 0.70,
     'The fastest and the lowest. A pawn shop prices for the risk that you never come '
     'back for it. Take this only if you need the money today.'),
]

# Materials people actually turn up with, beyond plain karat jewelry. `purity` is the
# fraction of pure gold by weight; `note` is what the calculator warns about.
# Dental: most yellow crowns run about 16K (~67% gold); ADA Type III is 75-78%, Type IV
# 60-70%, and both carry palladium and platinum that a general gold buyer ignores.
# Gold-filled: 1/20 means 5% of the weight is the karat layer, so a 1/20 14K piece is
# 5% x 58.5% = 2.9% gold. Real, but most counter buyers will not touch it.
EXTRA_MATERIALS = [
    ('Dental gold, typical crown (~16K)', 0.667, 'dental',
     'Most yellow crowns run near 16 karat. Crowns also contain palladium and platinum, '
     'which a general gold buyer does not assay and does not pay for.'),
    ('Dental gold, ADA Type III (~18K)', 0.760, 'dental',
     'Crown and inlay alloy, 75-78% gold plus palladium, platinum and silver.'),
    ('Dental gold, ADA Type IV (~15K)', 0.650, 'dental',
     'Bridge and partial alloy, 60-70% gold with up to 12% palladium.'),
    ('Gold-filled 1/20 14K', 0.02925, 'filled',
     'Five per cent of the weight is a bonded 14K layer, so 2.9% pure gold. Real, but '
     'low grade: expect a refiner rather than a counter, and a lot fee.'),
    ('Gold-filled 1/20 12K', 0.02500, 'filled',
     'Five per cent of the weight is a bonded 12K layer, so 2.5% pure gold.'),
    ('Gold-plated (GP, GEP, HGE)', 0.0, 'plated',
     'Microns of gold over base metal. There is no recoverable value at jewelry scale.'),
]

UNITS = [
    ('Grams (g)', 'g', 1.0),
    ('Pennyweight (dwt)', 'dwt', 1.55517),
    ('Troy ounces (ozt)', 'ozt', 31.1034768),
]

CONVERSIONS = [
    ('1 pennyweight (dwt)', '1.55517 g', '1/20 troy ounce'),
    ('1 troy ounce (ozt)', '31.1035 g', '20 dwt'),
    ('1 gram', '0.643 dwt', '0.0322 ozt'),
    ('1 ordinary ounce (avoirdupois)', '28.3495 g', 'Not what gold is priced in'),
]


def _channel_table():
    head = ('<table class="tbl"><thead><tr><th>Who you sell to</th>'
            '<th class="num">Share of melt</th><th>What you are trading away</th>'
            '</tr></thead><tbody>')
    rows = []
    for name, lo, hi, note in CHANNELS:
        rows.append('<tr><td><strong>' + name + '</strong></td>'
                    '<td class="num">' + str(int(lo * 100)) + '&ndash;' + str(int(hi * 100)) + '%</td>'
                    '<td>' + note + '</td></tr>')
    return head + ''.join(rows) + '</tbody></table>'


def _conv_table():
    head = '<table class="tbl"><thead><tr><th>Unit</th><th>In grams</th><th>Also</th></tr></thead><tbody>'
    rows = ['<tr><td><strong>' + a + '</strong></td><td>' + b + '</td><td>' + c + '</td></tr>'
            for a, b, c in CONVERSIONS]
    return head + ''.join(rows) + '</tbody></table>'


BODY = '''
  <section class="console">
    <div class="console-head"><span class="name"><span class="dot"></span> Scrap value</span><span class="status">melt &middot; and what you will be offered</span></div>
    <div class="console-body">
      <div class="console-in">
        <h3>What you are selling</h3>
        <div class="grid g2" style="gap:12px">
          <div class="field"><label>Weight</label><input type="number" id="sW" value="20" step="0.01" min="0"></div>
          <div class="field"><label>Weighed in</label><select id="sU"></select></div>
        </div>
        <div class="field"><label>Karat or purity</label><select id="sK"></select></div>
        <p class="small">Weigh only the metal. Stones, clasps of a different metal and spring bars are not paid for, and a buyer will deduct them.</p>
      </div>
      <div class="console-out" id="sOut"><div class="lab">Waiting for input</div></div>
    </div>
  </section>

  <div id="sChannels" class="grid g2" style="margin-top:22px"></div>

  <section class="section" style="padding-top:44px">
    <div class="panel" style="border-color:var(--gold-2)">
      <div class="eyebrow">Check an offer</div>
      <h2 style="font-size:24px;margin:6px 0 10px">Someone quoted you a price. Is it any good?</h2>
      <p class="small" style="margin-bottom:16px">Enter the number you were given exactly as they said it &mdash; including the unit. This converts it back into a share of melt, which is the only figure that lets you compare two offers.</p>
      <div class="grid g3" style="gap:12px">
        <div class="field"><label>They offered</label><input type="number" id="oAmt" value="85" step="0.01" min="0"></div>
        <div class="field"><label>Per</label><select id="oU"></select></div>
        <div class="field"><label>For karat</label><select id="oK"></select></div>
      </div>
      <div id="oOut" style="margin-top:16px"></div>
    </div>
  </section>

  <section class="section narrow">
    <h2>The pennyweight trap</h2>
    <p>A pennyweight is 1.55517 grams. Twenty of them make a troy ounce. It is the traditional unit of the US jewelry trade, and it is still how a lot of gold buyers quote &mdash; which matters, because the same money expressed per pennyweight looks about <strong>55% larger</strong> than it does per gram.</p>
    <p>Nothing requires a buyer to quote in a unit you understand. A shop can weigh in pennyweights, price in pennyweights and post per-pennyweight rates in the window, entirely legally. If you are mentally comparing that against a per-gram number from somewhere else, you are not comparing anything.</p>
    <div class="panel" style="margin-top:18px">
      <div class="eyebrow">Worked example &mdash; one 20 g 14K necklace</div>
      <p style="margin-top:8px">Shop A offers <strong>$60 per gram</strong>. That is 20 &times; $60 = <strong>$1,200</strong>.</p>
      <p style="margin-top:6px">Shop B offers <strong>$85 per pennyweight</strong>, which sounds far better. But 20 g is 12.86 dwt, so the check is 12.86 &times; $85 = <strong>$1,093</strong>.</p>
      <p style="margin-top:6px">The offer that sounded about 40% richer pays <strong>$107 less</strong>. Same necklace, same day.</p>
    </div>
    <p style="margin-top:18px">So before anything else: ask whether the quote is per gram, per pennyweight or per troy ounce, and watch the scale with the unit indicator visible. Then put both numbers through the checker above.</p>
    ''' + _conv_table() + '''
  </section>

  <section class="section narrow">
    <h2>What each kind of buyer pays</h2>
    <p>Melt value is what the metal in your jewelry is worth at today's spot price. Nobody pays it. Everyone in the chain takes a cut for testing, refining, holding stock and the risk that your 14K is not 14K. The size of that cut is the whole decision.</p>
    ''' + _channel_table() + '''
    <p style="margin-top:14px">The spot price every figure here is built from is published, with history, on our <a href="jewelry-price-index.html">jewelry price index</a> &mdash; free to reuse if you need it elsewhere. A <a href="class-ring-value-calculator.html">class ring</a> is the most common single item people bring to a scrap buyer, and has its own page.</p>
    <p style="margin-top:14px">The single most valuable thing you can do is get three quotes. The spread between the best and worst offer on the same lot is routinely 30 percentage points of melt, which on a few hundred dollars of gold is real money for an afternoon's work.</p>
  </section>

  <div id="sLead" style="margin-top:22px"></div>
  <div id="sBuyers" style="margin-top:22px"></div>

  <section class="section narrow">
    <h2>Dental gold</h2>
    <p>Dental alloys are not one thing. Most yellow crowns land near <strong>16 karat</strong>, about 67% gold; ADA Type III crown-and-inlay alloy runs 75&ndash;78%, and Type IV bridge alloy 60&ndash;70%. Across everything that turns up, the long-run average is nearer 11.5 karat. A single crown usually weighs about 3&nbsp;g, so a typical one carries roughly $150 of recoverable metal at current prices.</p>
    <p><strong>The mistake that costs money:</strong> dental alloy also contains palladium and platinum, and a general cash-for-gold buyer assays for gold only. Those metals can be 20&ndash;30% of the total precious value of a crown, and a buyer who does not test for them will not pay for them. Sell dental scrap to a refiner who handles dental specifically &mdash; they assay the whole alloy and typically pay around 85% of spot after refining costs of 15&ndash;18%.</p>
    <p>Porcelain fused to the metal is normal and is burned off in refining; you do not need to remove it, and you should not try. Nor does it need cleaning beyond the obvious.</p>
  </section>

  <section class="section narrow">
    <h2>Gold-filled and gold-plated</h2>
    <p>These two get confused constantly and they are not remotely the same thing.</p>
    <p><strong>Gold-filled</strong> is stamped <strong>GF</strong>, usually as a fraction: <em>1/20 14K</em> means a bonded 14K layer making up one twentieth &mdash; 5% &mdash; of the total weight. So the piece is 5% &times; 58.5% = <strong>2.9% pure gold</strong>. That is real and recoverable, but it is low-grade scrap. Most counter buyers refuse gold-filled outright because processing it is not worth their time; refiners take it in quantity, usually with a lot fee. Do not expect the percentages in the table above to hold on a small lot.</p>
    <p><strong>Gold-plated</strong> &mdash; stamped <strong>GP</strong>, <strong>GEP</strong>, <strong>HGE</strong> or nothing at all &mdash; is microns of gold over base metal. There is no recoverable value at jewelry scale. Nobody will weigh it, and no refiner will take it. If it still looks good, it is worth more worn than sold.</p>
    <p>Not sure which you have? The <a href="stamp.html">hallmark lookup</a> decodes every one of those marks, and a <a href="class-ring-value-calculator.html">class ring</a> is its own special case &mdash; half of them are base metal under a trade name.</p>
  </section>

  <section class="section narrow">
    <h2>Before you hand anything over</h2>
    <p><strong>Know the melt value first.</strong> Walking in with a number is the difference between negotiating and accepting. That is what the calculator at the top is for.</p>
    <p><strong>Watch the weighing.</strong> The scale should face you, with the unit &mdash; g or dwt &mdash; visible next to the number. Ask them to weigh each karat separately; mixing 10K in with 18K and paying the whole lot at the low rate is the oldest deduction there is.</p>
    <p><strong>Separate the karats yourself.</strong> Sort by stamp before you go. If a piece is unstamped, expect it to be tested and priced conservatively, or set it aside.</p>
    <p><strong>Do not scrap what is worth more whole.</strong> A signed piece, a period item, or anything with a decent stone in it is usually worth more as jewelry than as metal. Melt is the floor, not the price. If it might be the former, <a href="value.html">value it as a piece first</a>.</p>
    <p><strong>Keep the stones.</strong> Ask for them back in writing before you leave the item. A scrap buyer values the metal; any diamond in the setting is upside they are not paying you for.</p>
  </section>
'''

SCRIPT = r'''
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var UNITS = __UNITS__;
  var CHANNELS = __CHANNELS__;
  var KARATS = ['24K','22K','18K','14K','10K','9K','Platinum','Silver 925'];
  /* label, purity, kind, note — dental, gold-filled and plated */
  var EXTRA = __EXTRA__;

  function fillUnits(el){
    el.innerHTML = UNITS.map(function(u, i){ return '<option value="'+i+'">'+u[0]+'</option>'; }).join('');
  }
  function fillKarats(el){
    el.innerHTML =
      '<optgroup label="Karat gold and silver">' +
      KARATS.map(function(k){
        return '<option value="'+k+'"'+(k==='14K'?' selected':'')+'>'+k+'</option>'; }).join('') +
      '</optgroup><optgroup label="Dental, gold-filled and plated">' +
      EXTRA.map(function(e, i){
        return '<option value="x'+i+'">'+e[0]+'</option>'; }).join('') +
      '</optgroup>';
  }

  /* A selection is either a plain karat code or "x<index>" into EXTRA. */
  function material(v){
    if(v && v.charAt(0) === 'x'){
      var e = EXTRA[parseInt(v.slice(1), 10)];
      return {label:e[0], purity:e[1], kind:e[2], note:e[3]};
    }
    return {label:v, purity:null, kind:'karat', note:''};
  }
  fillUnits($('sU')); fillUnits($('oU')); fillKarats($('sK')); fillKarats($('oK'));
  $('oU').value = '1';   /* default the checker to pennyweight — the unit people get caught by */

  /* Melt value of one gram at the given purity, using the live spot prices. */
  function perGram(v){
    var m = material(v);
    if(m.purity !== null) return METAL_SPOT.gold * m.purity;
    if(v === 'Platinum')   return METAL_SPOT.platinum * 0.95;
    if(v === 'Silver 925') return METAL_SPOT.silver   * 0.925;
    return METAL_SPOT.gold * (KARAT_PURITY[v] || 0);
  }

  function calc(){
    var u = UNITS[parseInt($('sU').value, 10)] || UNITS[0];
    var grams = (parseFloat($('sW').value) || 0) * u[2];
    var k = $('sK').value;
    var m = material(k);
    var melt = grams * perGram(k);

    /* Plated is the one honest zero on this page. Say so plainly rather than
       showing a payout ladder against a value that does not exist. */
    if(m.kind === 'plated'){
      $('sOut').innerHTML =
        '<div class="lab">Recoverable value</div><div class="big">$0</div>' +
        '<div class="sub">' + m.label + '</div>' +
        '<div class="note">' + m.note + ' Scrap buyers will not weigh it, and a refiner ' +
        'will not take it. If the piece still looks good, it is worth more worn than sold.</div>';
      $('sChannels').innerHTML = '';
      return;
    }

    if(!melt){ $('sOut').innerHTML = '<div class="lab">Enter a weight</div>'; $('sChannels').innerHTML=''; return; }

    var best = CHANNELS[0], worst = CHANNELS[CHANNELS.length-1];
    $('sOut').innerHTML =
      '<div class="lab">Melt value — what the metal is worth</div>' +
      '<div class="big">' + fmt(melt) + '</div>' +
      '<div class="sub">' + grams.toFixed(2) + ' g of ' + m.label + ' · ' + fmt(perGram(k)) + '/g · ' +
        fmt(perGram(k) * 1.55517) + '/dwt</div>' +
      '<div class="split">' +
        '<div><div class="lab">Best realistic offer</div><div class="v">' + fmt(melt*best[2]) + '</div></div>' +
        '<div><div class="lab">Worst</div><div class="v">' + fmt(melt*worst[1]) + '</div></div>' +
      '</div>' +
      '<div class="note">' + (m.note ? m.note + ' ' : '') +
        (m.kind === 'dental'
          ? 'Sell dental scrap to a dental refiner, not a gold buyer: the palladium and platinum can be 20-30% of the total precious value and a general buyer pays for none of it.'
          : m.kind === 'filled'
          ? 'Gold-filled is real but low grade. Most counter buyers refuse it outright; a refiner will take it in quantity, usually with a lot fee, so the percentages below are optimistic for a small lot.'
          : 'Nobody pays melt. The spread between the best and worst offer on this lot is ' +
            fmt(melt*best[2] - melt*worst[1]) + '. Get three quotes.') + '</div>';

    $('sChannels').innerHTML = CHANNELS.map(function(c){
      return '<div class="panel"><div class="eyebrow">' + c[0] + '</div>' +
        '<div style="font-family:var(--serif);font-size:30px;font-weight:700;color:var(--gold-2);margin:8px 0 4px">' +
        fmt(melt*c[1]) + '–' + fmt(melt*c[2]) + '</div>' +
        '<p class="small">' + Math.round(c[1]*100) + '–' + Math.round(c[2]*100) + '% of melt</p></div>';
    }).join('');

    if(window.cbTrack) cbTrack('tool_use', {tool:'scrap_gold', karat:k, unit:u[1]});
  }

  /* The offer checker: turn "$85 a pennyweight" back into a share of melt. */
  function checkOffer(){
    var amt = parseFloat($('oAmt').value) || 0;
    var u = UNITS[parseInt($('oU').value, 10)] || UNITS[0];
    var k = $('oK').value;
    var meltPerUnit = perGram(k) * u[2];
    if(!amt || !meltPerUnit){ $('oOut').innerHTML = ''; return; }

    var share = amt / meltPerUnit;
    var pct = Math.round(share * 100);
    var verdict, cls;
    if(share >= 0.85){ verdict = 'Strong. That is refiner territory — take it.'; cls = 'pill pill-ice'; }
    else if(share >= 0.72){ verdict = 'Fair. In line with a good mail-in buyer or a decent local shop.'; cls = 'pill pill-ice'; }
    else if(share >= 0.60){ verdict = 'Low but not unreasonable for an over-the-counter offer. Worth one more quote.'; cls = 'pill'; }
    else if(share >= 0.40){ verdict = 'Pawn-shop level. You are paying a lot for speed. Get two more quotes first.'; cls = 'pill'; }
    else { verdict = 'Poor. Walk away and get other quotes before agreeing to anything.'; cls = 'pill'; }

    /* Restate the same offer in the other units — this is where the trap shows up. */
    var perG = amt / u[2];
    var others = UNITS.filter(function(x){ return x[1] !== u[1]; }).map(function(x){
      return fmt(perG * x[2]) + ' per ' + x[1];
    }).join(' · ');

    $('oOut').innerHTML =
      '<span class="' + cls + '">' + pct + '% of melt</span>' +
      '<p style="margin-top:10px"><strong>' + fmt(amt) + ' per ' + u[1] + '</strong> for ' + k +
      ' is <strong>' + pct + '% of melt value</strong>. ' + verdict + '</p>' +
      '<p class="small" style="margin-top:8px">The same offer stated differently: ' + others +
      '. Melt itself is ' + fmt(meltPerUnit) + ' per ' + u[1] + '.</p>';
    if(window.cbTrack) cbTrack('offer_check', {pct:pct, unit:u[1]});
  }

  if(typeof Partners !== 'undefined'){
    Partners.mount('sBuyers', 'metalBuyers', {
      title: 'Where to actually sell it',
      intro: 'Compare any offer against the melt figure above before you accept it. Mail-in '
           + 'buyers beat the high street on rate but you wait a few days for the money.',
      footer: 'Whatever you are offered, put it through the checker above first. A price per '
            + 'pennyweight is not what it looks like.'});
  }
  if(typeof Lead !== 'undefined'){
    Lead.render('sLead', {}, {
      eyebrow: 'Before you sell',
      title: 'Know the number before you walk in',
      after: 'The buyers below are the usual next step.'});
  }

  ['sW','sU','sK'].forEach(function(id){ $(id).addEventListener('input', calc); });
  ['oAmt','oU','oK'].forEach(function(id){ $(id).addEventListener('input', checkOffer); });

  /* Spot arrives asynchronously; reprice when it lands. */
  document.addEventListener('cb:spot', function(){ calc(); checkOffer(); });
  calc(); checkOffer();
})();
'''

# Substituted after the fact so SCRIPT stays a single raw string end to end — see the
# note in classring.py for why the r'''...''' + repr(...) + '''...''' form is a trap.
for _token, _value in (
    ('__UNITS__',    [[label, code, grams] for label, code, grams in UNITS]),
    ('__CHANNELS__', [[n, lo, hi] for n, lo, hi, _x in CHANNELS]),
    ('__EXTRA__',    [[l, pu, k, n] for l, pu, k, n in EXTRA_MATERIALS]),
):
    SCRIPT = SCRIPT.replace(_token, repr(_value).replace("'", '"'))


def page(faq):
    return dict(
        title='Scrap Gold Calculator — What a Buyer Will Really Pay',
        desc='Work out the melt value of scrap gold or silver in grams, pennyweight or '
             'troy ounces, see what each kind of buyer pays, and check whether an offer is fair.',
        eyebrow='Scrap gold',
        h1='What your scrap gold is really worth',
        lede='Melt value is what the metal is worth. Nobody pays it. Weigh your lot, see the '
             'melt figure and what a refiner, a mail-in buyer, a local jeweler and a pawn shop '
             'each pay against it — then put any offer you have been given through the '
             'checker, because a price quoted per pennyweight is not what it looks like.',
        schema=faq([
            ('How much do gold buyers pay for scrap gold?',
             'A share of melt value, and the share depends entirely on who you sell to. '
             'Refiners buying in bulk pay roughly 85–95%, reputable mail-in buyers about '
             '75–88%, a local gold buyer or jeweler 60–80%, and a pawn shop 40–70%. '
             'Nobody pays 100% of melt — the spread covers testing, refining and their risk. '
             'Getting three quotes on the same lot routinely moves the result by 30 percentage '
             'points of melt.'),
            ('What is a pennyweight and why do gold buyers use it?',
             'A pennyweight (dwt) is 1.55517 grams, and 20 of them make a troy ounce. It is the '
             'traditional unit of the US jewelry trade. It matters when selling because the same '
             'money expressed per pennyweight looks about 55% larger than per gram. A quote of '
             '$85 per dwt is worth less than one of $60 per gram: on a 20 g necklace that is '
             '$1,093 against $1,200. Always ask which unit a quote is in.'),
            ('How do I calculate the melt value of scrap gold?',
             'Multiply the weight in grams by the purity of the karat, then by the current gold '
             'price per gram. 14K is 58.5% gold, 18K is 75%, 10K is 41.7%, 22K is 91.6%. So 20 g '
             'of 14K contains 11.7 g of pure gold. The calculator on this page does it at live '
             'spot prices and also converts pennyweight and troy ounces.'),
            ('Is it better to sell gold jewelry as scrap or as jewelry?',
             'Melt value is the floor, not the price. Anything signed, period, or set with a '
             'decent stone is usually worth more intact than melted, and a scrap buyer pays for '
             'the metal only — any diamond in the setting is upside they keep. Scrap plain, '
             'broken, unfashionable or unmarked pieces; get anything else valued as jewelry first.'),
            ('How much is a gold dental crown worth?',
             'A typical yellow crown is about 16 karat (roughly 67% gold) and weighs around 3 g, '
             'which comes to roughly $150 of recoverable metal at current prices. The important part '
             'is where you sell it: dental alloy also contains palladium and platinum, which can be '
             '20\u201330% of its precious value, and a general cash-for-gold buyer assays only for '
             'gold and pays nothing for the rest. Use a refiner that handles dental scrap.'),
            ('Is gold-filled jewelry worth anything as scrap?',
             'Yes, but not much, and it is not the same as gold-plated. Gold-filled is stamped GF, '
             'usually as a fraction: 1/20 14K means a bonded 14K layer that is 5% of the total '
             'weight, so the piece is 2.9% pure gold. That is recoverable, but most counter buyers '
             'refuse gold-filled because processing it is not worth their time \u2014 a refiner will '
             'take it in quantity, generally with a lot fee. Gold-plated (GP, GEP, HGE) is microns '
             'over base metal and has no recoverable value at all.'),
            ('Do pawn shops pay well for gold?',
             'No, but they are fast. Pawn shops typically pay 40–70% of melt value because '
             'they are pricing for speed and for the risk of holding stock. If you can wait a few '
             'days, a reputable mail-in buyer or a refiner will usually pay 20 to 40 percentage '
             'points more of melt for exactly the same metal.'),
        ]),
        body=BODY,
        script=SCRIPT,
        scripts=('vault.js', 'lead.js'),
    )

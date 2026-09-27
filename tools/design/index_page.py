"""The jewelry price index.

Phase 4 of the ranking plan: the citation engine. Young sites cannot buy authority,
but they can publish data that other people need and make it trivially easy to reuse.
Everything here already exists in the pipeline — live spot from metals.json, the
per-carat curve from data.js, the resale bands from the valuation model — it has just
never been presented as a dataset.

Three things make it citable rather than merely readable: a real CC BY 4.0 license so
nobody has to ask, raw CSV and JSON downloads so it can be opened in a spreadsheet,
and a pre-written citation line so attribution is copy-paste. Attribution is a link.

Merged into PAGES by tools/design/pages.py.
"""

BODY = '''
  <section class="console">
    <div class="console-head"><span class="name"><span class="dot live-dot"></span> Live</span><span class="status">updated daily &middot; 06:15 UTC</span></div>
    <div class="console-body">
      <div class="console-in">
        <h3>Precious metals, per gram</h3>
        <div id="ixMetals"></div>
        <p class="small" style="margin-top:14px">Spot prices from a commercial feed with a futures fallback, converted to grams at 31.1034768 g per troy ounce. Jewelry never sells at spot &mdash; see <a href="scrap-gold-calculator.html">what a buyer actually pays</a>.</p>
      </div>
      <div class="console-out" id="ixOut"><div class="lab">Loading</div></div>
    </div>
  </section>

  <section class="section">
    <h2>Gold by karat</h2>
    <p class="small" style="margin-bottom:14px">The same spot price at each of the purities jewelry is actually made in, in the three units the trade quotes.</p>
    <div id="ixKarat"></div>
  </section>

  <section class="section">
    <h2>Price history</h2>
    <p class="small" style="margin-bottom:14px">One reading per day, recorded at 06:15 UTC. This series starts from the day we began keeping it rather than being backfilled from anywhere, so it is short and will stay honest about its length.</p>
    <div class="panel" id="ixChart" style="padding:22px"></div>
  </section>

  <section class="section">
    <h2>Diamond price per carat</h2>
    <p class="small" style="margin-bottom:14px">Retail price per carat for a natural round brilliant at G color, VS2 clarity, before the color, clarity, cut and shape multipliers. Price per carat climbs with weight, which is why one large stone costs far more than two of half the size.</p>
    <div id="ixPpc"></div>
  </section>

  <section class="section narrow">
    <h2>Resale and the lab-grown spread</h2>
    <div id="ixResale"></div>
    <p style="margin-top:14px">These are the ratios behind every resale figure on this site. A natural diamond resells into the trade at roughly a quarter to two fifths of what it retails for; a lab-grown stone at a small fraction of that, because supply is unconstrained and production cost has fallen every year. They are the least flattering numbers in the jewelry business and the ones hardest to find published.</p>
  </section>

  <section class="section narrow">
    <h2>Use this data</h2>
    <p>Everything on this page is published under <strong>Creative Commons Attribution 4.0</strong>. You may reproduce it, chart it, put it in an article or build something on top of it, commercially or otherwise, provided you credit CaratBase and link back.</p>
    <div class="bn-actions" style="margin:18px 0">
      <a class="btn btn-gold" href="assets/history.csv" download>Download CSV &darr;</a>
      <a class="btn btn-ghost" href="assets/history.json" download>Download JSON &darr;</a>
      <a class="btn btn-ghost" href="assets/metals.json" download>Today only (JSON) &darr;</a>
    </div>
    <div class="panel">
      <div class="eyebrow">Cite this page</div>
      <p class="small" style="margin-top:10px">CaratBase. <em>Jewelry Price Index</em>. Retrieved <span id="ixToday"></span>, from https://caratbase.com/jewelry-price-index.html</p>
      <button type="button" class="btn btn-ghost" id="ixCopy" style="margin-top:12px;padding:6px 14px;font-size:13px">Copy citation</button>
    </div>
    <p class="small" style="margin-top:16px">Metal prices come from a third-party spot feed and are reproduced here as a convenience; the daily series, the per-carat curve and the resale bands are ours. If you are using this for anything that matters, read <a href="methodology.html">how we arrive at the figures</a> first &mdash; particularly the limits section.</p>
  </section>
'''

SCRIPT = r'''
(function(){
  var $ = function(id){ return document.getElementById(id); };
  var DWT = 1.55517, OZT = 31.1034768;
  var KARATS = [['24K',0.999],['22K',0.916],['18K',0.750],['14K',0.585],['10K',0.417],['9K',0.375]];

  function tbl(head, rows){
    return '<table class="tbl"><thead><tr>' + head.map(function(h,i){
        return '<th' + (i ? ' class="num"' : '') + '>' + h + '</th>'; }).join('') +
      '</tr></thead><tbody>' + rows.map(function(r){
        return '<tr>' + r.map(function(c,i){
          return '<td' + (i ? ' class="num"' : '') + '>' + c + '</td>'; }).join('') + '</tr>';
      }).join('') + '</tbody></table>';
  }
  var money = function(n){ return '$' + n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}); };

  function render(){
    var M = METAL_SPOT;
    $('ixMetals').innerHTML = tbl(['Metal','Per gram','Per dwt','Per troy oz'], [
      ['Gold',      money(M.gold),     money(M.gold*DWT),     money(M.gold*OZT)],
      ['Silver',    money(M.silver),   money(M.silver*DWT),   money(M.silver*OZT)],
      ['Platinum',  money(M.platinum), money(M.platinum*DWT), money(M.platinum*OZT)]
    ]);

    $('ixOut').innerHTML =
      '<div class="lab">Gold, per gram</div>' +
      '<div class="big">' + money(M.gold) + '</div>' +
      '<div class="sub">' + money(M.gold*OZT) + ' per troy ounce · ' + money(M.gold*DWT) + ' per pennyweight</div>' +
      '<div class="split">' +
        '<div><div class="lab">Silver</div><div class="v">' + money(M.silver) + '</div></div>' +
        '<div><div class="lab">Platinum</div><div class="v">' + money(M.platinum) + '</div></div>' +
      '</div>' +
      '<div class="note">Per gram. Free to reuse with attribution.</div>';

    $('ixKarat').innerHTML = tbl(['Karat','Purity','Per gram','Per dwt','Per troy oz'],
      KARATS.map(function(k){
        var g = M.gold * k[1];
        return [k[0], (k[1]*100).toFixed(1)+'%', money(g), money(g*DWT), money(g*OZT)];
      }));

    $('ixPpc').innerHTML = tbl(['Carat weight','Price per carat','A stone this size'],
      [[0.25,'0.25 ct'],[0.50,'0.50 ct'],[0.75,'0.75 ct'],[1.00,'1.00 ct'],
       [1.50,'1.50 ct'],[2.00,'2.00 ct'],[3.00,'3.00 ct'],[5.00,'5.00 ct']].map(function(r){
        var ppc = ppcFor(r[0]);
        return [r[1], '$' + ppc.toLocaleString('en-US'), '$' + Math.round(ppc*r[0]).toLocaleString('en-US')];
      }));

    $('ixResale').innerHTML = tbl(['What it is','Share of retail'], [
      ['Natural diamond, resold into the trade',
       Math.round(RESALE_NATURAL[0]*100) + '–' + Math.round(RESALE_NATURAL[1]*100) + '%'],
      ['Lab-grown diamond, resold',
       Math.round(RESALE_LAB[0]*100) + '–' + Math.round(RESALE_LAB[1]*100) + '%'],
      ['Lab-grown retail, against an identical natural stone',
       Math.round(LAB_FACTOR*100) + '%'],
      ['Scrap gold, against melt value', '40–95%, depending entirely on the buyer']
    ]);
  }

  /* History chart. Short series by design — it started the day we began recording —
     so say so rather than drawing a lonely two-point line and calling it a trend. */
  function chart(){
    fetch('assets/history.json?t=' + Math.floor(Date.now()/3600000)).then(function(r){
      return r.ok ? r.json() : null;
    }).then(function(d){
      if(!d || !d.days){ $('ixChart').innerHTML = '<p class="small">History is not available right now.</p>'; return; }
      var days = Object.keys(d.days).sort();
      var vals = days.map(function(k){ return d.days[k].gold; }).filter(function(v){ return v; });
      var head = '<div class="eyebrow">Gold, USD per gram · ' + days.length + ' day' +
                 (days.length === 1 ? '' : 's') + ' recorded</div>';

      if(days.length < 3){
        $('ixChart').innerHTML = head +
          '<p style="margin-top:10px">The series begins on ' + days[0] + '. There is not yet enough of it to plot ' +
          'something meaningful, so here it is as numbers instead.</p>' +
          tbl(['Date','Gold per gram'], days.map(function(k){
            return [k, money(d.days[k].gold)]; }));
        return;
      }

      var W = 760, H = 220, P = 34;
      var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
      var pad = (hi - lo) * 0.15 || 1; lo -= pad; hi += pad;
      var x = function(i){ return P + i * (W - P*2) / (days.length - 1); };
      var y = function(v){ return H - P - (v - lo) / (hi - lo) * (H - P*2); };
      var path = days.map(function(k, i){
        return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(d.days[k].gold).toFixed(1); }).join(' ');

      $('ixChart').innerHTML = head +
        '<svg viewBox="0 0 ' + W + ' ' + H + '" style="width:100%;height:auto;margin-top:10px" role="img" ' +
        'aria-label="Gold price per gram over the recorded period">' +
        '<path d="' + path + '" fill="none" stroke="var(--gold-2)" stroke-width="2"/>' +
        '<text x="' + P + '" y="16" font-size="11" fill="var(--ink-3)">' + money(hi) + '</text>' +
        '<text x="' + P + '" y="' + (H-8) + '" font-size="11" fill="var(--ink-3)">' + money(lo) + '</text>' +
        '<text x="' + (W-P) + '" y="' + (H-8) + '" font-size="11" fill="var(--ink-3)" text-anchor="end">' +
        days[days.length-1] + '</text></svg>';
    }).catch(function(){
      $('ixChart').innerHTML = '<p class="small">History is not available right now.</p>';
    });
  }

  var today = new Date().toLocaleDateString('en-US',{year:'numeric',month:'long',day:'numeric'});
  $('ixToday').textContent = today;
  $('ixCopy').addEventListener('click', function(){
    var t = 'CaratBase. Jewelry Price Index. Retrieved ' + today +
            ', from https://caratbase.com/jewelry-price-index.html';
    if(navigator.clipboard) navigator.clipboard.writeText(t).then(function(){
      $('ixCopy').textContent = 'Copied'; setTimeout(function(){ $('ixCopy').textContent = 'Copy citation'; }, 1600);
    });
    if(window.cbTrack) cbTrack('cite_copy', {page:'index'});
  });

  render(); chart();
  document.addEventListener('cb:spot', render);
})();
'''


def page(faq):
    dataset = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": "CaratBase Jewelry Price Index",
        "description": "Daily precious metal spot prices per gram, gold by karat, diamond "
                       "price per carat by weight, and diamond resale ratios.",
        "url": "https://caratbase.com/jewelry-price-index.html",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "isAccessibleForFree": True,
        "keywords": ["gold price", "silver price", "platinum price", "diamond price per carat",
                     "diamond resale value", "scrap gold", "pennyweight"],
        "temporalCoverage": "2026-09-25/..",
        "creator": {"@type": "Organization", "name": "CaratBase", "url": "https://caratbase.com/"},
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "text/csv",
             "contentUrl": "https://caratbase.com/assets/history.csv"},
            {"@type": "DataDownload", "encodingFormat": "application/json",
             "contentUrl": "https://caratbase.com/assets/history.json"},
        ],
    }
    return dict(
        title='Jewelry Price Index — Gold, Silver and Diamond Data',
        desc='Daily gold, silver and platinum prices per gram, gold by karat, diamond price '
             'per carat and resale ratios. Free to reuse with attribution. CSV and JSON.',
        eyebrow='Open data',
        h1='The CaratBase jewelry price index',
        lede='Every figure this site prices from, in one place and free to reuse: precious '
             'metal spot per gram updated daily, gold at each karat, the diamond price-per-carat '
             'curve, and the resale ratios almost nobody publishes. Licensed CC BY 4.0, with the '
             'raw data as CSV and JSON.',
        schema=[dataset, faq([
            ('Can I use CaratBase price data on my own site?',
             'Yes. The index is published under Creative Commons Attribution 4.0, which means you '
             'may reproduce, chart, adapt and build on it \u2014 commercially included \u2014 as '
             'long as you credit CaratBase and link back. There is a copy-paste citation on the '
             'page and the raw data is available as CSV and JSON.'),
            ('How often is the price data updated?',
             'Once a day at 06:15 UTC, automatically. Metal prices come from a commercial spot '
             'feed with a futures fallback and are converted to grams at 31.1034768 g per troy '
             'ounce. Each reading is appended to a dated series, so the history file grows by one '
             'row per day and is never backfilled or smoothed.'),
            ('What is the difference between spot price and what I would be paid?',
             'Spot is the wholesale price of the pure metal. Nobody pays it for jewelry. A refiner '
             'buying scrap in bulk pays roughly 85\u201395% of melt value, a mail-in buyer '
             '75\u201388%, a local jeweler 60\u201380% and a pawn shop 40\u201370%. Melt value is '
             'itself only the metal content, so a 14K piece contains 58.5% gold by weight.'),
        ])],
        body=BODY,
        script=SCRIPT,
    )

"""Rebuild the homepage hero + tool families section from icons.py. Idempotent."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import icons
p = pathlib.Path(__file__).resolve().parents[2] / 'index.html'
s = p.read_text()
start = s.index('<!-- ================= HERO ================= -->')
end = s.index('<!-- ================= WHY ================= -->')
hero = '''<!-- ================= HERO ================= -->
<section class="hero3">
  <div class="ph" role="img" aria-label="A round brilliant diamond held in jeweller's tweezers"></div>
  <div class="in">
    <div class="copy">
      <div class="eyebrow live-dot">The jewellery reference · live prices</div>
      <h1>What is it <em style="color:var(--gold-2);font-style:normal">actually</em> worth?</h1>
      <p class="lede">
        Free tools for anything you own or are about to buy — with the number the trade
        keeps to itself: what a diamond really fetches when you sell it.
      </p>
      <div class="hero-cta">
        <a href="value.html" class="btn btn-gold btn-lg">Value my jewellery</a>
        <a href="compare.html" class="btn btn-ghost btn-lg">Compare two diamonds</a>
      </div>
      <label class="searchbar" for="homeSearch">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input id="homeSearch" type="search" placeholder="Search — ring size 7, 925, 1.5 carat oval, 18k…" autocomplete="off">
        <span class="kbd">⌘K</span>
      </label>
    </div>
    <div class="showcase" id="showcase" aria-live="polite">
      <div class="stage fade" id="scStage"></div>
      <div class="cap fade" id="scCap">
        <div class="spec">—<small>&nbsp;</small></div>
        <div class="nums"><div class="r">Retail <b>—</b></div><div class="s">Resells for —</div></div>
      </div>
      <div class="dots" id="scDots"></div>
    </div>
  </div>
</section>

<section class="wrap" style="padding:0 0 10px">
  <div class="trust-bar" style="margin-top:8px">
    <div><div class="n" id="tbGold">—</div><div class="t">Gold / gram today</div></div>
    <div><div class="n">250+</div><div class="t">Reference pages</div></div>
    <div><div class="n">37</div><div class="t">Ring sizes, 5 systems</div></div>
    <div><div class="n">21</div><div class="t">Gem types priced</div></div>
    <div><div class="n">$0</div><div class="t">Cost, always</div></div>
  </div>
</section>

<!-- ================= TOOLS BY INTENT ================= -->
<section class="wrap" style="padding:10px 0 10px">
''' + icons.families_html() + '''

  <div class="trust2">
    <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M4 19V5M4 19h16M8 15l4-6 4 3 4-7"/></svg><div><b>Every number is shown working</b><span>Our <a href="methodology.html">methodology</a> is public: the model, the sources, and what it cannot tell you.</span></div></div>
    <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7z"/></svg><div><b>Independent</b><span>We do not buy, sell or appraise. Where a link earns a commission, it says so beside the link.</span></div></div>
    <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg><div><b>Private by design</b><span>No account, no cookies, no tracking identifier. Your vault lives on your own device.</span></div></div>
    <div><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><div><b>Live data</b><span>Metal prices from the market every minute; diamond and gem models checked against real offers.</span></div></div>
  </div>
</section>

'''
s = s[:start] + hero + s[end:]
p.write_text(s); print('homepage: hero + families rebuilt')

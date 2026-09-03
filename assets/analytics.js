/* CaratBase — first-party analytics client.
   No cookies, no third parties, no personal data beyond what a user types into a lead form. */
(function () {
  // Defined HERE, not per page. A page-level <script> constant is silently lost whenever
  // a page is rewritten, which already cost us all tracking on the home page, the gold
  // calculator and the ring sizer. window.CB_ANALYTICS_ENDPOINT still overrides it.
  const DEFAULT_ENDPOINT = 'https://caratbase-analytics.sunnyatlanta20.workers.dev';
  const ENDPOINT = window.CB_ANALYTICS_ENDPOINT || DEFAULT_ENDPOINT;
  window.CB_ANALYTICS_ENDPOINT = ENDPOINT;   // so spot.js and others can rely on it

  const uid = () => Math.random().toString(36).slice(2) + Date.now().toString(36);

  function visitorId() {
    try {
      let v = localStorage.getItem('cb_vid');
      if (!v) { v = uid(); localStorage.setItem('cb_vid', v); }
      return v;
    } catch { return 'anon'; }
  }

  function sessionId() {
    try {
      const now = Date.now();
      let s = JSON.parse(sessionStorage.getItem('cb_sid') || 'null');
      if (!s || now - s.t > 1800000) s = { id: uid(), t: now };   // 30-min idle window
      s.t = now;
      sessionStorage.setItem('cb_sid', JSON.stringify(s));
      return s.id;
    } catch { return 'anon'; }
  }

  function device() {
    const w = window.innerWidth;
    return w < 768 ? 'mobile' : w < 1024 ? 'tablet' : 'desktop';
  }

  function buffer(payload) {
    try {
      const k = 'cb_buffer';
      const b = JSON.parse(localStorage.getItem(k) || '[]');
      b.push(payload);
      localStorage.setItem(k, JSON.stringify(b.slice(-500)));
    } catch {}
  }

  function track(name, meta) {
    const payload = {
      name,
      visitor:  visitorId(),
      session:  sessionId(),
      path:     location.pathname.replace(/index\.html$/, '') || '/',
      url:      location.href,
      referrer: document.referrer || '',
      device:   device(),
      meta:     meta || null,
      ts:       Date.now()
    };
    buffer(payload);
    if (!ENDPOINT) return;
    const body = JSON.stringify(payload);
    try {
      // text/plain keeps this a CORS "simple request" — no preflight, no blocked beacon.
      // The Worker parses the body as JSON regardless of the declared type.
      if (navigator.sendBeacon) {
        const sent = navigator.sendBeacon(ENDPOINT + '/collect',
          new Blob([body], { type: 'text/plain;charset=UTF-8' }));
        if (sent) return;
      }
      fetch(ENDPOINT + '/collect', { method: 'POST', body, keepalive: true, mode: 'cors',
        headers: { 'content-type': 'text/plain;charset=UTF-8' } }).catch(() => {});
    } catch {}
  }

  window.cbTrack = track;
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => track('pageview'));
  } else {
    track('pageview');
  }
})();

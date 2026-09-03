/* CaratBase — first-party analytics client.
   No cookies, no third parties, no personal data beyond what a user types into a lead form. */
(function () {
  // Point this at your deployed Worker. Until then events buffer locally so the
  // dashboard still works in dev.
  const ENDPOINT = window.CB_ANALYTICS_ENDPOINT || '';

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
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT + '/collect', new Blob([body], { type: 'application/json' }));
      } else {
        fetch(ENDPOINT + '/collect', { method: 'POST', body, keepalive: true,
          headers: { 'content-type': 'application/json' } }).catch(() => {});
      }
    } catch {}
  }

  window.cbTrack = track;
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => track('pageview'));
  } else {
    track('pageview');
  }
})();

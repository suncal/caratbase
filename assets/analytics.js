/* CaratBase — first-party analytics client.
   No cookies, no third parties, no personal data beyond what a user types into a lead form. */
(function () {
  // Defined HERE, not per page. A page-level <script> constant is silently lost whenever
  // a page is rewritten, which already cost us all tracking on the home page, the gold
  // calculator and the ring sizer. window.CB_ANALYTICS_ENDPOINT still overrides it.
  const DEFAULT_ENDPOINT = 'https://caratbase-analytics.sunnyatlanta20.workers.dev';
  const ENDPOINT = window.CB_ANALYTICS_ENDPOINT || DEFAULT_ENDPOINT;
  window.CB_ANALYTICS_ENDPOINT = ENDPOINT;   // so spot.js and others can rely on it

  // No identifier is generated or stored here, deliberately.
  //
  // A persistent id in localStorage is a tracking identifier under GDPR/ePrivacy and would
  // oblige us to show a consent banner. Instead the Worker derives a short-lived hash from
  // the request itself (IP + user agent + a salt that rotates daily), keeps only the hash,
  // and can therefore count people without ever being able to follow one across days.
  // Nothing about analytics is written to the visitor's device.

  function device() {
    const w = window.innerWidth;
    return w < 768 ? 'mobile' : w < 1024 ? 'tablet' : 'desktop';
  }

  function track(name, meta) {
    const payload = {
      name,
      path:     location.pathname.replace(/index\.html$/, '') || '/',
      url:      location.href,
      referrer: document.referrer || '',
      device:   device(),
      meta:     meta || null,
      ts:       Date.now()
    };
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

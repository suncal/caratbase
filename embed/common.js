/* CaratBase embed — runs inside the iframe.
   Reads ?host= and ?accent= from the loader, reports its height to the parent so the
   frame never needs a scrollbar, and records one embed_view so we can see which sites
   run the widget (that list is also the backlink list). */
(function(){
  const q = new URLSearchParams(location.search);
  const host = (q.get('host') || '').replace(/[^a-z0-9.-]/gi, '').slice(0, 120);
  const accent = q.get('accent');
  if(accent && /^#?[0-9a-f]{3,8}$/i.test(accent)){
    document.documentElement.style.setProperty('--accent', accent.startsWith('#') ? accent : '#' + accent);
    document.documentElement.style.setProperty('--accent-dim', 'color-mix(in srgb, ' + (accent.startsWith('#') ? accent : '#' + accent) + ' 12%, white)');
  }
  window.CB_EMBED = { host, widget: document.body.dataset.widget || '', plan: 'free', features: [] };

  /* Licensed behaviour.

     The frame verifies the key itself rather than believing the parent, because the parent
     is the customer's own page and could simply postMessage itself a licence. That said, be
     honest about the limit: the attribution badge is rendered by the loader in the host DOM,
     so a determined host can remove it whatever we do here. This is not DRM. It keeps honest
     customers honest and gives us a clean record of who is licensed.

     Config that carries no entitlement — the CTA wording and URL — does come from the
     parent, because only the parent knows it. */
  const API = 'https://caratbase-analytics.sunnyatlanta20.workers.dev';
  const licKey = (q.get('k') || '').replace(/[^a-z0-9_]/gi, '').slice(0, 80);
  let pending = null;

  function has(f){ return window.CB_EMBED.features.indexOf(f) !== -1; }

  function applyLicense(){
    if(has('no_outbound')){
      document.documentElement.classList.add('cb-no-outbound');
    }
    if(pending && pending.cta && pending.ctaUrl && has('custom_cta')) renderCta(pending);
    if(has('own_leads')) window.CB_EMBED.ownLeads = true;
    report();
  }

  function renderCta(cfg){
    if(document.getElementById('cbCta')) return;
    const a = document.createElement('a');
    a.id = 'cbCta';
    a.href = cfg.ctaUrl;
    a.target = '_top';
    a.className = 'btn cb-cta';
    a.textContent = String(cfg.cta).slice(0, 60);
    a.addEventListener('click', function(){
      if(window.cbTrack) cbTrack('embed_cta', { widget: window.CB_EMBED.widget, host: host });
    });
    document.body.appendChild(a);
  }

  if(licKey){
    fetch(API + '/api/license?key=' + encodeURIComponent(licKey) +
          '&domain=' + encodeURIComponent(host))
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(lic){
        if(lic && lic.ok){
          window.CB_EMBED.plan = lic.plan;
          window.CB_EMBED.features = lic.features || [];
          applyLicense();
        }
      })
      .catch(function(){ /* fail open: stays on the free tier */ });
  }

  window.addEventListener('message', function(e){
    if(!e.data || e.data.cb !== 'license') return;
    pending = e.data;                        // wording only; entitlement comes from the API
    if(window.CB_EMBED.features.length) applyLicense();
  });

  function report(){
    const h = document.documentElement.scrollHeight;
    if(window.parent !== window) window.parent.postMessage({ cb: 'height', h, widget: window.CB_EMBED.widget }, '*');
  }
  new ResizeObserver(report).observe(document.body);
  window.addEventListener('load', report);

  // Every outbound link opens the full site in the top window, not inside the box.
  // A licensee paying for `no_outbound` is paying not to have their visitors sent to us,
  // so those links stop being links rather than quietly still working.
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if(!a || !/^https?:/.test(a.href)) return;
    if(has('no_outbound') && a.hostname.indexOf('caratbase.com') !== -1){
      e.preventDefault();
      return;
    }
    a.target = '_top';
  });

  window.addEventListener('load', () => {
    if(window.cbTrack) cbTrack('embed_view', { widget: window.CB_EMBED.widget, host });
  });
  window.cbEmbedUse = (meta) => { if(window.cbTrack) cbTrack('embed_use', Object.assign({ widget: window.CB_EMBED.widget, host }, meta || {})); };

  /* A lead raised inside a licensed widget is the licensee's, not ours — that is most of
     what they are paying for. It is stored tagged with their host so it can be handed
     over; automatic delivery turns on with the mailer. */
  window.cbEmbedLead = (meta) => {
    if(!window.cbTrack) return;
    cbTrack('lead', Object.assign({
      widget: window.CB_EMBED.widget,
      host: host,
      licensee: window.CB_EMBED.ownLeads ? host : '',
      intent: 'widget'
    }, meta || {}));
  };
})();

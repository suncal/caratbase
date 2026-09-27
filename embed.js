/* CaratBase widgets — host-page loader.

   Free:
     <div class="caratbase-widget" data-widget="ring-size"></div>
     <script async src="https://caratbase.com/embed.js"></script>

   Licensed, which removes the attribution and sends the leads to you instead of us:
     <div class="caratbase-widget" data-widget="ring-size"
          data-key="cb_live_…"
          data-cta="Book a fitting" data-cta-url="/appointments"></div>

   Renders the widget in a sandboxed iframe sized to its content. On the free tier it
   adds the "Powered by CaratBase" attribution beneath it — that link is the price.

   License resolution FAILS OPEN to free, always. If the API is slow, the key is wrong,
   or our worker is down, the widget still renders with the badge. A paying customer
   seeing an attribution link for an hour is an annoyance; a blank box on their site is a
   catastrophe, and we would deserve to lose them for it. Nothing here blocks the render:
   the frame goes in immediately and the badge is removed afterwards if the key checks out.
*/
(function(){
  const BASE = 'https://caratbase.com';
  const API  = 'https://caratbase-analytics.sunnyatlanta20.workers.dev';
  const WIDGETS = {
    'ring-size':    { path: '/embed/ring-size/',    page: '/ring-size.html', text: 'CaratBase ring size converter', h: 380 },
    'diamond-size': { path: '/embed/diamond-size/', page: '/size.html',      text: 'CaratBase diamond size chart',  h: 420 },
    'gold':         { path: '/embed/gold/',         page: '/metals.html',    text: 'CaratBase gold calculator',     h: 360 }
  };
  const frames = new Map();
  const CACHE_KEY = 'cb_lic';
  const CACHE_MS  = 6 * 60 * 60 * 1000;      // re-check a few times a day, no more

  /* Cached so a licensed site does not call the API on every pageview. A revoked key
     therefore keeps working until the cache lapses, which is the right trade: we are not
     defending a vault, and hammering the worker to catch a rare revocation is silly. */
  function cached(key){
    try {
      const raw = JSON.parse(localStorage.getItem(CACHE_KEY) || 'null');
      if(raw && raw.key === key && Date.now() - raw.at < CACHE_MS) return raw.lic;
    } catch(e){}
    return null;
  }
  function remember(key, lic){
    try { localStorage.setItem(CACHE_KEY, JSON.stringify({ key, at: Date.now(), lic })); }
    catch(e){}
  }

  const FREE = { ok:false, plan:'free', features:[] };

  function resolve(key){
    if(!key) return Promise.resolve(FREE);
    const hit = cached(key);
    if(hit) return Promise.resolve(hit);
    return fetch(API + '/api/license?key=' + encodeURIComponent(key) +
                 '&domain=' + encodeURIComponent(location.hostname))
      .then(function(r){ return r.ok ? r.json() : FREE; })
      .then(function(lic){ remember(key, lic); return lic || FREE; })
      .catch(function(){ return FREE; });
  }

  function badge(el, w, width){
    const p = document.createElement('p');
    p.className = 'cb-attrib';
    p.style.cssText = 'font:12px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#6b6b6b;text-align:right;max-width:' + width + ';margin:6px auto 0';
    p.innerHTML = 'Powered by <a href="' + BASE + w.page + '" style="color:#4a4a4a;text-decoration:underline">' + w.text + '</a>';
    el.appendChild(p);
    return p;
  }

  function mount(el){
    if(el.dataset.cbMounted) return;
    const w = WIDGETS[el.dataset.widget];
    if(!w) return;
    el.dataset.cbMounted = '1';

    const width = el.dataset.width || '560px';
    const key   = el.dataset.key || '';

    const q = new URLSearchParams({ host: location.hostname });
    if(el.dataset.accent) q.set('accent', el.dataset.accent);
    if(key) q.set('k', key);

    const f = document.createElement('iframe');
    f.src = BASE + w.path + '?' + q.toString();
    f.title = w.text;
    f.loading = 'lazy';
    f.style.cssText = 'width:100%;max-width:' + width + ';height:' + w.h + 'px;border:0;display:block;margin:0 auto;overflow:hidden';
    f.setAttribute('scrolling', 'no');
    el.appendChild(f);
    frames.set(f.contentWindow, f);

    /* Badge first, removed on a confirmed license. The other way round would flash an
       attribution onto a paying customer's page on every load. */
    const attrib = badge(el, w, width);

    resolve(key).then(function(lic){
      const has = function(x){ return lic.features && lic.features.indexOf(x) !== -1; };
      if(lic.ok && has('no_badge') && attrib.parentNode) attrib.parentNode.removeChild(attrib);

      /* Tell the frame what it is allowed to do. It has already loaded, so this is a
         message rather than a query parameter — and the frame treats absence as free. */
      if(lic.ok && f.contentWindow){
        const send = function(){
          f.contentWindow.postMessage({
            cb: 'license',
            plan: lic.plan,
            features: lic.features || [],
            cta: el.dataset.cta || '',
            ctaUrl: el.dataset.ctaUrl || '',
            leadTo: el.dataset.leadTo || ''
          }, BASE);
        };
        send();
        f.addEventListener('load', send);   // in case the frame was not ready yet
      }
    });
  }

  window.addEventListener('message', e => {
    if(!e.data || e.data.cb !== 'height') return;
    const f = frames.get(e.source);
    if(f && e.data.h > 80) f.style.height = Math.ceil(e.data.h) + 'px';
  });

  function scan(){ document.querySelectorAll('.caratbase-widget[data-widget]').forEach(mount); }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', scan); else scan();
  window.CaratBaseWidgets = { scan };
})();

/* CaratBase widgets — host-page loader.
   <div class="caratbase-widget" data-widget="ring-size"></div>
   <script async src="https://caratbase.com/embed.js"></script>
   Renders the widget in a sandboxed iframe sized to its content, and adds the
   "Powered by CaratBase" attribution beneath it. The attribution is the licence. */
(function(){
  const BASE = 'https://caratbase.com';
  const WIDGETS = {
    'ring-size':    { path: '/embed/ring-size/',    page: '/ring-size.html', text: 'CaratBase ring size converter', h: 380 },
    'diamond-size': { path: '/embed/diamond-size/', page: '/size.html',      text: 'CaratBase diamond size chart',  h: 420 },
    'gold':         { path: '/embed/gold/',         page: '/metals.html',    text: 'CaratBase gold calculator',     h: 360 }
  };
  const frames = new Map();

  function mount(el){
    if(el.dataset.cbMounted) return;
    const w = WIDGETS[el.dataset.widget];
    if(!w) return;
    el.dataset.cbMounted = '1';
    const q = new URLSearchParams({ host: location.hostname });
    if(el.dataset.accent) q.set('accent', el.dataset.accent);
    const f = document.createElement('iframe');
    f.src = BASE + w.path + '?' + q.toString();
    f.title = w.text;
    f.loading = 'lazy';
    f.style.cssText = 'width:100%;max-width:' + (el.dataset.width || '560px') + ';height:' + w.h + 'px;border:0;display:block;margin:0 auto;overflow:hidden';
    f.setAttribute('scrolling', 'no');
    el.appendChild(f);
    frames.set(f.contentWindow, f);

    const p = document.createElement('p');
    p.style.cssText = 'font:12px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#6b6b6b;text-align:right;max-width:' + (el.dataset.width || '560px') + ';margin:6px auto 0';
    p.innerHTML = 'Powered by <a href="' + BASE + w.page + '" style="color:#4a4a4a;text-decoration:underline">' + w.text + '</a>';
    el.appendChild(p);
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

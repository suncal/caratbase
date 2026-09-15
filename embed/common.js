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
  window.CB_EMBED = { host, widget: document.body.dataset.widget || '' };

  function report(){
    const h = document.documentElement.scrollHeight;
    if(window.parent !== window) window.parent.postMessage({ cb: 'height', h, widget: window.CB_EMBED.widget }, '*');
  }
  new ResizeObserver(report).observe(document.body);
  window.addEventListener('load', report);

  // every outbound link opens the full site in the top window, not inside the box
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if(a && /^https?:/.test(a.href)) a.target = '_top';
  });

  window.addEventListener('load', () => {
    if(window.cbTrack) cbTrack('embed_view', { widget: window.CB_EMBED.widget, host });
  });
  window.cbEmbedUse = (meta) => { if(window.cbTrack) cbTrack('embed_use', Object.assign({ widget: window.CB_EMBED.widget, host }, meta || {})); };
})();

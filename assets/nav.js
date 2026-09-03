/* CaratBase — one nav, injected everywhere */
(function(){
  const LINKS=[
    ['index.html',   'Daily'],
    ['value.html',   'Value my diamond'],
    ['vault.html',   'My vault'],
    ['stamp.html',   'Hallmarks'],
    ['metals.html',  'Metal prices'],
    ['size.html',    'Size chart']
  ];
  const here=(location.pathname.split('/').pop()||'index.html');
  const nav=document.querySelector('nav.nav'); if(!nav) return;
  let badge=0;
  try{ badge=JSON.parse(localStorage.getItem('cb_vault')||'[]').length }catch{}
  nav.innerHTML=LINKS.map(([href,label])=>{
    const on=(href==='index.html'&&(here==='index.html'||here===''))||href===here;
    const b=(href==='vault.html'&&badge)?` <span class="pill" style="padding:1px 8px;font-size:11px">${badge}</span>`:'';
    return `<a href="${href}"${on?' class="on"':''}>${label}${b}</a>`;
  }).join('');
})();

/**
 * CaratBase analytics — Cloudflare Worker + D1
 *
 *   POST /collect      ingest one event (called by assets/analytics.js)
 *   GET  /api/stats    realtime dashboard payload   (?key=DASH_KEY)
 *   GET  /api/leads    captured leads               (?key=DASH_KEY)
 *   POST /api/lead-status  update a lead's status   (?key=DASH_KEY)
 *
 * Free tier headroom: D1 allows 100k row writes/day, which is roughly
 * 100k pageviews/day. Well past the point this site starts paying for itself.
 */

const JSON_HEADERS = { 'content-type': 'application/json; charset=utf-8' };

function cors(env, request) {
  const origin  = request.headers.get('Origin') || '';
  const allowed = (env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim());
  const ok      = allowed.includes(origin) || allowed.includes('*');
  return {
    'Access-Control-Allow-Origin':  ok ? origin : allowed[0] || '',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'content-type',
    'Access-Control-Max-Age':       '86400'
  };
}

/** Turn a raw referrer into a channel label. */
function classify(ref, url) {
  const utm = new URL(url).searchParams.get('utm_source');
  if (utm) return utm.toLowerCase().slice(0, 40);
  if (!ref) return 'direct';
  let host;
  try { host = new URL(ref).hostname.replace(/^www\./, ''); } catch { return 'direct'; }
  if (/google\./.test(host))                 return 'google';
  if (/bing\.com/.test(host))                return 'bing';
  if (/duckduckgo/.test(host))               return 'duckduckgo';
  if (/yahoo\./.test(host))                  return 'yahoo';
  if (/yandex\./.test(host))                 return 'yandex';
  if (/ecosia|brave|startpage/.test(host))   return 'other-search';
  if (/reddit/.test(host))                   return 'reddit';
  if (/pinterest/.test(host))                return 'pinterest';
  if (/chatgpt|openai|perplexity|claude/.test(host)) return 'ai-assistant';
  return host.slice(0, 40);
}

async function collect(request, env) {
  let b;
  try { b = await request.json(); } catch { return new Response('bad json', { status: 400 }); }
  if (!b || !b.name || !b.visitor) return new Response('missing fields', { status: 400 });

  const cf      = request.cf || {};
  const ref     = (b.referrer || '').slice(0, 300);
  const source  = classify(ref, b.url || 'https://caratbase.com/');

  await env.DB.prepare(
    `INSERT INTO events (ts,visitor,session,name,path,referrer,source,country,device,meta)
     VALUES (?,?,?,?,?,?,?,?,?,?)`
  ).bind(
    Date.now(),
    String(b.visitor).slice(0, 40),
    String(b.session || '').slice(0, 40),
    String(b.name).slice(0, 40),
    String(b.path || '/').slice(0, 200),
    ref,
    source,
    cf.country || 'ZZ',
    String(b.device || 'desktop').slice(0, 12),
    b.meta ? JSON.stringify(b.meta).slice(0, 1000) : null
  ).run();

  // A lead is the thing we actually sell — mirror it into its own table.
  if (b.name === 'lead' && b.meta) {
    const m = b.meta;
    await env.DB.prepare(
      `INSERT INTO leads (ts,email,intent,carat,shape,color,clarity,origin,est_low,est_high,country,source)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)`
    ).bind(
      Date.now(), (m.email || '').slice(0, 160), (m.intent || '').slice(0, 20),
      parseFloat(m.carat) || null, m.shape || null, m.color || null, m.clarity || null,
      m.origin || null, parseInt(m.est_low) || null, parseInt(m.est_high) || null,
      cf.country || 'ZZ', source
    ).run();
  }
  return new Response('ok');
}

async function stats(env) {
  const now   = Date.now();
  const DAY   = 86400000;
  const today = now - DAY, yday = now - DAY * 2, live = now - 300000;
  const q     = (sql, ...a) => env.DB.prepare(sql).bind(...a).all().then(r => r.results || []);
  const one   = (sql, ...a) => env.DB.prepare(sql).bind(...a).first();

  const [
    activeNow, todayRow, ydayRow, minutes, pages, sources, countries, devices, feed, funnel, leadCount
  ] = await Promise.all([
    one(`SELECT COUNT(DISTINCT session) c FROM events WHERE ts > ?`, live),
    one(`SELECT COUNT(*) views, COUNT(DISTINCT visitor) uniques FROM events WHERE ts > ? AND name='pageview'`, today),
    one(`SELECT COUNT(*) views, COUNT(DISTINCT visitor) uniques FROM events WHERE ts > ? AND ts <= ? AND name='pageview'`, yday, today),
    q(`SELECT CAST((? - ts)/60000 AS INTEGER) m, COUNT(*) c FROM events
        WHERE ts > ? AND name='pageview' GROUP BY m`, now, now - 1800000),
    q(`SELECT path, COUNT(*) c FROM events WHERE ts > ? AND name='pageview'
        GROUP BY path ORDER BY c DESC LIMIT 8`, today),
    q(`SELECT source, COUNT(DISTINCT session) c FROM events WHERE ts > ? AND name='pageview'
        GROUP BY source ORDER BY c DESC LIMIT 8`, today),
    q(`SELECT country, COUNT(DISTINCT visitor) c FROM events WHERE ts > ? AND name='pageview'
        GROUP BY country ORDER BY c DESC LIMIT 8`, today),
    q(`SELECT device, COUNT(DISTINCT session) c FROM events WHERE ts > ? AND name='pageview'
        GROUP BY device ORDER BY c DESC`, today),
    q(`SELECT ts,name,path,source,country,meta FROM events ORDER BY ts DESC LIMIT 30`),
    q(`SELECT name, COUNT(DISTINCT session) c FROM events WHERE ts > ?
        AND name IN ('pageview','tool_use','valuation','lead') GROUP BY name`, today),
    one(`SELECT COUNT(*) c FROM leads WHERE ts > ?`, today)
  ]);

  const spark = Array(30).fill(0);
  minutes.forEach(r => { if (r.m >= 0 && r.m < 30) spark[29 - r.m] = r.c; });
  const f = Object.fromEntries(funnel.map(r => [r.name, r.c]));

  return new Response(JSON.stringify({
    generated: now,
    activeNow: activeNow?.c || 0,
    today:     { views: todayRow?.views || 0, uniques: todayRow?.uniques || 0 },
    yesterday: { views: ydayRow?.views  || 0, uniques: ydayRow?.uniques  || 0 },
    spark, pages, sources, countries, devices, feed,
    funnel: {
      visitors:   f.pageview  || 0,
      toolUsers:  f.tool_use  || 0,
      valuations: f.valuation || 0,
      leads:      f.lead      || 0
    },
    leadsToday: leadCount?.c || 0
  }), { headers: JSON_HEADERS });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const ch  = cors(env, request);
    if (request.method === 'OPTIONS') return new Response(null, { headers: ch });

    try {
      if (url.pathname === '/collect' && request.method === 'POST') {
        const r = await collect(request, env);
        return new Response(r.body, { status: r.status, headers: ch });
      }

      const authed = url.searchParams.get('key') === env.DASH_KEY;

      if (url.pathname === '/api/stats') {
        if (!authed) return new Response('unauthorized', { status: 401, headers: ch });
        const r = await stats(env);
        return new Response(r.body, { headers: { ...JSON_HEADERS, ...ch } });
      }

      if (url.pathname === '/api/leads') {
        if (!authed) return new Response('unauthorized', { status: 401, headers: ch });
        const { results } = await env.DB.prepare(
          `SELECT * FROM leads ORDER BY ts DESC LIMIT 200`).all();
        return new Response(JSON.stringify(results || []), { headers: { ...JSON_HEADERS, ...ch } });
      }

      if (url.pathname === '/api/lead-status' && request.method === 'POST') {
        if (!authed) return new Response('unauthorized', { status: 401, headers: ch });
        const { id, status } = await request.json();
        await env.DB.prepare(`UPDATE leads SET status=? WHERE id=?`).bind(status, id).run();
        return new Response('ok', { headers: ch });
      }

      return new Response('CaratBase analytics', { headers: ch });
    } catch (err) {
      return new Response(JSON.stringify({ error: String(err) }),
        { status: 500, headers: { ...JSON_HEADERS, ...ch } });
    }
  }
};

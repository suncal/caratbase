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
    'Access-Control-Allow-Origin':      ok ? origin : allowed[0] || '',
    'Access-Control-Allow-Methods':     'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers':     'content-type',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Max-Age':           '86400'
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

/**
 * Privacy-preserving visitor counting.
 *
 * The client sends no identifier at all. We derive one here from the request itself —
 * IP address, user agent, and a salt that rotates every day — keep only the hash, and
 * never write anything to the visitor's device.
 *
 * The consequence is deliberate: because the salt changes at midnight UTC, yesterday's
 * hashes cannot be matched to today's. We can count how many people visited on a given
 * day, and we cannot follow anyone between days, build a profile, or re-identify a
 * person from what is stored. That is what keeps the site free of a consent banner —
 * there is no persistent identifier to consent to.
 */
async function sha256Hex(str) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(str));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

/* Truncate before hashing: an IPv4 address keeps its first three octets and an IPv6 its
   first four groups. This is standard GDPR practice — it coarsens the input so the hash
   maps to a neighbourhood rather than a household — and it also steadies counting, since
   a phone moving between cell IPs inside the same block stays one visitor. It does not
   fix a client switching between IPv4 and IPv6 entirely, which will read as two visitors;
   that is a known and accepted limitation of counting this way. */
function coarseIp(ip) {
  if (!ip) return '';
  if (ip.includes(':')) return ip.split(':').slice(0, 4).join(':');   // IPv6 -> /64
  return ip.split('.').slice(0, 3).join('.');                          // IPv4 -> /24
}

async function deriveIds(request, env) {
  const ip = coarseIp(request.headers.get('CF-Connecting-IP') || '');
  const ua = request.headers.get('User-Agent') || '';
  const day = new Date().toISOString().slice(0, 10);            // rotates at midnight UTC
  const salt = await sha256Hex(`${env.DASH_KEY || 'cb'}|${day}`);
  const visitor = (await sha256Hex(`${salt}|${ip}|${ua}`)).slice(0, 32);
  // A coarse half-hour bucket gives session-like grouping without any extra identifier.
  const bucket = Math.floor(Date.now() / 1800000);
  const session = (await sha256Hex(`${salt}|${ip}|${ua}|${bucket}`)).slice(0, 32);
  return { visitor, session };
}

async function collect(request, env) {
  let b;
  try { b = await request.json(); } catch { return new Response('bad json', { status: 400 }); }
  if (!b || !b.name) return new Response('missing fields', { status: 400 });

  // Derived here, never taken from the request body — an older cached client may still
  // be sending its own id, and we deliberately ignore it.
  const { visitor, session } = await deriveIds(request, env);
  const cf      = request.cf || {};
  const ref     = (b.referrer || '').slice(0, 300);
  const source  = classify(ref, b.url || 'https://caratbase.com/');

  await env.DB.prepare(
    `INSERT INTO events (ts,visitor,session,name,path,referrer,source,country,device,meta)
     VALUES (?,?,?,?,?,?,?,?,?,?)`
  ).bind(
    Date.now(),
    visitor,
    session,
    String(b.name).slice(0, 40),
    String(b.path || '/').slice(0, 200),
    ref,
    source,
    cf.country || 'ZZ',
    String(b.device || 'desktop').slice(0, 12),
    b.meta ? JSON.stringify(b.meta).slice(0, 1000) : null
  ).run();

  // Reported offers are the resale dataset — keep them out of the analytics churn.
  if (b.name === 'offer_report' && b.meta) {
    const m = b.meta;
    await env.DB.prepare(
      `INSERT INTO offers (ts,amount,offered_by,pct_of_est,carat,shape,color,clarity,cut,
         origin,cert,est_low,est_high,country)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
    ).bind(
      Date.now(), parseFloat(m.amount) || null, (m.offeredBy || '').slice(0, 30),
      parseInt(m.pctOfEstimate) || null, parseFloat(m.carat) || null,
      m.shape || null, m.color || null, m.clarity || null, m.cut || null,
      m.origin || null, m.cert || null,
      parseInt(m.est_low) || null, parseInt(m.est_high) || null, cf.country || 'ZZ'
    ).run();
  }

  // A lead is the thing we actually sell — mirror it into its own table.
  if (b.name === 'lead' && b.meta) {
    const m = b.meta;
    await env.DB.prepare(
      `INSERT INTO leads (ts,email,intent,carat,shape,color,clarity,origin,cert,cert_no,est_low,est_high,country,source)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
    ).bind(
      Date.now(), (m.email || '').slice(0, 160), (m.intent || '').slice(0, 20),
      parseFloat(m.carat) || null, m.shape || null, m.color || null, m.clarity || null,
      m.origin || null, m.cert || null, (m.cert_no || '').slice(0, 30) || null,
      parseInt(m.est_low) || null, parseInt(m.est_high) || null,
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

/**
 * Email delivery via Resend.
 * Requires two secrets that are NOT in this repo:
 *   npx wrangler secret put RESEND_API_KEY
 *   npx wrangler secret put MAIL_FROM        e.g. reports@caratbase.com
 * Until both exist this returns a clear "not configured" rather than pretending to send.
 */
async function sendReport(request, env) {
  if (!env.RESEND_API_KEY || !env.MAIL_FROM) {
    return new Response(JSON.stringify({ ok: false, reason: 'not_configured' }),
      { status: 503, headers: JSON_HEADERS });
  }
  let b;
  try { b = await request.json(); } catch { return new Response('bad json', { status: 400 }); }
  const to = String(b.email || '').trim();
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(to)) {
    return new Response(JSON.stringify({ ok: false, reason: 'bad_email' }),
      { status: 400, headers: JSON_HEADERS });
  }

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'content-type': 'application/json',
               authorization: `Bearer ${env.RESEND_API_KEY}` },
    body: JSON.stringify({
      from: env.MAIL_FROM,
      to: [to],
      subject: b.subject || 'Your CaratBase valuation report',
      html: String(b.html || '').slice(0, 400000)
    })
  });

  if (!r.ok) {
    const detail = await r.text();
    return new Response(JSON.stringify({ ok: false, reason: 'provider_error', detail: detail.slice(0, 300) }),
      { status: 502, headers: JSON_HEADERS });
  }
  return new Response(JSON.stringify({ ok: true }), { headers: JSON_HEADERS });
}

/**
 * Live spot prices, fetched on demand and cached at Cloudflare's edge.
 *
 * Why this and not a cron job: a scheduled task pushes data on a fixed clock whether or
 * not anyone is looking, and its freshness is capped by the interval. This instead fetches
 * when a visitor actually asks, then serves that answer from the edge for CACHE_SECONDS.
 * So the data is never more than a minute old, upstream sees at most one call a minute no
 * matter how much traffic arrives, and nothing has to be committed to the repo.
 *
 * Per-second updates are deliberately not attempted: free metals APIs refresh about once a
 * minute and rate-limit abuse, spot moves by fractions of a cent in that window, and the
 * metals markets are closed at weekends entirely.
 */
const CACHE_SECONDS = 60;
const OZ_TO_G = 31.1034768;
const SPOT_SYMS = {
  gold:      ['XAU', 'GC=F'],
  silver:    ['XAG', 'SI=F'],
  platinum:  ['XPT', 'PL=F'],
  palladium: ['XPD', 'PA=F']
};
/* Per troy ounce. Catches a source returning nonsense rather than shipping it to users. */
const SANE = { gold:[500,20000], silver:[5,500], platinum:[200,10000], palladium:[200,10000] };

async function fetchSpot() {
  const UA = { 'User-Agent': 'caratbase.com price fetcher' };
  const getJson = async (u) => {
    const r = await fetch(u, { headers: UA, cf: { cacheTtl: 30 } });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  };
  const goldApi = async (sym) => parseFloat((await getJson(`https://api.gold-api.com/price/${sym}`)).price);
  const yahoo   = async (sym) => parseFloat(
    (await getJson(`https://query1.finance.yahoo.com/v8/finance/chart/${sym}?interval=1d&range=5d`))
      .chart.result[0].meta.regularMarketPrice);

  const perGram = {};
  const sources = {};
  await Promise.all(Object.entries(SPOT_SYMS).map(async ([name, [g, y]]) => {
    for (const [label, fn, arg] of [['gold-api', goldApi, g], ['yahoo', yahoo, y]]) {
      try {
        const oz = await fn(arg);
        const [lo, hi] = SANE[name];
        if (!(oz >= lo && oz <= hi)) continue;
        perGram[name] = +(oz / OZ_TO_G).toFixed(4);
        sources[name] = label;
        return;
      } catch { /* try the fallback */ }
    }
  }));
  if (!perGram.gold) throw new Error('no gold price from any source');
  return { updated: new Date().toISOString(), perGram, sources, cacheSeconds: CACHE_SECONDS };
}

async function spotHandler(request, ctx) {
  const cache = caches.default;
  const key = new Request('https://caratbase.internal/spot', { method: 'GET' });
  const hit = await cache.match(key);
  if (hit) return hit;

  let payload;
  try {
    payload = await fetchSpot();
  } catch (e) {
    // Never serve a wrong number: say plainly that live pricing is unavailable and let the
    // page fall back to the committed daily snapshot.
    return new Response(JSON.stringify({ ok: false, reason: String(e) }),
      { status: 503, headers: { ...JSON_HEADERS, 'cache-control': 'no-store' } });
  }
  const res = new Response(JSON.stringify(payload), {
    headers: { ...JSON_HEADERS, 'cache-control': `public, max-age=${CACHE_SECONDS}` }
  });
  ctx.waitUntil(cache.put(key, res.clone()));
  return res;
}

export default {
  /**
   * Retention, enforced rather than promised.
   *
   * The privacy policy says analytics events are deleted after 14 months and that email
   * addresses go after two years of silence. A policy that says that while nothing deletes
   * anything is worse than having no policy, so this runs nightly and actually does it.
   * Reported offers are exempt: they carry nothing identifying and their value is as a
   * long-run record of what jewellery really sells for.
   */
  async scheduled(event, env, ctx) {
    const MONTH = 2629800000;                    // average month in ms
    const eventsCutoff = Date.now() - 14 * MONTH;
    const leadsCutoff  = Date.now() - 24 * MONTH;
    const r1 = await env.DB.prepare('DELETE FROM events WHERE ts < ?').bind(eventsCutoff).run();
    const r2 = await env.DB.prepare(
      "DELETE FROM leads WHERE ts < ? AND status = 'new'").bind(leadsCutoff).run();
    console.log('retention purge', {
      events: r1.meta?.changes ?? 0,
      leads:  r2.meta?.changes ?? 0
    });
  },

  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const ch  = cors(env, request);
    if (request.method === 'OPTIONS') return new Response(null, { headers: ch });

    try {
      if (url.pathname === '/collect' && request.method === 'POST') {
        const r = await collect(request, env);
        return new Response(r.body, { status: r.status, headers: ch });
      }

      if (url.pathname === '/api/send-report' && request.method === 'POST') {
        const r = await sendReport(request, env);
        return new Response(r.body, { status: r.status, headers: { ...JSON_HEADERS, ...ch } });
      }

      // Lets the page ask whether emailing actually works before it offers to email.
      if (url.pathname === '/api/spot') {
        const r = await spotHandler(request, ctx);
        return new Response(r.body, { status: r.status,
          headers: { ...Object.fromEntries(r.headers), ...ch } });
      }

      // Public, aggregate only — no amounts, no specs, nothing identifying. Lets the
      // methodology page show honestly how much real data sits behind the estimates.
      if (url.pathname === '/api/offers-summary') {
        const row = await env.DB.prepare(
          `SELECT COUNT(*) n, MIN(ts) first FROM offers`).first();
        return new Response(JSON.stringify({
          reported: row?.n || 0,
          since: row?.first || null
        }), { headers: { ...JSON_HEADERS, 'cache-control': 'public, max-age=300', ...ch } });
      }

      if (url.pathname === '/api/capabilities') {
        return new Response(JSON.stringify({ email: !!(env.RESEND_API_KEY && env.MAIL_FROM) }),
          { headers: { ...JSON_HEADERS, ...ch } });
      }

      const authed = url.searchParams.get('key') === env.DASH_KEY;

      if (url.pathname === '/api/stats') {
        if (!authed) return new Response('unauthorized', { status: 401, headers: ch });
        const r = await stats(env);
        return new Response(r.body, { headers: { ...JSON_HEADERS, ...ch } });
      }

      if (url.pathname === '/api/offers') {
        if (!authed) return new Response('unauthorized', { status: 401, headers: ch });
        const { results } = await env.DB.prepare(
          `SELECT * FROM offers ORDER BY ts DESC LIMIT 500`).all();
        return new Response(JSON.stringify(results || []), { headers: { ...JSON_HEADERS, ...ch } });
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

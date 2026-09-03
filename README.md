# CaratBase — Phase 1

Static site + free realtime analytics. No build step, no framework, no hosting cost.

```
index.html      Home + "Guess the Carat" daily game
value.html      Diamond valuation calculator → intent/lead capture   ← the money page
stamp.html      Gold & silver hallmark lookup (27 marks)
size.html       Carat size chart, drawn to true mm scale
dashboard.html  Realtime traffic dashboard (noindex)
assets/         style.css, data.js (hallmarks + pricing engine), game.js, value.js, stamp.js, analytics.js
worker/         Cloudflare Worker + D1 schema for analytics & lead storage
```

## Deploy the site (5 minutes, free)

```bash
gh repo create caratbase --public --source=. --push
```

Then in the repo: **Settings → Pages → Deploy from branch → main / root.**
Add a `CNAME` file containing `caratbase.com` and point the domain's DNS at GitHub Pages.

## Deploy the analytics (10 minutes, free)

```bash
cd worker
npx wrangler d1 create caratbase          # copy the database_id into wrangler.toml
npx wrangler d1 execute caratbase --remote --file=schema.sql
# set DASH_KEY in wrangler.toml to something private first
npx wrangler deploy
```

Then add the Worker URL to every page, just before `assets/analytics.js`:

```html
<script>window.CB_ANALYTICS_ENDPOINT='https://caratbase-analytics.YOURNAME.workers.dev'</script>
```

Open `/dashboard.html`, paste the Worker URL and your `DASH_KEY`. It polls every 5 seconds.

**Free tier headroom:** D1 allows 100,000 row writes/day — roughly 100,000 pageviews/day.
Far past the point this site starts paying for itself.

### What the dashboard shows
Active visitors now · views and uniques today · 30-minute sparkline · **the funnel that
matters (visitors → tool users → valuations → leads)** · top pages, sources, countries ·
live event feed · every captured lead with its stone specs and estimated value.

Local mode works with no Worker at all — it reads this browser's own buffered events, which
is enough to confirm tracking fires before you deploy.

## Still stubbed — wire these when you have traffic

| What | Where | Note |
|---|---|---|
| Sending the PDF report | `assets/value.js` → lead submit | Leads are captured and stored now; the email itself is not sent |
| Insurance partner link | `value.html` intent = `insure` | Apply to BriteCo / Jewelers Mutual first — this is the highest-converting money event |
| Buyer routing | `value.html` intent = `sell` | Run the manual concierge test before automating anything |
| Gold spot price | `assets/data.js` → `METAL_SPOT` | Currently a static figure. A daily GitHub Action can refresh it |

## The valuation engine

`assets/data.js` holds the model: price-per-carat brackets that step at each magic size,
multiplied by colour, clarity, cut and shape factors, with a separate lab-grown factor and
resale bands. Verified against real market anchors:

| Stone | Model output | Market |
|---|---|---|
| 1.00 ct G VS2 natural | $4,575–5,925 | ✓ |
| 2.00 ct G VS2 natural | $14,950–19,375 | ✓ |
| 1.00 ct G VS2 lab | $650–825 | ✓ post-collapse |

Resale bands: natural 25–40% of retail, lab-grown 5–12%. These are the numbers nobody
else publishes and they are the reason to visit the site.

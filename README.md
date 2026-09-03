# CaratBase — Phase 1  ·  LIVE

- **Site:** https://suncal.github.io/caratbase/  (moves to caratbase.com once DNS is pointed)
- **Analytics Worker:** https://caratbase-analytics.sunnyatlanta20.workers.dev
- **Dashboard:** /dashboard.html — open it, paste the Worker URL and the key from `.dashkey`
- **Repo:** https://github.com/suncal/caratbase

`.dashkey` holds the dashboard key and is gitignored. It is a Cloudflare **secret**, not a
var — do not put it back in `wrangler.toml`, the repo is public and lead emails sit behind it.

## Pointing caratbase.com here

At your DNS provider, for the apex:

    A     @   185.199.108.153
    A     @   185.199.109.153
    A     @   185.199.110.153
    A     @   185.199.111.153
    CNAME www suncal.github.io

Then add a `CNAME` file containing `caratbase.com` and push. Do that **after** DNS resolves —
adding it early takes the github.io URL offline while you wait.


Static site + free realtime analytics. No build step, no framework, no hosting cost.

```
index.html      Home + "Guess the Carat" daily game, streaks, stats, playable archive
value.html      Valuation calculator + certificate number → vault + lead   ← the money page
vault.html      My vault — saved pieces, collection total          ← return hook
metals.html     Gold price today, per karat, refreshed daily       ← return hook
stamp.html      Gold & silver hallmark lookup (27 marks)
size.html       Carat size chart, drawn to true mm scale
dashboard.html  Realtime traffic dashboard (noindex)
assets/         style.css, data.js, game.js, value.js, vault.js, metals.js, stamp.js, nav.js, analytics.js
worker/         Cloudflare Worker + D1 schema for analytics & lead storage
.github/        Daily workflow refreshing assets/metals.json from free stooq quotes
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


## Return hooks

Three reasons to come back, none of which need social:

1. **Daily game** — a new stone every day, streaks, accuracy stats, and a 14-day playable
   archive so a missed day is a reason to return rather than a lost user.
2. **My vault** — every valued piece saved on-device, with a running collection total.
   Turns a one-time valuation into something the user owns. A vault with five pieces in it
   is also a far richer lead than a single anonymous valuation.
3. **Metal prices** — refreshed daily by GitHub Action, so the vault total moves on its own.
   `metals.html` also targets "gold price today per gram", which is high, habitual search volume.

## Certificate numbers

`value.html` takes a GIA or IGI report number. **Neither lab offers a free public lookup API** —
GIA Report Check is a web form and their data API is a partner agreement, so nothing is fetched
automatically. What the field does do:

- validates the number against each lab's usual format
- detects an `LG` prefix and switches both origin and lab accordingly
- links to the official verification page
- stores the number on the vault entry and on the lead

That last point is the commercial reason it exists. A certified stone can be graded and priced
without anyone handling it, which is exactly what makes a lead sellable to a dealer.

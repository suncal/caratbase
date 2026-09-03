# CaratBase — Phase 1  ·  LIVE

- **Site:** https://caratbase.com  (HTTPS enforced, www redirects to apex)
- **Analytics Worker:** https://caratbase-analytics.sunnyatlanta20.workers.dev
- **Dashboard:** /dashboard.html — open it, paste the Worker URL and the key from `.dashkey`
- **Repo:** https://github.com/suncal/caratbase

`.dashkey` holds the dashboard key and is gitignored. It is a Cloudflare **secret**, not a
var — do not put it back in `wrangler.toml`, the repo is public and lead emails sit behind it.

## DNS (done)

GoDaddy, apex `caratbase.com`:

    A     @   185.199.108.153   600s
    A     @   185.199.109.153   600s
    A     @   185.199.110.153   600s
    A     @   185.199.111.153   600s
    CNAME www suncal.github.io.

NS, SOA and `_domainconnect` were left untouched. There are no MX records, so no email to break.

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


## Turning email on

The report downloads instantly today, so nothing is blocked. To also send it by email:

1. **You:** create a free Resend account (3,000 emails/month) and generate an API key.
2. **You or me:** add Resend's domain-verification DNS records to GoDaddy for caratbase.com.
3. **Then:**

```bash
cd worker
npx wrangler secret put RESEND_API_KEY     # paste the key when prompted
npx wrangler secret put MAIL_FROM          # e.g. reports@caratbase.com
```

Check it took effect:

```bash
curl https://caratbase-analytics.sunnyatlanta20.workers.dev/api/capabilities
```

`{"email":true}` means sending is live. Only then should the UI offer to email a report —
`/api/capabilities` exists precisely so the page can ask before it promises.


## How prices stay current

Three layers, none of which involve your machine:

1. **Live** — `/api/spot` on the Worker fetches gold, silver, platinum and palladium on
   demand and caches the answer at Cloudflare's edge for 60 seconds. Data is never more
   than a minute old, and upstream sees at most one request per minute no matter how much
   traffic arrives. Pages poll every 60s, and only while the tab is visible.
2. **Snapshot** — `.github/workflows/metals.yml` still commits `assets/metals.json` daily.
   It is the fallback when the Worker or the upstream feed is down, and its commit history
   doubles as the site's price record.
3. **Sanity** — both layers reject a figure outside a plausible per-ounce range rather
   than publishing nonsense, and the page labels itself "live" or "daily snapshot" so a
   stale number is never passed off as current.

Per-second updates are deliberately not attempted. Free metals APIs refresh about once a
minute and rate-limit abuse, spot moves fractions of a cent in that window, and the metals
markets close entirely at weekends. Tick-level data is a paid market feed.

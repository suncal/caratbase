# GIA Report Results API — what it would take, and whether it is worth it

Status: **not integrated, deliberately.** `gia-report-value.html` works today with no
API and no account. This note records what the API adds, what it costs, and the
condition under which buying it becomes the right call — so the decision can be made
on numbers rather than enthusiasm.

## What GIA actually offers

Five services, from <https://www.gia.edu/report-data-services>:

| Service | Access | Use to us |
|---|---|---|
| **Report Check** | Free, public, any valid report | We link to it. This is the right answer for verification. |
| Report Check Plus | Free, 20 at a time, needs a lab account | No |
| **Report Results API** | GraphQL, paid, needs approval | The only one that could autofill our form |
| My Lab Portal | Submitting clients only | No — we submit nothing |
| Client Self-Service API | Submitting clients only | No |

## Cost

- **Free tier is useless to us.** "Unlimited lookups" applies only to *your own direct
  GIA submissions*. We have none, so our effective free quota is zero.
- **Pay as you go: $0.20 per lookup**, expiring after 6 months.
- Monthly plans: $1,000/mo for 10,000 ($0.10 each), down to $0.03 each at 500,000/mo.
- **Re-reading the same report is free for 18 months** after the first lookup. This is
  the whole economic argument: cost is per *unique* report, not per pageview.

Access requires a GIA client portal account and a formal approval step. The API is
described as being for "gem and jewelry producers, manufacturers, wholesalers, traders
and retailers" — approval for an independent reference site is not guaranteed.

## Why it is not integrated yet

1. **It buys convenience, not the product.** The value here is the valuation and the
   grade interpretation, neither of which GIA provides. The API would autofill eight
   form fields that a person holding their report can read off in about twenty seconds.
2. **Unbounded downside on a free public tool.** At $0.20 per unique report, a tool that
   gets scraped or goes briefly viral bills us for every distinct number thrown at it,
   with no revenue attached to a lookup.
3. **Wrong order.** Paying for a data API while the site takes 19 impressions a month is
   spending before there is anything to spend on. Traffic first.
4. **We cannot legitimately fake it.** Scraping Report Check is against GIA's terms and
   would break the moment they change the page. Linking to it is correct and free.

## The architecture, when it is justified

The site is static on GitHub Pages, so an API key can never live in the page. The call
has to go through the existing Cloudflare Worker (`worker/worker.js`), which already
holds secrets and serves `/api/spot`:

```
browser → Worker /api/gia-report?n=<report number>
             ├─ KV cache hit  → return cached grades       ($0)
             └─ miss → GIA GraphQL with the key → cache in KV → return   ($0.20 once)
```

Required: cache in KV **indefinitely** (GIA grades do not change; re-reads are free for
18 months anyway), rate-limit per IP, reject anything that is not a plausible report
number before spending a lookup, and cap daily spend in the Worker the same way
`lumen/motion` caps fal spend.

## The number that decides it

Blue Nile pays **3.5%**. A $5,000 stone is $175 in commission, which covers **875**
lookups at pay-as-you-go. So the API pays for itself if roughly **1 in 875 lookups**
leads to a purchase.

That is a plausible conversion rate for high-intent traffic — but it is not measurable
until the page has traffic. Revisit when `gia-report-value.html` is drawing real
sessions and the affiliate dashboard shows a conversion rate to put against it.

**Trigger to revisit:** the page is indexed, drawing 500+ sessions/month, and there is
at least one recorded Blue Nile conversion from it.

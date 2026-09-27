# Link building — the three pitches

The site's bottleneck is referring domains. 244 pages sit at "Discovered – currently not
indexed", which is Google saying it found the URLs and decided we were not worth the crawl
budget. Content does not fix that. Links do.

These are the three angles worth running, in descending order of conversion rate. All of
them need a sending mailbox that is not the personal Gmail — see the Zoho item still
outstanding.

**Non-negotiables.** One follow-up, ever. No tracking pixels. No "I noticed your excellent
blog". Never claim a link is broken without checking it yourself first — `prospect.py`
confirms every 404 with a real GET and refuses to flag a 403, because a 403 is a bot block
and the link works fine for their readers. If you get it wrong once, that domain is gone.

---

## 1. Broken link — highest conversion

You are fixing their page, not asking for a favor. That is the whole reason this works.

Find them with:

```bash
python3 tools/outreach/prospect.py --urls tools/outreach/link-candidates.txt --out tools/outreach/prospects.csv
```

Rows with a `broken_example` are these. Two confirmed live as of 2026-09-27:

| Page | Dead link on it | What we offer instead |
|---|---|---|
| [Texas Jewelers Association — Estate Jewelry & Silver Research](https://texasjewelers.org/estate-jewelry-silver-research-reference-sites/) | `globalgemology.com/jewelery-trademark-directory.html` (404) | [Hallmark lookup](https://caratbase.com/stamp.html) |
| [Hallmark Research Institute — Links](https://www.hallmarkresearch.com/html/links.htm) | `incorporationofgoldsmiths.org/content/hallmarkingarchive-home/` (404) | [Hallmark lookup](https://caratbase.com/stamp.html) |

A state jewelers association and a hallmark institute are both exactly the kind of
relevant, non-commercial domain that moves the needle. Write these two by hand.

**Subject:** dead link on your reference sites page

> Hi —
>
> I was working through the reference list on {{page}} and the link to {{dead_link}}
> is returning a 404. Looks like the site restructured.
>
> Not asking for anything in return, but if you want a replacement for that slot: I run
> a free hallmark lookup at https://caratbase.com/stamp.html — enter a stamp (925, 750,
> 585, GF, EPNS) and it gives you what the mark means, the metal content, and what the
> piece is worth at today's prices. No signup, no ads.
>
> Either way, thought you'd want to know about the dead one.
>
> Sunny

---

## 2. Resource page — already links to tools like ours

Lower hit rate, but these people have already decided to link out to this category. Rows in
`prospects.csv` with `broken_links = 0` and a high `category_links` count.

Lead with the thing they do not have. Our differentiators, in order of how unusual they are:

- **Honest resale value.** Every competitor quotes retail because they are selling. We
  publish the 25–40% of retail a natural diamond actually resells for.
- **The pennyweight offer checker** on the [scrap gold page](https://caratbase.com/scrap-gold-calculator.html).
  Nobody else converts a buyer's quote back into a share of melt.
- **Fluorescence priced properly** on the [GIA report page](https://caratbase.com/gia-report-value.html) —
  the effect flips sign with color grade and no other calculator models it.

**Subject:** a resale number for your {{topic}} page

> Hi {{firstName}},
>
> Your {{page}} list is the one I keep ending up on, so this is a slightly awkward email.
>
> I built {{tool}}, and the thing it does that the others on your list don't is publish the
> resale figure — what a diamond actually fetches when you sell it, not the retail price.
> It's usually 25–40% of retail and almost nobody prints it, because most sites in this
> space are trying to sell you a stone.
>
> If it's useful for the list: {{url}}. If not, no reply needed.
>
> Sunny

---

## 3. The data pitch — for the price index

[jewelry-price-index.html](https://caratbase.com/jewelry-price-index.html) is published
CC BY 4.0 with CSV and JSON downloads and a copy-paste citation. The license is the pitch:
anyone can use the numbers, and attribution is the price.

Targets are people who need a price figure and currently have none: jewelry bloggers,
personal-finance writers covering gold, insurance and estate-planning sites, and anyone
who has published a gold price chart that has gone stale.

**Subject:** free gold + diamond price data, CC licensed

> Hi {{firstName}},
>
> You quoted a gold price in {{article}} from {{date}} — it's well out of date now, which
> is the problem with putting a number in an article.
>
> I publish a daily price index that's free to reuse under CC BY: gold, silver and platinum
> per gram, gold by karat, and diamond price per carat by weight. CSV and JSON if you want
> to pull it in automatically, or just the page if you want to link it and let it stay
> current.
>
> https://caratbase.com/jewelry-price-index.html
>
> No catch — attribution is all it asks.
>
> Sunny

---

## Where the candidate list comes from

`prospect.py` no longer searches: DuckDuckGo serves an anti-bot page to scripts, and
hammering a search engine for this is both rude and fragile. Collect candidates with a
real search tool using the `SEED_QUERIES` in the script, paste them into
`link-candidates.txt`, and let the script do the link analysis. It honors robots.txt per
host, rate-limits itself, and caps how much it fetches.

Queries that worked:

- `jeweler website "useful links" OR "helpful resources" ring size chart diamond education`
- `"jewelry resources" links page gemology appraisal hallmark reference list`
- `antique jewelry "useful resources" hallmark links`
- `gemology resources links "price guide" tools`

## What not to bother with

- **Paid links and guest-post farms.** Cheap, detectable, and the downside is a manual
  action on a site that currently has nothing to lose but will.
- **Directory blasts.** The free-tool directories worth submitting to are a handful, and
  they are worth doing by hand once.
- **Competitor calculator sites.** ringsize.online, calc4now and the rest are not linking
  to a competitor. Skip them; they are in `link-candidates.txt` only as evidence of what a
  page in this category links to.

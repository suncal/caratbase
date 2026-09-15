# Jeweller outreach — free widget → backlink

**Goal:** get independent jewellers to paste the ring sizer onto their site. Each one is a
relevant, editorially-placed backlink, which is the thing Google is waiting for before it
crawls the 234 pages it has already discovered. Secondary: every embed is a jeweller who has
now heard of CaratBase — the lead-buyer list for later.

**Who:** independent jewellers with their own website and no ring sizer on it (most).
Check before sending: open their site, search "ring size". If they have a chart image or
nothing, they qualify. If they have an interactive sizer, skip.

**Where the list comes from (no scraping needed):**
- Jewelers of America member directory (jewelers.org) — US independents, ~8,000
- National Association of Jewellers (naj.co.uk) member list — UK
- Instantly's lead finder filtered: industry "Jewelry", company size 1–20, has website
- Wedding directories (The Knot / Hitched vendor lists) — engagement ring retailers

**From:** one of the warmed veloexa.org inboxes. Sign as Sunny. Plain text, no images,
no tracking pixels — these are small shops and the email should look like a person wrote it.

**Volume:** 30–50/day per inbox to stay warm. 200 in the first week is the test: if fewer
than 5 embed, the copy is wrong; if 10+, scale to all five inboxes.

---

## Email 1 — day 0

**Subject:** ring sizer for {{website}}

Hi {{firstName}},

I was on {{website}} looking at the {{something specific — a collection, a ring}} and
noticed there's no ring size finder on the site. Every jeweller I talk to says "what size
am I?" is their most common email.

I built a free one. It converts US/UK/EU/Indian sizes, finds a size from a ring's inside
diameter or a finger measurement, and matches your brand colour. It's two lines of code:

https://caratbase.com/widgets.html

No sign-up, nothing to pay, and it doesn't collect anything about your visitors. The only
thing it asks is a small "powered by" line underneath.

If you'd like it on the site and don't have someone to paste the code, reply and I'll
tell you exactly where it goes for {{platform — Shopify / WordPress / Squarespace}}.

Sunny
CaratBase

---

## Email 2 — day 4 (no reply)

**Subject:** re: ring sizer for {{website}}

{{firstName}} — one more thing on this, then I'll leave you alone.

There's also a diamond size chart (any carat in any shape, drawn true to scale on a
finger) and a live gold calculator for "we buy gold" pages. Same two lines, same terms:
free, no sign-up.

https://caratbase.com/widgets.html

If a ring sizer isn't useful to you, no need to reply.

Sunny

---

## Email 3 — day 10 (no reply)

**Subject:** last one

Hi {{firstName}} — closing the loop. If you ever want the free ring sizer for
{{website}}, the code is at caratbase.com/widgets.html and it takes about a minute.

All the best with the shop.

Sunny

---

## Reply handling

- **"How do I add it to Shopify?"** → Online Store → Themes → Customize → Add section →
  Custom Liquid → paste both lines → Save. Send the two lines in the reply.
- **"WordPress?"** → Edit the page → add a Custom HTML block → paste → Update.
- **"Squarespace / Wix?"** → Add an Embed / HTML block → paste.
- **"Can I remove the powered-by line?"** → No — that's the only condition, and it's how the
  project stays free. Polite, firm, one sentence.
- **"Can you make it match our font / colours?"** → `data-accent="#hex"` for the colour.
  Fonts follow theirs already (system font stack).
- **"Do you sell leads / can you send us customers?"** → This is the lead-sales conversation.
  Log it. Answer: "Not yet — we're building the audience first. Can I come back to you when
  we do?" Get a yes. That list is the second business.

## Tracking

Every site running a widget shows up in the analytics DB (`events.name = 'embed_view'`,
`meta.host`). Weekly:

    cd worker && npx wrangler d1 execute caratbase --remote --json --command \
      "SELECT json_extract(meta,'$.host') host, COUNT(*) views FROM events WHERE name='embed_view' GROUP BY host ORDER BY views DESC"

That query is the backlink list. Cross-check against Bing Webmaster Tools → Backlinks
after two weeks to see which ones Bing has credited.

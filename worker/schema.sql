-- CaratBase analytics — Cloudflare D1 schema
DROP TABLE IF EXISTS events;
CREATE TABLE events (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  ts        INTEGER NOT NULL,        -- epoch ms
  visitor   TEXT    NOT NULL,        -- anonymous, first-party, no PII
  session   TEXT    NOT NULL,
  name      TEXT    NOT NULL,        -- pageview | tool_use | valuation | lead | email
  path      TEXT,
  referrer  TEXT,
  source    TEXT,                    -- google | direct | bing | reddit | ...
  country   TEXT,
  device    TEXT,                    -- desktop | mobile | tablet
  meta      TEXT                     -- JSON blob, event specific
);
CREATE INDEX idx_events_ts      ON events(ts);
CREATE INDEX idx_events_name_ts ON events(name, ts);
CREATE INDEX idx_events_sess    ON events(session, ts);

-- Leads are the product. Kept separate so analytics purges never touch them.
DROP TABLE IF EXISTS leads;
CREATE TABLE leads (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  ts        INTEGER NOT NULL,
  email     TEXT,
  intent    TEXT,                    -- sell | insure | appraise | curious
  carat     REAL,
  shape     TEXT,
  color     TEXT,
  clarity   TEXT,
  origin    TEXT,
  cert      TEXT,
  cert_no   TEXT,
  est_low   INTEGER,
  est_high  INTEGER,
  country   TEXT,
  source    TEXT,
  status    TEXT DEFAULT 'new'       -- new | contacted | sold | dead
);
CREATE INDEX idx_leads_ts     ON leads(ts);
CREATE INDEX idx_leads_intent ON leads(intent);

-- Reported real-world offers. This is the dataset the trade does not publish and the
-- reason the valuations can eventually be better than anyone else's.
DROP TABLE IF EXISTS offers;
CREATE TABLE offers (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  ts         INTEGER NOT NULL,
  amount     REAL,
  offered_by TEXT,
  pct_of_est INTEGER,
  carat      REAL,
  shape      TEXT,
  color      TEXT,
  clarity    TEXT,
  cut        TEXT,
  origin     TEXT,
  cert       TEXT,
  est_low    INTEGER,
  est_high   INTEGER,
  country    TEXT
);
CREATE INDEX idx_offers_ts     ON offers(ts);
CREATE INDEX idx_offers_carat  ON offers(carat);
CREATE INDEX idx_offers_origin ON offers(origin);

-- Widget licenses. The free tier needs no row: absence of a key means free, and the
-- attribution link is the price. A row here removes the badge and unlocks the features
-- a jeweler actually pays for — the leads from their own visitors going to them.
DROP TABLE IF EXISTS licenses;
CREATE TABLE licenses (
  key        TEXT PRIMARY KEY,        -- cb_live_… handed to the customer
  domain     TEXT NOT NULL,           -- bare host, no scheme or www
  plan       TEXT NOT NULL DEFAULT 'pro',
  features   TEXT,                    -- JSON array; null = the plan's defaults
  email      TEXT,                    -- who to invoice / contact
  notes      TEXT,
  status     TEXT NOT NULL DEFAULT 'active',   -- active | paused | revoked
  created    INTEGER NOT NULL,
  expires    INTEGER                  -- epoch ms; null = no expiry
);
CREATE INDEX idx_licenses_domain ON licenses(domain);
CREATE INDEX idx_licenses_status ON licenses(status);

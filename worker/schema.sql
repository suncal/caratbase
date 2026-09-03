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

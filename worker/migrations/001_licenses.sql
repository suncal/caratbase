-- Adds the widget licenses table to an EXISTING database.
--
-- schema.sql drops every table before creating it, which is right for a fresh setup and
-- catastrophic on a live one — it would take the leads and offers with it. Run this
-- instead against the deployed D1:
--
--   npx wrangler d1 execute caratbase --remote --file worker/migrations/001_licenses.sql
--
-- Safe to run twice.
CREATE TABLE IF NOT EXISTS licenses (
  key        TEXT PRIMARY KEY,
  domain     TEXT NOT NULL,
  plan       TEXT NOT NULL DEFAULT 'pro',
  features   TEXT,
  email      TEXT,
  notes      TEXT,
  status     TEXT NOT NULL DEFAULT 'active',
  created    INTEGER NOT NULL,
  expires    INTEGER
);
CREATE INDEX IF NOT EXISTS idx_licenses_domain ON licenses(domain);
CREATE INDEX IF NOT EXISTS idx_licenses_status ON licenses(status);

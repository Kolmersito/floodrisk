"""Esquema SQLite. Las migraciones se incorporarán cuando cambie el contrato."""
SCHEMA = """
CREATE TABLE IF NOT EXISTS counties (
 county_fips TEXT PRIMARY KEY, name TEXT NOT NULL, state TEXT NOT NULL,
 state_code TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS predictions (
 county_fips TEXT NOT NULL REFERENCES counties(county_fips),
 target_year INTEGER NOT NULL,
 model_version TEXT NOT NULL,
 payload TEXT NOT NULL,
 PRIMARY KEY (county_fips, target_year, model_version)
);
CREATE TABLE IF NOT EXISTS history (
 county_fips TEXT NOT NULL REFERENCES counties(county_fips),
 year INTEGER NOT NULL, event_count INTEGER NOT NULL CHECK(event_count >= 0),
 is_demo INTEGER NOT NULL,
 PRIMARY KEY (county_fips, year)
);
"""

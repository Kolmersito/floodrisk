import json
from .database import fetch_all


def active_version(year):
    configured = fetch_all('SELECT model_version FROM active_versions WHERE target_year=?',(year,))
    if configured:
        return configured[0]['model_version']
    # Compatibilidad con instalaciones previas: elegir una versión global por año,
    # nunca completar cada condado con una versión distinta.
    latest = fetch_all("SELECT model_version FROM predictions WHERE target_year=? ORDER BY "
        "json_extract(payload,'$.is_demo') ASC,json_extract(payload,'$.generated_at') DESC,model_version DESC LIMIT 1",(year,))
    return latest[0]['model_version'] if latest else None


def version_policy(version):
    rows = fetch_all('SELECT payload FROM version_metadata WHERE model_version=?',(version,))
    return json.loads(rows[0]['payload']) if rows else None


def version_predictions(year):
    version = active_version(year)
    return version, fetch_all('SELECT county_fips,payload FROM predictions WHERE target_year=? AND model_version=?',(year,version))

import json
from functools import lru_cache
from fastapi import APIRouter, HTTPException, Path, Query
from ..database import ROOT, fetch_all

router = APIRouter()


@router.get('/states')
def national_map():
    path = ROOT/'data/geographic/states_2025.geojson'
    if not path.exists():
        raise HTTPException(503,'Límites estatales no preparados. Ejecuta api.scripts.prepare_geography.')
    return json.loads(path.read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def load_geography():
    path = ROOT/'data/geographic/counties_2025.geojson'
    if not path.exists():
        raise HTTPException(503,'Geografía no preparada. Ejecuta api.scripts.prepare_geography.')
    return json.loads(path.read_text(encoding='utf-8'))


@router.get('/map/{state_code}')
def state_map(state_code: str = Path(pattern=r'^[A-Z]{2}$'),
              target_year: int = Query(ge=2000,le=2100)):
    original = load_geography()
    features = [f for f in original['features'] if f['properties']['state_code'] == state_code]
    if not features:
        raise HTTPException(404,'No hay límites para ese estado')
    rows = fetch_all("""SELECT county_fips,payload FROM (
        SELECT county_fips,payload,ROW_NUMBER() OVER (
          PARTITION BY county_fips ORDER BY json_extract(payload,'$.generated_at') DESC,model_version DESC) AS rank
        FROM predictions WHERE target_year=? AND
          (json_extract(payload,'$.is_demo')=0 OR NOT EXISTS (
            SELECT 1 FROM predictions p WHERE p.target_year=? AND json_extract(p.payload,'$.is_demo')=0))
        ) WHERE rank=1""",(target_year,target_year))
    predictions = {r['county_fips']:json.loads(r['payload']) for r in rows}
    geometry_ids = {f['id'] for f in features}
    prefix = features[0]['id'][:2]
    unplaced = sorted(f for f in predictions if f.startswith(prefix) and f not in geometry_ids)
    result = []
    for feature in features:
        prediction = predictions.get(feature['id'])
        props = {**feature['properties'],'probability':prediction['probability'] if prediction else None,
                 'is_demo':prediction['is_demo'] if prediction else None,
                 'model_version':prediction['model_version'] if prediction else None}
        result.append({**feature,'properties':props})
    return {'type':'FeatureCollection','features':result,'metadata':{
        'source':'U.S. Census Bureau','geometry_year':2025,'target_year':target_year,
        'source_url':'https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html',
        'n_with_prediction':sum(f['properties']['probability'] is not None for f in result),
        'prediction_codes_without_geometry':unplaced}}

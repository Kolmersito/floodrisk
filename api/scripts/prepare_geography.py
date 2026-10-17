"""Descarga límites Census oficiales; requiere pyshp solo para esta preparación."""
import io
import json
import hashlib
from datetime import datetime, timezone
import urllib.request
import zipfile
from pathlib import Path
import shapefile

from api.app.database import ROOT, connect, initialize
from api.scripts.import_colab import STATE_CODES

STATE_NAMES = dict(zip(STATE_CODES, [
    'Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware',
    'District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa',
    'Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota',
    'Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey',
    'New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon',
    'Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah',
    'Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']))


def download(year, kind='county'):
    url = f'https://www2.census.gov/geo/tiger/GENZ{year}/shp/cb_{year}_us_{kind}_5m.zip'
    request = urllib.request.Request(url,headers={'User-Agent':'FloodRisk academic prototype'})
    with urllib.request.urlopen(request,timeout=120) as response:
        payload = response.read(30_000_001)
    if len(payload) > 30_000_000:
        raise ValueError('Descarga demasiado grande')
    archive = zipfile.ZipFile(io.BytesIO(payload))
    def part(extension):
        name = next(n for n in archive.namelist() if n.endswith(extension))
        return io.BytesIO(archive.read(name))
    reader = shapefile.Reader(shp=part('.shp'),shx=part('.shx'),dbf=part('.dbf'),encoding='utf-8')
    return reader, {'url':url,'year':year,'sha256':hashlib.sha256(payload).hexdigest()}


def prepare():
    catalog, features, sources = {}, [], []
    # 2020 solo recupera nombres antiguos; nunca transfiere su predicción a límites nuevos.
    for year in [2020,2025]:
        reader, source = download(year)
        sources.append(source)
        for record in reader.iterShapeRecords():
            props = record.record.as_dict()
            state = props['STATEFP']
            if state not in STATE_CODES:
                continue
            fips = props['GEOID']
            county = {'county_fips':fips,'name':props['NAMELSAD'],
                      'state':STATE_NAMES[state],'state_code':STATE_CODES[state],
                      'catalog_year':year,'geometry_available':year==2025}
            catalog[fips] = county
            if year == 2025:
                features.append({'type':'Feature','id':fips,
                                 'properties':county,'geometry':record.shape.__geo_interface__})
        reader.close()
    collection = {'type':'FeatureCollection','features':features}
    assert len(features) > 3000 and len({f['id'] for f in features}) == len(features)
    output = ROOT/'data/geographic'
    output.mkdir(parents=True,exist_ok=True)
    (output/'counties_2025.geojson').write_text(json.dumps(collection,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    (output/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False),encoding='utf-8')
    reader, state_source = download(2025, 'state')
    sources.append(state_source)
    state_features = []
    for record in reader.iterShapeRecords():
        props = record.record.as_dict()
        if props['STATEFP'] in STATE_CODES:
            state_features.append({'type':'Feature','id':props['STATEFP'],
                'properties':{'state_code':props['STUSPS'],'name':props['NAME']},
                'geometry':record.shape.__geo_interface__})
    reader.close()
    assert len(state_features) == 51
    (output/'states_2025.geojson').write_text(json.dumps({'type':'FeatureCollection','features':state_features},ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    initialize()
    connection = connect()
    try:
        with connection:
            for c in catalog.values():
                connection.execute('INSERT INTO counties VALUES (?,?,?,?) ON CONFLICT(county_fips) DO UPDATE SET '
                    'name=excluded.name,state=excluded.state,state_code=excluded.state_code',
                    (c['county_fips'],c['name'],c['state'],c['state_code']))
        predictions = {r[0] for r in connection.execute("SELECT DISTINCT county_fips FROM predictions WHERE json_extract(payload,'$.is_demo')=0")}
    finally:
        connection.close()
    metadata = {'source':'U.S. Census Bureau Cartographic Boundary Files',
                'retrieved_at':datetime.now(timezone.utc).isoformat(),'sources':sources,
                'geometry_year':2025,'scale':'1:5,000,000','scope':'50 states and DC',
                'geometry_count':len(features),'catalog_count':len(catalog),
                'prediction_fips_without_geometry':sorted(predictions-{f['id'] for f in features}),
                'prediction_fips_without_name':sorted(predictions-set(catalog)),
                'note':'2020 supplements historical names only. No remapping or redistribution of probabilities.'}
    (output/'source_manifest.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(metadata,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    prepare()

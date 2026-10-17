import json
from fastapi import APIRouter
from ..database import ROOT, fetch_all
from ..schemas import County

router = APIRouter()


@router.get("/counties", response_model=list[County])
def counties():
    path = ROOT/'data/geographic/catalog.json'
    catalog = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    result = fetch_all("SELECT * FROM counties ORDER BY state, name")
    for row in result:
        match = catalog.get(row['county_fips'])
        row['name_verified'] = match is not None
        row['geometry_available'] = bool(match and match['geometry_available'])
        if catalog and not match:
            row['name'] = f"Código {row['county_fips']} sin validar"
    return result

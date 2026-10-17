import json
from fastapi import APIRouter, HTTPException, Path, Query
from ..database import fetch_all
from ..schemas import Prediction
from ..versions import active_version

router = APIRouter()


@router.get("/years", response_model=list[int])
def years():
    return [row["target_year"] for row in fetch_all(
        "SELECT DISTINCT target_year FROM predictions ORDER BY target_year")]


@router.get("/predictions/{county_fips}", response_model=Prediction)
def prediction(county_fips: str = Path(pattern=r"^\d{5}$"),
               target_year: int = Query(ge=2000, le=2100)):
    version = active_version(target_year)
    rows = fetch_all('SELECT payload FROM predictions WHERE county_fips=? AND target_year=? AND model_version=?',
                     (county_fips,target_year,version))
    if not rows:
        raise HTTPException(404, f"Sin predicción disponible en {version or 'la versión activa'} para este condado y año.")
    return json.loads(rows[0]["payload"])

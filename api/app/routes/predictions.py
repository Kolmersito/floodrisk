import json
from fastapi import APIRouter, HTTPException, Path, Query
from ..database import fetch_all
from ..schemas import Prediction

router = APIRouter()


@router.get("/years", response_model=list[int])
def years():
    return [row["target_year"] for row in fetch_all(
        "SELECT DISTINCT target_year FROM predictions ORDER BY target_year")]


@router.get("/predictions/{county_fips}", response_model=Prediction)
def prediction(county_fips: str = Path(pattern=r"^\d{5}$"),
               target_year: int = Query(ge=2000, le=2100)):
    rows = fetch_all("SELECT payload FROM predictions WHERE county_fips = ? "
                     "AND target_year = ? ORDER BY json_extract(payload, '$.generated_at') DESC, "
                     "model_version DESC LIMIT 1", (county_fips, target_year))
    if not rows:
        raise HTTPException(404, "No hay predicción para ese condado y año")
    return json.loads(rows[0]["payload"])

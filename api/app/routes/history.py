from fastapi import APIRouter, Path, Query
from ..database import fetch_all
from ..schemas import HistoryEntry

router = APIRouter()


@router.get("/history/{county_fips}", response_model=list[HistoryEntry])
def history(county_fips: str = Path(pattern=r"^\d{5}$"),
            through_year: int = Query(ge=2000, le=2100),
            is_demo: bool | None = None):
    sql = "SELECT * FROM history WHERE county_fips = ? AND year <= ?"
    parameters = [county_fips, through_year]
    if is_demo is not None:
        sql += " AND is_demo = ?"
        parameters.append(int(is_demo))
    return fetch_all(sql + " ORDER BY year", parameters)

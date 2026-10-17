from fastapi import APIRouter, Path, Query, HTTPException
from ..versions import active_version, version_policy
from ..database import fetch_all
from ..schemas import HistoryEntry

router = APIRouter()


@router.get("/history/{county_fips}", response_model=list[HistoryEntry])
def history(county_fips: str = Path(pattern=r"^\d{5}$"),
            through_year: int = Query(ge=2000, le=2100),
            is_demo: bool | None = None,
            target_year: int | None = Query(default=None,ge=2000,le=2100),
            model_version: str | None = None):
    sql = "SELECT * FROM history WHERE county_fips = ? AND year <= ?"
    parameters = [county_fips, through_year]
    if is_demo is not None:
        sql += " AND is_demo = ?"
        parameters.append(int(is_demo))
    entries = fetch_all(sql + " ORDER BY year", parameters)
    version = model_version or (active_version(target_year) if target_year else None)
    if version is None:
        configured = fetch_all('SELECT model_version FROM active_versions')
        if len(configured) == 1:
            version = configured[0]['model_version']
        elif len(configured) > 1:
            raise HTTPException(422,'Indica target_year para consultar el historial de la versión activa.')
    if target_year and model_version and model_version != active_version(target_year):
        raise HTTPException(409,'La versión activa cambió. Vuelve a consultar el resultado.')
    policy = version_policy(version) if version else None
    if policy:
        if county_fips not in policy['allowed_fips']:
            return []
        quarantine = {(r['county_fips'],r['year']) for r in policy['quarantine_county_year']}
        entries = [r for r in entries if (county_fips,r['year']) not in quarantine and not r['is_demo']]
    return entries

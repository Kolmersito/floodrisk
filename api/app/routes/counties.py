from fastapi import APIRouter
from ..database import fetch_all
from ..schemas import County

router = APIRouter()


@router.get("/counties", response_model=list[County])
def counties():
    return fetch_all("SELECT * FROM counties ORDER BY state, name")

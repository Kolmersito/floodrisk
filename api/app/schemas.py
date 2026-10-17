from datetime import date, datetime
from pydantic import BaseModel, Field, model_validator


class County(BaseModel):
    county_fips: str = Field(pattern=r"^\d{5}$")
    name: str
    state: str
    state_code: str


class Prediction(BaseModel):
    county_fips: str = Field(pattern=r"^\d{5}$")
    target_year: int = Field(ge=2000, le=2100)
    probability: float = Field(ge=0, le=1, allow_inf_nan=False)
    data_cutoff: date
    generated_at: datetime
    model_version: str = Field(min_length=1)
    is_demo: bool
    factors: list[str]

    @model_validator(mode="after")
    def check_temporal_cutoff(self):
        if self.data_cutoff >= date(self.target_year, 1, 1):
            raise ValueError("El corte debe ser anterior al año objetivo")
        return self


class HistoryEntry(BaseModel):
    county_fips: str = Field(pattern=r"^\d{5}$")
    year: int
    event_count: int = Field(ge=0)
    is_demo: bool

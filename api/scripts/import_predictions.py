"""Carga explícita y validada; ejecuta desde la raíz con python -m api.scripts.import_predictions."""
import argparse
import json
from pathlib import Path
from api.app.database import ROOT, connect, initialize
from api.app.schemas import County, HistoryEntry, Prediction


def import_file(path: Path, demo: bool = False):
    payload = json.loads(path.read_text(encoding="utf-8"))
    counties = [County.model_validate(item) for item in payload["counties"]]
    predictions = [Prediction.model_validate(item) for item in payload["predictions"]]
    history = [HistoryEntry.model_validate(item) for item in payload["history"]]
    if any(item.is_demo != demo for item in predictions + history):
        raise ValueError("La marca is_demo no coincide con el modo de importación")
    initialize()
    connection = connect()
    try:
        with connection:
            for county in counties:
                connection.execute("INSERT INTO counties VALUES (?, ?, ?, ?) ON CONFLICT(county_fips) "
                                   "DO UPDATE SET name=excluded.name, state=excluded.state, state_code=excluded.state_code",
                                   (county.county_fips, county.name, county.state, county.state_code))
            for item in predictions:
                connection.execute("INSERT INTO predictions VALUES (?, ?, ?, ?) "
                                   "ON CONFLICT(county_fips,target_year,model_version) DO UPDATE SET payload=excluded.payload",
                                   (item.county_fips, item.target_year, item.model_version, item.model_dump_json()))
            for item in history:
                connection.execute("INSERT INTO history VALUES (?, ?, ?, ?) ON CONFLICT(county_fips,year) "
                                   "DO UPDATE SET event_count=excluded.event_count, is_demo=excluded.is_demo",
                                   (item.county_fips, item.year, item.event_count, item.is_demo))
    finally:
        connection.close()
    return len(predictions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--demo", action="store_true")
    source.add_argument("--file", type=Path)
    args = parser.parse_args()
    path = ROOT / "data/demo/demo.json" if args.demo else args.file
    print(f"Predicciones importadas: {import_file(path, demo=args.demo)}")

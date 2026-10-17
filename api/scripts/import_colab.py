"""Importa solo CSV/JSON del ZIP de Colab. Nunca deserializa modelo.joblib."""
import argparse
import csv
from contextlib import closing
from datetime import datetime
import hashlib
import io
import json
import math
from pathlib import Path
import sqlite3
import zipfile

from api.app.database import ROOT, connect, initialize
from api.app.schemas import Prediction

STATE_CODES = dict(item.split(":") for item in (
    "01:AL 02:AK 04:AZ 05:AR 06:CA 08:CO 09:CT 10:DE 11:DC 12:FL 13:GA 15:HI 16:ID "
    "17:IL 18:IN 19:IA 20:KS 21:KY 22:LA 23:ME 24:MD 25:MA 26:MI 27:MN 28:MS "
    "29:MO 30:MT 31:NE 32:NV 33:NH 34:NJ 35:NM 36:NY 37:NC 38:ND 39:OH "
    "40:OK 41:OR 42:PA 44:RI 45:SC 46:SD 47:TN 48:TX 49:UT 50:VT 51:VA 53:WA 54:WV 55:WI 56:WY"
).split())


def member(archive, name):
    matches = [i for i in archive.infolist() if not i.filename.startswith("__MACOSX/")
               and Path(i.filename).name == name and not i.is_dir()]
    if len(matches) != 1 or matches[0].file_size > 100_000_000:
        raise ValueError(f"Archivo ausente, repetido o demasiado grande: {name}")
    return archive.read(matches[0]).decode("utf-8-sig")


def rows(text):
    return csv.DictReader(io.StringIO(text))


def boolean(value):
    if value not in ("True", "False", "true", "false"):
        raise ValueError(f"Booleano inválido: {value}")
    return value.lower() == "true"


def import_colab(path: Path, dataset_zip: Path | None = None):
    with zipfile.ZipFile(path) as archive:
        metadata = json.loads(member(archive, "metadatos.json"))
        data = list(rows(member(archive, "predicciones.csv")))
    if not data or len(data) != metadata["n_predictions"]:
        raise ValueError("Cantidad de predicciones distinta de los metadatos")
    predictions = []
    keys = set()
    for row in data:
        fips = row["county_fips"]
        if len(fips) != 5 or not fips.isascii() or not fips.isdigit() or fips.endswith("000") or fips[:2] not in STATE_CODES:
            raise ValueError(f"FIPS fuera del alcance: {fips}")
        item = Prediction.model_validate({
            **row, "is_demo": boolean(row["is_demo"]),
            "is_experimental": boolean(row["is_experimental"]),
            "generated_at": metadata["generated_at_utc"], "factors": [],
            "horizon_years": metadata["horizon_years"],
            "input_snapshot_at": metadata["source_generated_at"],
            "limitations": metadata["limitations"],
        })
        if item.is_demo or not item.is_experimental:
            raise ValueError("Se requieren predicciones entrenadas experimentales, no demo")
        if (item.target_year != metadata["target_year"] or item.model_version != metadata["model_version"]
                or item.data_cutoff.isoformat() != f'{metadata["last_feature_year"]}-12-31'
                or int(row["base_year"]) != metadata["last_feature_year"]
                or item.target_year - int(row["base_year"]) != metadata["horizon_years"]
                or row["state_fips"] != fips[:2]):
            raise ValueError("Año, corte, desfase, versión o estado no coinciden con metadatos")
        key = (fips, item.target_year, item.model_version)
        if key in keys:
            raise ValueError(f"Predicción duplicada: {key}")
        keys.add(key)
        predictions.append(item)
    history = []
    fips_set = {p.county_fips for p in predictions}
    if dataset_zip:
        if hashlib.sha256(dataset_zip.read_bytes()).hexdigest() != metadata["source_zip_sha256"]:
            raise ValueError("El ZIP original no coincide con el utilizado en Colab")
        history_keys = set()
        with zipfile.ZipFile(dataset_zip) as archive:
            for row in rows(member(archive, "storm_events_county_year.csv")):
                fips, year = row["county_fips"].zfill(5), int(row["year"])
                if fips not in fips_set or year > metadata["last_feature_year"]:
                    continue
                count = float(row["flood_related_event_count"])
                if not math.isfinite(count) or count < 0 or not count.is_integer() or (fips, year) in history_keys:
                    raise ValueError("Historial duplicado o con conteo inválido")
                history_keys.add((fips, year))
                history.append((fips, year, int(count), False))

    # Toda validación termina antes de escribir. Respaldo recuperable de la BD previa.
    initialize()
    connection = connect()
    try:
        db_path = Path(connection.execute("PRAGMA database_list").fetchone()["file"])
        backup_path = db_path.with_name(db_path.stem + ".before-colab-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".db")
        with closing(sqlite3.connect(backup_path)) as backup:
            connection.backup(backup)
        with connection:
            for fips in sorted(fips_set):
                code = STATE_CODES[fips[:2]]
                # No reemplaza nombres conocidos por etiquetas FIPS.
                connection.execute("INSERT INTO counties VALUES (?, ?, ?, ?) ON CONFLICT(county_fips) DO NOTHING",
                                   (fips, f"Condado FIPS {fips}", code, code))
            for p in predictions:
                connection.execute("INSERT INTO predictions VALUES (?, ?, ?, ?) "
                    "ON CONFLICT(county_fips,target_year,model_version) DO UPDATE SET payload=excluded.payload",
                    (p.county_fips,p.target_year,p.model_version,p.model_dump_json()))
            connection.executemany("INSERT INTO history VALUES (?, ?, ?, ?) ON CONFLICT(county_fips,year) "
                "DO UPDATE SET event_count=excluded.event_count,is_demo=excluded.is_demo", history)
    finally:
        connection.close()
    return {"predictions":len(predictions),"history":len(history),"backup":str(backup_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip",type=Path,required=True)
    parser.add_argument("--dataset-zip",type=Path,help="ZIP original exacto usado en Colab para cargar historial")
    args = parser.parse_args()
    print(json.dumps(import_colab(args.zip,args.dataset_zip),ensure_ascii=False,indent=2))

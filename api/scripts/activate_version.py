"""Activa una versión ya importada y su política; conserva resultados previos."""
import argparse
from contextlib import closing
from datetime import datetime
import csv
import io
import json
from pathlib import Path
import sqlite3
import zipfile
from api.app.database import connect, initialize
from api.scripts.import_colab import member


def activate(path):
    with zipfile.ZipFile(path) as archive:
        metadata = json.loads(member(archive,'metadatos.json'))
        policy = json.loads(member(archive,'politica_geografica.json'))
        predictions = list(csv.DictReader(io.StringIO(member(archive,'predicciones.csv'))))
    year, version = metadata['target_year'], metadata['model_version']
    expected = {r['county_fips']:float(r['probability']) for r in predictions}
    if len(expected) != len(predictions) or len(expected) != metadata['n_predictions']:
        raise ValueError('Conteo o claves duplicadas en el paquete')
    allowed=set(policy['allowed_fips'])
    quarantine={(r['county_fips'],r['year']) for r in policy['quarantine_county_year']}
    if not expected.keys() <= allowed or any((f,metadata['last_feature_year']) in quarantine for f in expected):
        raise ValueError('Emisión incompatible con política geográfica')
    if metadata.get('geographic_policy') != policy['version']:
        raise ValueError('Versión de política incompatible')
    initialize()
    with closing(connect()) as connection:
        actual={r['county_fips']:json.loads(r['payload'])['probability'] for r in connection.execute(
            'SELECT county_fips,payload FROM predictions WHERE target_year=? AND model_version=?',(year,version))}
        if actual != expected:
            raise ValueError('La base no contiene exactamente las predicciones del paquete')
        db=Path(connection.execute('PRAGMA database_list').fetchone()['file'])
        backup=db.with_name(db.stem+'.before-activation-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.db')
        with closing(sqlite3.connect(backup)) as target:
            connection.backup(target)
        with connection:
            connection.execute('INSERT INTO version_metadata VALUES (?,?) ON CONFLICT(model_version) DO UPDATE SET payload=excluded.payload',
                               (version,json.dumps(policy)))
            connection.execute('INSERT INTO active_versions VALUES (?,?) ON CONFLICT(target_year) DO UPDATE SET model_version=excluded.model_version',(year,version))
    return {'year':year,'active_version':version,'count':len(expected),'backup':str(backup)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip',type=Path,required=True)
    print(json.dumps(activate(parser.parse_args().zip),indent=2))

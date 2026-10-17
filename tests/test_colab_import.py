import csv
from contextlib import closing
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from fastapi.testclient import TestClient
from api.app.database import ROOT, connect
from api.app.main import app
from api.scripts.import_colab import import_colab
from api.scripts.import_predictions import import_file
from api.scripts.activate_version import activate


class ColabImportTests(unittest.TestCase):
    def test_activation_never_falls_back_and_filters_history(self):
        import_file(ROOT/'data/demo/demo.json',demo=True)
        package=self.package()
        with zipfile.ZipFile(package) as z:
            contents={n:z.read(n) for n in z.namelist()}
        metadata=json.loads(contents['metadatos.json'])
        metadata['geographic_policy']='test-policy'
        contents['metadatos.json']=json.dumps(metadata).encode()
        contents['politica_geografica.json']=json.dumps({'version':'test-policy',
            'allowed_fips':['48201','48453'],'quarantine_county_year':[{'county_fips':'48453','year':2023}]}).encode()
        with zipfile.ZipFile(package,'w') as z:
            for n,data in contents.items(): z.writestr(n,data)
        import_colab(package)
        activation=activate(package)
        self.assertTrue(Path(activation['backup']).exists())
        self.assertEqual(self.client.get('/api/predictions/48201?target_year=2027').json()['model_version'],'experimental-v1')
        # Activación explícita no permite recurrir a demo u otra versión.
        response=self.client.get('/api/predictions/48453?target_year=2027')
        self.assertEqual(response.status_code,404)
        self.assertIn('experimental-v1',response.json()['detail'])
        history=self.client.get('/api/history/48453?through_year=2025&target_year=2027').json()
        self.assertEqual(history,[])  # No mezclar historial demo con política entrenada.
        with closing(connect()) as connection:
            with connection:
                connection.execute('INSERT OR REPLACE INTO history VALUES (?,?,?,?)',('48453',2023,50,0))
                connection.execute('INSERT OR REPLACE INTO history VALUES (?,?,?,?)',('48453',2024,3,0))
        history=self.client.get('/api/history/48453?through_year=2025&target_year=2027').json()
        self.assertEqual([(r['year'],r['event_count']) for r in history],[(2024,3)])
        self.assertEqual(self.client.get('/api/history/48453?through_year=2025&target_year=2027&model_version=other').status_code,409)
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {'FLOODRISK_DB': str(Path(self.directory.name)/'test.db')})
        self.env.start()
        self.client = TestClient(app)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None,None,None)
        self.env.stop()
        self.directory.cleanup()

    def package(self, changes=None, duplicate=False):
        row = dict(county_fips='48201',target_year=2027,base_year=2025,
                   probability=.8938,state_fips='48',data_cutoff='2025-12-31',
                   model_version='experimental-v1',event_definition='NOAA relacionado > 0',
                   is_demo='False',is_experimental='True')
        row.update(changes or {})
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer,fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
        if duplicate:
            writer.writerow(row)
        metadata = dict(n_predictions=2 if duplicate else 1,target_year=2027,
                        last_feature_year=2025,horizon_years=2,model_version='experimental-v1',
                        generated_at_utc='2026-10-17T02:30:46Z',source_generated_at='2026-08-21T17:33:19Z',
                        limitations=['Experimental'])
        path = Path(self.directory.name)/'colab.zip'
        with zipfile.ZipFile(path,'w') as archive:
            archive.writestr('predicciones.csv',buffer.getvalue())
            archive.writestr('metadatos.json',json.dumps(metadata))
            archive.writestr('modelo.joblib',b'not a model; must never deserialize')
        return path

    def test_real_import_idempotent_preserves_names_and_hides_demo(self):
        import_file(ROOT/'data/demo/demo.json',demo=True)
        path = self.package()
        for _ in range(2):
            result = import_colab(path)
            self.assertTrue(Path(result['backup']).exists())
        response = self.client.get('/api/predictions/48201?target_year=2027').json()
        self.assertEqual(response['probability'],.8938)
        self.assertFalse(response['is_demo'])
        self.assertTrue(response['is_experimental'])
        self.assertEqual(response['horizon_years'],2)
        self.assertEqual(response['factors'],[])
        self.assertEqual(self.client.get('/health').json()['trained_prediction_count'],1)
        self.assertEqual(self.client.get('/api/predictions/48453?target_year=2027').status_code,404)
        counties = self.client.get('/api/counties').json()
        self.assertFalse(next(c for c in counties if c['county_fips']=='48201')['name'].startswith('Condado FIPS'))
        self.assertEqual(self.client.get('/api/history/48201?through_year=2025&is_demo=false').json(),[])

    def test_rejects_bad_rows_without_importing(self):
        for changes in [{'probability':'NaN'}, {'probability':2}, {'county_fips':'48000'},
                        {'is_demo':'True'}, {'base_year':2026}, {'target_year':2028},
                        {'state_fips':'12'}, {'data_cutoff':'2027-01-01'}]:
            with self.assertRaises((ValueError,TypeError)):
                import_colab(self.package(changes))
        self.assertEqual(self.client.get('/api/years').json(),[])
        with self.assertRaises(ValueError):
            import_colab(self.package(duplicate=True))

    def test_real_history_filter_and_cutoff(self):
        import_file(ROOT/'data/demo/demo.json',demo=True)
        import_colab(self.package())
        with closing(connect()) as connection:
            with connection:
                connection.execute('INSERT OR REPLACE INTO history VALUES (?,?,?,?)',('48201',2025,7,0))
                connection.execute('INSERT OR REPLACE INTO history VALUES (?,?,?,?)',('48201',2026,99,0))
        entries = self.client.get('/api/history/48201?through_year=2025&is_demo=false').json()
        self.assertEqual([(e['year'],e['event_count']) for e in entries],[(2025,7)])

    def test_cors_for_vite_alternative_port(self):
        response = self.client.get('/health',headers={'Origin':'http://127.0.0.1:5174'})
        self.assertEqual(response.headers['access-control-allow-origin'],'http://127.0.0.1:5174')

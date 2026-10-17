import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.app.database import ROOT, connect
from api.app.main import app
from api.app.routes.geography import load_geography
from api.scripts.import_predictions import import_file


class GeographyTests(unittest.TestCase):
    def test_national_states_endpoint(self):
        state_data = {'type':'FeatureCollection','features':[
            {'type':'Feature','id':'48','properties':{'state_code':'TX','name':'Texas'},
             'geometry':{'type':'Polygon','coordinates':[[[-106,25],[-94,25],[-94,36],[-106,25]]]}}]}
        with patch('api.app.routes.geography.ROOT',Path(self.temp.name)):
            directory = Path(self.temp.name)/'data/geographic'
            directory.mkdir(parents=True)
            (directory/'states_2025.geojson').write_text(json.dumps(state_data),encoding='utf-8')
            response = self.client.get('/api/states')
            self.assertEqual(response.status_code,200)
            self.assertEqual(response.json()['features'][0]['properties']['state_code'],'TX')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ,{'FLOODRISK_DB':str(Path(self.temp.name)/'test.db')})
        self.env.start()
        self.client = TestClient(app)
        self.client.__enter__()
        self.features = {'type':'FeatureCollection','features':[
            {'type':'Feature','id':fips,'properties':{'county_fips':fips,'name':name,'state_code':'TX'},
             'geometry':{'type':'Polygon','coordinates':[[[-96,30],[-95,30],[-95,31],[-96,30]]]}}
            for fips,name in [('48201','Harris County'),('48203','Harrison County')]]}
        self.geo = patch('api.app.routes.geography.load_geography',return_value=self.features)
        self.geo.start()

    def tearDown(self):
        self.geo.stop()
        self.client.__exit__(None,None,None)
        self.env.stop()
        self.temp.cleanup()

    def test_no_prediction_is_null_not_zero(self):
        response = self.client.get('/api/map/TX?target_year=2027')
        self.assertEqual(response.status_code,200)
        self.assertTrue(all(f['properties']['probability'] is None for f in response.json()['features']))
        self.assertEqual(response.json()['metadata']['n_with_prediction'],0)

    def test_values_and_missing_year_and_state(self):
        import_file(ROOT/'data/demo/demo.json',demo=True)
        data = self.client.get('/api/map/TX?target_year=2027').json()
        self.assertEqual(data['features'][0]['properties']['probability'],.68)
        self.assertIsNone(data['features'][1]['properties']['probability'])
        self.assertTrue(all(f['properties']['probability'] is None for f in self.client.get('/api/map/TX?target_year=2028').json()['features']))
        self.assertEqual(self.client.get('/api/map/ZZ?target_year=2027').status_code,404)
        self.assertEqual(self.client.get('/api/map/invalid?target_year=2027').status_code,422)

    def test_map_selection_matches_detail_and_excludes_demo(self):
        import_file(ROOT/'data/demo/demo.json',demo=True)
        connection = connect()
        try:
            demo = json.loads(connection.execute("SELECT payload FROM predictions WHERE county_fips='48201'").fetchone()[0])
            trained = {**demo,'probability':.89,'is_demo':False,'model_version':'experimental-v1'}
            with connection:
                connection.execute('INSERT INTO predictions VALUES (?,?,?,?)',('48201',2027,'experimental-v1',json.dumps(trained)))
        finally:
            connection.close()
        data = self.client.get('/api/map/TX?target_year=2027').json()
        self.assertEqual(data['features'][0]['properties']['probability'],.89)
        self.assertEqual(data['metadata']['prediction_codes_without_geometry'],[])
        self.assertEqual(self.client.get('/api/predictions/48201?target_year=2027').json()['probability'],.89)
        # La caché fuente nunca debe modificarse con probabilidades de una consulta.
        self.assertNotIn('probability',self.features['features'][0]['properties'])

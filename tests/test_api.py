import os
import tempfile
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from pydantic import ValidationError
from api.app.database import ROOT
from api.app.main import app
from api.app.schemas import Prediction
from api.scripts.import_predictions import import_file


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.environment = patch.dict(os.environ, {"FLOODRISK_DB": os.path.join(self.directory.name, "test.db")})
        self.environment.start()
        self.client = TestClient(app)
        self.client.__enter__()

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.environment.stop()
        self.directory.cleanup()

    def test_no_prediction_is_invented_for_empty_database(self):
        self.assertEqual(self.client.get("/api/years").json(), [])
        self.assertEqual(self.client.get("/api/predictions/48201?target_year=2027").status_code, 404)

    def test_import_is_idempotent_and_exposes_demo_flag(self):
        for _ in range(2):
            self.assertEqual(import_file(ROOT / "data/demo/demo.json", demo=True), 3)
        self.assertEqual(len(self.client.get("/api/counties").json()), 3)
        response = self.client.get("/api/predictions/48201?target_year=2027")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_demo"])
        self.assertEqual(response.json()["probability"], 0.68)
        self.assertEqual(self.client.get("/api/predictions/48201?target_year=2028").status_code, 404)
        entries = self.client.get("/api/history/48201?through_year=2023").json()
        self.assertTrue(all(row["year"] <= 2023 for row in entries))

    def test_rejects_invalid_prediction_contract(self):
        example = {"county_fips": "48201", "target_year": 2027, "probability": 0.68,
                   "data_cutoff": "2025-12-31", "generated_at": "2026-10-16T12:00:00Z",
                   "model_version": "demo-v1", "is_demo": True, "factors": []}
        for changes in ({"data_cutoff": "2027-01-01"}, {"probability": 1.5},
                        {"probability": float("nan")}, {"county_fips": "201"}):
            with self.assertRaises(ValidationError):
                Prediction.model_validate({**example, **changes})

import json
import unittest
from pathlib import Path
from ml.src.features import validate_availability, validate_cutoff


class TemporalTests(unittest.TestCase):
    def test_rejects_target_year_information(self):
        for cutoff in ("2027-01-01", "2027-08-21", "2028-01-01"):
            with self.assertRaises(ValueError):
                validate_cutoff(2027, cutoff)

    def test_accepts_previous_year(self):
        validate_cutoff(2027, "2026-12-31")

    def test_rejects_late_publication(self):
        with self.assertRaises(ValueError):
            validate_availability("2026-12-31", "2027-02-01")

    def test_demo_contract(self):
        data = json.loads((Path(__file__).resolve().parents[1] / "data/demo/demo.json").read_text())
        fips = {row["county_fips"] for row in data["counties"]}
        for row in data["predictions"]:
            self.assertIn(row["county_fips"], fips)
            self.assertTrue(row["is_demo"])
            self.assertTrue(0 <= row["probability"] <= 1)
            validate_cutoff(row["target_year"], row["data_cutoff"])

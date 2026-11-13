
import unittest
import pandas as pd
from pathlib import Path


# Locate main project folder
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


class TestShipmentRouteOptimizer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Load all generated datasets
        cls.original = pd.read_csv(
            DATA_DIR / "shipment_routes.csv"
        )

        cls.normalized = pd.read_csv(
            DATA_DIR / "normalized_routes.csv"
        )

        cls.scored = pd.read_csv(
            DATA_DIR / "scored_routes.csv"
        )

        cls.recommended = pd.read_csv(
            DATA_DIR / "recommended_routes.csv"
        )

        cls.top3 = pd.read_csv(
            DATA_DIR / "top3_routes.csv"
        )

        cls.explanations = pd.read_csv(
            DATA_DIR / "explainable_recommendations.csv"
        )

    # Test 1: Dataset loading
    def test_dataset_loading(self):

        self.assertEqual(len(self.original), 120)

        self.assertEqual(
            self.original["shipment_id"].nunique(),
            30
        )

    # Test 2: Check missing values
    def test_missing_values(self):

        self.assertFalse(
            self.original.isnull().any().any()
        )

    # Test 3: Check normalization
    def test_normalized_values(self):

        for column in [
            "cost_norm",
            "time_norm",
            "risk_norm"
        ]:

            self.assertTrue(
                self.normalized[column].between(0, 1).all()
            )

    # Test 4: Check risk calculation
    def test_risk_calculation(self):

        expected_risk = (
            0.5 * self.original["delay_probability"] +
            0.3 * self.original["congestion_risk"] +
            0.2 * self.original["geopolitical_risk"]
        )

        actual_risk = self.normalized["risk_score"]

        pd.testing.assert_series_equal(
            expected_risk.reset_index(drop=True),
            actual_risk.reset_index(drop=True),
            check_names=False
        )

    # Test 5: Check weighted score
    def test_weighted_score(self):

        expected_score = (
            0.40 * self.scored["cost_norm"] +
            0.30 * self.scored["time_norm"] +
            0.30 * self.scored["risk_norm"]
        )

        pd.testing.assert_series_equal(
            expected_score.reset_index(drop=True),
            self.scored["weighted_score"].reset_index(drop=True),
            check_names=False
        )

    # Test 6: Check best route selection
    def test_best_route_selection(self):

        for shipment_id in self.scored["shipment_id"].unique():

            group = self.scored[
                self.scored["shipment_id"] == shipment_id
            ]

            expected_route = group.loc[
                group["weighted_score"].idxmin(),
                "route_id"
            ]

            actual_route = self.recommended.loc[
                self.recommended["shipment_id"] == shipment_id,
                "route_id"
            ].iloc[0]

            self.assertEqual(
                expected_route,
                actual_route
            )

    # Test 7: Check top 3 routes
    def test_top_three_routes(self):

        counts = self.top3.groupby(
            "shipment_id"
        ).size()

        self.assertTrue(
            (counts == 3).all()
        )

        self.assertEqual(
            self.top3["shipment_id"].nunique(),
            30
        )

    # Test 8: Check explanation generation
    def test_explanations(self):

        self.assertEqual(
            len(self.explanations),
            30
        )

        self.assertFalse(
            self.explanations[
                "recommendation_explanation"
            ].isnull().any()
        )

    # Test 9: Check output files
    def test_output_files(self):

        files = [
            "recommended_routes.csv",
            "top3_routes.csv",
            "explainable_recommendations.csv"
        ]

        for filename in files:

            self.assertTrue(
                (DATA_DIR / filename).exists()
            )


if __name__ == "__main__":

    unittest.main(verbosity=2)

from crop_lca.lca import ClimateChangeTotals
from crop_lca.models import load_crop_farm_data
import unittest
import pandas as pd


class DatasetLoadingTestCase(unittest.TestCase):
    def setUp(self):
        # Create the DataFrame with the provided data

        data = {
            'ef_country': ['ireland', 'ireland', 'ireland', 'ireland', 'ireland'],
            'farm_id': [2020, 2020, 2020, 2020, 2020],
            'year': [2020, 2020, 2020, 2020, 2020],
            'crop_type': ['barley', 'crops', 'maize', 'spring_wheat', 'winter_wheat'],
            'kg_dm_per_ha': [7.289189, 3.86546, 7.125387, 8.968263, 8.968263],
            'area': [5557.922952642, 200.003617085, 1299.493637777, 1634.363389845, 1634.363389845]
        }

        self.data_frame = pd.DataFrame(data)

        self.climatechange = ClimateChangeTotals("ireland")
        self.baseline_index = 2020

        self.urea_proportion =0.2
        self.urea_abated_proportion = 0

    def test_emissions(self):
        data = load_crop_farm_data(self.data_frame)

        self.assertIsNotNone(
            self.climatechange.total_residue_per_crop_direct(
                data[self.baseline_index],
            ),
            "No result generated for residues N2O emissions",
        )

        self.assertIsNotNone(
            self.climatechange.total_fertiliser_direct(
                data[self.baseline_index],
                self.urea_proportion,
                self.urea_abated_proportion,
            ),
            "No result generated for direct fertiliser emissions",
        )
        self.assertIsNotNone(
            self.climatechange.total_fertiliser_indirect(
                data[self.baseline_index],
                self.urea_proportion,
                self.urea_abated_proportion,
            ),
            "No result generated for indirect fertiliser emissions",
        )

        self.assertIsNotNone(
            self.climatechange.urea_co2(
                data[self.baseline_index],
                self.urea_proportion,
                self.urea_abated_proportion
            ),
            "No result generated for Urea CO2 emmissions",
        )

    if __name__ == "__main__":
        unittest.main()

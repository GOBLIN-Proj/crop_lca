from crop_lca.lca import ClimateChangeTotals
from crop_lca.models import load_crop_farm_data
import unittest
import pandas as pd
    
class ClassesTestCase(unittest.TestCase):
    def setUp(self):

        data = {
            'ef_country': ['ireland', 'ireland', 'ireland', 'ireland', 'ireland'],
            'farm_id': ['2020', '2020', '2020', '2020', '2020'],
            'year': ['2020', '2020', '2020', '2020', '2020'],
            'crop_type': ['barley', 'crops', 'maize', 'spring_wheat', 'winter_wheat'],
            'kg_dm_per_ha': [7.289189, 3.86546, 7.125387, 8.968263, 8.968263],
            'area': [5557.922952642, 200.003617085, 1299.493637777, 1634.363389845, 1634.363389845]
        }

        self.data_frame = pd.DataFrame(data)

        self.climatechange = ClimateChangeTotals("ireland")
        self.id = "2020"

    def test_class(self):
        data = load_crop_farm_data(self.data_frame)
        print(self.climatechange.total_residue_per_crop_direct(data[self.id]))

if __name__ == "__main__":
    unittest.main()
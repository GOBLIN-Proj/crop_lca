from crop_lca.lca import ClimateChangeTotals
from crop_lca.models import load_crop_farm_data, load_farm_data
import unittest
import pandas as pd
import matplotlib.pyplot as plt
import os

class EmissionsTestCase(unittest.TestCase):
    def setUp(self):

        data = {
            'ef_country': ['ireland', 'ireland', 'ireland', 'ireland', 'ireland'],
            'farm_id': [2020, 2020, 2020, 2020, 2020],
            'year': [2020, 2020, 2020, 2020, 2020],
            'crop_type': ['barley', 'crops', 'maize', 'spring_wheat', 'winter_wheat'],
            'kg_dm_per_ha': [7.289189, 3.86546, 7.125387, 8.968263, 8.968263],
            'area': [5557.922952642, 200.003617085, 1299.493637777, 1634.363389845, 1634.363389845]
        }

        self.data_frame = pd.DataFrame(data)

        farm_data = {
            "ef_country": ["ireland"],
            "farm_id": [2020],
            "year": [2020],
            "diesel_kg": [0],
            "elec_kwh": [0],
        }

        self.farm_dataframe = pd.DataFrame(farm_data)
        self.climatechange = ClimateChangeTotals("ireland")

        self.baseline_index = 2020
        self.crop_emissions_dict = self.climatechange.create_extended_emissions_dictionary(
            [self.baseline_index]
        )

        self.urea_proportion =0.2
        self.urea_abated_proportion = 0

    def test_class(self):
        data = load_crop_farm_data(self.data_frame)
        farm_data = load_farm_data(self.farm_dataframe)

        self.crop_emissions_dict["crop_residue_direct"][self.baseline_index] += (
            self.climatechange.total_residue_per_crop_direct(
                data[self.baseline_index],
            )
        )* 298

        self.crop_emissions_dict["N_direct_fertiliser"][self.baseline_index] += (
            self.climatechange.total_fertiliser_direct(
                data[self.baseline_index],
                self.urea_proportion,
                self.urea_abated_proportion,
            )
            
        )* 298

        self.crop_emissions_dict["N_indirect_fertiliser"][self.baseline_index] += (
            self.climatechange.total_fertiliser_indirect(
                data[self.baseline_index],
                self.urea_proportion,
                self.urea_abated_proportion,
            ) 
        )* 298 

        self.crop_emissions_dict["soils_N2O"][self.baseline_index] += (
            self.crop_emissions_dict["crop_residue_direct"][self.baseline_index]
            + self.crop_emissions_dict["N_direct_fertiliser"][self.baseline_index]
            + self.crop_emissions_dict["N_indirect_fertiliser"][self.baseline_index]
        ) 

        self.crop_emissions_dict["soils_CO2"][self.baseline_index] += (
            self.climatechange.urea_co2(
                data[self.baseline_index],
                self.urea_proportion,
                self.urea_abated_proportion,

            )
            
        )

        self.crop_emissions_dict["upstream"][self.baseline_index] += (
            self.climatechange.upstream_and_inputs_and_fuel_co2(
                data[self.baseline_index],
                self.urea_proportion,
                farm_data[self.baseline_index].diesel_kg,
                farm_data[self.baseline_index].elec_kwh,
            )
            
        )

        print(self.crop_emissions_dict)

        path = "data"
        labels = self.crop_emissions_dict.keys()
        values = [self.crop_emissions_dict[label][self.baseline_index] for label in labels] 

        plt.bar(labels, values)
        plt.xticks(rotation=90)
        plt.ylabel('Values')
        plt.xlabel('Categories')
        plt.title('Bar Chart')
        plt.tight_layout()

        plt.savefig(os.path.join(path,"emissions_test.png"))


if __name__ == "__main__":
    unittest.main()
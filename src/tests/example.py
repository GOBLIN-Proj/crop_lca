import pandas as pd
from crop_lca.models import load_crop_farm_data
from crop_lca.lca import ClimateChangeTotals


def main():
    # Instantiate ClimateChange Totals Class, passing Ireland as the emissions factor country
    climatechange = ClimateChangeTotals("ireland")

    # Create a dictionary to store results
    index = "2020"
    crop_emissions_dict = climatechange.create_emissions_dictionary([index])

    # Create some data to generate results

    data = {
        'ef_country': ['ireland', 'ireland', 'ireland', 'ireland', 'ireland'],
        'farm_id': ['2020', '2020', '2020', '2020', '2020'],
        'year': ['2020', '2020', '2020', '2020', '2020'],
        'crop_type': ['barley', 'crops', 'maize', 'spring_wheat', 'winter_wheat'],
        'kg_dm_per_ha': [7.289189, 3.86546, 7.125387, 8.968263, 8.968263],
        'area': [5557.922952642, 200.003617085, 1299.493637777, 1634.363389845, 1634.363389845]
    }

    data_frame = pd.DataFrame(data)

    #proportion of fertiliser inputs that is urea
    urea_proportion =0.2
    urea_abated_proportion = 0
    # generate results and store them in the dictionary

    data = load_crop_farm_data(data_frame)

    crop_emissions_dict["crop_residue_direct"][index] += (
        climatechange.total_residue_per_crop_direct(
            data[index],
        )
    )
    crop_emissions_dict["N_direct_fertiliser"][index] += (
        climatechange.total_fertiliser_direct(
            data[index],
            urea_proportion,
            urea_abated_proportion,
        )
        
    )
    crop_emissions_dict["N_indirect_fertiliser"][index] += (
        climatechange.total_fertiliser_indirect(
            data[index],
            urea_proportion,
            urea_abated_proportion,
        )
    )
    crop_emissions_dict["soils_N2O"][index] += (
        crop_emissions_dict["crop_residue_direct"][index]
        + crop_emissions_dict["N_direct_fertiliser"][index]
        + crop_emissions_dict["N_indirect_fertiliser"][index]
    )
    crop_emissions_dict["soils_CO2"][index] += (
        climatechange.urea_co2(
            data[index],
            urea_proportion,
            urea_abated_proportion,
        )
        
    )

    print(crop_emissions_dict)


if __name__ == "__main__":
    main()

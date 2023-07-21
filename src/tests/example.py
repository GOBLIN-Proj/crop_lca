import pandas as pd
from crop_lca.models import load_crop_farm_data
from crop_lca.lca import ClimateChangeTotals
from crop_lca.national_crop_production import NationalCropData


def main():
    # Instantiate ClimateChange Totals Class, passing Ireland as the emissions factor country
    climatechange = ClimateChangeTotals("ireland")

    # Create a dictionary to store results
    index = 2020
    crop_emissions_dict = climatechange.create_emissions_dictionary([index])

    # Create some data to generate results
    data = NationalCropData.gen_national_crop_production_dataframe(index)
    
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

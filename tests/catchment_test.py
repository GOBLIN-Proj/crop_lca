import pandas as pd
from crop_lca.geo_crop_lca.catchment_crop_production import CatchmentCropData
from crop_lca.geo_crop_lca.catchment_crop_generator import CatchmentCropGenerator


def main():

    # Create a dictionary to store results
    index = 2020
    ef_country = "ireland"

    # Create some data to generate results
    data = CatchmentCropData.gen_catchment_crop_production_dataframe(ef_country, "blackwater", index)

    print(data)

    # Create a generator object
    generator = CatchmentCropGenerator("ireland","blackwater")

    # Generate some results
    results = generator.gen_catchment_crop_dataframe()

    print(results)
    

    scenarios = list(range(3))

    calibration_year = 2020
    target_year = 2050 

    df = None 
    
    for sc in scenarios:
        if sc > 0:
            df = CatchmentCropData.gen_scenario_crop_production_dataframe(ef_country, "blackwater", calibration_year, target_year, sc, df)
        else:
            df = CatchmentCropData.gen_scenario_crop_production_dataframe(ef_country, "blackwater",calibration_year, target_year, sc)
   
    print(df)
    
    inputs = CatchmentCropData.gen_farm_data(df, pd.DataFrame({"Urea proportion":[0.2,0.2,0.3], "Urea abated proportion": [0.1,0,0]}), 0.2, 0)

    print(inputs)
if __name__ == "__main__":
    main()

from crop_lca.national_crop_production import NationalCropData
import pandas as pd

def main():
    scenarios = list(range(3))

    print(scenarios)

    calibration_year = 2020
    target_year = 2050 

    for sc in scenarios:
        if sc > 0:
            df = NationalCropData.gen_scenario_crop_production_dataframe(calibration_year, target_year, sc, df)
        else:
            df = NationalCropData.gen_scenario_crop_production_dataframe(calibration_year, target_year, sc)
    data = {"Scenarios":[0,1,2],
            "Urea proportion":[0.2,0.2,0.3],
            "Urea abated proportion": [0.1,0,0]}
    
    fert = pd.DataFrame(data)

    farm_data = NationalCropData.gen_farm_data(df, fert, 0.2, 0)

    print(farm_data)
    print(df)

if __name__ == "__main__":
    main()
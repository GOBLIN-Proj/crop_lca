from crop_lca.national_crop_production import NationalCropData


def main():
    scenarios = list(range(10))

    print(scenarios)

    calibration_year = 2020
    target_year = 2050 

    for sc in scenarios:
        if sc > 0:
            df = NationalCropData.gen_scenario_crop_production_dataframe(calibration_year, target_year, sc, df)
        else:
            df = NationalCropData.gen_scenario_crop_production_dataframe(calibration_year, target_year, sc)

    farm_data = NationalCropData.gen_farm_data(df, 0.2, 0)

    print(farm_data)

if __name__ == "__main__":
    main()
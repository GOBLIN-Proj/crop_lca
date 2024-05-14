import pandas as pd
from crop_lca.geo_crop_lca.catchment_crop_production import CatchmentCropData
from crop_lca.geo_crop_lca.catchment_crop_generator import CatchmentCropGenerator


def main():

    names_file = "./data/geo_data/catchment_names.csv"

    catchment_names = pd.read_csv(names_file)
    # Create a dictionary to store results
    index = 2020
    ef_country = "ireland"

    for name in catchment_names["Catchment"]:

        print(name)
        # Create some data to generate results
        data = CatchmentCropData.gen_catchment_crop_production_dataframe(ef_country, name, index)

        print(data)
        print("#"*50)

        # Create a generator object

        generator = CatchmentCropGenerator("ireland","blackwater")

        # Generate some results
        results = generator.gen_catchment_crop_dataframe()

        print(results)
        print("@"*50)


if __name__ == "__main__":
    main()

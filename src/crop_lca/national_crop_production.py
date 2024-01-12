from crop_lca.data_loader import Loader
import pandas as pd 

class NationalCropData:

    @classmethod
    def gen_national_crop_production_dataframe(cls, year):

        loader_class = Loader()

        cso_crops = loader_class.get_national_crop_production()

        cols = ['ef_country','farm_id','year', 'crop_type','kg_dm_per_ha','area']

        national_crop_df = pd.DataFrame(columns=cols)
        
        
        index = 0 
        for crop in cso_crops.crop_type.unique():
            mask = ((cso_crops["Year"]== year) & (cso_crops["crop_type"]==crop))
            
            national_crop_df.loc[index, "ef_country"] = "ireland"
            national_crop_df.loc[index, "farm_id"] = year
            national_crop_df.loc[index, "year"] = year
            national_crop_df.loc[index, "crop_type"] = crop
            national_crop_df.loc[index, "kg_dm_per_ha"]  = cso_crops.loc[mask, "yield_t_per_ha"].item()
            national_crop_df.loc[index, "area"]  = cso_crops.loc[mask, "Hectares_000"].item()

            index += 1

        return national_crop_df
    

    @classmethod
    def gen_scenario_crop_production_dataframe(cls, calibration_year, target_year, scenario= None, crop_dataframe=None):

        loader_class = Loader()

        cso_crops = loader_class.get_national_crop_production()

        if crop_dataframe is None:
            national_crop_df = NationalCropData.gen_national_crop_production_dataframe(calibration_year)
        else:
            national_crop_df = crop_dataframe
        
        scenario_crop_dataframe = pd.DataFrame()

        index = 0 
        for crop in cso_crops.crop_type.unique():
            mask = ((cso_crops["Year"]== calibration_year) & (cso_crops["crop_type"]==crop))
            
            scenario_crop_dataframe.loc[index, "ef_country"] = "ireland"
            scenario_crop_dataframe.loc[index, "farm_id"] = scenario
            scenario_crop_dataframe.loc[index, "year"] = target_year
            scenario_crop_dataframe.loc[index, "crop_type"] = crop
            scenario_crop_dataframe.loc[index, "kg_dm_per_ha"]  = cso_crops.loc[mask, "yield_t_per_ha"].item()
            scenario_crop_dataframe.loc[index, "area"]  = cso_crops.loc[mask, "Hectares_000"].item()

            index += 1


        return pd.concat([national_crop_df, scenario_crop_dataframe], ignore_index=True) 

    @classmethod
    def gen_farm_data(cls, crop_dataframe, urea_proportion, default_urea, default_urea_abated):

        loader_class = Loader()

        application_rate = loader_class.get_fertiliser()


        cols = [
            "ef_country",
            "farm_id",
            "total_urea",
            "total_urea_abated",
            "total_n_fert",
            "total_p_fert",
            "total_k_fert",
        ]

        farm_data = pd.DataFrame(columns=cols)

        
        for sc in crop_dataframe.farm_id.unique():
            farm_data.at[sc, "ef_country"] = "ireland"
            farm_data.at[sc, "farm_id"] = sc

            farm_data.at[sc, "total_urea"] = 0
            farm_data.at[sc, "total_urea_abated"] = 0
            farm_data.at[sc, "total_n_fert"] = 0
            farm_data.at[sc, "total_p_fert"] = 0
            farm_data.at[sc, "total_k_fert"] = 0

            for crop in crop_dataframe.crop_type.unique():

                try:
                    print(f"sc: {sc}, urea_proportion: {urea_proportion.loc[sc, 'Urea proportion']}")
                    urea_value = urea_proportion.loc[sc, "Urea proportion"].item()

                    urea_abated_value = urea_proportion.loc[sc, "Urea abated proportion"].item()
                
                except KeyError:
                    urea_value = default_urea
                    urea_abated_value = default_urea_abated


                mask = ((crop_dataframe["farm_id"]== sc) & (crop_dataframe["crop_type"]==crop))

                farm_data.at[sc, "total_urea"] += crop_dataframe.loc[mask, "area"].item() *(application_rate.get_fert_kg_n_per_ha(crop)
                        * urea_value)

                farm_data.at[sc, "total_urea_abated"] += crop_dataframe.loc[mask, "area"].item() * (crop_dataframe.loc[mask, "area"].item() * (application_rate.get_fert_kg_n_per_ha(crop)
                        * urea_value * urea_abated_value))

                farm_data.at[sc, "total_n_fert"] += crop_dataframe.loc[mask, "area"].item() *(application_rate.get_fert_kg_n_per_ha(crop)
                        * (1 -urea_value))
                
                farm_data.at[sc, "total_p_fert"] += crop_dataframe.loc[mask, "area"].item() * application_rate.get_fert_kg_p_per_ha(crop)
                farm_data.at[sc, "total_k_fert"] += crop_dataframe.loc[mask, "area"].item() * application_rate.get_fert_kg_k_per_ha(crop)

        return farm_data


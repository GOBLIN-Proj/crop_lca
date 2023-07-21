from crop_lca.data_loader import Loader
import pandas as pd 

class NationalCropData:

    @classmethod
    def gen_national_crop_production_dataframe(cls, year):

        loader_class = Loader()

        cso_crops = loader_class.get_national_crop_production()

        print(cso_crops)

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
            national_crop_df.loc[index, "area"]  = cso_crops.loc[mask, "total_prod_000"].item()

            index += 1

        return national_crop_df
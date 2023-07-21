
"""
    Container classes for data loaded from files
"""

class DynamicData(object):
    def __init__(self, data, defaults={}):

        # Set the defaults first
        for variable, value in defaults.items():
            setattr(self, variable, value)

        # Overwrite the defaults with the real values
        for variable, value in data.items():
            setattr(self, variable, value)


class CropCategory(DynamicData):
    def __init__(self, data):

        defaults = {"kg_dm_per_ha": 0.0, "area": 0.0}

        super(CropCategory, self).__init__(data, defaults)


class CropCollection(DynamicData):
    def __init__(self, data):

        super(CropCollection, self).__init__(data)


class Farm(DynamicData):
    def __init__(self, data):#, crop_collections):

        #self.crops = crop_collections.get(data.get("farm_id"))

        super(Farm, self).__init__(data)


########################################################################################
# Crop Chars class
########################################################################################
class CropChars(object):
    def __init__(self, data):

        self.data_frame = data

        self.crop_char = {}

        for _, row in self.data_frame.iterrows():

            crop_type = row.get("crop_type".lower())
            crop_dry_matter = row.get("crop_dry_matter")
            crop_below_ground_ratio_to_above_ground_biomass = row.get(
                "crop_below_ground_ratio_to_above_ground_biomass"
            )
            crop_above_ground_residue_dry_matter_to_harvested_yield = row.get(
                "crop_above_ground_residue_dry_matter_to_harvested_yield"
            )
            crop_n_content_below_ground = row.get("crop_n_content_below_ground")
            crop_n_content_of_above_ground_residues = row.get(
                "crop_n_content_of_above_ground_residues"
            )
            crop_slope = row.get("crop_slope")
            crop_intercept = row.get("crop_intercept")

            self.crop_char[crop_type] = {
                "crop_dry_matter": crop_dry_matter,
                "crop_below_ground_ratio_to_above_ground_biomass": crop_below_ground_ratio_to_above_ground_biomass,
                "crop_above_ground_residue_dry_matter_to_harvested_yield": crop_above_ground_residue_dry_matter_to_harvested_yield,
                "crop_n_content_below_ground": crop_n_content_below_ground,
                "crop_n_content_of_above_ground_residues": crop_n_content_of_above_ground_residues,
                "crop_slope": crop_slope,
                "crop_intercept": crop_intercept,
            }

    def get_crop_dry_matter(self, crop_char):
        return self.crop_char.get(crop_char).get("crop_dry_matter")

    def get_crop_below_ground_ratio_to_above_ground_biomass(self, crop_char):
        return self.crop_char.get(crop_char).get(
            "crop_below_ground_ratio_to_above_ground_biomass"
        )

    def get_crop_above_ground_residue_dry_matter_to_harvested_yield(self, crop_char):
        return self.crop_char.get(crop_char).get(
            "crop_above_ground_residue_dry_matter_to_harvested_yield"
        )

    def get_crop_n_content_below_ground(self, crop_char):
        return self.crop_char.get(crop_char).get("crop_n_content_below_ground")

    def get_crop_n_content_of_above_ground_residues(self, crop_char):
        return self.crop_char.get(crop_char).get(
            "crop_n_content_of_above_ground_residues"
        )

    def get_crop_slope(self, crop_char):
        return self.crop_char.get(crop_char).get("crop_slope")

    def get_crop_intercept(self, crop_char):
        return self.crop_char.get(crop_char).get("crop_intercept")

    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False

######################################################################################
# Emissions Factors Data
######################################################################################
class Emissions_Factors(object):
    def __init__(self, data):

        self.data_frame = data

        self.emissions_factors = {}

        for _, row in self.data_frame.iterrows():

            ef_emissions_factor_1_ipcc_2019 = row.get("ef_emissions_factor_1_ipcc_2019")
            ef_urea = row.get("ef_urea")
            ef_urea_and_nbpt = row.get("ef_urea_and_nbpt")
            ef_fracGASF_urea_fertilisers_to_nh3_and_nox = row.get(
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox"
            )
            ef_fracGASF_urea_and_nbpt_to_nh3_and_nox = row.get(
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox"
            )
            ef_frac_leach_runoff = row.get("ef_frac_leach_runoff")
            ef_ammonium_nitrate = row.get("ef_ammonium_nitrate")
            ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox = row.get(
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
            )
            ef_indirect_n2o_atmospheric_deposition_to_soils_and_water = row.get(
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
            )
            ef_indirect_n2o_from_leaching_and_runoff = row.get(
                "ef_indirect_n2o_from_leaching_and_runoff"
            )
            ef_grassland_dm_t = row.get("ef_grassland_dm_t")
            ef_dm_carbon_stock_crops = row.get("ef_dm_carbon_stock_crops")
            ef_Frac_P_Leach = row.get("ef_Frac_P_Leach")

            self.emissions_factors= {
                "ef_emissions_factor_1_ipcc_2019": ef_emissions_factor_1_ipcc_2019,
                "ef_urea": ef_urea,
                "ef_urea_and_nbpt": ef_urea_and_nbpt,
                "ef_fracGASF_urea_fertilisers_to_nh3_and_nox": ef_fracGASF_urea_fertilisers_to_nh3_and_nox,
                "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox": ef_fracGASF_urea_and_nbpt_to_nh3_and_nox,
                "ef_frac_leach_runoff": ef_frac_leach_runoff,
                "ef_ammonium_nitrate": ef_ammonium_nitrate,
                "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox": ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox,
                "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water": ef_indirect_n2o_atmospheric_deposition_to_soils_and_water,
                "ef_indirect_n2o_from_leaching_and_runoff": ef_indirect_n2o_from_leaching_and_runoff,
                "ef_grassland_dm_t": ef_grassland_dm_t,
                "ef_dm_carbon_stock_crops": ef_dm_carbon_stock_crops,
                "ef_Frac_P_Leach": ef_Frac_P_Leach,
            }

    def get_ef_emissions_factor_1_ipcc_2019(self):
        return self.emissions_factors.get(
            "ef_emissions_factor_1_ipcc_2019"
        )

    def get_ef_urea(self):
        return self.emissions_factors.get("ef_urea")

    def get_ef_urea_and_nbpt(self):
        return self.emissions_factors.get("ef_urea_and_nbpt")

    def get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox(self):
        return self.emissions_factors.get(
            "ef_fracGASF_urea_fertilisers_to_nh3_and_nox"
        )

    def get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox(self):
        return self.emissions_factors.get(
            "ef_fracGASF_urea_and_nbpt_to_nh3_and_nox"
        )

    def get_ef_frac_leach_runoff(self):
        return self.emissions_factors.get("ef_frac_leach_runoff")

    def get_ef_ammonium_nitrate(self):
        return self.emissions_factors.get("ef_ammonium_nitrate")

    def get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox(self):
        return self.emissions_factors.get(
            "ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox"
        )

    def get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
        self
    ):
        return self.emissions_factors.get(
            "ef_indirect_n2o_atmospheric_deposition_to_soils_and_water"
        )

    def get_ef_indirect_n2o_from_leaching_and_runoff(self):
        return self.emissions_factors.get(
            "ef_indirect_n2o_from_leaching_and_runoff"
        )

    def get_ef_grassland_dm_t(self):
        return self.emissions_factors.get("ef_grassland_dm_t")

    def get_ef_dm_carbon_stock_crops(self):
        return self.emissions_factors.get(
            "ef_dm_carbon_stock_crops"
        )

    def get_ef_Frac_P_Leach(self):
        return self.emissions_factors.get("ef_Frac_P_Leach")


    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False

########################################################################################
# Upstream class
########################################################################################
class Upstream(object):
    def __init__(self, data):

        self.data_frame = data

        self.upstream = {}

        for _, row in self.data_frame.iterrows():

            upstream_type = row.get("upstream_type".lower())
            upstream_fu = row.get("upstream_fu")
            upstream_kg_co2e = row.get("upstream_kg_co2e")
            upstream_kg_po4e = row.get("upstream_kg_po4e")
            upstream_kg_so2e = row.get("upstream_kg_so2e")
            upstream_mje = row.get("upstream_mje")
            upstream_kg_sbe = row.get("upstream_kg_sbe")

            self.upstream[upstream_type] = {
                "upstream_fu": upstream_fu,
                "upstream_kg_co2e": upstream_kg_co2e,
                "upstream_kg_po4e": upstream_kg_po4e,
                "upstream_kg_so2e": upstream_kg_so2e,
                "upstream_mje": upstream_mje,
                "upstream_kg_sbe": upstream_kg_sbe,
            }

    def get_upstream_fu(self, upstream_type):
        return self.upstream.get(upstream_type).get("upstream_fu")

    def get_upstream_kg_co2e(self, upstream_type):
        return self.upstream.get(upstream_type).get("upstream_kg_co2e")

    def get_upstream_kg_po4e(self, upstream_type):
        return self.upstream.get(upstream_type).get("upstream_kg_po4e")

    def get_upstream_kg_so2e(self, upstream_type):
        return self.upstream.get(upstream_type).get("upstream_kg_so2e")

    def get_upstream_mje(self, upstream_type):
        return self.upstream.get(upstream_type).get("upstream_mje")

    def get_upstream_kg_sbe(self, upstream_type):
        return self.upstream.get(upstream_type).get("upstream_kg_sbe")

    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False
        
#############################################################################################
# Fertiliser class
########################################################################################
class Fertiliser(object):
    def __init__(self, data):

        self.data_frame = data

        self.fertiliser = {}

        for _, row in self.data_frame.iterrows():

            fert_crop_type = row.get("fert_crop_type".lower())
            fert_kg_n_per_ha = row.get("fert_kg_n_per_ha")
            fert_kg_p_per_ha = row.get("fert_kg_p_per_ha")
            fert_kg_k_per_ha = row.get("fert_kg_k_per_ha")

            self.fertiliser[fert_crop_type] = {
                "fert_kg_n_per_ha": fert_kg_n_per_ha,
                "fert_kg_p_per_ha": fert_kg_p_per_ha,
                "fert_kg_k_per_ha": fert_kg_k_per_ha,
            }

    def get_fert_kg_n_per_ha(self, fert_crop_type):
        return self.fertiliser.get(fert_crop_type).get("fert_kg_n_per_ha")

    def get_fert_kg_p_per_ha(self, fert_crop_type):
        return self.fertiliser.get(fert_crop_type).get("fert_kg_p_per_ha")

    def get_fert_kg_k_per_ha(self, fert_crop_type):
        return self.fertiliser.get(fert_crop_type).get("fert_kg_k_per_ha")

    def is_loaded(self):
        if self.data_frame is not None:
            return True
        else:
            return False
        
################################################################################################
# Data Loading
################################################################################################


def load_crop_farm_data(crop_type_dataframe):

    # 1. Load each animal category into an object

    categories = []

    for _, row in crop_type_dataframe.iterrows():

        data = dict([(x, row.get(x)) for x in row.keys()])
        categories.append(CropCategory(data))

    # 2. Aggregate the animal categories into collection based on the farm ID

    collections = {}

    for category in categories:

        farm_id = category.farm_id

        crop_type = category.crop_type

        if farm_id not in collections:
            collections[farm_id] = {crop_type: category}
        else:
            collections[farm_id][crop_type] = category

    # 3. Convert the raw collection data into animal collection objects

    collection_objects = {}

    for farm_id, raw_data in collections.items():
        collection_objects[farm_id] = {"crop_group":CropCollection(raw_data)}

    return collection_objects


def load_farm_data(farm_data_frame):
    subset = [
        "diesel_kg",
        "elec_kwh",
    ]
    farm_data_frame.drop_duplicates(subset=subset, keep="first", inplace=True)

    scenario_list = []
    keys = []
    for _, row in farm_data_frame.iterrows():
        data = dict([(x, row.get(x)) for x in row.keys()])
        scenario_list.append(Farm(data))
        #keys.append(row.get("farm_id"))

    #collections ={}

    #for _, sc in scenario_list:
        #collections[sc] = scenario_list[sc]

    #return dict(enumerate(scenario_list))
    return dict([(x.farm_id, x) for x in scenario_list])
####################################################################################################
# Load Additional Databases
####################################################################################################


def load_crop_chars_data():
    return CropChars()


def load_emissions_factors_data(ef_country):
    return Emissions_Factors(ef_country)


def load_upstream_data():
    return Upstream()


def load_fertiliser_data():
    return Fertiliser()



def print_crop_data(data):
    for _, key in enumerate(data):
        for crops in data[key].keys():
            for crop in data[key].__getitem__(crops).__dict__.keys():
                for attribute in data[key].__getitem__(crops).__getattribute__(crop).__dict__.keys():
                    print(
                        f"{crop}: {attribute} = {data[key].__getitem__(crops).__getattribute__(crop).__getattribute__(attribute)}"
                    )


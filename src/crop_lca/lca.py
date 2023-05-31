# IMPORTS
import numpy as np
import pandas as pd

from crop_lca.data_loader import Loader
import copy



# CO2 from Crop Biomass

class Conversion:
    def __init__(self, ef_country) -> None:
        self.loader_class = Loader(ef_country)

    def co2_form_grassland_to_crop(self, data):

        """
        returns the carbon from transition from grass to crop
        """

        grass = self.loader_class.emissions_factors.get_ef_grassland_dm_t()

        carbon_fraction = 0.5

        crop_dm = self.loader_class.emissions_factors.get_ef_dm_carbon_stock_crops()

        return data.temp_grass.area * ((0 - grass * carbon_fraction) + crop_dm)


######################################################################################################################

# Direct N2O Emissions from crop Residues
class Residues:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)

    def n_from_crop_residue_direct(self, data):
        """

        EQUATION 11.6 (UPDATED) N FROM CROP RESIDUES AND FORAGE/PASTURE RENEWAL (TIER 1) (2019 IPCC)

        Fcr = annual amount of N in crop residues (above and below ground), including N-fixing crops,
        and from forage/pasture renewal, returned to soils annually, kg N yr-1

        AGR = annual total amount of above-ground crop residue for crop T, kg d.m. yr-1.

        NAG = N content of above-ground residues for crop T, kg N (kg d.m.) -1

        FracRemove= fraction of above-ground residues of crop T removed annually for purposes such as feed, bedding and construction, dimensionless. Survey of experts in country is required to obtain
        data. If data for FracRemove are not available, assume no removal

        BGR = annual total amount of belowground crop residue for crop T, kg d.m. yr-1

        Crop_t = harvested annual dry matter yield for crop T, kg d.m. ha-1

        AG_dm = Above-ground residue dry matter for crop T, kg d.m. ha-1

        Rag = ratio of above-ground residue dry matter to harvested yield for crop T (Crop(T)), kg d.m. ha-
        1 (kg d.m. ha-1)-1, (Table 11.1a)

        RS = ratio of below-ground root biomass to above-ground shoot biomass for crop T, kg d.m.ha-1
        (kg d.m. ha-1)-1, (Table 11.1a)

        FracRenew = = fraction of total area under crop T that is renewed annually 15, dimensionless. For countries
        where pastures are renewed on average every X years, FracRenew = 1/X. For annual crops
        FracRenew = 1

        """

        dry_matter_fraction = {
            "grains": self.loader_class.crop_chars.get_crop_dry_matter("grains"),
            "crops": self.loader_class.crop_chars.get_crop_dry_matter("crops"),
            "maize": self.loader_class.crop_chars.get_crop_dry_matter("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_dry_matter("winter_wheat"),
            "spring_wheat": self.loader_class.crop_chars.get_crop_dry_matter("spring_wheat"),
            "oats": self.loader_class.crop_chars.get_crop_dry_matter("oats"),
            "barley": self.loader_class.crop_chars.get_crop_dry_matter("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_dry_matter("beans_pulses"),
            "potatoes": self.loader_class.crop_chars.get_crop_dry_matter("potatoes_tubers"),
            "turnips": self.loader_class.crop_chars.get_crop_dry_matter("potatoes_tubers"),
            "sugar_beat": self.loader_class.crop_chars.get_crop_dry_matter("potatoes_tubers"),
            "fodder_beat": self.loader_class.crop_chars.get_crop_dry_matter("potatoes_tubers"),
            "rye": self.loader_class.crop_chars.get_crop_dry_matter("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_dry_matter("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_dry_matter("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_dry_matter("non_legume_hay"),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_dry_matter("n_fixing_forage"),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_dry_matter("perennial_grasses"),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_dry_matter("grass_clover_mix"),
        }

        Rag = {
            "grains": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "grains"
            ),
            "crops": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "crops"
            ),
            "maize": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "maize"
            ),
            "winter_wheat": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "winter_wheat"
            ),
            "spring_wheat": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "spring_wheat"
            ),
            "oats": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "oats"
            ),
            "barley": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "barley"
            ),
            "beans_peas": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "beans_pulses"
            ),
            "potatoes": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "potatoes_tubers"
            ),
            "turnips": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "potatoes_tubers"
            ),
            "sugar_beat": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "potatoes_tubers"
            ),
            "fodder_beat": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "potatoes_tubers"
            ),
            "rye": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "rye"
            ),
            "sorghum": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "sorghum"
            ),
            "alfalfa": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "alfalfa"
            ),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "non_legume_hay"
            ),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "n_fixing_forage"
            ),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "perennial_grasses"
            ),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "grass_clover_mix"
            ),
        }

        RS = {
            "grains": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "grains"
            ),
            "crops": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "crops"
            ),
            "maize": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "maize"
            ),
            "winter_wheat": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "winter_wheat"
            ),
            "spring_wheat": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "spring_wheat"
            ),
            "oats": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass("oats"),
            "barley": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "barley"
            ),
            "beans_peas": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "beans_pulses"
            ),
            "potatoes": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "potatoes_tubers"
            ),
            "turnips": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "potatoes_tubers"
            ),
            "sugar_beat": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "potatoes_tubers"
            ),
            "fodder_beat": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "potatoes_tubers"
            ),
            "rye": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "sorghum"
            ),
            "alfalfa": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "alfalfa"
            ),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "non_legume_hay"
            ),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "n_fixing_forage"
            ),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "perennial_grasses"
            ),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
                "grass_clover_mix"
            ),
        }

        crops_n_above = {
            "grains": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("grains"),
            "crops": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("crops"),
            "maize": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "winter_wheat"
            ),
            "spring_wheat": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "spring_wheat"
            ),
            "oats": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("oats"),
            "barley": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "beans_pulses"
            ),
            "potatoes": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "potatoes_tubers"
            ),
            "turnips": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "potatoes_tubers"
            ),
            "sugar_beat": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "potatoes_tubers"
            ),
            "fodder_beat": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "potatoes_tubers"
            ),
            "rye": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "non_legume_hay"
            ),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "n_fixing_forage"
            ),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "perennial_grasses"
            ),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues(
                "grass_clover_mix"
            ),
        }

        crops_n_below = {
            "grains": self.loader_class.crop_chars.get_crop_n_content_below_ground("grains"),
            "crops": self.loader_class.crop_chars.get_crop_n_content_below_ground("crops"),
            "maize": self.loader_class.crop_chars.get_crop_n_content_below_ground("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_n_content_below_ground("winter_wheat"),
            "spring_wheat": self.loader_class.crop_chars.get_crop_n_content_below_ground("spring_wheat"),
            "oats": self.loader_class.crop_chars.get_crop_n_content_below_ground("oats"),
            "barley": self.loader_class.crop_chars.get_crop_n_content_below_ground("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_n_content_below_ground("beans_pulses"),
            "potatoes": self.loader_class.crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
            "turnips": self.loader_class.crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
            "sugar_beat": self.loader_class.crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
            "fodder_beat": self.loader_class.crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
            "rye": self.loader_class.crop_chars.get_crop_n_content_below_ground("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_n_content_below_ground("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_n_content_below_ground("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_n_content_below_ground("non_legume_hay"),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_n_content_below_ground(
                "n_fixing_forage"
            ),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_n_content_below_ground(
                "perennial_grasses"
            ),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_n_content_below_ground(
                "grass_clover_mix"
            ),
        }

        slope = {
            "grains": self.loader_class.crop_chars.get_crop_slope("grains"),
            "crops": self.loader_class.crop_chars.get_crop_slope("crops"),
            "maize": self.loader_class.crop_chars.get_crop_slope("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_slope("winter_wheat"),
            "spring_wheat": self.loader_class.crop_chars.get_crop_slope("spring_wheat"),
            "oats": self.loader_class.crop_chars.get_crop_slope("oats"),
            "barley": self.loader_class.crop_chars.get_crop_slope("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_slope("beans_pulses"),
            "potatoes": self.loader_class.crop_chars.get_crop_slope("potatoes_tubers"),
            "turnips": self.loader_class.crop_chars.get_crop_slope("potatoes_tubers"),
            "sugar_beat": self.loader_class.crop_chars.get_crop_slope("potatoes_tubers"),
            "fodder_beat": self.loader_class.crop_chars.get_crop_slope("potatoes_tubers"),
            "rye": self.loader_class.crop_chars.get_crop_slope("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_slope("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_slope("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_slope("non_legume_hay"),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_slope("n_fixing_forage"),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_slope("perennial_grasses"),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_slope("grass_clover_mix"),
        }

        intercept = {
            "grains": self.loader_class.crop_chars.get_crop_intercept("grains"),
            "crops": self.loader_class.crop_chars.get_crop_intercept("crops"),
            "maize": self.loader_class.crop_chars.get_crop_intercept("maize"),
            "winter_wheat": self.loader_class.crop_chars.get_crop_intercept("winter_wheat"),
            "spring_wheat": self.loader_class.crop_chars.get_crop_intercept("spring_wheat"),
            "oats": self.loader_class.crop_chars.get_crop_intercept("oats"),
            "barley": self.loader_class.crop_chars.get_crop_intercept("barley"),
            "beans_peas": self.loader_class.crop_chars.get_crop_intercept("beans_pulses"),
            "potatoes": self.loader_class.crop_chars.get_crop_intercept("potatoes_tubers"),
            "turnips": self.loader_class.crop_chars.get_crop_intercept("potatoes_tubers"),
            "sugar_beat": self.loader_class.crop_chars.get_crop_intercept("potatoes_tubers"),
            "fodder_beat": self.loader_class.crop_chars.get_crop_intercept("potatoes_tubers"),
            "rye": self.loader_class.crop_chars.get_crop_intercept("rye"),
            "sorghum": self.loader_class.crop_chars.get_crop_intercept("sorghum"),
            "alfalfa": self.loader_class.crop_chars.get_crop_intercept("alfalfa"),
            "non_legume_hay": self.loader_class.crop_chars.get_crop_intercept("non_legume_hay"),
            "n_fixing_forage": self.loader_class.crop_chars.get_crop_intercept("n_fixing_forage"),
            "perennial_grasses": self.loader_class.crop_chars.get_crop_intercept("perennial_grasses"),
            "grass_clover_mix": self.loader_class.crop_chars.get_crop_intercept("grass_clover_mix"),
        }

        test_value = lambda x: True if (x > 0) else False

        Crop_t = dry_matter_fraction.get(data.crop_type)

        Crop_t_output = 0

        if test_value(Crop_t) == True:
            Crop_t_output = Crop_t
        else:
            Crop_t_output = self.loader_class.crop_chars.get_crop_dry_matter("crops")

        AG_dm = Rag.get(data.crop_type)

        AG_dm_output = 0

        if test_value(AG_dm) == True:
            AG_dm_output = Crop_t_output * AG_dm
        else:
            AG_dm_output = (
                Crop_t_output
                * self.loader_class.crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                    "crops"
                )
            )

        ratio_below_ground = RS.get(data.crop_type)

        ratio_below_ground_output = 0

        if test_value(ratio_below_ground) == True:
            ratio_below_ground_output = ratio_below_ground
        else:
            ratio_below_ground_output = (
                self.loader_class.crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass("crops")
            )

        NAG = crops_n_above.get(data.crop_type)

        NAG_output = 0

        if test_value(NAG) == True:
            NAG_output = NAG
        else:
            NAG_output = self.loader_class.crop_chars.get_crop_n_content_of_above_ground_residues("crops")

        NBG = crops_n_below.get(data.crop_type)

        NBG_output = 0

        if test_value(NAG) == True:
            NBG_output = NBG
        else:
            NBG_output = self.loader_class.crop_chars.get_crop_n_content_below_ground("crops")

        FracRemove = 0.95

        FracRenew = 1

        AGR = Crop_t_output

        BGR = (
            (Crop_t_output + AG_dm_output)
            * ratio_below_ground_output
            * data.area
            * FracRenew
        ) * NBG_output

        AGR_total = AGR * NAG_output * (1 - FracRemove)

        Fcr = AGR_total + BGR

        return Fcr





###############################################################################
# Farm & Upstream Emissions
###############################################################################
# Fertiliser Use Calculations

class FertilserUse:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)

    def total_an_fert_use(self, data, urea_proportion):

        """
        Total AN fert use in kg
        """

        crop_names = list(data.__getitem__("crop_group").__dict__.keys())

        total_fert_an = 0

        for crop in crop_names:
            try:
                total_fert_an += self.loader_class.fertiliser.get_fert_kg_n_per_ha(crop) * (
                    data.__getitem__("crop_group").__getattribute__(crop).area * (1 - urea_proportion)
                )

            except AttributeError:

                total_fert_an += self.loader_class.fertiliser.get_fert_kg_n_per_ha("average") * (
                    data.__getitem__("crop_group").__getattribute__(crop).area * (1 - urea_proportion)
                )

        return total_fert_an


    def total_urea_fert_use(self, data, urea_proportion):

        """
        Total Urea fert use in kg
        """
        crop_names = list(data.__getitem__("crop_group").__dict__.keys())

        total_fert_urea = 0

        for crop in crop_names:
            try:
                total_fert_urea += self.loader_class.fertiliser.get_fert_kg_n_per_ha(crop) * (
                    data.__getitem__("crop_group").__getattribute__(crop).area * urea_proportion
                )

            except AttributeError:
                total_fert_urea += self.loader_class.fertiliser.get_fert_kg_n_per_ha("average") * (
                    data.__getitem__("crop_group").__getattribute__(crop).area * urea_proportion
                )

        return total_fert_urea


    def total_p_fert_use(self, data):

        crop_names = list(data.__getitem__("crop_group").__dict__.keys())

        total_fert_p = 0

        for crop in crop_names:
            try:
                total_fert_p += (
                    self.loader_class.fertiliser.get_fert_kg_p_per_ha(crop) * data.__getitem__("crop_group").__getattribute__(crop).area
                )

            except AttributeError:
                total_fert_p += (
                    self.loader_class.fertiliser.get_fert_kg_p_per_ha("average")
                    * data.__getitem__("crop_group").__getattribute__(crop).area
                )

        return total_fert_p


    def total_k_fert_use(self, data):

        crop_names = list(data.__getitem__("crop_group").__dict__.keys())

        total_fert_k = 0

        for crop in crop_names:
            try:
                total_fert_k += (
                    self.loader_class.fertiliser.get_fert_kg_k_per_ha(crop) * data.__getitem__("crop_group").__getattribute__(crop).area
                )

            except AttributeError:
                total_fert_k += (
                    self.loader_class.fertiliser.get_fert_kg_k_per_ha("average")
                    * data.__getitem__("crop_group").__getattribute__(crop).area
                )

        return total_fert_k


########################################################################################################
# Urea Fertiliser Emissions
########################################################################################################
class FertiliserInputs:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.fertiliser_use_class = FertilserUse(ef_country)


    def urea_N2O_direct(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):

        """
        this function returns the total emissions from urea and abated urea applied to soils

        proporiton of urea abated (urea_abated_factor) is currently set to zero, as there is not parameter for this.
        """

        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        ef_urea = self.loader_class.emissions_factors.get_ef_urea()
        ef_urea_abated = self.loader_class.emissions_factors.get_ef_urea_and_nbpt()

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)


    def urea_NH3(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):

        """
        This function returns  the amount of urea and abated urea volatised.
        Below is the original fraction used in the Costa Rica version, however this seems to be incorrect.
        FRAC=0.02 #FracGASF ammoinium-fertilisers [fraction of synthetic fertiliser N that volatilises as NH3 and NOx under different conditions]

        proporiton of urea abated (urea_abated_factor) is currently set to zero, as there is not parameter for this.

        """
        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        ef_urea = self.loader_class.emissions_factors.get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox(
            
        )
        ef_urea_abated = self.loader_class.emissions_factors.get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox(
            
        )

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)


    def urea_nleach(
        self,
        data,
        urea_proportion,
        urea_abated_proportion
    ):

        """
        This function returns  the amount of urea and abated urea leached from soils.

        Below is the original fraction used in the Costa Rica version, however this seems to be incorrect.
        FRAC=0.02 #FracGASF ammoinium-fertilisers [fraction of synthetic fertiliser N that volatilises as NH3 and NOx under different conditions]

        proporiton of urea abated (urea_abated_factor) is currently set to zero, as there is not parameter for this.

        """
        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        leach = self.loader_class.emissions_factors.get_ef_frac_leach_runoff()

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return (total_urea + total_urea_abated) * leach


    def urea_N2O_indirect(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        this function returns the indirect emissions from urea
        """
        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
                
            )
        )
        indirect_leaching = self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(
            
        )

        return (
            self.urea_NH3(
                data,
                urea_proportion,
                urea_abated_proportion,
            )
            * indirect_atmosphere
        ) + (
            self.urea_nleach(
                data,
                urea_proportion,
                urea_abated_proportion,
            )
            * indirect_leaching
        )


    def urea_P_leach(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        this function returns the idirect emissions from urea
        """

        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return (total_urea + total_urea_abated) * frac_leach


    #########################################################################################################
    # Nitrogen Fertiliser Emissions
    #########################################################################################################
    def n_fertiliser_P_leach(
        self, data, urea_proportion
    ):
        """
        this function returns the idirect emissions from urea
        """
        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)

        return total_n_fert * frac_leach


    def p_fertiliser_P_leach(self, data):
        """
        this function returns the idirect emissions from urea
        """
        frac_leach = float(self.loader_class.emissions_factors.get_ef_Frac_P_Leach())

        total_p_fert = self.fertiliser_use_class.total_p_fert_use(data)

        return total_p_fert * frac_leach


    def n_fertiliser_direct(
        self, data, urea_proportion
    ):

        """
        This function returns total direct emissions from ammonium nitrate application at field level
        """
        ef = self.loader_class.emissions_factors.get_ef_ammonium_nitrate()

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)

        return total_n_fert * ef


    def n_fertiliser_NH3(self, data, urea_proportion):

        """
        This function returns total NH3 emissions from ammonium nitrate application at field level
        """
        ef = self.loader_class.emissions_factors.get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox(
            
        )

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)

        return total_n_fert * ef


    def n_fertiliser_nleach(
        self, data, urea_proportion
    ):
        """
        This function returns total leached emissions from ammonium nitrate application at field level
        """

        leach = self.loader_class.emissions_factors.get_ef_frac_leach_runoff()

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)

        return total_n_fert * leach


    def n_fertiliser_indirect(
        self, data, urea_proportion
    ):

        """
        this function returns the indirect emissions from ammonium nitrate fertiliser
        """

        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
                
            )
        )
        indirect_leaching = self.loader_class.emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(
            
        )

        return (
            self.n_fertiliser_NH3(
                 data, urea_proportion
            )
            * indirect_atmosphere
        ) + (
            self.n_fertiliser_nleach(
                data, urea_proportion
            )
            * indirect_leaching
        )



class Upstream:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.fertiliser_use_class = FertilserUse()


    def fert_upstream_P(self, data, urea_proportion):

        """
        this function returns the upstream emissions from urea and ammonium fertiliser manufature
        """
        AN_fert_PO4 = self.loader_class.upstream.get_upstream_kg_po4e(
            "ammonium_nitrate_fertiliser"
        )  # Ammonium Nitrate Fertiliser
        Urea_fert_PO4 = self.loader_class.upstream.get_upstream_kg_po4e("urea_fert")
        Triple_superphosphate = self.loader_class.upstream.get_upstream_kg_po4e("triple_superphosphate")
        Potassium_chloride = self.loader_class.upstream.get_upstream_kg_po4e("potassium_chloride")

        total_n_fert = self.fertiliser_use_class.total_an_fert_use(data, urea_proportion)
        total_p_fert = self.fertiliser_use_class.total_p_fert_use(data)
        total_k_fert = self.fertiliser_use_class.total_k_fert_use(data)
        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion)

        return (
            (total_n_fert * AN_fert_PO4)
            + (total_urea * Urea_fert_PO4)
            + (total_p_fert * Triple_superphosphate)
            + (total_k_fert * Potassium_chloride)
        )

################################################################################
# Total Global Warming Potential of whole farms
################################################################################
class ClimateChangeTotals:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.residues_class = Residues(ef_country)
        self.fertiliser_emissions_class = FertiliserInputs(ef_country)
        self.fertiliser_use_class = FertilserUse(ef_country)

    def create_emissions_dictionary(self, keys):
        crop_key_list = [
            "crop_residue_direct",
            "N_direct_fertiliser",
            "N_indirect_fertiliser",
            "soils_CO2",
            "soils_N2O",
        ]

        crop_keys_dict = dict.fromkeys(keys)

        crop_emissions_dict = dict.fromkeys(crop_key_list)

        for key in crop_emissions_dict.keys():
            crop_emissions_dict[key] = copy.deepcopy(crop_keys_dict)
            for inner_k in crop_keys_dict.keys():
                crop_emissions_dict[key][inner_k] = 0

        return crop_emissions_dict
    
    #######################################################################################################
    # Total  N from All crops
    #######################################################################################################
    def total_residue_per_crop_direct(self, data):

        mole_weight = 44.0 / 28.0

        EF_1 = self.loader_class.emissions_factors.get_ef_emissions_factor_1_ipcc_2019()

        result = 0
        for crop in data.__getitem__("crop_group").__dict__.keys():
            
            result += (
                self.residues_class.n_from_crop_residue_direct(data.__getitem__("crop_group").__getattribute__(crop)) * EF_1
            ) * data.__getitem__("crop_group").__getattribute__(crop).area

        return result * mole_weight

    # Fertiliser Application Totals for N20 and CO2


    def total_fertiliser_direct(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        This function returns the total direct and indirect emissions from urea and ammonium fertilisers
        """

        result = self.fertiliser_emissions_class.urea_N2O_direct(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_direct(
           data,  urea_proportion
        )

        return result


    def total_fertiliser_indirect(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        This function returns the total direct and indirect emissions from urea and ammonium fertilisers
        """

        result = self.fertiliser_emissions_class.urea_N2O_indirect(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_indirect(data, urea_proportion
        )

        return result
    


    def urea_co2(self, data, urea_proportion, urea_abated_proportion):
        """
        returns the total CO2 from urea application

        proporiton of urea abated (urea_abated_factor) is currently set to zero, as there is not parameter for this.

        """

        urea_abated_factor = urea_abated_proportion

        urea_factor = 1 - urea_abated_proportion

        total_urea = self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_factor

        total_urea_abated = (
            self.fertiliser_use_class.total_urea_fert_use(data, urea_proportion) * urea_abated_factor
        )

        return ((total_urea + total_urea_abated) * 0.2) * (
            44 / 12
        )  # adjusted to the NIR version of this calculation
    

###############################################################################
# Water Quality EP PO4e
###############################################################################

class EutrophicationTotals:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.residues_class = Residues(ef_country)
        self.fertiliser_emissions_class = FertiliserInputs(ef_country)
        self.upstream_class = Upstream(ef_country)

    # SOILS
    def total_soils_NH3_and_LEACH_EP(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):
        """
        Convert N to PO4  = 0.42

        """
        indirect_atmosphere = (
            self.loader_class.emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
            )
        )

        NH3N = self.fertiliser_emissions_class.urea_NH3(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_NH3(
           data, urea_proportion
        )

        LEACH = self.fertiliser_emissions_class.urea_nleach(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_nleach(
            data,urea_proportion
        )

        return (NH3N * indirect_atmosphere) + LEACH * 0.42


    def total_soils_P_LEACH_EP(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):

        PLEACH = (
            self.fertiliser_emissions_class.urea_P_leach(
                data,
                urea_proportion,
                urea_abated_proportion,
            )
            + self.fertiliser_emissions_class.n_fertiliser_P_leach(data, urea_proportion
            )
            + self.fertiliser_emissions_class.p_fertiliser_P_leach(data)
        )

        return PLEACH * 3.06


    def total_soils_EP(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):

        return self.total_soils_NH3_and_LEACH_EP(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.total_soils_P_LEACH_EP(
            data,
            urea_proportion,
            urea_abated_proportion,
        )



    def upstream_EP(self, data, urea_proportion):

        return self.upstream_class.fert_upstream_P( data, urea_proportion)


###############################################################################
# Air Quality
###############################################################################
class AirQualityTotals:
    def __init__(self, ef_country):
        self.loader_class = Loader(ef_country)
        self.fertiliser_emissions_class = FertiliserInputs(ef_country)


# SOILS
    def total_soils_NH3_AQ(
        self,
        data,
        urea_proportion,
        urea_abated_proportion,
    ):

        NH3N = self.fertiliser_emissions_class.urea_NH3(
            data,
            urea_proportion,
            urea_abated_proportion,
        ) + self.fertiliser_emissions_class.n_fertiliser_NH3(data, urea_proportion
        )

        return NH3N

# IMPORTS
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

# import models
###################################################################################################################

# CO2 from Crop Biomass


def co2_form_grassland_to_crop(ef_country, data, emissions_factors):

    """
    returns the co2e from transition from grass to crop
    """

    co2e = 3.62

    grass = emissions_factors.get_ef_grassland_dm_t(ef_country)

    carbon_fraction = 0.5

    crop_dm = emissions_factors.get_ef_dm_carbon_stock_crops(ef_country)

    return data.temp_grass.area * ((0 - grass * carbon_fraction) + crop_dm) * co2e


######################################################################################################################

# Direct N2O Emissions from crop Residues


def n_from_crop_residue_direct(data, crop_chars):
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
        "grains": crop_chars.get_crop_dry_matter("grains"),
        "crops": crop_chars.get_crop_dry_matter("crops"),
        "maize": crop_chars.get_crop_dry_matter("maize"),
        "winter_wheat": crop_chars.get_crop_dry_matter("winter_wheat"),
        "spring_wheat": crop_chars.get_crop_dry_matter("spring_wheat"),
        "oats": crop_chars.get_crop_dry_matter("oats"),
        "barley": crop_chars.get_crop_dry_matter("barley"),
        "beans_peas": crop_chars.get_crop_dry_matter("beans_pulses"),
        "potatoes": crop_chars.get_crop_dry_matter("potatoes_tubers"),
        "turnips": crop_chars.get_crop_dry_matter("potatoes_tubers"),
        "sugar_beat": crop_chars.get_crop_dry_matter("potatoes_tubers"),
        "fodder_beat": crop_chars.get_crop_dry_matter("potatoes_tubers"),
        "rye": crop_chars.get_crop_dry_matter("rye"),
        "sorghum": crop_chars.get_crop_dry_matter("sorghum"),
        "alfalfa": crop_chars.get_crop_dry_matter("alfalfa"),
        "non_legume_hay": crop_chars.get_crop_dry_matter("non_legume_hay"),
        "n_fixing_forage": crop_chars.get_crop_dry_matter("n_fixing_forage"),
        "perennial_grasses": crop_chars.get_crop_dry_matter("perennial_grasses"),
        "grass_clover_mix": crop_chars.get_crop_dry_matter("grass_clover_mix"),
    }

    Rag = {
        "grains": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "grains"
        ),
        "crops": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "crops"
        ),
        "maize": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "maize"
        ),
        "winter_wheat": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "winter_wheat"
        ),
        "spring_wheat": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "spring_wheat"
        ),
        "oats": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "oats"
        ),
        "barley": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "barley"
        ),
        "beans_peas": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "beans_pulses"
        ),
        "potatoes": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "potatoes_tubers"
        ),
        "turnips": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "potatoes_tubers"
        ),
        "sugar_beat": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "potatoes_tubers"
        ),
        "fodder_beat": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "potatoes_tubers"
        ),
        "rye": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "rye"
        ),
        "sorghum": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "sorghum"
        ),
        "alfalfa": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "alfalfa"
        ),
        "non_legume_hay": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "non_legume_hay"
        ),
        "n_fixing_forage": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "n_fixing_forage"
        ),
        "perennial_grasses": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "perennial_grasses"
        ),
        "grass_clover_mix": crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
            "grass_clover_mix"
        ),
    }

    RS = {
        "grains": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "grains"
        ),
        "crops": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "crops"
        ),
        "maize": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "maize"
        ),
        "winter_wheat": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "winter_wheat"
        ),
        "spring_wheat": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "spring_wheat"
        ),
        "oats": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass("oats"),
        "barley": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "barley"
        ),
        "beans_peas": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "beans_pulses"
        ),
        "potatoes": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "potatoes_tubers"
        ),
        "turnips": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "potatoes_tubers"
        ),
        "sugar_beat": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "potatoes_tubers"
        ),
        "fodder_beat": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "potatoes_tubers"
        ),
        "rye": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass("rye"),
        "sorghum": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "sorghum"
        ),
        "alfalfa": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "alfalfa"
        ),
        "non_legume_hay": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "non_legume_hay"
        ),
        "n_fixing_forage": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "n_fixing_forage"
        ),
        "perennial_grasses": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "perennial_grasses"
        ),
        "grass_clover_mix": crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass(
            "grass_clover_mix"
        ),
    }

    crops_n_above = {
        "grains": crop_chars.get_crop_n_content_of_above_ground_residues("grains"),
        "crops": crop_chars.get_crop_n_content_of_above_ground_residues("crops"),
        "maize": crop_chars.get_crop_n_content_of_above_ground_residues("maize"),
        "winter_wheat": crop_chars.get_crop_n_content_of_above_ground_residues(
            "winter_wheat"
        ),
        "spring_wheat": crop_chars.get_crop_n_content_of_above_ground_residues(
            "spring_wheat"
        ),
        "oats": crop_chars.get_crop_n_content_of_above_ground_residues("oats"),
        "barley": crop_chars.get_crop_n_content_of_above_ground_residues("barley"),
        "beans_peas": crop_chars.get_crop_n_content_of_above_ground_residues(
            "beans_pulses"
        ),
        "potatoes": crop_chars.get_crop_n_content_of_above_ground_residues(
            "potatoes_tubers"
        ),
        "turnips": crop_chars.get_crop_n_content_of_above_ground_residues(
            "potatoes_tubers"
        ),
        "sugar_beat": crop_chars.get_crop_n_content_of_above_ground_residues(
            "potatoes_tubers"
        ),
        "fodder_beat": crop_chars.get_crop_n_content_of_above_ground_residues(
            "potatoes_tubers"
        ),
        "rye": crop_chars.get_crop_n_content_of_above_ground_residues("rye"),
        "sorghum": crop_chars.get_crop_n_content_of_above_ground_residues("sorghum"),
        "alfalfa": crop_chars.get_crop_n_content_of_above_ground_residues("alfalfa"),
        "non_legume_hay": crop_chars.get_crop_n_content_of_above_ground_residues(
            "non_legume_hay"
        ),
        "n_fixing_forage": crop_chars.get_crop_n_content_of_above_ground_residues(
            "n_fixing_forage"
        ),
        "perennial_grasses": crop_chars.get_crop_n_content_of_above_ground_residues(
            "perennial_grasses"
        ),
        "grass_clover_mix": crop_chars.get_crop_n_content_of_above_ground_residues(
            "grass_clover_mix"
        ),
    }

    crops_n_below = {
        "grains": crop_chars.get_crop_n_content_below_ground("grains"),
        "crops": crop_chars.get_crop_n_content_below_ground("crops"),
        "maize": crop_chars.get_crop_n_content_below_ground("maize"),
        "winter_wheat": crop_chars.get_crop_n_content_below_ground("winter_wheat"),
        "spring_wheat": crop_chars.get_crop_n_content_below_ground("spring_wheat"),
        "oats": crop_chars.get_crop_n_content_below_ground("oats"),
        "barley": crop_chars.get_crop_n_content_below_ground("barley"),
        "beans_peas": crop_chars.get_crop_n_content_below_ground("beans_pulses"),
        "potatoes": crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
        "turnips": crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
        "sugar_beat": crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
        "fodder_beat": crop_chars.get_crop_n_content_below_ground("potatoes_tubers"),
        "rye": crop_chars.get_crop_n_content_below_ground("rye"),
        "sorghum": crop_chars.get_crop_n_content_below_ground("sorghum"),
        "alfalfa": crop_chars.get_crop_n_content_below_ground("alfalfa"),
        "non_legume_hay": crop_chars.get_crop_n_content_below_ground("non_legume_hay"),
        "n_fixing_forage": crop_chars.get_crop_n_content_below_ground(
            "n_fixing_forage"
        ),
        "perennial_grasses": crop_chars.get_crop_n_content_below_ground(
            "perennial_grasses"
        ),
        "grass_clover_mix": crop_chars.get_crop_n_content_below_ground(
            "grass_clover_mix"
        ),
    }

    slope = {
        "grains": crop_chars.get_crop_slope("grains"),
        "crops": crop_chars.get_crop_slope("crops"),
        "maize": crop_chars.get_crop_slope("maize"),
        "winter_wheat": crop_chars.get_crop_slope("winter_wheat"),
        "spring_wheat": crop_chars.get_crop_slope("spring_wheat"),
        "oats": crop_chars.get_crop_slope("oats"),
        "barley": crop_chars.get_crop_slope("barley"),
        "beans_peas": crop_chars.get_crop_slope("beans_pulses"),
        "potatoes": crop_chars.get_crop_slope("potatoes_tubers"),
        "turnips": crop_chars.get_crop_slope("potatoes_tubers"),
        "sugar_beat": crop_chars.get_crop_slope("potatoes_tubers"),
        "fodder_beat": crop_chars.get_crop_slope("potatoes_tubers"),
        "rye": crop_chars.get_crop_slope("rye"),
        "sorghum": crop_chars.get_crop_slope("sorghum"),
        "alfalfa": crop_chars.get_crop_slope("alfalfa"),
        "non_legume_hay": crop_chars.get_crop_slope("non_legume_hay"),
        "n_fixing_forage": crop_chars.get_crop_slope("n_fixing_forage"),
        "perennial_grasses": crop_chars.get_crop_slope("perennial_grasses"),
        "grass_clover_mix": crop_chars.get_crop_slope("grass_clover_mix"),
    }

    intercept = {
        "grains": crop_chars.get_crop_intercept("grains"),
        "crops": crop_chars.get_crop_intercept("crops"),
        "maize": crop_chars.get_crop_intercept("maize"),
        "winter_wheat": crop_chars.get_crop_intercept("winter_wheat"),
        "spring_wheat": crop_chars.get_crop_intercept("spring_wheat"),
        "oats": crop_chars.get_crop_intercept("oats"),
        "barley": crop_chars.get_crop_intercept("barley"),
        "beans_peas": crop_chars.get_crop_intercept("beans_pulses"),
        "potatoes": crop_chars.get_crop_intercept("potatoes_tubers"),
        "turnips": crop_chars.get_crop_intercept("potatoes_tubers"),
        "sugar_beat": crop_chars.get_crop_intercept("potatoes_tubers"),
        "fodder_beat": crop_chars.get_crop_intercept("potatoes_tubers"),
        "rye": crop_chars.get_crop_intercept("rye"),
        "sorghum": crop_chars.get_crop_intercept("sorghum"),
        "alfalfa": crop_chars.get_crop_intercept("alfalfa"),
        "non_legume_hay": crop_chars.get_crop_intercept("non_legume_hay"),
        "n_fixing_forage": crop_chars.get_crop_intercept("n_fixing_forage"),
        "perennial_grasses": crop_chars.get_crop_intercept("perennial_grasses"),
        "grass_clover_mix": crop_chars.get_crop_intercept("grass_clover_mix"),
    }

    test_value = lambda x: True if (x > 0) else False

    Crop_t = dry_matter_fraction.get(data.crop_type)

    Crop_t_output = 0

    if test_value(Crop_t) == True:
        Crop_t_output = Crop_t
    else:
        Crop_t_output = crop_chars.get_crop_dry_matter("crops")

    AG_dm = Rag.get(data.crop_type)

    AG_dm_output = 0

    if test_value(AG_dm) == True:
        AG_dm_output = Crop_t_output * AG_dm
    else:
        AG_dm_output = (
            Crop_t_output
            * crop_chars.get_crop_above_ground_residue_dry_matter_to_harvested_yield(
                "crops"
            )
        )

    ratio_below_ground = RS.get(data.crop_type)

    ratio_below_ground_output = 0

    if test_value(ratio_below_ground) == True:
        ratio_below_ground_output = ratio_below_ground
    else:
        ratio_below_ground_output = (
            crop_chars.get_crop_below_ground_ratio_to_above_ground_biomass("crops")
        )

    NAG = crops_n_above.get(data.crop_type)

    NAG_output = 0

    if test_value(NAG) == True:
        NAG_output = NAG
    else:
        NAG_output = crop_chars.get_crop_n_content_of_above_ground_residues("crops")

    NBG = crops_n_below.get(data.crop_type)

    NBG_output = 0

    if test_value(NAG) == True:
        NBG_output = NBG
    else:
        NBG_output = crop_chars.get_crop_n_content_below_ground("crops")

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


#######################################################################################################
# Total  N from All crops
#######################################################################################################
def total_residue_per_crop_direct(ef_country, data, crop_chars, emissions_factors):

    mole_weight = 44.0 / 28.0

    EF_1 = emissions_factors.get_ef_emissions_factor_1_ipcc_2019(ef_country)

    result = 0
    for crop in data.__dict__.keys():
        result += (
            n_from_crop_residue_direct(data.__getattribute__(crop), crop_chars) * EF_1
        ) * data.__getattribute__(crop).area

    return result * mole_weight


def total_residue_per_crop_direct_co2e(ef_country, data, crop_chars, emissions_factors):

    CO2E_converstion = (44.0 / 28.0) * 298

    EF_1 = emissions_factors.get_ef_emissions_factor_1_ipcc_2019(ef_country)

    result = 0
    for crop in data.__dict__.keys():
        result += (
            n_from_crop_residue_direct(data.__getattribute__(crop), crop_chars) * EF_1
        ) * data.__getattribute__(crop).area

    return result * CO2E_converstion


def total_residues_gwp(ef_country, data, crop_chars, emissions_factors):

    CO2E_converstion = (44.0 / 28.0) * 298

    EF_1 = emissions_factors.get_ef_emissions_factor_1_ipcc_2019(ef_country)

    result = (
        n_from_crop_residue_direct(data.maize, crop_chars)
        + n_from_crop_residue_direct(data.winter_wheat, crop_chars)
        + n_from_crop_residue_direct(data.spring_wheat, crop_chars)
        + n_from_crop_residue_direct(data.oats, crop_chars)
        + n_from_crop_residue_direct(data.barley, crop_chars)
        + n_from_crop_residue_direct(data.beans_peas, crop_chars)
        + n_from_crop_residue_direct(data.potatoes, crop_chars)
        + n_from_crop_residue_direct(data.turnips, crop_chars)
        + n_from_crop_residue_direct(data.sugar_beat, crop_chars)
        + n_from_crop_residue_direct(data.fodder_beat, crop_chars)
    ) * EF_1

    return result * CO2E_converstion


###############################################################################
# Farm & Upstream Emissions
###############################################################################
# Fertiliser Use Calculations


def total_an_fert_use(data, fertiliser, urea_proportion):

    """
    Total AN fert use in kg
    """

    crop_names = list(data.__dict__.keys())

    total_fert_an = 0

    for name in crop_names:
        try:
            total_fert_an += fertiliser.get_fert_kg_n_per_ha(name) * (
                data.__getattribute__(name).area * (1 - urea_proportion)
            )

        except AttributeError:

            total_fert_an += fertiliser.get_fert_kg_n_per_ha("average") * (
                data.__getattribute__(name).area * (1 - urea_proportion)
            )

    return total_fert_an


def total_urea_fert_use(data, fertiliser, urea_proportion):

    """
    Total Urea fert use in kg
    """
    crop_names = list(data.__dict__.keys())

    total_fert_urea = 0

    for name in crop_names:
        try:
            total_fert_urea += fertiliser.get_fert_kg_n_per_ha(name) * (
                data.__getattribute__(name).area * urea_proportion
            )

        except AttributeError:
            total_fert_urea += fertiliser.get_fert_kg_n_per_ha("average") * (
                data.__getattribute__(name).area * urea_proportion
            )

    return total_fert_urea


def total_p_fert_use(data, fertiliser):

    crop_names = list(data.__dict__.keys())

    total_fert_p = 0

    for name in crop_names:
        try:
            total_fert_p += (
                fertiliser.get_fert_kg_p_per_ha(name) * data.__getattribute__(name).area
            )

        except AttributeError:
            total_fert_p += (
                fertiliser.get_fert_kg_p_per_ha("average")
                * data.__getattribute__(name).area
            )

    return total_fert_p


def total_k_fert_use(data, fertiliser):

    crop_names = list(data.__dict__.keys())

    total_fert_k = 0

    for name in crop_names:
        try:
            total_fert_k += (
                fertiliser.get_fert_kg_k_per_ha(name) * data.__getattribute__(name).area
            )

        except AttributeError:
            total_fert_k += (
                fertiliser.get_fert_kg_k_per_ha("average")
                * data.__getattribute__(name).area
            )

    return total_fert_k


########################################################################################################
# Urea Fertiliser Emissions
########################################################################################################
def urea_N2O_direct(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):

    """
    this function returns the total emissions from urea and abated urea applied to soils

    proporiton of urea abated (urea_abated_factor) is currently set to zero, as there is not parameter for this.
    """

    urea_abated_factor = urea_abated_proportion

    urea_factor = 1 - urea_abated_proportion

    ef_urea = emissions_factors.get_ef_urea(ef_country)
    ef_urea_abated = emissions_factors.get_ef_urea_and_nbpt(ef_country)

    total_urea = total_urea_fert_use(data, fertiliser, urea_proportion) * urea_factor

    total_urea_abated = (
        total_urea_fert_use(data, fertiliser, urea_proportion) * urea_abated_factor
    )

    return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)


def urea_NH3(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
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

    ef_urea = emissions_factors.get_ef_fracGASF_urea_fertilisers_to_nh3_and_nox(
        ef_country
    )
    ef_urea_abated = emissions_factors.get_ef_fracGASF_urea_and_nbpt_to_nh3_and_nox(
        ef_country
    )

    total_urea = total_urea_fert_use(data, fertiliser, urea_proportion) * urea_factor

    total_urea_abated = (
        total_urea_fert_use(data, fertiliser, urea_proportion) * urea_abated_factor
    )

    return (total_urea * ef_urea) + (total_urea_abated * ef_urea_abated)


def urea_nleach(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):

    """
    This function returns  the amount of urea and abated urea leached from soils.

    Below is the original fraction used in the Costa Rica version, however this seems to be incorrect.
    FRAC=0.02 #FracGASF ammoinium-fertilisers [fraction of synthetic fertiliser N that volatilises as NH3 and NOx under different conditions]

    proporiton of urea abated (urea_abated_factor) is currently set to zero, as there is not parameter for this.

    """
    urea_abated_factor = urea_abated_proportion

    urea_factor = 1 - urea_abated_proportion

    leach = emissions_factors.get_ef_frac_leach_runoff(ef_country)

    total_urea = total_urea_fert_use(data, fertiliser, urea_proportion) * urea_factor

    total_urea_abated = (
        total_urea_fert_use(data, fertiliser, urea_proportion) * urea_abated_factor
    )

    return (total_urea + total_urea_abated) * leach


def urea_N2O_indirect(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):
    """
    this function returns the indirect emissions from urea
    """
    indirect_atmosphere = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
            ef_country
        )
    )
    indirect_leaching = emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(
        ef_country
    )

    return (
        urea_NH3(
            ef_country,
            data,
            fertiliser,
            emissions_factors,
            urea_proportion,
            urea_abated_proportion,
        )
        * indirect_atmosphere
    ) + (
        urea_nleach(
            ef_country,
            data,
            fertiliser,
            emissions_factors,
            urea_proportion,
            urea_abated_proportion,
        )
        * indirect_leaching
    )


def urea_co2(data, fertiliser, urea_proportion, urea_abated_proportion):
    """
    returns the total CO2 from urea application

    proporiton of urea abated (urea_abated_factor) is currently set to zero, as there is not parameter for this.

    """

    urea_abated_factor = urea_abated_proportion

    urea_factor = 1 - urea_abated_proportion

    total_urea = total_urea_fert_use(data, fertiliser, urea_proportion) * urea_factor

    total_urea_abated = (
        total_urea_fert_use(data, fertiliser, urea_proportion) * urea_abated_factor
    )

    return ((total_urea + total_urea_abated) * 0.2) * (
        44 / 12
    )  # adjusted to the NIR version of this calculation


def urea_P_leach(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):
    """
    this function returns the idirect emissions from urea
    """

    frac_leach = float(emissions_factors.get_ef_Frac_P_Leach(ef_country))

    urea_abated_factor = urea_abated_proportion

    urea_factor = 1 - urea_abated_proportion

    total_urea = total_urea_fert_use(data, fertiliser, urea_proportion) * urea_factor

    total_urea_abated = (
        total_urea_fert_use(data, fertiliser, urea_proportion) * urea_abated_factor
    )

    return (total_urea + total_urea_abated) * frac_leach


#########################################################################################################
# Nitrogen Fertiliser Emissions
#########################################################################################################
def n_fertiliser_P_leach(
    ef_country, data, emissions_factors, fertiliser, urea_proportion
):
    """
    this function returns the idirect emissions from urea
    """
    frac_leach = float(emissions_factors.get_ef_Frac_P_Leach(ef_country))

    total_n_fert = total_an_fert_use(data, fertiliser, urea_proportion)

    return total_n_fert * frac_leach


def p_fertiliser_P_leach(ef_country, data, fertiliser, emissions_factors):
    """
    this function returns the idirect emissions from urea
    """
    frac_leach = float(emissions_factors.get_ef_Frac_P_Leach(ef_country))

    total_p_fert = total_p_fert_use(data, fertiliser)

    return total_p_fert * frac_leach


def n_fertiliser_direct(
    ef_country, data, fertiliser, emissions_factors, urea_proportion
):

    """
    This function returns total direct emissions from ammonium nitrate application at field level
    """
    ef = emissions_factors.get_ef_ammonium_nitrate(ef_country)

    total_n_fert = total_an_fert_use(data, fertiliser, urea_proportion)

    return total_n_fert * ef


def n_fertiliser_NH3(ef_country, data, fertiliser, emissions_factors, urea_proportion):

    """
    This function returns total NH3 emissions from ammonium nitrate application at field level
    """
    ef = emissions_factors.get_ef_fracGASF_ammonium_fertilisers_to_nh3_and_nox(
        ef_country
    )

    total_n_fert = total_an_fert_use(data, fertiliser, urea_proportion)

    return total_n_fert * ef


def n_fertiliser_nleach(
    ef_country, data, fertiliser, emissions_factors, urea_proportion
):
    """
    This function returns total leached emissions from ammonium nitrate application at field level
    """

    leach = emissions_factors.get_ef_frac_leach_runoff(ef_country)

    total_n_fert = total_an_fert_use(data, fertiliser, urea_proportion)

    return total_n_fert * leach


def n_fertiliser_indirect(
    ef_country, data, fertiliser, emissions_factors, urea_proportion
):

    """
    this function returns the indirect emissions from ammonium nitrate fertiliser
    """

    indirect_atmosphere = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
            ef_country
        )
    )
    indirect_leaching = emissions_factors.get_ef_indirect_n2o_from_leaching_and_runoff(
        ef_country
    )

    return (
        n_fertiliser_NH3(
            ef_country, data, fertiliser, emissions_factors, urea_proportion
        )
        * indirect_atmosphere
    ) + (
        n_fertiliser_nleach(
            ef_country, data, fertiliser, emissions_factors, urea_proportion
        )
        * indirect_leaching
    )


# Fertiliser Application Totals for N20 and CO2


def total_fertiliser_direct(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):
    """
    This function returns the total direct and indirect emissions from urea and ammonium fertilisers
    """

    result = urea_N2O_direct(
        ef_country,
        data,
        fertiliser,
        emissions_factors,
        urea_proportion,
        urea_abated_proportion,
    ) + n_fertiliser_direct(
        ef_country, data, fertiliser, emissions_factors, urea_proportion
    )

    return result


def total_fertiliser_indirect(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):
    """
    This function returns the total direct and indirect emissions from urea and ammonium fertilisers
    """

    result = urea_N2O_indirect(
        ef_country,
        data,
        fertiliser,
        emissions_factors,
        urea_proportion,
        urea_abated_proportion,
    ) + n_fertiliser_indirect(
        ef_country, data, fertiliser, emissions_factors, urea_proportion
    )

    return result


def fert_upstream_P(ef_country, data, fertiliser, upstream, urea_proportion):

    """
    this function returns the upstream emissions from urea and ammonium fertiliser manufature
    """
    AN_fert_PO4 = upstream.get_upstream_kg_po4e(
        "ammonium_nitrate_fertiliser"
    )  # Ammonium Nitrate Fertiliser
    Urea_fert_PO4 = upstream.get_upstream_kg_po4e("urea_fert")
    Triple_superphosphate = upstream.get_upstream_kg_po4e("triple_superphosphate")
    Potassium_chloride = upstream.get_upstream_kg_po4e("potassium_chloride")

    total_n_fert = total_an_fert_use(data, fertiliser, urea_proportion)
    total_p_fert = total_p_fert_use(data, fertiliser)
    total_k_fert = total_k_fert_use(data, fertiliser)
    total_urea = total_urea_fert_use(data, fertiliser, urea_proportion)

    return (
        (total_n_fert * AN_fert_PO4)
        + (total_urea * Urea_fert_PO4)
        + (total_p_fert * Triple_superphosphate)
        + (total_k_fert * Potassium_chloride)
    )


###############################################################################
# Water Quality EP PO4e
###############################################################################

# SOILS
def total_soils_NH3_and_LEACH_EP(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):
    """
    Convert N to PO4  = 0.42

    """
    indirect_atmosphere = (
        emissions_factors.get_ef_indirect_n2o_atmospheric_deposition_to_soils_and_water(
            ef_country
        )
    )

    NH3N = urea_NH3(
        ef_country,
        data,
        fertiliser,
        emissions_factors,
        urea_proportion,
        urea_abated_proportion,
    ) + n_fertiliser_NH3(
        ef_country, data, fertiliser, emissions_factors, urea_proportion
    )

    LEACH = urea_nleach(
        ef_country,
        data,
        fertiliser,
        emissions_factors,
        urea_proportion,
        urea_abated_proportion,
    ) + n_fertiliser_nleach(
        ef_country, data, fertiliser, emissions_factors, urea_proportion
    )

    return (NH3N * indirect_atmosphere) + LEACH * 0.42


def total_soils_P_LEACH_EP(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):

    PLEACH = (
        urea_P_leach(
            ef_country,
            data,
            fertiliser,
            emissions_factors,
            urea_proportion,
            urea_abated_proportion,
        )
        + n_fertiliser_P_leach(
            ef_country, data, emissions_factors, fertiliser, urea_proportion
        )
        + p_fertiliser_P_leach(ef_country, data, fertiliser, emissions_factors)
    )

    return PLEACH * 3.06


def total_soils_EP(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):

    return total_soils_NH3_and_LEACH_EP(
        ef_country,
        data,
        fertiliser,
        emissions_factors,
        urea_proportion,
        urea_abated_proportion,
    ) + total_soils_P_LEACH_EP(
        ef_country,
        data,
        fertiliser,
        emissions_factors,
        urea_proportion,
        urea_abated_proportion,
    )


# Imported Feeds


def upstream_EP(ef_country, data, fertiliser, upstream, urea_proportion):

    return fert_upstream_P(ef_country, data, fertiliser, upstream, urea_proportion)


###############################################################################
# Air Quality
###############################################################################

# SOILS
# SOILS
def total_soils_NH3_AQ(
    ef_country,
    data,
    fertiliser,
    emissions_factors,
    urea_proportion,
    urea_abated_proportion,
):

    NH3N = urea_NH3(
        ef_country,
        data,
        fertiliser,
        emissions_factors,
        urea_proportion,
        urea_abated_proportion,
    ) + n_fertiliser_NH3(
        ef_country, data, fertiliser, emissions_factors, urea_proportion
    )

    return NH3N

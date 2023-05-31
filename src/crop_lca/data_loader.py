from crop_lca.database_manager import DataManager
from crop_lca.models import (
    Fertiliser,
    CropChars,
    Upstream,
    Emissions_Factors,
)


class Loader:
    def __init__(self, ef_country):
        self.ef_country = ef_country
        self.dataframes = DataManager(ef_country)
        self.crop_chars = self.get_crop_chars()
        self.fertiliser = self.get_fertiliser()
        self.emissions_factors = self.get_emissions_factors()
        self.upstream = self.get_upstream()

    def get_crop_chars(self):
        return CropChars(self.dataframes.crop_char_data())

    def get_fertiliser(self):
        return Fertiliser(self.dataframes.fertiliser_data())

    def get_emissions_factors(self):
        return Emissions_Factors(self.dataframes.emissions_factor_data())

    def get_upstream(self):
        return Upstream(self.dataframes.upstream_data())

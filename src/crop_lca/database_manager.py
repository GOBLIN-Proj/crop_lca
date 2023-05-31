import sqlalchemy as sqa
import pandas as pd
from crop_lca.database import get_local_dir
import os


class DataManager:
    def __init__(self, ef_country):
        self.database_dir = get_local_dir()
        self.engine = self.data_engine_creater()
        self.ef_country = ef_country

    def data_engine_creater(self):
        database_path = os.path.abspath(
            os.path.join(self.database_dir, "crop_database.db")
        )
        engine_url = f"sqlite:///{database_path}"

        return sqa.create_engine(engine_url)

    def crop_char_data(self, index=None):
        table = "crop_params"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe

    def upstream_data(self, index=None):
        table = "upstream_crop"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe

    def emissions_factor_data(self, index=None):
        table = "emission_factor_crop"

        if index == None:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, self.ef_country),
                self.engine,
            )

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s' WHERE ef_country = '%s'" % (table, self.ef_country),
                self.engine,
                index_col=[index],
            )

        return dataframe

    def fertiliser_data(self, index=None):
        table = "fertiliser_crop"

        if index == None:
            dataframe = pd.read_sql("SELECT * FROM '%s'" % (table), self.engine)

        else:
            dataframe = pd.read_sql(
                "SELECT * FROM '%s'" % (table),
                self.engine,
                index_col=[index],
            )

        return dataframe

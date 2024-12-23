import ast

import numpy as np
import pandas as pd

from globals_dir.utils import handle_errors
from .db_api_base import DBApiBase

class DBApi(DBApiBase):

    def __init__(self, db_path: str, columns_names: list):
        """
        ensure your db_path is good. e.g. example.csv
        :param db_path:
        """
        super().__init__(db_path, columns_names)

    def write_new_type(self, type_name, schema, description, default_values,
                       default_rule_instance,
                       rule_type, embedding) -> None:
        """
        Add or update a new type_name in the DataFrame and save the changes to S3.
        :param embedding:
        :param type_name: The type name.
        :param schema:
        :param description:
        :param default_values:
        :param default_rule_instance:
        :param rule_type: The new type_name to be added or updated.
        """
        new_row = {
            'type_name': type_name,
            'schema': schema,
            'description': description,
            'default_values': default_values,
            'default_rule_instance': default_rule_instance,
            'rule_type': rule_type,
            'embedding': embedding
        }

        if type_name in self.get_col("type_name"):
            self.df.loc[self.df['type_name'] == type_name, list(new_row.keys())] = list(new_row.values())
        else:
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.save_db()

    def set_df(self, df):
        self.df = df
        self.save_db()

    def get_df_type_name(self, value, col_value="type_name", _not=False):
        if not _not:
            return self.df[self.df[col_value] == value]
        return self.df[self.df[col_value] != value]




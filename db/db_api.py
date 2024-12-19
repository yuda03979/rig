import ast

import numpy as np
import pandas as pd

from globals_dir.utils import handle_errors


class DBApiBase:

    def __init__(self, db_path: str, columns_names: list):
        self.validate_db_path(db_path)
        print("the first column is the index column. e.g. - type_name")
        self.db_path = db_path
        self.columns_names = columns_names
        self.index_column = columns_names[0]
        self.df = None
        self.init_df()

    def init_df(self) -> None:
        try:
            self.df = pd.read_csv(self.db_path)
            self.df = self.df.map(self.parse_value)
        except:
            self.df = pd.DataFrame(columns=self.columns_names)
            self.save_db()

    def validate_db_path(self, db_path):
        if not db_path.endswith('.csv'):
            message = f"the db_path should end with '.csv'! your path: {db_path}"
            handle_errors(e=message)

    def get_col(self, col_name):
        return self.df[col_name].tolist()

    def get_row(self, row_name):
        return self.df[self.df[self.index_column] == row_name].tolist()

    def get_index(self, indexes):
        row_name, col_name = indexes
        return self.df[self.df[self.index_column] == row_name][col_name].iloc[0]  # .tolist()[0]

    def set_row(self, row_values: dict):
        if row_values[self.index_column] in self.get_col(self.index_column):
            self.df.loc[self.df['type_name'] == row_values[self.index_column], list(row_values.keys())] = list(
                row_values.values())
        else:
            self.df = pd.concat([self.df, pd.DataFrame([row_values])], ignore_index=True)
        self.save_db()

    def save_db(self):
        self.df.to_csv(self.db_path, index=False)
        self.df = pd.read_csv(self.db_path)
        self.df.map(self.parse_value)

    def parse_value(self, value):
        """
        when reading from csv, everything is str. so it conver it
        :param value:
        :return: the actual value
        """
        try:
            # Attempt to parse the value using literal_eval
            parsed_value = ast.literal_eval(value)
            # Convert lists to NumPy arrays
            if isinstance(parsed_value, list):
                return np.array(parsed_value)
            # Return dictionaries as is
            elif isinstance(parsed_value, dict):
                return parsed_value
            else:
                return value  # Return the value unchanged if not a list or dict
        except (ValueError, SyntaxError):
            # If parsing fails, return the original value
            return value


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

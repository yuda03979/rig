import ast
import pandas as pd


class DBManager:
    """
    DBManager class to manage a CSV-based database, enabling CRUD operations
    for types and associated data. Uses pandas for DataFrame operations
    and ast for string-to-dict/list conversions.
    """

    def __init__(self, db_path):
        """
        Initialize the DBManager instance by loading the CSV file.

        If the CSV does not exist, an empty DataFrame is created.

        Parameters:
            db_path (str): Path to the database CSV file. Must end with .csv.
        """
        self.db_path = db_path
        self.df = self.get_df()

    def validate_db_path(self):
        """
        Validate if db_path ends with '.csv'.

        Raises:
            Exception: If db_path does not end with '.csv'.
        """
        if self.db_path[-4:] != '.csv':
            raise Exception(
                f"The db_path should end with '.csv'! Your path: {self.db_path}"
            )

    def get_df(self) -> pd.DataFrame:
        """
        Load the CSV into a DataFrame or return an empty one if not found.

        The empty DataFrame contains predefined columns.

        Returns:
            pd.DataFrame: DataFrame loaded from CSV or an empty DataFrame.
        """
        try:
            df = pd.read_csv(self.db_path)
        except FileNotFoundError:
            df = pd.DataFrame(
                columns=[
                    "type_name", "schema", "description",
                    "default_values", "default_rule_instance",
                    "rule_type", "embedding"
                ]
            )
        return df

    def update_db(self) -> None:
        """
        Save the current DataFrame to the CSV file.
        Updates the database with recent changes.
        """
        self.df.to_csv(self.db_path, index=False)

    def get_all_types_names(self) -> list:
        """
        Retrieve a list of all type names from the DataFrame.

        Returns:
            list: List of all 'type_name' values in the DataFrame.
        """
        return self.df['type_name'].tolist()

    def get_dict_features(self, type_name, feature) -> dict:
        """
        Get dictionary data from a specified feature for a given type.

        Parameters:
            type_name (str): The name of the type (must exist in 'rule_type').
            feature (str): The DataFrame column containing the dictionary.

        Returns:
            dict: Dictionary representation of the specified feature.
        """
        return ast.literal_eval(
            self.df[self.df['type_name'] == type_name][feature].iloc[0]
        )

    def get_embedding(self, type_name) -> list:
        """
        Retrieve the embedding list for a given type_name.

        Parameters:
            type_name (str): The name of the type.

        Returns:
            list: List representation of the embedding.
        """
        return ast.literal_eval(
            self.df[self.df['type_name'] == type_name]["embedding"].tolist()[0]
        )

    def write_new_type(
        self, type_name: str, schema: str, description: str,
        default_values: str, default_rule_instance: str,
        rule_type: str, embedding: str
    ) -> None:
        """
        Add or update a type entry in the DataFrame and save to CSV.

        If the type_name already exists, update the existing entry.
        Otherwise, create a new entry.

        Parameters:
            type_name (str): Unique identifier for the type.
            schema (str): Schema definition.
            description (str): Description of the type.
            default_values (str): Default values for the type.
            default_rule_instance (str): Rule instance details.
            rule_type (str): Rule type for the entry.
            embedding (str): Embedding information (stored as stringified list).
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

        if type_name in self.get_all_types_names():
            self.df.loc[self.df['type_name'] == type_name, list(new_row.keys())] = \
                list(new_row.values())
        else:
            self.df = pd.concat(
                [self.df, pd.DataFrame([new_row])], ignore_index=True
            )
        self.update_db()
import os
import csv
import re
import ast
import json
import yaml
import numpy as np
from yaml import SafeLoader
from datetime import datetime
from globals_dir.globals import GLOBALS
from globals_dir.api import API
from datetime import datetime
import pandas as pd

class PromptExamples:
    def __init__(self):
        """
        Initialize the CreateExamples with the RAG API and log file.
        :param log_file: The path to the CSV log file.
        """
        pass

    def clean_text(self, text):
        """Remove all non-alphanumeric characters and convert to lowercase."""
        return ''.join(char.lower() for char in text if char.isalnum())

    def get_closest_question(self, query, type_name, row_id=None):
        """
        Find the closest two questions in the log file to the given question.
        :return: A dictionary containing the two closest questions, answers, and distances.
        """
        # print("id =", row_id)


        # Initialize placeholders for the top two closest matches
        closest = {"distance": -float("inf"), "free_text": None, "schema": None, "description": None, "response": None,
                   "type_name": None}
        second_closest = {"distance": -float("inf"), "free_text": None, "schema": None, "description": None, "response": None,
                          "type_name": None}

        examples = {
            "example_1": closest,
            "example_2": second_closest,
        }

        if API.db_api_examples.get_len() < 2:
            return examples

        closests = API.rag_api_examples.get_closest_type_name(query=query)
        # set all the differences you want
        row1 = API.db_api_examples.get_row(closests[0][0])
        row2 = API.db_api_examples.get_row(closests[1][0])

        def rowlist_to_rowdict(row_list):
            row_dict = {}
            keys = GLOBALS.db_examples["columns_names"]
            for k, v in zip(keys, row_list):
                row_dict[k] = v
            return row_dict

        examples["example_1"] = rowlist_to_rowdict(row1)
        examples["example_2"] = rowlist_to_rowdict(row2)

        # Prepare the output examples

        # print(examples)
        return examples
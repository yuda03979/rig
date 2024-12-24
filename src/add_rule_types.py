import json
import logging
import os
import pandas
import pandas as pd

from globals_dir.api import API
from classification.rag_api import RagApi


class NewType:

    def __init__(self):
        pass

    def add(self, json_input):
        if isinstance(json_input, dict):
            rule_type = json_input
        else:
            try:
                # Check if the input is a file path
                if json_input.endswith('.json') and os.path.isfile(json_input):
                    with open(json_input, 'r') as file:
                        rule_type_json = file.read()
                    rule_type = json.loads(rule_type_json)
            except (IOError, json.JSONDecodeError) as e:
                print(f"{e}")
                message = f"Please load file.json or dict, and make sure it's in correct rule type format. Error: {str(e)}"
                logging.error(message)
                raise ValueError(message)

        type_name = rule_type['name'].lower()
        schema = self.create_schema(rule_type)
        description = self.create_description(rule_type)
        default_values = self.create_default_values(rule_type)
        default_rule_instance = self.create_default_rule_instance(rule_type, default_values)
        # embedding = self.create_embedding(type_name, schema)

        return {
            'type_name': type_name,
            'schema': schema,
            'description': description,
            'default_values': default_values,
            'default_rule_instance': default_rule_instance,
            'rule_type': rule_type,
            'embedding': None
        }

    def create_schema(self, rule_type) -> dict:
        schema = {}
        for param in rule_type["parameters"]:
            schema[param["name"]] = str(param["type"])
        schema['ruleInstanceName'] = "string"
        schema['severity'] = "int"
        return schema

    def create_description(self, rule_type) -> dict:
        description = {}
        for param in rule_type["parameters"]:
            description[param["name"] + "_description"] = str(param["description"])
        description['ruleInstanceName_description'] = "about what the message and to what it related in the db."
        description['severity_description'] = "level of importance, criticality, or risk."
        description["event details"] = {}
        description["event details"]["global description"] = str(rule_type["description"])
        description["event details"]["object name"] = rule_type["eventDetails"][0]["objectName"]
        return description

    def create_default_values(self, rule_type) -> dict:
        """ assuming severity and ruleInstanceName default values"""
        default_values = {}
        for param in rule_type["parameters"]:
            default_values[param["name"]] = str(param["defaultValue"])
        return default_values

    # rule_type["description"]
    def create_default_rule_instance(self, rule_type, default_values) -> dict:
        rule_instance = {
            "_id": "00000000-0000-0000-0000-000000000000",  # Sample ID
            "description": "string",
            "isActive": True,
            "lastUpdateTime": "00/00/0000 00:00:00",
            "params": default_values,
            "ruleInstanceName": '',
            "severity": '',
            "ruleType": rule_type['logicType'],
            "ruleOwner": "",
            "ruleTypeId": rule_type["_id"],
            "eventDetails": rule_type["eventDetails"],
            "additionalInformation": rule_type['additionalInformation'],
            "presetId": "00000000-0000-0000-0000-000000000000"
        }
        return rule_instance


class AddRuleTypes:
    def __init__(self, folder: str):
        if folder == "":
            return
        self.df = pd.DataFrame()

        for file_name in os.listdir(folder):
            if file_name.endswith(".json"):
                new_data = NewType().add(os.path.join(folder, file_name))
                self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)

        # Create embeddings for all rows at once
        self.df["embedding"] = self.create_embeddings()
        API.db_api_rule_types.set_df(self.df)
        API.rag_api_classification = RagApi(API.db_api_examples, "free_text")

    def create_embeddings(self) -> list:
        # Combine all rows into a list of embedding texts
        embedding_words = [
            f"rule type name: {type_name}\nschema: {schema}"
            for type_name, schema in zip(self.df["type_name"], self.df["schema"])
        ]

        # Generate embeddings for all rows at once
        embeddings = API.rag_api_classification.get_batch_embeddings(embedding_words)  # Assuming batch processing is supported
        return embeddings

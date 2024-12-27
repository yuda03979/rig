import json
import os

from RIG.globals import GLOBALS, MODELS


class NewType:
    """
    Class to handle adding new rule types to the database.
    """

    def __init__(self):
        """
        Initialize the NewType instance with the database manager.
        """
        self.db_manager = GLOBALS.db_manager

    def add(self, json_input) -> None:
        """
        Add a new rule type from a JSON input (file or dictionary).

        :param json_input: Either a file path to a .json file or a dictionary containing the rule type.
        :return: None
        :raises ValueError: If input is not in the expected format.
        """
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
                raise ValueError(
                    f"Please load file.json or dict, and make sure it's in correct rule type format. Error: {str(e)}")

        type_name = rule_type['name'].lower()
        schema = self.create_schema(rule_type)
        description = self.create_description(rule_type)
        default_values = self.create_default_values(rule_type)
        default_rule_instance = self.create_default_rule_instance(rule_type, default_values)
        embedding = self.create_embedding(type_name, schema)

        self.db_manager.write_new_type(
            str(type_name),
            str(schema),
            str(description),
            str(default_values),
            str(default_rule_instance),
            str(rule_type),
            str(embedding)
        )

    def create_schema(self, rule_type) -> dict:
        """
        Create the schema dictionary from the rule type.

        :param rule_type: The rule type data.
        :return: A dictionary representing the schema.
        """
        schema = {}
        for param in rule_type["parameters"]:
            schema[param["name"]] = str(param["type"])
        schema['ruleInstanceName'] = "string"
        schema['severity'] = "int"
        return schema

    def create_description(self, rule_type) -> dict:
        """
        Create the description dictionary from the rule type.

        :param rule_type: The rule type data.
        :return: A dictionary representing the descriptions for each parameter.
        """
        description = {}
        for param in rule_type["parameters"]:
            description[param["name"] + "_description"] = str(param["description"])
        description['ruleInstanceName_description'] = "About what the message is and to what it relates in the DB."
        description['severity_description'] = "Level of importance, criticality, or risk."
        description["global description"] = str(rule_type["description"])
        description["object name"] = rule_type["eventDetails"][0]["objectName"]
        return description

    def create_default_values(self, rule_type) -> dict:
        """
        Create the default values dictionary from the rule type.

        :param rule_type: The rule type data.
        :return: A dictionary of default values for each parameter.
        """
        default_values = {}
        for param in rule_type["parameters"]:
            default_values[param["name"]] = str(param["defaultValue"])
        return default_values

    def create_default_rule_instance(self, rule_type, default_values) -> dict:
        """
        Create the default rule instance based on the rule type.

        :param rule_type: The rule type data.
        :param default_values: The default values for the parameters.
        :return: A dictionary representing the default rule instance.
        """
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

    def create_embedding(self, type_name, schema) -> str:
        """
        Create the embedding for a new rule type based on its name and schema.

        :param type_name: The name of the rule type.
        :param schema: The schema of the rule type.
        :return: The embedding as a string.
        """
        embedding_words = f"rule type name: {type_name}\nschema: {schema}"
        embedding_json, embedding = MODELS.rag_api.get_embedding(str(embedding_words))
        MODELS.rag_api.add_rule_type_embedding(type_name, embedding)
        return str(embedding_json)
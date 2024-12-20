from typing import Tuple, List, Any
from globals_dir.api import API
from globals_dir.globals import GLOBALS
from globals_dir.models import MODELS
from classification.prompts import prompt_for_gemma, prefix_document, prefix_query


class Classifier:

    def __init__(self):
        pass

    def predict(self, query) -> tuple[Any, int, bool]:

        # using rag:
        type_names_list, succeed = self.using_rag(query)
        if succeed:
            return type_names_list[0][0], type_names_list[0][1], False

        # # using regex
        # type_names, succeed = self.find_rule_name_in_query(query)
        # if succeed:
        #     return type_names[0], -1, False
        #
        # # using llm
        # type_name, succeed = self.ask_model(query, type_names_list)
        # if succeed:
        #     return type_name, -2, False

        # failed
        return "null", -3, True

    def find_rule_name_in_query(self, query) -> tuple[list[Any], bool]:
        """
        (regex search) - searching in the string matchhing between any rulu_type_nameto the query
        :param query:
        :return:
        """

        def clean_text(text):
            """Remove all non-alphanumeric characters and convert to lowercase."""
            return ''.join(char.lower() for char in text if char.isalnum())

        rule_names_list = API.db_api.get_col("type_name")
        results = []
        for type_name in rule_names_list:
            if clean_text(type_name) in clean_text(query):
                results.append(type_name.lower())

        if len(results) == 1:
            return [results[0]], True
        else:
            return results, False

    def using_rag(self, query):
        succeed = False
        type_names_list = API.rag_api.get_closest_type_name(query=query, prefix_query=prefix_query)
        closest_distance = type_names_list[0][1]
        difference = type_names_list[0][1] - type_names_list[1][1]
        if difference > GLOBALS.rag_difference and difference != float('inf'):  # the case of empty list
            if closest_distance > GLOBALS.rag_threshold:
                succeed = True
        if type_names_list[0][0] != 'None' and type_names_list[1][0] == 'None':  # in case of one type name
            succeed = True
        return type_names_list, succeed

    def ask_model(self, query, type_names):
        schema_a = API.db_api.get_dict_features(type_name=type_names[0][0], feature="schema")
        description_a = API.db_api.get_dict_features(type_name=type_names[0][0], feature="description")

        schema_b = API.db_api.get_dict_features(type_name=type_names[1][0], feature="schema")
        description_b = API.db_api.get_dict_features(type_name=type_names[1][0], feature="description")


        type_name = get_dict(MODELS.gemma_api.predict(prompt) + '}')[0]
        try:
            if type_name["type_name"] in API.db_api.get_all_types_names():
                return type_name["type_name"], True
        except:
            return f'model didnt generate well: {str(type_name)}', False

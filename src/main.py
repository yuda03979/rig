import os

from .get_rule_instance import GetRuleInstance
from .add_rule_types import AddRuleTypes
from globals_dir.models import MODELS
from globals_dir.globals import GLOBALS
from globals_dir.api import API
from globals_dir.utils import handle_errors

import time
from datetime import datetime

GLOBALS.init()
MODELS.init()

class RIG:

    def __init__(self, ):
        self.get_rule_instance = GetRuleInstance()


    def load_ollamamia(self):
        # to do! raise an error.
        GLOBALS.init()
        MODELS.init()
        return True


    def add_rule_types(self):
        try:
            AddRuleTypes(GLOBALS.rule_types_directory)
            return True
        except:
            return False

    def is_ollamamia_running(self):
        return GLOBALS.ollamamia.is_running()

    def stop(self):
        GLOBALS.ollamamia.stop()
        return True


    def predict(self, free_text: str) -> dict:
        """
        Processes user input and returns a response with its validation status.

        Args:
            free_text (str): User input text to be processed.

        Returns:
            dict:
                -"rule_instance": desire response,
                -"error": True if error occurs, else False,
                -"free_text": free_text,
                -"type_name": the predicted type name,
                -"rag_score": score of how much we are sure the type name is correct, higher is better.
                -"model_response": the model response before preprocessing.
        """

        start_time = time.time()

        response = {
            "rule_instance": None,
            "is_error": True,
            "error_message": '',
            "free_text": free_text,
            "type_name": None,
            "rag_score": None,
            "model_response": None,
            "schema": None
        }

        if any(char.isalpha() for char in free_text) and len(free_text) > 10:
            try:
                response = self.get_rule_instance.predict(free_text)

            except Exception as e:
                response["error_message"] = f"Processing failed: {type(e).__name__}, {str(e)}"

        else:
            response["error_message"] = f"please enter meaningful text"

        current_time = datetime.now()
        response["time"] = f"{current_time.strftime('%Y-%m-%d')}|{current_time.strftime('%H:%M:%S')}"
        response["inference_time"] = time.time() - start_time
        try:
            response["rag_score"] = response["rag_score"].item()
        except:
            pass
        return response

    def tweak_rag_parameters(self, rag_threshold=GLOBALS.rag_threshold, rag_difference=GLOBALS.rag_difference):
        GLOBALS.rag_threshold = rag_threshold
        GLOBALS.rag_difference = rag_difference
        return True

    def get_rule_types_names(self):
        return API.db_api_rule_types.get_col("type_name")

    def feedback(self, rig_response: dict, good: bool):
        free_text = rig_response["free_text"]
        type_name = rig_response["type_name"]
        schema = rig_response["schema"]
        description = ""
        model_response = rig_response["model_response"]
        is_error = rig_response["is_error"]
        error_message = rig_response["error_message"]
        rag_score = rig_response["rag_score"]

        if good:
            embedding = API.rag_api_examples.get_embedding(free_text)
            row = {
                "free_text": free_text,
                "type_name": type_name,
                "schema": schema,
                "description": description,
                "expected": model_response,
                "embedding": embedding,
            }
            API.db_api_examples.set_row(row_values=row)

        values = {
            "free_text": free_text,
            "type_name": type_name,
            "schema": schema,
            "description": description,
            "model_response": model_response,
            "is_error": is_error,
            "error_message": error_message,
            "rag_score": rag_score,
        }

        # save the values into the logs file
        return "thank you :)"

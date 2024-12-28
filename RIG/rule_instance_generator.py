import os
import time
from datetime import datetime
import subprocess

from RIG.globals import GLOBALS, MODELS
from RIG.src.App.rule_instance.get import Get
from RIG.src.App.new_type import NewType
from RIG.src.Utils.utils import log_interactions, log_question_and_answer
from RIG.src.Utils.rag_api import RagApi
from RIG.src.Utils.gemma_api import GemmaApi
from RIG.rig_evaluate import *


class RuleInstanceGenerator:
    """
    A class to handle the generation, evaluation, and management of rule instances.
    """

    def __init__(self):
        """
        Initialize the RuleInstanceGenerator with required services and models.
        """
        self.globals = GLOBALS
        MODELS.rag_api = RagApi()
        MODELS.gemma_api = GemmaApi()
        self.models = MODELS
        self.get_instance = Get()
        self.new_type = NewType()

    def new_rule_type(self, rule_type) -> bool:
        """
        Adds a new rule type to the system.

        Args:
            rule_type (dict or str): The rule type to be added, can be a dictionary or path to a .json file.

        Returns:
            bool: True if the rule type was added successfully, else False.
        """
        self.new_type.add(rule_type)
        log_interactions({"succeeded": True, "file upload": rule_type})
        return True

    def get_rule_instance(self, free_text: str, row_id=None, for_eval=False) -> dict:
        """
        Processes user input and returns a response with its validation status.

        Args:
            free_text (str): User input text to be processed.

        Returns:
            dict:
                - "rule_instance": Desired response.
                - "is_error": True if error occurs, else False.
                - "free_text": Input text.
                - "type_name": The predicted type name.
                - "rag_score": Score indicating how confident the system is in the predicted type name.
                - "model_response": The raw model response before preprocessing.
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
            "examples": None,
            "schema": None
        }

        # Check if input is meaningful
        if any(char.isalpha() for char in free_text) and len(free_text) > 10:
            response = self.get_instance.predict(free_text, row_id, for_eval)
        else:
            response["error_message"] = "Please enter meaningful text"

        # Track time of the response
        current_time = datetime.now()
        response["time"] = f"{current_time.strftime('%Y-%m-%d')}|{current_time.strftime('%H:%M:%S')}"
        response["inference_time"] = time.time() - start_time

        # Try to access rag_score
        try:
            response["rag_score"] = response["rag_score"].item()
        except:
            pass

        # Log interactions
        log_interactions(response)
        if not response["is_error"]:
            log_interactions(response)

        return response

    def add_rule_types_from_folder(self):
        """
        Load rule types from a specified folder and add them to the system.

        Returns:
            bool: True if all rule types were loaded successfully, else an error message.
        """
        rule_types_directory = GLOBALS.rule_types_directory

        for file_name in os.listdir(rule_types_directory):
            print(f"Loading {file_name}")
            if file_name.endswith(".json"):
                if not self.new_rule_type(os.path.join(rule_types_directory, file_name)):
                    return f"Error in add_rule_types_from_folder, loading didn't complete. Error with: {file_name}"

        return True

    def tweak_rag_parameters(self, rag_threshold=GLOBALS.rag_threshold, rag_difference=GLOBALS.rag_difference):
        """
        Adjust the RAG parameters.

        Args:
            rag_threshold (float): The threshold for RAG score.
            rag_difference (float): The threshold for RAG difference.

        Returns:
            bool: Always returns True.
        """
        GLOBALS.rag_threshold = rag_threshold
        GLOBALS.rag_difference = rag_difference
        return True

    def get_rule_types_names(self):
        """
        Retrieve all rule type names.

        Returns:
            list: List of all rule type names.
        """
        return GLOBALS.db_manager.get_all_types_names()

    def feedback(self, rig_response: dict, good: bool) -> str:
        """
        Provide feedback on the system's response.

        Args:
            rig_response (dict): The response from the system.
            good (bool): Whether the feedback is positive.

        Returns:
            str: A message acknowledging the feedback.
        """
        if good:
            log_interactions({"feedback": rig_response, "time": datetime.now()})
            log_question_and_answer(rig_response)
        return "Thank you :)"

    def evaluate(
        self,
        data_file_path=GLOBALS.df_eval_path,
        output_directory=GLOBALS.eval_output_dir,
        start_point=0,
        end_point=2,  # None or -1 = all the data
        sleep_time_each_10_iter=30,
        batch_size=250,
    ):
        """
        Evaluate the system with a dataset.

        Args:
            data_file_path (str): Path to the dataset for evaluation.
            output_directory (str): Directory to store the evaluation results.
            start_point (int): The start point for evaluation.
            end_point (int): The end point for evaluation (None or -1 for all data).
            sleep_time_each_10_iter (int): The sleep time between each 10 iterations - for local computers.
            batch_size (int): The batch size for evaluation.

        Returns:
            None
        """
        evaluate_func(
            self,
            data_file_path=data_file_path,
            output_directory=output_directory,
            start_point=start_point,
            end_point=end_point,  # -1 all the data (almost...)
            sleep_time_each_10=sleep_time_each_10_iter,
            batch_size=batch_size
        )


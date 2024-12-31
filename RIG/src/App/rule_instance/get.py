from RIG.src.Utils.utils import get_dict
from .classification import Classification
from .generation import Generation
from .post_processing import post_processing
from RIG.globals import GLOBALS
from RIG.src.App.validation import Validation

class Get:
    """
    Get class orchestrates the classification and generation processes
    to predict and process rule instances from free-text input.
    """

    def __init__(self):
        """
        Initialize the Get instance.

        This sets up the classifier and generator required for prediction.
        """
        self.classifier = Classification()
        self.generator = Generation()
        self.validator = Validation()

    def predict(self, free_text: str, row_id: str = 'id', for_eval: bool = False) -> dict:
        """
        Predict and generate rule instances from free-text input.

        This method classifies the input text, generates model responses,
        and performs post-processing to extract structured rule instances.

        Parameters:
            free_text (str): The input free-text to process.
            row_id (str, optional): Row identifier for evaluation (default is 'id').
            for_eval (bool, optional): If True, uses the row_id for evaluation.

        Returns:
            dict: A response containing prediction details and error status.
                  Keys include:
                  - rule_instance (dict or None)
                  - is_error (bool)
                  - error_message (str)
                  - free_text (str)
                  - type_name (str or None)
                  - rag_score (float or None)
                  - model_response (str or None)
                  - examples (list or None)
                  - schema (dict or None)
        """
        # Initialize response structure
        response = {
            "rule_instance": None,
            "is_error": True,
            "error_message": "",
            "free_text": free_text,
            "type_name": None,
            "rag_score": None,
            "model_response": None,
            "examples": None,
            "schema": None,
            "validation_score": 0,
        }

        # Perform classification to predict type_name and rag_score
        response["type_name"], response["rag_score"], is_error = self.classifier.predict(free_text)

        # Handle classification errors
        if is_error:
            response["error_message"] = (
                "Error! Can't identify ruleType. No ruleType exists or it didn't pass the threshold."
            )
            return response

        # Perform generation to predict model response and retrieve schema/examples
        response["model_response"], response["schema"], response["examples"] = (
            self.generator.predict(response["type_name"], free_text, row_id if for_eval else None)
        )

        # Extract structured data from model response
        model_response, succeed = get_dict(response["model_response"])


        if succeed:
            # validate_socre
            score: int = self.validator.get_score(
                free_text=free_text,
                description=GLOBALS.db_manager.get_dict_features(type_name=response["type_name"], feature="description"),
                llm_response=model_response)


        response["validation_score"] = score

        # Handle extraction errors
        if not succeed:
            response["error_message"] = (
                "Error! Can't extract JSON from model response."
            )
            return response

        # Perform post-processing to finalize rule instance
        response["rule_instance"] = post_processing(response["type_name"], model_response)
        response["is_error"] = False

        return response

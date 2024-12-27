from RIG.src.Utils.prompts import prompt_json_gemma_v5
from RIG.src.Utils.utils import get_dict
from RIG.src.Utils.craeate_examples import CreateExamples
from RIG.globals import GLOBALS, MODELS


class Generation:
    """
    Generation class for predicting structured responses based on free-text input
    and schema information for a specific type.
    """

    def __init__(self):
        """
        Initialize the Generation instance.

        Sets up the database manager and example creation utility.
        """
        self.db_manager = GLOBALS.db_manager
        self.create_examples = CreateExamples()

    def predict(self, type_name: str, free_text: str, row_id: str = None) -> tuple:
        """
        Predict structured output based on free-text input and schema information.

        This method retrieves schema and description for the specified type,
        fetches relevant examples, and uses a language model to generate
        a structured response.

        Parameters:
            type_name (str): The type to classify the text under.
            free_text (str): The input free-text to analyze.
            row_id (str, optional): Row identifier for context (if available).

        Returns:
            tuple: (Generated response, schema, relevant examples)
        """
        # Retrieve schema and description from the database
        schema = self.db_manager.get_dict_features(
            type_name=type_name, feature="schema"
        )
        description = self.db_manager.get_dict_features(
            type_name=type_name, feature="description"
        )

        # Get relevant examples based on the query and type
        examples = self.create_examples.get_closest_question(
            question=free_text,
            type_name=type_name,
            row_id=row_id if row_id else None
        )

        # Generate the response using the language model
        response = MODELS.gemma_api.predict(
            prompt=prompt_json_gemma_v5(free_text, type_name, schema, description, examples)
        )

        return response, schema, examples

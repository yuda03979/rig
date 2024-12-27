from typing import Any, Tuple
from RIG.src.Utils.utils import get_dict
from RIG.globals import GLOBALS, MODELS


class Classification:
    """
    Classification class for predicting the closest matching type
    for a given query using RAG (Retrieval-Augmented Generation)
    and language models.
    """

    def __init__(self):
        """
        Initialize the Classification instance.
        """
        pass

    def predict(self, query: str) -> Tuple[Any, int, bool]:
        """
        Predict the best matching type for the provided query.

        This method attempts to classify the query using RAG first,
        and if unsuccessful, falls back to a language model.

        Parameters:
            query (str): The free-text query to classify.

        Returns:
            tuple: (Predicted type name, similarity score or error code, failure flag)
                   - If successful, returns type_name and similarity score.
                   - If unsuccessful, returns failure details.
        """
        # Attempt classification using RAG
        type_names_list, succeed = self.using_rag(query)
        if succeed:
            return type_names_list[0][0], type_names_list[0][1], False

        # If RAG fails, use the language model for classification
        type_name, succeed = self.using_model(query, type_names_list)
        if succeed:
            return type_name, -1, False

        # Classification failed
        return type_name, -2, True

    def using_rag(self, query: str) -> Tuple[list, bool]:
        """
        Classify the query using RAG to find the closest matching type.

        Parameters:
            query (str): The query to classify.

        Returns:
            tuple: (List of closest type names and their similarity scores, success flag)
        """
        succeed = False
        type_names_list = MODELS.rag_api.get_closest_type_name(query)
        closest_distance = type_names_list[0][1]
        difference = type_names_list[0][1] - type_names_list[1][1]

        # Validate based on threshold and difference
        if difference > GLOBALS.rag_difference and difference != float('inf'):
            if closest_distance > GLOBALS.rag_threshold:
                succeed = True

        # Handle case where only one type is detected
        if type_names_list[0][0] != 'None' and type_names_list[1][0] == 'None':
            succeed = True

        return type_names_list, succeed

    def using_model(self, query: str, type_names: list) -> Tuple[str, bool]:
        """
        Use the language model to classify the query by comparing two types.

        A prompt is generated based on schema and description of the two
        closest matching types. The model predicts the best match.

        Parameters:
            query (str): The query to classify.
            type_names (list): List of closest type names.

        Returns:
            tuple: (Predicted type name, success flag)
                   - Returns the predicted type if found in the database.
                   - Returns an error message if the model output is invalid.
        """
        # Retrieve schema and description for the top two type matches
        schema_a = GLOBALS.db_manager.get_dict_features(
            type_name=type_names[0][0], feature="schema"
        )
        description_a = GLOBALS.db_manager.get_dict_features(
            type_name=type_names[0][0], feature="description"
        )

        schema_b = GLOBALS.db_manager.get_dict_features(
            type_name=type_names[1][0], feature="schema"
        )
        description_b = GLOBALS.db_manager.get_dict_features(
            type_name=type_names[1][0], feature="description"
        )

        # Construct prompt for LLM
        prompt = f"""
        Analyze the following query:  
{query} <END>

Based on the query, choose which type is a better match from the two options provided. Use the schema and description as context for your decision.  

Option 1:  
- Name: {type_names[0][0]}  
- Schema: {schema_a}  
- Description: {description_a}  

Option 2:  
- Name: {type_names[1][0]}  
- Schema: {schema_b}  
- Description: {description_b}  

You must return ONLY ONE: either {{"type_name": "{type_names[0][0]}"}} or {{"type_name": "{type_names[1][0]}"}}.  

Note: it must be in json form!
Example of expected output:  
{{"type_name": "Hay_field"}}  

Actual output:
        """
        # Get prediction from model
        type_name = get_dict(MODELS.gemma_api.predict(prompt) + '}')[0]

        try:
            if type_name["type_name"] in GLOBALS.db_manager.get_all_types_names():
                return type_name["type_name"], True
        except Exception:
            return f'model did not generate well: {str(type_name)}', False

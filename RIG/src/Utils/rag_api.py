import json
import numpy as np
from RIG.globals import GLOBALS
from sklearn.metrics.pairwise import cosine_similarity


class RagApi:
    """
    RagApi class provides functionality for classifying free-text queries
    to the closest matching rule type using embeddings and cosine similarity.
    """

    def __init__(self):
        """
        Initialize the RagApi instance.

        Sets up the database manager and initializes rule type embeddings.
        """
        self.db_manager = GLOBALS.db_manager
        self.rule_types_embedding = self.init_rule_types_embeddings()

    def init_rule_types_embeddings(self) -> dict:
        """
        Initialize rule type embeddings by loading from the database.

        Iterates over all type names in the database and stores their embeddings.

        Returns:
            dict: A dictionary mapping type names to their embeddings.
        """
        rule_types_embeddings = {}
        for type_name in self.db_manager.get_all_types_names():
            rule_types_embeddings[type_name] = list(
                np.array(self.db_manager.get_embedding(type_name))
            )
        return rule_types_embeddings

    def add_rule_type_embedding(self, type_name: str, embedding: list) -> None:
        """
        Add a new rule type embedding to the existing embeddings.

        Parameters:
            type_name (str): The name of the rule type.
            embedding (list): The embedding to associate with the rule type.
        """
        self.rule_types_embedding[type_name] = embedding

    def get_embedding(self, text):
        """
        Generate an embedding for the provided text using the RAG model.

        Parameters:
            text (str or list): The text or list of text strings to embed.

        Returns:
            tuple: JSON representation of the embedding and the raw embedding list (for saving in csv).
        """
        if isinstance(text, list):
            text = ["classification:\n" + query for query in text]
        if isinstance(text, str):
            text = "classification:\n" + text

        # get embedding
        embedding = GLOBALS.ollamamia[GLOBALS.rag_model_name] << text
        embedding_json = json.dumps(embedding[0])
        return embedding_json, embedding

    def get_closest_type_name(self, query: str) -> list:
        """
        Classify a free-form query to the closest matching rule_type.

        This method calculates the similarity between the query embedding
        and rule type embeddings, returning the top matches.

        Parameters:
            query (str): The free-text query to classify.

        Returns:
            list: A sorted list of tuples with type names and similarity scores.
                  Includes 'None' for unmatched queries.
        """
        query = "classification" + query
        query_embedding = GLOBALS.ollamamia[GLOBALS.rag_model_name] << query
        query_embedding = query_embedding[0]

        # Prepare matrix of rule type embeddings
        type_names = list(self.rule_types_embedding.keys())
        embeddings_matrix = np.vstack([
            self.rule_types_embedding[type_name] for type_name in type_names
        ])

        # Calculate similarities using matrix multiplication
        similarities = embeddings_matrix @ query_embedding

        # Pair type names with their corresponding similarity scores
        types_names_result = {
            type_name: similarity
            for type_name, similarity in zip(type_names, similarities)
        }

        # Sort and prepare the result list
        types_names_result_list = sorted(
            types_names_result.items(),
            key=lambda item: item[1],
            reverse=True
        )

        # Add placeholders for unmatched types
        types_names_result_list.append(('None', 0))
        types_names_result_list.append(('None', -float('inf')))

        return types_names_result_list[:2]
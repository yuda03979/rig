from RIG.globals import GLOBALS
import json
import numpy as np
from RIG.globals import GLOBALS
from sklearn.metrics.pairwise import cosine_similarity


class RagApi:
    def __init__(self):
        self.db_manager = GLOBALS.db_manager
        self.rule_types_embedding = self.init_rule_types_embeddings()

    def init_rule_types_embeddings(self):
        rule_types_embeddings = {}
        # Example database of rule types
        for type_name in self.db_manager.get_all_types_names():
            rule_types_embeddings[type_name] = list(np.array(self.db_manager.get_embedding(type_name)))
        return rule_types_embeddings

    def add_rule_type_embedding(self, type_name, embedding):
        self.rule_types_embedding[type_name] = embedding

    def get_embedding(self, text):
        text = "classification:\n" + text
        embedding = GLOBALS.ollamamia[GLOBALS.rag_model_name] << text
        embedding_json = json.dumps(embedding[0])
        return embedding_json, embedding

    def get_closest_type_name(self, query: str):
        """
        Classifies a free-form query to the closest rule_type.
        :param query: The free-text
        :return: The closest type_name
        """
        query = "classification" + query
        query_embedding = GLOBALS.ollamamia[GLOBALS.rag_model_name] << query
        query_embedding = query_embedding[0]
        # Prepare matrix of rule type embeddings
        type_names = list(self.rule_types_embedding.keys())
        embeddings_matrix = np.vstack([self.rule_types_embedding[type_name] for type_name in type_names])

        # Calculate similarities using matrix multiplication
        similarities = embeddings_matrix @ query_embedding

        # Pair type names with their corresponding similarity scores
        types_names_resault = {type_name: similarity for type_name, similarity in zip(type_names, similarities)}

        # Sort and prepare the result list
        types_names_resault_list = sorted(types_names_resault.items(), key=lambda item: item[1], reverse=True)

        # Add placeholders for "None" types
        types_names_resault_list.append(('None', 0))
        types_names_resault_list.append(('None', -float('inf')))

        return types_names_resault_list[:2]
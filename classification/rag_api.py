from globals_dir.utils import handle_errors
from globals_dir.models import MODELS
from classification.utils import *
from sklearn.metrics.pairwise import cosine_similarity
from .prompts import prefix_document

class RagApi:
    def __init__(self, db_api):
        self.db_api = db_api
        self.rag_model = MODELS.embed_model

        self.rule_types_embedding: np.array
        self.rule_types_names: list
        self.rule_types_names, self.rule_types_embedding = self.init_rule_types_embeddings()

    def init_rule_types_embeddings(self):
        rule_types_names: list = self.db_api.get_col("type_name")
        rule_types_embedding: list = self.db_api.get_col("embedding")
        return rule_types_names, np.array(rule_types_embedding)

    def get_embedding(self, text: str, prefix_doc: str = prefix_document):
        text = prefix_doc + text
        embedding = MODELS.embed_model << text
        return embedding

    def get_batch_embeddings(self, list_texts: list[str], prefix_doc: str = prefix_document):
        list_texts = [prefix_doc + text for text in list_texts]
        embeddings = MODELS.embed_model << list_texts
        return embeddings

    def get_closest_type_name(
            self, query: str,
            *,
            prefix_query: str = '',
            len_response: int = 2,
            softmax: bool = False,
            temperature: float = 0
    ):
        """
        Classifies a free-form query to the closest rule_type.
        :param len_response:
        :param prefix_query:
        :param query: The free-text
        :return: list in shape [(type_name, similarity), ...] with length of len_response.
        """
        query = prefix_query + query
        query_embedding = MODELS.embed_model << query
        type_names_result_list = []

        if len(self.rule_types_names) < 1:
            handle_errors(e="no rule types provided")

        elif len(self.rule_types_names) == 1:
            array_similarity = cosine_similarity(query_embedding, self.rule_types_embedding)
            type_names_result_list = [
                (self.rule_types_names[0], array_similarity[0]),
            ]

        else:
            array_similarity = cosine_similarity(query_embedding, self.rule_types_embedding)[0]
            if softmax:
                array_similarity = softmax_with_temperature(logits=array_similarity, temperature=temperature)
            indexes = np.argsort(array_similarity)[::-1]
            type_names_result_list = [
                (self.rule_types_names[indexes[i]], array_similarity[indexes[i]]) for i in range(len(self.rule_types_names))
            ]

        [type_names_result_list.append(('None', -float('inf'))) for i in range(len_response)]
        # print(type_names_result_list[:len_response])
        return type_names_result_list[:len_response]

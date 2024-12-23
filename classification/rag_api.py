from globals_dir.utils import handle_errors
from globals_dir.models import MODELS
from classification.utils import *
from sklearn.metrics.pairwise import cosine_similarity
from .prompts import prefix_document


class RagApi:
    def __init__(self, db_api, text_to_find="type_name"):
        #  to do!! the db dont update!!!!!
        self.db_api = db_api

        self.text_embedding: np.array
        self.text: list
        self.text, self.text_embedding = self.init_text_embeddings(text_to_find)

    def init_text_embeddings(self, text_to_find="type_name"):
        text: list = self.db_api.get_col(text_to_find)
        text_embedding: list = self.db_api.get_col("embedding")
        return text, np.array(text_embedding)

    def get_embedding(self, query: str, prefix_doc: str = prefix_document):
        query = prefix_doc + query
        embedding = MODELS.embed_model << query  # inference
        return embedding

    def get_batch_embeddings(self, list_querys: list[str], prefix_doc: str = prefix_document):
        list_querys = [prefix_doc + query for query in list_querys]
        embeddings = MODELS.embed_model << list_querys
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

        if len(self.text) < 1:
            handle_errors(e="no rule types provided")

        elif len(self.text) == 1:
            array_similarity = cosine_similarity(query_embedding, self.text_embedding)
            type_names_result_list = [
                (self.text[0], array_similarity[0]),
            ]

        else:
            array_similarity = cosine_similarity(query_embedding, self.text_embedding)[0]
            if softmax:
                array_similarity = softmax_with_temperature(logits=array_similarity, temperature=temperature)
            indexes = np.argsort(array_similarity)[::-1]
            type_names_result_list = [
                (self.text[indexes[i]], array_similarity[indexes[i]]) for i in
                range(len(self.text))
            ]

        [type_names_result_list.append(('None', -float('inf'))) for i in range(len_response)]
        # print(type_names_result_list[:len_response])
        return type_names_result_list[:len_response]

    def update(self):
        # to do! change that to something more efficient
        self.__init__(self.db_api)

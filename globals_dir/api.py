from .globals import GLOBALS

from classification.rag_api import RagApi
from db.db_api import DBApi


class Api:

    def __init__(self):
        self.db_api_rule_types = DBApi(**GLOBALS.db_rule_types)
        self.db_api_examples = DBApi(**GLOBALS.db_examples)

        self.rag_api_classification = RagApi(self.db_api_rule_types, "type_name")
        self.rag_api_examples = RagApi(self.db_api_examples, "free_text")


API = Api()

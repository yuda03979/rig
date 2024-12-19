from .globals import GLOBALS

from classification.rag_api import RagApi
from db.db_api import DBApi


class Api:

    def __init__(self):
        self.db_api = DBApi(**GLOBALS.db_rule_types)
        self.rag_api = RagApi(self.db_api)


API = Api()

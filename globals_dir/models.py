from Ollamamia import Ollamamia
from .globals import GLOBALS


class Models:

    def __init__(self):
        self.ollamamia = None
        self.embed_model = None
        self.gemma = None

    def init(self):
        self.ollamamia = Ollamamia(on_docker=False)
        self.embed_model = self.ollamamia.model.embed(model_name=GLOBALS.embed_model_path)
        self.gemma = self.ollamamia.model.generate(model_name=GLOBALS.gemma_model_path)


MODELS = Models()
MODELS.init()

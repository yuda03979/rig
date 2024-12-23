from generation.generate_model import GenerateModel
from classification.embed_model import EmbedModel


class Models:

    def __init__(self):
        self.embed_model = None
        self.generate_model = None

    def init(self):
        self.embed_model = EmbedModel().init()
        self.generate_model = GenerateModel().init()


MODELS = Models()
MODELS.init()

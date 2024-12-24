from generation.generate_model import GenerateModel
from classification.embed_model import EmbedModel

from Ollamamia.src.ollamamia import Ollamamia


class Models:

    def __init__(self):

        self.ollamamia = Ollamamia()

        self.rag_model = "snowflake-arctic-embed:137m"
        rag_model_config = self.ollamamia.model_config(model_name=self.rag_model, task="embed")
        self.ollamamia[self.rag_model] = rag_model_config

        self.gemma_model = "gemma2:2b"
        gemma_model_config = self.ollamamia.model_config(model_name=self.gemma_model, task="generate")
        gemma_model_config.keep_alive = -1
        gemma_model_config.format = "json"
        gemma_model_config.options.temperature = 0.1
        gemma_model_config.options.top_p = 1.0
        gemma_model_config.options.num_ctx = 2048
        gemma_model_config.options.num_predict = 300
        self.ollamamia[self.gemma_model] = gemma_model_config


MODELS = Models()

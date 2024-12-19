from .init_ollama import InitOllama
from .model import Model
from .funcs import Funcs
from .chitchat import ChitChat


class Ollamamia(InitOllama):

    def __init__(self, on_docker=True):
        super().__init__(on_docker=on_docker)
        self.funcs = Funcs()
        self.model = Model()

    def ChitChat(self, model_name, prompt=None):
        ChitChat(model_name, prompt)

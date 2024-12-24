from .core.model_config import ModelConfig
from .core.models_control import ModelsControl
from .core.model import Model
from .globals_dir.globals import GLOBALS


class Ollamamia:
    def __init__(self, models_location=GLOBALS.default_ollama_folder):
        GLOBALS.init()
        self.model_config = ModelConfig
        self._models_control = ModelsControl()

    def add(self, model_name, model_config: ModelConfig):
        model = Model(model_name=model_name, task=model_config.task)
        model.config = model_config
        self._models_control.add(model_name, model)

    def infer(self, model_name, query):
        return self._models_control.models[model_name].infer(query)

    def __getitem__(self, key):
        if key not in self._models_control.models:
            raise KeyError(f"Model '{key}' not found.")
        return self._models_control.models[key]

    def __setitem__(self, key, model_config):
        self.add(key, model_config)

    def stop(self):
        pass

    def ps(self):
        pass

    def chitchat(self):
        pass

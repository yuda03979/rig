from globals_dir.globals import GLOBALS


class EmbedModel:

    def __init__(self):
        # to do! to init the model from local
        self.model_name = GLOBALS.embed_model_path
        self.config = GLOBALS.ollamamia.model_config


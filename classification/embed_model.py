from globals_dir.globals import GLOBALS


class EmbedModel:

    def __init__(self):
        # to do! to init the model from local
        self.model_name = GLOBALS.embed_model_path
        self.params = GLOBALS.ollamamia.params
        self.params.keep_alive = -1

    def init(self):
        model = GLOBALS.ollamamia.model.embed(model_name=self.model_name)
        model.update_params(self.params)
        return model

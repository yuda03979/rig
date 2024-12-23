from globals_dir.globals import GLOBALS


class GenerateModel:

    def __init__(self):
        # to do! -> initiate the model.
        self.model_name = GLOBALS.gemma_model_path
        self.params = GLOBALS.ollamamia.params

        self.params.keep_alive = -1
        self.params.format = "json"
        self.params.options.temperature = 0.1
        self.params.options.top_p = 1.0
        self.params.options.num_ctx = 2048
        self.params.options.num_predict = 300

    def init(self):
        model = GLOBALS.ollamamia.model.generate(model_name=self.model_name)
        model.update_params(self.params)
        return model
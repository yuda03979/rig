import os

from dotenv import find_dotenv, load_dotenv
from RIG.src.Utils.db_manager import DBManager
from ollama import Client

class Globals:
    # these is in purpose not in the .env
    gemma_model_name = "gemma-2-2b-it-Q8_0:rig"
    rag_model_name = "snowflake-arctic-embed-137m:rig"
    def __init__(self):
        load_dotenv(find_dotenv())
        self.project_directory = self.validate_path("PROJECT_DIRECTORY")
        self.evaluation_directory = self.validate_path("EVALUATION_DIRECTORY")
        self.rule_types_directory = self.validate_path("RULE_TYPES_DIRECTORY")
        self.rag_difference = self.validate_numeric("RAG_DIFFERENCE", float)
        self.rag_threshold = self.validate_numeric("RAG_THRESHOLD", float)
        self.temperature = self.validate_numeric("TEMPERATURE", float)
        self.top_p = self.validate_numeric("TOP_P", float)
        self.max_context_length = self.validate_numeric("MAX_CONTEXT_LENGTH", int)
        self.max_new_tokens = self.validate_numeric("MAX_NEW_TOKENS", int)


        self.db_manager = DBManager(os.path.join(self.project_directory, "db_data.csv"))

        self.db_examples_path = os.path.join(self.project_directory, "db_examples.csv")
        self.df_eval_path = os.path.join(self.evaluation_directory, "data_eval.csv")
        self.eval_output_dir = os.path.join(self.evaluation_directory, "output")


        self.ollama_client = Client()


        self.gemma_model_params = {
            "model": self.gemma_model_name,
            "prompt": "",  # fill every time
            "keep_alive": -1,  # the model keep load forever.
            "options": {"temperature": self.temperature, "top_p": self.top_p, "stop": ["}"], "num_ctx": self.max_context_length, "num_predict": self.max_new_tokens}
        }
        self.gemma_model = self.ollama_client.generate

        self.rag_model_params = {"model": self.rag_model_name, "input": []}   # fill prompt every time
        self.rag_model = self.ollama_client.embed

        # try:
        #     ollama.pull(self.rag_model_name)
        #     ollama.pull(self.gemma_model_name)
        # except:
        #     pass

    def validate_path(self, var_name):
        value = os.getenv(var_name)
        if not value or not os.path.exists(value):
            raise ValueError(f"{var_name} is not set or the path does not exist: {value}")
        return value

    def validate_numeric(self, var_name, value_type):
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"{var_name} is not set")
        try:
            return value_type(value)
        except ValueError:
            raise ValueError(f"{var_name} must be a valid {value_type.__name__}")


GLOBALS = Globals()


class Models:

    def __init__(self):
        self.rag_api = None
        self.gemma_api = None

MODELS = Models()
import os
import logging
from dotenv import find_dotenv, load_dotenv
from ollamamia import Ollamamia
from RIG.src.Utils.db_manager import DBManager

load_dotenv(find_dotenv())


def validate_path(env_var, var_name):
    """Validate and return the path or None if invalid."""
    if not env_var or not os.path.exists(env_var):
        logging.error(f"Warning: {var_name} is invalid or does not exist: {env_var}")
    return env_var


def validate_numeric(env_var, var_name, cast_func, default=None):
    try:
        return cast_func(env_var) if env_var else default
    except ValueError:
        logging.error(f"Warning: {var_name} is invalid: {env_var}")
        return default


class Globals:
    gemma_model_name = "gemma2:2b-instruct-q8_0"
    rag_model_name = "snowflake-arctic-embed:137m"
    def __init__(self):
        self.project_directory = validate_path(os.getenv("PROJECT_DIRECTORY"), "PROJECT_DIRECTORY")
        self.rule_types_directory = validate_path(os.getenv("RULE_TYPES_DIRECTORY"), "RULE_TYPES_DIRECTORY")
        self.rag_difference = validate_numeric(os.getenv("RAG_DIFFERENCE"), "RAG_DIFFERENCE", float)
        self.rag_threshold = validate_numeric(os.getenv("RAG_THRESHOLD"), "RAG_THRESHOLD", float)
        self.temperature = validate_numeric(os.getenv("TEMPERATURE"), "TEMPERATURE", float)
        self.top_p = validate_numeric(os.getenv("TOP_P"), "TOP_P", float)
        self.max_context_length = validate_numeric(os.getenv("MAX_CONTEXT_LENGTH"), "MAX_CONTEXT_LENGTH", int)
        self.max_new_tokens = validate_numeric(os.getenv("MAX_NEW_TOKENS"), "MAX_NEW_TOKENS", int)

        self.db_manager = DBManager(os.path.join(self.project_directory, "db_data.csv"))

        self.ollamamia = Ollamamia()

        # this is the rag_model
        self.rag_model = self.rag_model_name
        rag_model_config = self.ollamamia.model_config(model_name=self.rag_model, task="embed")
        self.ollamamia[self.rag_model:rag_model_config]

        # this is gemma model
        self.gemma_model = self.gemma_model_name
        gemma_model_config = self.ollamamia.model_config(model_name=self.gemma_model, task="generate")
        gemma_model_config.keep_alive = -1
        gemma_model_config.options.stop = ["}"]
        gemma_model_config.options.temperature = 0.1
        gemma_model_config.options.top_p = self.top_p
        gemma_model_config.options.num_ctx = self.max_context_length
        gemma_model_config.options.num_predict = self.max_new_tokens
        self.ollamamia[self.gemma_model:gemma_model_config]


GLOBALS = Globals()

class Models:

    def __init__(self):
        self.rag_api = None
        self.gemma_api = None

MODELS = Models()
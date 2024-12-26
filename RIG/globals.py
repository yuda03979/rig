import os
import logging

import ollama
from dotenv import find_dotenv, load_dotenv
from ollamamia import Ollamamia
from RIG.src.Utils.db_manager import DBManager


class Globals:
    gemma_model_name = ["gemma-2-2b-it-Q8_0", "hermes3:3b", "gemma2:2b-instruct-q8_0", "granite3-dense", "stablelm-zephyr:3b", "dolphin-phi", "internlm2:1.8b"][0]
    #                   good            ours                        good-
    rag_model_name = "snowflake-arctic-embed:137m"
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
        self.df_eval_path = os.path.join(self.evaluation_directory, "data_yuda.csv")
        self.eval_output_dir = os.path.join(self.evaluation_directory, "output")

        self.ollamamia = Ollamamia()

        # this is the rag_model
        self.rag_model = self.rag_model_name
        rag_model_config = self.ollamamia.model_config(model_name=self.rag_model, task="embed")
        rag_model_config.pull = True
        self.ollamamia[self.rag_model] = rag_model_config

        # this is gemma model
        self.gemma_model = self.gemma_model_name
        gemma_model_config = self.ollamamia.model_config(model_name=self.gemma_model, task="generate")
        gemma_model_config.pull = True
        gemma_model_config.keep_alive = -1
        gemma_model_config.options.stop = ["}"]
        gemma_model_config.options.temperature = 0.1
        gemma_model_config.options.top_p = self.top_p
        gemma_model_config.options.num_ctx = self.max_context_length
        gemma_model_config.options.num_predict = self.max_new_tokens
        self.ollamamia[self.gemma_model] = gemma_model_config

        try:
            ollama.pull(self.rag_model_name)
            ollama.pull(self.gemma_model_name)
        except:
            pass

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
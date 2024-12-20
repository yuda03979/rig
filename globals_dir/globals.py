import os
import logging

from dotenv import find_dotenv, load_dotenv

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

    def __init__(self):
        self.project_directory = validate_path(os.getenv("PROJECT_DIRECTORY"), "PROJECT_DIRECTORY")
        self.gemma_model_path = validate_path(os.getenv("GEMMA_MODEL_PATH"), "GEMMA_MODEL_PATH")
        self.embed_model_path = validate_path(os.getenv("EMBED_MODEL_PATH"), "EMBED_MODEL_PATH")
        self.rule_types_directory = validate_path(os.getenv("RULE_TYPES_DIRECTORY"), "RULE_TYPES_DIRECTORY")
        self.rag_difference = validate_numeric(os.getenv("RAG_DIFFERENCE"), "RAG_DIFFERENCE", float)
        self.rag_threshold = validate_numeric(os.getenv("RAG_THRESHOLD"), "RAG_THRESHOLD", float)
        self.max_context_length = validate_numeric(os.getenv("MAX_CONTEXT_LENGTH"), "MAX_CONTEXT_LENGTH", int)
        self.max_new_tokens = validate_numeric(os.getenv("MAX_NEW_TOKENS"), "MAX_NEW_TOKENS", int)

        self.db_rule_types = {
            "db_path": str(os.path.join(self.project_directory, "db_rule_types.csv")),
            "columns_names": [
                "type_name",
                "schema",
                "description",
                "default_values",
                "default_rule_instance",
                "rule_type",
                "embedding"
            ]
        }


GLOBALS = Globals()

from globals_dir.api import API
from globals_dir.models import MODELS
from .prompts import prompt_json_gemma_v6
from .prompt_examples import PromptExamples


class Generator:

    def __init__(self):
        self.prompt_examples = PromptExamples()

    def predict(self, type_name, free_text):
        schema = API.db_api_rule_types.get_index((type_name, "schema"))
        description = API.db_api_rule_types.get_index((type_name, "description"))
        examples = self.prompt_examples.get_closest_question(query=free_text, type_name=type_name)
        response = MODELS.generate_model << prompt_json_gemma_v6(free_text, type_name, schema, description, examples)
        return response, schema

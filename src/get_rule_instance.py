from classification.classifier import Classifier
from generation.generator import Generator
from post_processing.pp import post_processing
from post_processing.utils import get_dict


class GetRuleInstance:

    def __init__(self):
        self.classifier = Classifier()
        self.generator = Generator()

    def predict(self, free_text):

        response = {
            "rule_instance": None,
            "is_error": True,
            "error_message": "",
            "free_text": free_text,
            "type_name": None,
            "rag_score": None,
            "model_response": None,
            "schema": None
        }

        response["type_name"], response["rag_score"], is_error = self.classifier.predict(free_text)
        if is_error:
            response["error_message"] = "error! can't identify ruleType. no ruleType exist or didnt pass the threshold."
            return response

        response["model_response"], response["schema"] = self.generator.predict(response["type_name"], free_text)
        model_response, succeed = get_dict(response["model_response"])

        # if did not succeed, we give it to the model back, only one time.
        if not succeed:
            response["model_response"], _ = self.generator.predict(response["type_name"], response["model_response"])
            model_response, succeed = get_dict(response["model_response"])
        if not succeed:
            response["error_message"] = "error! can't extract json from model response"
            return response

        response["rule_instance"] = post_processing(response["type_name"], model_response)
        response["is_error"] = False
        return response


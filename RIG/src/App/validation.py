import json
from typing import Union
from RIG.src.Utils.utils import get_dict
import pandas as pd
import re
import time
from RIG.src.Utils.prompts import validation_prompt_v2, validation_prompt_v3, validation_prompt_v4, validation_prompt_v5, analyze_prompt_v5
from RIG.globals import GLOBALS


class Validation:
    def __init__(self):
        pass

    def get_score(self, free_text: str, type_name: str, schema, description, llm_response: dict):
        """
        model should generate score between 0 - 1
        """
        prompt = validation_prompt_v5(free_text, type_name, schema, description, str(llm_response))
        model_params = GLOBALS.validation_model_params
        model_params["prompt"] = prompt
        output_text = GLOBALS.validation_model(**model_params)['response']
        print(f"Model output: {output_text}")
        output_text = get_dict(output_text + "}")[0]
        print(f"Model output: {type(output_text)}")

        try:
            output_text = int(output_text["score"])
        except:
            output_text = -1
        return output_text
        # Using same output processing as original
        # print(f"Model output: {output_text}")
        #
        #
        # match = re.findall(r'\b([1-9][0-9]?|100)\b', output_text)
        # if match:
        #     score = int(match[-1])
        #     return max(1, min(100, score))
        # else:
        #     print("Warning: No valid score found in model output.")
        #     return 0

    def validation_results(self):
        # to do!!
        results_df = pd.read_csv('evaluation_results.csv')

        for index, row in results_df.iterrows():
            current_time = time.time()
            print(f"Processing row {index + 1}/{len(results_df)}")
            local_score = self.get_score(row['free_text'], row['response'])
            print(f"GPT Score: {row['gpt_score']}, Local Model Score: {local_score}")
            results_df.loc[index, 'local_model'] = local_score
            elapsed_time = time.time() - current_time
            results_df.loc[index, 'processing_time'] = elapsed_time
            print(elapsed_time)

        results_df.to_csv('evaluation_results_with_local.csv', index=False)


    def analyze(self, free_text: str, type_name: str, schema, description, llm_response: dict):
        prompt = analyze_prompt_v5(free_text, type_name, schema, description, str(llm_response))
        model_params = GLOBALS.validation_model_params
        model_params["prompt"] = prompt
        output_text = GLOBALS.validation_model(**model_params)['response']
        return output_text

    def generate(self, free_text: str, type_name: str, schema, description, llm_response: dict):
        """
        model should generate score between 0 - 1
        """
        prompt = validation_prompt_v5(free_text, type_name, schema, description, str(llm_response), eval=str(self.analyze(free_text, type_name, schema, description, llm_response)))
        print(prompt)
        model_params = GLOBALS.validation_model_params
        model_params["prompt"] = prompt
        output_text = GLOBALS.validation_model(**model_params)['response']
        return output_text + "}"




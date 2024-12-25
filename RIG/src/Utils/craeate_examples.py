import os
import csv
import re
import ast
import json
import yaml
import numpy as np
from yaml import SafeLoader
from datetime import datetime
from RIG.globals import GLOBALS,MODELS
from datetime import datetime
import pandas as pd



class CreateExamples:
    def __init__(self):
        """
        Initialize the CreateExamples with the RAG API and log file.
        :param log_file: The path to the CSV log file.
        """
        self.rag_api = MODELS.rag_api
        self.log_dir = os.path.join(GLOBALS.project_directory, 'logs')
        self.log_file = os.path.join(self.log_dir,"logs_examples5.csv")


    def clean_text(self,text):
        """Remove all non-alphanumeric characters and convert to lowercase."""
        return ''.join(char.lower() for char in text if char.isalnum())

    #
    # def get_closest_question(self, question, type_name, row_id = None):
    #     """
    #     Find the closest two questions in the log file to the given question.
    #     :return: A dictionary containing the two closest questions, answers, and distances.
    #     """
    #     print("id =",row_id)
    #     if not os.path.exists(self.log_file) or os.stat(self.log_file).st_size == 0:
    #         print("Log file is empty or does not exist.")
    #         return {"example_1": {"free_text":None}, "example_2": {"free_text":None}}
    #
    #     # Generate embedding for the input question
    #     _, query_embedding = self.rag_api.get_embedding(question)
    #
    #     # Initialize placeholders for the top two closest matches
    #     closest = {"distance": -float("inf"), "free_text": None, "response": None, "response_id": None, "type_name": None}
    #     second_closest = {"distance": -float("inf"), "free_text": None, "response": None, "response_id": None,
    #                       "type_name": None}
    #
    #     # Read the log file and calculate similarity
    #     with open(self.log_file, mode="r", newline="", encoding="utf-8") as file:
    #         reader = csv.DictReader(file)
    #
    #         for row in reader:
    #             logged_embedding = np.array(json.loads(row["Embedding"]))
    #             distance = query_embedding @ logged_embedding.T
    #             if row_id:
    #                 match = re.search(r'D(\d+)Q', row_id)
    #                 id_dict_qust = match.group(1) if match else None
    #
    #                 match = re.search(r'D(\d+)Q', row["id"])
    #                 id_dict_resp = match.group(1) if match else None
    #
    #             # Check if this row is closer than the current closest match
    #             if distance > closest["distance"] and self.clean_text(type_name)  != self.clean_text(row["Type_Name"]):
    #                 if distance > second_closest["distance"]:
    #                     if row_id:
    #                         match = re.search(r'D(\d+)Q', row_id)
    #                         id_dict_qust = match.group(1) if match else None
    #
    #                         match = re.search(r'D(\d+)Q', row["id"])
    #                         id_dict_resp = match.group(1) if match else None
    #                         if id_dict_qust != id_dict_resp:
    #                             second_closest = closest.copy()
    #                     else:
    #                         second_closest = closest.copy()
    #
    #                 # Update closest with the new closest match
    #                 closest = {
    #                     "distance": distance,
    #                     "free_text": row["Question"],
    #                     "response": row["Answer"],
    #                     "response_id": row["id"],
    #                     "type_name": row["Type_Name"],
    #                 }
    #             # Check if this row is closer than the current second_closest
    #             elif distance > second_closest["distance"] and row["id"] != closest["response_id"] and id_dict_qust != id_dict_resp if row_id else True:
    #
    #                 second_closest = {
    #                     "distance": distance,
    #                     "free_text": row["Question"],
    #                     "response": row["Answer"],
    #                     "response_id": row["id"],
    #                     "type_name": row["Type_Name"],
    #                 }
    #     # Prepare the output examples
    #     examples = {
    #         "example_1": closest,
    #         "example_2": second_closest,
    #     }
    #     print(examples)
    #     return examples
    #
    # def get_closest_type_name(
    #         self, query: str,
    #         *,
    #         prefix_query: str = '',
    #         len_response: int = 2,
    #         softmax: bool = False,
    #         temperature: float = 0
    # ):
    #     """
    #     Classifies a free-form query to the closest rule_type.
    #     :param len_response:
    #     :param prefix_query:
    #     :param query: The free-text
    #     :return: list in shape [(type_name, similarity), ...] with length of len_response.
    #     """
    #     query = prefix_query + query
    #     query_embedding = MODELS.embed_model << query
    #     type_names_result_list = []
    # 
    #     if len(self.text) < 1:
    #         handle_errors(e="no rule types provided")
    # 
    #     elif len(self.text) == 1:
    #         array_similarity = cosine_similarity(query_embedding, self.text_embedding)
    #         type_names_result_list = [
    #             (self.text[0], array_similarity[0]),
    #         ]
    # 
    #     else:
    #         array_similarity = cosine_similarity(query_embedding, self.text_embedding)[0]
    #         if softmax:
    #             array_similarity = softmax_with_temperature(logits=array_similarity, temperature=temperature)
    #         indexes = np.argsort(array_similarity)[::-1]
    #         type_names_result_list = [
    #             (self.text[indexes[i]], array_similarity[indexes[i]]) for i in
    #             range(len(self.text))
    #         ]
    # 
    #     [type_names_result_list.append(('None', -float('inf'))) for i in range(len_response)]
    #     # print(type_names_result_list[:len_response])
    #     return type_names_result_list[:len_response]
    def get_closest_question(self, question, type_name, row_id=None):
        """
        Find the closest two questions in the log file to the given question.
        :return: A dictionary containing the two closest questions, answers, and distances.
        """
        print("id =", row_id)
        if not os.path.exists(self.log_file) or os.stat(self.log_file).st_size == 0:
            print("Log file is empty or does not exist.")
            return {"example_1": {"free_text": None}, "example_2": {"free_text": None}}

        # Generate embedding for the input question
        _, query_embedding = self.rag_api.get_embedding(question)

        # Load the log file into memory
        rows = []
        embeddings = []

        with open(self.log_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
                embeddings.append(np.array(json.loads(row["Embedding"])))

        # Stack all embeddings into a matrix
        log_embeddings = np.vstack(embeddings)

        # Compute cosine similarity between the query and all logged embeddings
        array_similarity = query_embedding @ log_embeddings.T

        # Initialize placeholders for the top two closest matches
        closest = {"distance": -float("inf"), "free_text": None, "response": None, "response_id": None,
                   "type_name": None}
        second_closest = {"distance": -float("inf"), "free_text": None, "response": None, "response_id": None,
                          "type_name": None}

        # Iterate over rows to find the closest and second closest matches
        for idx, row in enumerate(rows):
            distance = array_similarity[idx]

            # Match ID for question and response
            id_dict_qust = None
            id_dict_resp = None
            if row_id:
                match = re.search(r'D(\d+)Q', row_id)
                id_dict_qust = match.group(1) if match else None

                match = re.search(r'D(\d+)Q', row["id"])
                id_dict_resp = match.group(1) if match else None

            # Check if this row is closer than the current closest match
            if distance > closest["distance"] and self.clean_text(type_name) != self.clean_text(row["Type_Name"]):
                if distance > second_closest["distance"]:
                    if row_id and id_dict_qust != id_dict_resp:
                        second_closest = closest.copy()
                    else:
                        second_closest = closest.copy()

                # Update closest with the new closest match
                closest = {
                    "distance": distance,
                    "free_text": row["Question"],
                    "response": row["Answer"],
                    "response_id": row["id"],
                    "type_name": row["Type_Name"],
                }

            # Check if this row is closer than the current second_closest
            elif distance > second_closest["distance"] and row["id"] != closest["response_id"]:
                if not row_id or id_dict_qust != id_dict_resp:
                    second_closest = {
                        "distance": distance,
                        "free_text": row["Question"],
                        "response": row["Answer"],
                        "response_id": row["id"],
                        "type_name": row["Type_Name"],
                    }

        # Prepare the output examples
        examples = {
            "example_1": closest,
            "example_2": second_closest,
        }
        return examples

import os
import csv
import re
import json
import numpy as np
from RIG.globals import GLOBALS, MODELS


class CreateExamples:
    def __init__(self):
        """
        Initialize the CreateExamples with the RAG API and log file.
        :param log_file: The path to the CSV log file.
        """

        self.rag_api = MODELS.rag_api
        self.log_file = GLOBALS.db_examples_path

    def clean_text(self, text):
        """Remove all non-alphanumeric characters and convert to lowercase."""
        return ''.join(char.lower() for char in text if char.isalnum())

    def get_closest_question(self, question, type_name, row_id=None):
        """
        Find the closest two questions in the log file to the given question.
        :return: A dictionary containing the two closest questions, answers, and distances.
        """
        # print("id =", row_id)
        if not os.path.exists(self.log_file) or os.stat(self.log_file).st_size == 0:
            print("Log file is empty or does not exist.")
            return {"example_1": {"free_text": None}, "example_2": {"free_text": None}}

            # Generate embedding for the input question
        _, query_embedding = self.rag_api.get_embedding(question)

        # Ensure query_embedding is a 1D vector
        query_embedding = np.array(query_embedding).squeeze()

        # Load the log file into memory
        rows = []
        embeddings = []

        with open(self.log_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
                embeddings.append(np.array(json.loads(row["Embedding"])))

        # Stack all embeddings into a matrix
        log_embeddings = np.vstack([np.array(json.loads(row["Embedding"])) for row in rows])

        # Debugging shapes

        # Compute cosine similarity between the query and all logged embeddings
        array_similarity = query_embedding @ log_embeddings.T

        # Initialize placeholders for the top two closest matches
        closest = {"distance": -float("inf"), "free_text": None, "response": None, "response_id": None,
                   "type_name": None}
        second_closest = {"distance": -float("inf"), "free_text": None, "response": None, "response_id": None,
                          "type_name": None}
        # Iterate over rows to find the closest and second closest matches
        for idx, row in enumerate(rows):
            if not isinstance(array_similarity[idx], (int, float)):
                raise ValueError(f"Invalid distance value: {array_similarity[idx]}")
            distance = array_similarity[idx]
            # Match ID for question and response
            id_dict_qust = None
            id_dict_resp = None
            if row_id and row["row_id"]:
                match = re.search(r'D(\d+)Q', row_id)
                id_dict_qust = match.group(1) if match else None

                match = re.search(r'D(\d+)Q', row["row_id"])
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
                    "response_id": row["row_id"],
                    "type_name": row["Type_Name"],
                }

            # Check if this row is closer than the current second_closest
            elif distance > second_closest["distance"] and row["row_id"] != closest["response_id"]:
                if not row_id or id_dict_qust != id_dict_resp:
                    second_closest = {
                        "distance": distance,
                        "free_text": row["Question"],
                        "response": row["Answer"],
                        "response_id": row["row_id"],
                        "type_name": row["Type_Name"],
                    }

        # Prepare the output examples
        examples = {
            "example_1": closest,
            "example_2": second_closest,
        }
        # print ("examples = ",examples)
        return examples
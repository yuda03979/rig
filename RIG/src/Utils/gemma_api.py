import random
import os
import numpy as np
import torch
from RIG.globals import GLOBALS

torch.set_num_threads(4)
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)


class GemmaApi:
    """this class is if you want to change the way of communicating with the model."""

    def __init__(self):
        pass


    def predict(self, prompt) -> str:
        gemma_model_params = GLOBALS.gemma_model_params
        gemma_model_params["prompt"] = prompt
        response = GLOBALS.gemma_model(**gemma_model_params)
        # since the model should not generate } in the end:
        return response['response'] + "}"

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
        # inference
        response = GLOBALS.ollamamia[GLOBALS.gemma_model_name] << prompt
        # since the model should not generate } in the end:
        return response + "}"

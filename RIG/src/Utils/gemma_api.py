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

    def __init__(self):
        pass


    def predict(self, prompt) -> str:
        response = GLOBALS.ollamamia[GLOBALS.gemma_model_name] << prompt
        return response + "}"

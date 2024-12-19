import numpy as np

def softmax_with_temperature(logits, temperature=1.0):
    logits = np.array(logits)
    scaled_logits = logits / temperature
    exps = np.exp(scaled_logits - np.max(scaled_logits))  # Stability adjustment
    return exps / np.sum(exps)

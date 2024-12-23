from ollama import Client


class Globals:
    len_logs = 100  # history for each model

    def __init__(self):
        self.client = Client(host='http://localhost:11434')


GLOBALS = Globals()

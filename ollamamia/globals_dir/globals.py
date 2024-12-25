from ollama import Client


class Globals:
    len_logs = 100
    available_tasks = ["null", "generate", "chat", "stream_chat", "embed"]
    default_ollama_folder = "~/. ollama/models"  # where to save to download models

    def __init__(self, ollama_folder=None):
        if ollama_folder:
            self.default_ollama_folder = ollama_folder
        self.client = Client()


GLOBALS = Globals()

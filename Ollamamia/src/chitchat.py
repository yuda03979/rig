from enum import Enum
import ollama
from .funcs import *
from .utils import *
from .model import Chat, Role


class ChitChat(Chat):

    def __init__(self, model_name, prompt=None):
        super().__init__(model_name, prompt)
        while True:
            query = self.get_user_text()
            if not query:
                break
            self.infer(query)

    def infer(self, query) -> str:
        self._add_step(role=Role.USER, content=query)
        response = self.chat_stream(messages=self.messages)
        self._add_step(role=Role.ASSISTANT, content=response)
        return response

    def get_user_text(self):
        try:
            user_input = input_with_placeholder()
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("exiting...")
                return False
            return user_input
        except (EOFError, KeyboardInterrupt):
            print("exiting...")
            return False

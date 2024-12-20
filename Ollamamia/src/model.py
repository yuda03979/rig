from enum import Enum
from typing import Union, Sequence, Optional, Literal, Mapping, Any
from pydantic.json_schema import JsonSchemaValue
from pydantic import BaseModel
import ollama
from .funcs import *
from .utils import *
from .params import Params
from .globals import GLOBALS


class Role(Enum):
    USER = -1
    ASSISTANT = 0
    SYSTEM = 'a'


###########################

class TemplateModel:

    def __init__(
            self,
            model_name,
    ):

        self.params = Params()
        self.model_name = model_name
        self.logs = []

    def _manage_logs(self, response):
        if len(self.logs) >= GLOBALS.len_logs:
            self.logs.pop(0)
        self.logs.append(response)

    def chat_stream(self, messages: list[dict]):
        response = ''
        for part in ollama.chat(self.model_name, messages=messages, stream=True):
            response += part['message']['content']
            print(part['message']['content'], end='', flush=True)
        return response

    def chat(self, messages: list[dict]):
        response = ollama.chat(
            model=self.model_name,
            messages=messages
        )

        self._manage_logs(response)
        return response.message.content

    def embed(self, query: Union[str, Sequence[str]]):
        response = ollama.embed(model=self.model_name, input=query)
        self._manage_logs(response)
        return response['embeddings']

    def generate(self, query):
        response = ollama.generate(
            model=self.model_name,
            prompt=query,
            suffix=self.params.suffix,
            system=self.params.system,
            template=self.params.template,
            context=self.params.context,
            raw=self.params.raw,
            format=self.params.format,
            keep_alive=self.params.keep_alive,
            options=self.params.options.__dict__
        )
        self._manage_logs(response)
        return response['response']

    def update_params(self, other: Union[dict, Params]):
        if isinstance(other, Params):
            self.params = other
        else:
            for key, value in other.items():
                if hasattr(self.params, key):
                    setattr(self.params, key, value)

    def infer(self, query):
        # overwrite
        pass

    def __lshift__(self, query):
        return self.infer(query)

    def __le__(self, other: Union[dict, Params]):
        self.update_params(other)
        return True

    def stop(self):
        self.params.keep_alive = 0
        self.infer("generate: i'm dying!!")
        return True


############################

class Chat(TemplateModel):

    def __init__(self, model_name, prompt=None):
        super().__init__(model_name)
        self.messages = []
        self.prompt = prompt
        self._init_prompt()

    def _init_prompt(self):
        if self.prompt:
            self.messages.append({'role': 'assistant', 'content': self.prompt})

    def _add_step(self, role: Role, content: str):
        message = {
            "role": role.name.lower(),
            "content": content
        }
        self.messages.append(message)

    def infer(self, query) -> str:
        self._add_step(role=Role.USER, content=query)
        response = self.chat(messages=self.messages)
        self._add_step(role=Role.ASSISTANT, content=response)
        return response


############################

class Embed(TemplateModel):

    def __init__(self, model_name, prefix=None):
        super().__init__(model_name)
        self.messages = []
        self.prefix = prefix

    def infer(self, query: Union[str, Sequence[str]]) -> list[list]:
        return self.embed(query)


###############################

class Generate(TemplateModel):

    def __init__(
            self,
            model_name
    ):
        super().__init__(model_name)

    def infer(self, query):
        return self.generate(query)


class Model:

    def __init__(self):
        pass

    def chat(self, model_name):
        return Chat(model_name)

    def generate(self, model_name):
        return Generate(model_name)

    def embed(self, model_name):
        return Embed(model_name)

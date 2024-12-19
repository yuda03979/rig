from enum import Enum
from typing import Union, Sequence, Optional, Literal, Mapping, Any
from pydantic.json_schema import JsonSchemaValue
from pydantic import BaseModel
import ollama
from .funcs import *
from .utils import *
from .core._types import Options

from .globals import GLOBALS


class Role(Enum):
    USER = 1
    ASSISTANT = 2


###########################

class TemplateModel:

    def __init__(
            self,
            model_name,
            docker=False,
            suffix: str = '',
            *,
            system: str = '',
            template: str = '',
            context: Optional[Sequence[int]] = None,
            stream: Literal[True] = True,
            raw: bool = False,
            format: Optional[Union[Literal['', 'json'], JsonSchemaValue]] = None,
            images: Optional[Sequence[Union[str, bytes]]] = None,
            options: Optional[Union[Mapping[str, Any], Options]] = None,
            keep_alive: Optional[Union[float, str]] = None,
    ):
        """
         see https://github.com/ollama/ollama/blob/main/docs/modelfile.md#valid-parameters-and-values for details
        """
        self.model_name = model_name
        self.logs = []

        self.docker = docker
        self.suffix: suffix
        self.system = system
        self.template = template
        self.context = context
        self.stream = stream
        self.raw = raw
        self.format = format
        self.images = images
        self.options = options
        self.keep_alive = keep_alive

    def init_ollama(self):
        """for the docker if needed. maybe do not need this"""
        pass

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
        response = ollama.generate(model=self.model_name, prompt=query)
        self._manage_logs(response)
        return response['response']

    def infer(self, query):
        # overwrite
        pass

    def __lshift__(self, query):
        return self.infer(query)


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

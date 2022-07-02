import json
import logging
from abc import ABC, abstractmethod
from typing import List

import requests


class ResponseGeneratorHandler:
    def __init__(self, rg_models: dict):
        self.rg_models = dict()
        self.logger = logging.getLogger("MacawLogger")

        for model_name, model in rg_models.items():
            if isinstance(model, ResponseGenerator):
                self.rg_models[model_name] = model
            elif isinstance(model, str) and model.startswith("http://"):
                self.rg_models[model_name] = ResponseGeneratorDocker(model_name, model)
            else:
                self.logger.warning(f"Response generator {model_name}:{model} is not supported.")

    def models_selector(self, conv_list) -> List[str]:
        selected_models = []
        for model_name in self.rg_models:
            if model_name == "qa":
                # decide if qa RG should be run or not here.
                selected_models.append(model_name)
            elif model_name == "punctuation":
                selected_models.append(model_name)
            else:
                self.logger.warning(f"Model selector not written for {model_name}. Ignoring the model.")
        return selected_models

    def run_models(self, model_names: List[str], conv_list) -> dict:
        models_response = dict()
        for model_name in model_names:
            models_response[model_name] = self.rg_models[model_name].run(conv_list)
        return models_response


class ResponseGenerator(ABC):
    """
    An abstract class for response generator (RG). It can be implemented as a local RG using a local class or as a
    remote RG using a docker container to generate the response.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, conv_list) -> dict:
        pass


class ResponseGeneratorPunctuation(ResponseGenerator):
    def __init__(self, name):
        super().__init__(name)

    def run(self, conv_list) -> dict:
        return {
            "response": f"this response is produced by a local RG: {self.name}."
        }


class ResponseGeneratorDocker(ResponseGenerator):
    """
    A class that encapsulates an ML model running in a local docker container.
    """

    def __init__(self, name: str, endpoint: str):
        super().__init__(name)
        self.endpoint = endpoint

    def run(self, conv_list) -> dict:
        # extract request from the conversation.
        request = {
            "text": "input message for RG docker model."
        }

        try:
            response = requests.post(url=self.endpoint, data=json.dumps(request))
            return response.json()
        except Exception as e:
            return {
                "response": f"Error in post request call for {self.name}: {e}",
                "error": True
            }

import json
from typing import List

import requests

from core.interaction_handler import Message


class RemoteModel:
    def __init__(self, model_name: str, endpoint: str):
        self.model_name = model_name
        self.endpoint = endpoint

    def run(self, request: dict) -> dict:
        try:
            response = requests.post(url=self.endpoint, data=json.dumps(request))
            return response.json()
        except Exception as e:
            return {
                "response": f"Error in post request call for {self.model_name}: {e}",
                "error": True
            }


class NlpPipeline:
    def __init__(self, modules: dict):
        self.modules = dict()
        for model_name, endpoint in modules.items():
            self.modules[model_name] = RemoteModel(model_name, endpoint)

    def run(self, conv_list: List[Message]):
        """
        Runs all the models and saves their results in the latest conversation (conv_list[0]) message.
        """
        nlp_pipeline_result = {}
        for model_name, model in self.modules.items():
            # TODO: pass in required input to every model.
            model_output = model.run({
                "text": "input text for model"
            })
            print(f"{model_name} model output: {model_output}")
            nlp_pipeline_result[model_name] = model_output
        conv_list[0].nlp_pipeline_result = nlp_pipeline_result

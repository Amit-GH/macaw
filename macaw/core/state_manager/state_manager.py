"""
The state manager.

Authors: George Wei (gzwei@umass.edu)
"""
import json

from typing import Optional

from injector import singleton

from .mongodb_manager import MongoDbManager


@singleton
class CurrentAttributes:
    pass


class State:
    def __init__(self, state_dict: dict[str, any]) -> None:
        self.__dict__.update(state_dict)

    @classmethod
    def from_json(cls, json_str: str) -> "State":
        json_dict = json.loads(json_str)
        return cls(**json_dict)


@singleton
class StateManager:
    DEFAULT_LIMIT = 50

    def __init__(self, collection_name: str) -> None:
        self.collection_name = collection_name
        self._current_attributes = CurrentAttributes()

    def to_json(self) -> str:
        pass

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, state_json: str) -> None:
        self._current_state = State.from_json(state_json)

    @property
    def current_attributes(self):
        return self._current_attributes

    @current_attributes.setter
    def current_attributes(self, current_attributes: CurrentAttributes) -> None:
        self._current_attributes = current_attributes

    @property
    def conversation_history(self):
        return self._conversation_history

    @conversation_history.setter
    def conversation_history(self, params: tuple[str, int]) -> None:
        conversation_id, limit = params
        self._conversation_history = self.fetch_conversation_history(
            conversation_id, limit
        )

    def fetch_conversation_history(
        self, conversation_id: str, limit: Optional[int] = None
    ):
        if limit is None:
            limit = StateManager.DEFAULT_LIMIT

        documents = MongoDbManager.query(
            collection_name=self.collection_name,
            filter=dict(conversation_id=conversation_id),
            limit=limit,
        )
        return documents

    def save_state(self, state: Optional[State] = None) -> bool:
        if state is not None:
            self._current_state = state

        result = MongoDbManager.put_document(
            collection_name=self.collection_name, document=state.__dict__
        )
        return result.acknowledged

"""
The message used to represent each interaction in Macaw.

Authors: Hamed Zamani (hazamani@microsoft.com), George Wei (gzwei@umass.edu)
"""
from datetime import datetime
from typing import Optional


class Message:
    def __init__(
        self,
        user_interface: str,
        user_id: str | int,
        text: str,
        timestamp: datetime,
        user_info: Optional[dict[str, any]] = None,
        msg_info: Optional[dict[str, any]] = None,
        actions: Optional[dict[str, any]] = None,
        dialog_state_tracking: Optional[dict[str, any]] = None,
    ):
        """
        An object for input and output Message.

        Args:
            user_interface(str): The interface name used for this message (e.g., 'telegram')
            user_id(str | int): The user ID.
            text(str): The message text.
            timestamp(datetime.datetime): The timestamp of message.
            user_info(dict): (Optional) The dict containing some more information about the user.
            msg_info(dict): (Optional) The dict containing some more information about the message.
            actions(dict): (Optional) The results from the various actions given the conversation history.
            dialog_state_tracking(dict): (Optional) The dialog state tracking dict.
        """
        self.user_interface = user_interface
        self.user_id = user_id
        self.text = text
        self.timestamp = timestamp
        self.user_info = user_info
        self.msg_info = msg_info
        self.actions = actions
        self.dialog_state_tracking = dialog_state_tracking

    @classmethod
    def from_dict(cls, msg_dict):
        """
        Get a Message object from dict.
        Args:
            msg_dict(dict): A dict containing all the information required to construct a Message object.

        Returns:
            A Message object.
        """
        return cls(**msg_dict)

"""
The message used to represent each interaction in Macaw.

Authors: Hamed Zamani (hazamani@microsoft.com), George Wei (gzwei@umass.edu)
"""


class Message:
    def __init__(self, user_interface, user_id, user_info, msg_info, text, timestamp):
        """
        An object for input and output Message.

        Args:
            user_interface(str): The interface name used for this message (e.g., 'telegram')
            user_id(str or int): The user ID.
            user_info(dict): The dict containing some more information about the user.
            msg_info(dict): The dict containing some more information about the message.
            text(str): The message text.
            timestamp(int): The timestamp of message.
        """
        self.user_id = user_id
        self.user_info = user_info
        self.msg_info = msg_info
        self.text = text
        self.timestamp = timestamp
        self.user_interface = user_interface

    @classmethod
    def from_dict(cls, msg_dict):
        """
        Get a Message object from dict.
        Args:
            msg_dict(dict): A dict containing all the information required to construct a Message object.

        Returns:
            A Message object.
        """
        user_interface = msg_dict.get("user_interface", None)
        user_id = msg_dict.get("user_id", None)
        user_info = msg_dict.get("user_info", None)
        msg_info = msg_dict.get("msg_info", None)
        text = msg_dict.get("text", None)
        timestamp = msg_dict.get("timestamp", None)
        return cls(user_interface, user_id, user_info, msg_info, text, timestamp)

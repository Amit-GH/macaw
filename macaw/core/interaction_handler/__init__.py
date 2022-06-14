"""
The interaction handler init

Authors: Hamed Zamani (hazamani@microsoft.com), George Wei (gzwei@umass.edu)
"""
from injector import singleton

from .msg import Message
from .user_requests_db import InteractionDB


@singleton
class CurrentAttributes:
    pass

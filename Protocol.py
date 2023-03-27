from enum import Enum


class EProtocol(Enum):
    INFO = 0
    TOKEN = 1
    COMMAND = 2
    CHAT = 3

    def __int__(self):
        return self.value

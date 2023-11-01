from enum import Enum

class TransmitOption(Enum):
    """All the available transmit options."""
    NONE = 'None'
    USER_INPUT = 'User Input'
    SFTP = 'SFTP'
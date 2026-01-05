from enum import Enum

class SQLErrorType(str, Enum):
    RETRYABLE = "retryable"
    TERMINAL = "terminal"

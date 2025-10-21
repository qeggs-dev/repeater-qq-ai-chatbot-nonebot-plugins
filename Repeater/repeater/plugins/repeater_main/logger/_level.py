from enum import StrEnum

class Level(StrEnum):
    TRACE = "trace"
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    EXCEPTION = "exception"
    SUCCESS = "success"
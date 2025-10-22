from enum import StrEnum

class Level(StrEnum):
    TRACE = "TRACE" # 5
    DEBUG = "DEBUG" # 10
    INFO = "INFO" # 20
    SUCCESS = "SUCCESS" # 25
    WARNING = "WARNING" # 30
    ERROR = "ERROR" # 40
    CRITICAL = "CRITICAL" # 50
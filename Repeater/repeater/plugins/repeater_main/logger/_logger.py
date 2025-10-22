from nonebot import logger
from nonebot import get_plugin_config
from pydantic import BaseModel, Field
from typing import Optional
from ._level import Level

class LoggerConfig(BaseModel):
    repeater_logger_level: Optional[Level] = Field(Level.INFO)
    repeater_logger_format: Optional[str] = Field("{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {extra[module]} - {message}")
    repeater_logger_path: Optional[str] = Field("logs/repeater-log-{time:YYYY-MM-DD-HH-mm-ss}.log")
    repeater_logger_enable_queue: Optional[bool] = Field(True)
    repeater_logger_delay: Optional[bool] = Field(True)
    repeater_logger_rotation: Optional[str] = Field("1 week")
    repeater_logger_retention: Optional[str] = Field("1 month")
    repeater_logger_compression: Optional[str] = Field("zip")

logger_config = get_plugin_config(LoggerConfig)

base_logger = logger

# file
base_logger.add(
    logger_config.repeater_logger_path,
    level = logger_config.repeater_logger_level.value,
    format = logger_config.repeater_logger_format,
    enqueue = logger_config.repeater_logger_enable_queue,
    delay = logger_config.repeater_logger_delay,
    rotation = logger_config.repeater_logger_rotation,
    retention = logger_config.repeater_logger_retention,
    compression = logger_config.repeater_logger_compression,
)

base_logger.configure(
    extra={
        "module": "[Unknown Module]"
    }
)
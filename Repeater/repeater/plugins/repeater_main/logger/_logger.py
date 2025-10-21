from loguru import logger as golbal_logger
from ..configs import Loader, Mode
from pydantic import BaseModel, Field
from ._console_output_stream import get_console_output_stream, ConsoleOutputStream
from ._level import Level

class LoggerConfig(BaseModel):
    name: str = Field("repeater")
    level: Level = Field(Level.INFO)
    stream: ConsoleOutputStream = Field(ConsoleOutputStream.STDOUT)
    format: str = Field("{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {extra[module]} - {message}")
    console_format: str = Field("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{extra[module]}</cyan> - <level>{message}</level>")
    path: str = Field("logs/repeater.log")
    enable_queue: bool = Field(True)
    delay: bool = Field(True)
    rotation: str = Field("1 week")
    retention: str = Field("1 month")
    compression: str = Field("zip")

loader = Loader(LoggerConfig, "configs/logger.json", Mode.JSON)
logger_config = loader.load(write_on_failure=True)

base_logger = golbal_logger.bind(
    name=logger_config.name
)

base_logger.remove()

base_logger.add(
    get_console_output_stream(logger_config.stream),
    level = logger_config.level,
    format = logger_config.console_format,
    enqueue = logger_config.enable_queue,
)

# file
base_logger.add(
    logger_config.path,
    level = logger_config.level,
    format = logger_config.format,
    enqueue = logger_config.enable_queue,
    delay = logger_config.delay,
    rotation = logger_config.rotation,
    retention = logger_config.retention,
    compression = logger_config.compression,
)

base_logger.configure(
    extra={
        "module": "[Unknown Module]"
    }
)
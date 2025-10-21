from ._sync_base_storage import BinaryStorage
from pathlib import Path
from typing import Any, Generator, Iterable, TypeVar
import orjson
from nonebot import logger

T = TypeVar("T")

class OrjsonStorage(BinaryStorage):
    """
    orjson存储

    存储json数据
    """
    def load_json(self, path: Path | str, default: T = None) -> Any | T:
        try:
            logger.info(f"Loading json from {path}")
            return orjson.loads(
                self.load(path)
            )
        except Exception as e:
            logger.error(f"Error loading json from {path}: {e}")
            if default is None:
                raise
            else:
                return default
    
    def save_json(self, path: Path | str, data: Any):
        try:
            logger.info(f"Saving json to {path}")
            self.save(
                path,
                orjson.dumps(data)
            )
        except Exception as e:
            logger.error(f"Error saving json to {path}: {e}")
            raise
    
    def load_jsonl(self, path: Path | str, default: T = None) -> Generator[Any | T, None, None]:
        try:
            logger.info(f"Loading jsonl from {path}")
            for line in self.load_line_stream(path):
                try:
                    yield orjson.loads(line)
                except Exception as e:
                    if default is None:
                        raise
                    else:
                        yield default
        except Exception as e:
            logger.error(f"Error loading jsonl from {path}: {e}")
            if default is None:
                raise
            else:
                yield default
            
    def save_jsonl(self, path: Path | str, data: Iterable[Any], append: bool = False):
        try:
            logger.info(f"Saving jsonl to {path}")
            def json_dumps(obj: Iterable[Any]):
                for line in obj:
                    yield orjson.dumps(line)
                    yield b"\n"
            
            self.save_stream(
                path,
                json_dumps(data),
                append = append
            )
        except Exception as e:
            logger.error(f"Error saving jsonl to {path}: {e}")
            raise
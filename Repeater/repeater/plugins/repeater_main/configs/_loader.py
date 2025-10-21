from ..storage import json_storage, yaml_storage
from ._mode import Mode
from pydantic import BaseModel
from typing import Type, Any, TypeVar, Generic
from pathlib import Path
from nonebot import logger

T_MODEL = TypeVar("T_MODEL", bound=BaseModel)

class Loader(Generic[T_MODEL]):
    def __init__(self, model: Type[T_MODEL], path: str | Path, mode: Mode = Mode.JSON):
        self._model = model
        self._path = path
        self._mode = mode
    
    def load(self, write_on_failure: bool = False) -> T_MODEL:
        try:
            if self._mode == Mode.JSON:
                return self._model(**self._decode_json(self._path))
            elif self._mode == Mode.YAML:
                return self._model(**self._decode_yaml(self._path))
            else:
                raise ValueError("Unknown mode")
        except Exception as e:
            if write_on_failure:
                logger.warning(f"Failed to load config from \"{self._path}\", writing default config")
                model = self._model()
                self.save(model)
                return model
            else:
                logger.error(f"Failed to load config from \"{self._path}\"")
                raise e

    def save(self, data: T_MODEL):
        if self._mode == Mode.JSON:
            return self._encode_json(self._path, data.model_dump())
        elif self._mode == Mode.YAML:
            return self._encode_yaml(self._path, data.model_dump())
        else:
            raise ValueError("Unknown mode")

    @staticmethod
    def _decode_json(file_path: str | Path):
        return json_storage.load_json(file_path)

    @staticmethod
    def _decode_yaml(file_path: str | Path):
        return yaml_storage.load_yaml(file_path)
    
    @staticmethod
    def _encode_json(file_path: str | Path, data: Any):
        return json_storage.save_json(file_path, data)

    @staticmethod
    def _encode_yaml(file_path: str | Path, data: Any):
        return yaml_storage.save_yaml(file_path, data)
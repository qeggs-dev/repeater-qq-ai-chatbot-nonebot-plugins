from ..storage import async_json_storage, async_yaml_storage
from ._mode import Mode
from pydantic import BaseModel
from typing import Type, Any, TypeVar, Generic
from pathlib import Path
from ..logger import logger as base_logger

logger = base_logger.bind(module = "Configs.Core")

T_MODEL = TypeVar("T_MODEL", bound=BaseModel)

class AsyncLoader(Generic[T_MODEL]):
    def __init__(self, model: Type[T_MODEL], path: str | Path, mode: Mode = Mode.JSON):
        self._model = model
        self._path = path
        self._mode = mode
    
    async def load(self, write_on_failure: bool = False) -> T_MODEL:
        try:
            if self._mode == Mode.JSON:
                return self._model(**(await self._decode_json(self._path)))
            elif self._mode == Mode.YAML:
                return self._model(**(await self._decode_yaml(self._path)))
            else:
                raise ValueError("Unknown mode")
        except Exception as e:
            if write_on_failure:
                logger.warning(f"Failed to load config from \"{self._path}\", writing default config")
                model = self._model()
                await self.save(model)
                return model
            else:
                logger.error(f"Failed to load config from \"{self._path}\"")
                raise e

    async def save(self, data: T_MODEL):
        if self._mode == Mode.JSON:
            return await self._encode_json(self._path, data.model_dump())
        elif self._mode == Mode.YAML:
            return await self._encode_yaml(self._path, data.model_dump())
        else:
            raise ValueError("Unknown mode")

    @staticmethod
    async def _decode_json(file_path: str | Path):
        return await async_json_storage.load_json(file_path)

    @staticmethod
    async def _decode_yaml(file_path: str | Path):
        return await async_yaml_storage.load_yaml(file_path)
    
    @staticmethod
    async def _encode_json(file_path: str | Path, data: Any):
        return await async_json_storage.save_json(file_path, data)


    async def _encode_yaml(file_path: str | Path, data: Any):
        return await async_yaml_storage.save_yaml(file_path, data)
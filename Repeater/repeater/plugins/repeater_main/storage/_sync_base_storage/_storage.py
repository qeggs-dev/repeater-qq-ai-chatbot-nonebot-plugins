import aiofiles
from pathlib import Path
from typing import AsyncGenerator, AsyncIterable, Iterable, Generic, TypeVar
from abc import ABC, abstractmethod

T_STORAGE_DATA = TypeVar("T_STORAGE_DATA")

class Storage(ABC, Generic[T_STORAGE_DATA]):
    """
    Storage

    文件存储管理器
    """
    def __init__(self, storage_base_path: str | Path):
        """
        :param storage_base_path: 存储路径
        """
        self.storage_base_path = Path(storage_base_path)
    
    def _path(self, path: Path | str):
        path = Path(path)
        if path.is_absolute():
            return path
        return self.storage_base_path / path
    
    @abstractmethod
    def load(self, path: Path | str) -> T_STORAGE_DATA:
        pass
    
    @abstractmethod
    def save(self, path: Path | str, data: T_STORAGE_DATA) -> None:
        pass

    @abstractmethod
    def load_line_stream(self, path: Path | str) -> AsyncGenerator[T_STORAGE_DATA, None]:
        pass

    @abstractmethod
    def load_stream(self, path: Path | str) -> AsyncGenerator[T_STORAGE_DATA, None]:
        pass

    @abstractmethod
    def save_stream(self, path: Path | str, data: Iterable[T_STORAGE_DATA]) -> None:
        pass
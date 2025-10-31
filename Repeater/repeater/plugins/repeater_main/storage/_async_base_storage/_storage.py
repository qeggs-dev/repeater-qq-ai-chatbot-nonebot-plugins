import aiofiles
from pathlib import Path
from typing import AsyncGenerator, AsyncIterable, Iterable, Generic, TypeVar
from abc import ABC, abstractmethod
import shutil

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
    async def load(self, path: Path | str) -> T_STORAGE_DATA:
        pass
    
    @abstractmethod
    async def save(self, path: Path | str, data: T_STORAGE_DATA) -> None:
        pass

    @abstractmethod
    async def load_line_stream(self, path: Path | str) -> AsyncGenerator[T_STORAGE_DATA, None]:
        pass

    @abstractmethod
    async def load_stream(self, path: Path | str) -> AsyncGenerator[T_STORAGE_DATA, None]:
        pass

    @abstractmethod
    async def save_stream(self, path: Path | str, data: Iterable[T_STORAGE_DATA]) -> None:
        pass

    @abstractmethod
    async def save_astream(self, path: Path | str, data: AsyncIterable[T_STORAGE_DATA]) -> None:
        pass

    def move(self, src: Path | str, dst: Path | str) -> None:
        src = self._path(src)
        dst = self._path(dst)
        src.rename(dst)
    
    def remove(self, path: Path | str) -> None:
        path = self._path(path)
        if path.exists():
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
    
    def copy(self, src: Path | str, dst: Path | str) -> None:
        src = self._path(src)
        dst = self._path(dst)
        if src.is_file():
            shutil.copy(src, dst)
        elif src.is_dir():
            shutil.copytree(src, dst)
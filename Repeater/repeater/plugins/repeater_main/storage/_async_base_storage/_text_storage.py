import aiofiles
from pathlib import Path
from typing import AsyncGenerator, AsyncIterable, Iterable
from ._storage import Storage
from nonebot import logger

class TextStorage(Storage[str]):
    async def load(self, path: Path | str, encoding: str = "utf-8") -> str:
        try:
            path = self._path(path)
            logger.info(f"Load {path}")
            async with aiofiles.open(path, "r", encoding = encoding) as f:
                return await f.read()
        except Exception as e:
            logger.exception(f"Load {path} failed: {e}")
            raise
    
    async def load_line_stream(self, path: Path | str, encoding: str = "utf-8") -> AsyncGenerator[str, None]:
        try:
            path = self._path(path)
            logger.info(f"Use line-by-line chunk streaming to load the file \"{path}\"")
            async with aiofiles.open(path, "r", encoding = encoding) as f:
                async for line in f:
                    yield line
        except Exception as e:
            logger.exception(f"Load {path} failed: {e}")
            raise
    
    async def load_stream(self, path: Path | str, encoding: str = "utf-8", chunk_size: int = 1024) -> AsyncGenerator[str, None]:
        try:
            path = self._path(path)
            logger.info(f"Stream load the file \"{path}\" in {chunk_size}-byte chunks")
            async with aiofiles.open(self._path(path), "r", encoding=encoding) as f:
                while True:
                    chunk = await f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            logger.exception(f"Load {path} failed: {e}")
            raise

    async def save(self, path: Path | str, data: str, encoding: str = "utf-8", append: bool = False) -> None:
        try:
            path = self._path(path)
            logger.info(f"Saving text to {path}")
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            async with aiofiles.open(path, "w" if not append else "a", encoding=encoding) as f:
                await f.write(data)
        except Exception as e:
            logger.exception(f"Save {path} failed: {e}")
            raise
    
    async def save_stream(self, path: Path | str, data: Iterable[str], encoding: str = "utf-8", append: bool = False) -> None:
        try:
            path = self._path(path)
            logger.info(f"Saving text stream to {path}")
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            async with aiofiles.open(self._path(path), "w" if not append else "a", encoding=encoding) as f:
                for line in data:
                    await f.write(line)
        except Exception as e:
            logger.exception(f"Save {path} failed: {e}")
            raise
    
    async def save_astream(self, path: Path | str, data: AsyncIterable[str], encoding: str = "utf-8", append: bool = False) -> None:
        try:
            path = self._path(path)
            logger.info(f"Saving text async stream to {path}")
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            async with aiofiles.open(path, "w" if not append else "a", encoding=encoding) as f:
                async for line in data:
                    await f.write(line)
        except Exception as e:
            logger.exception(f"Save {path} failed: {e}")
            raise
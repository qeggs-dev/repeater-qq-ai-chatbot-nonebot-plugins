import aiofiles
from pathlib import Path
from typing import AsyncGenerator, AsyncIterable, Iterable
from ._storage import Storage

class TextStorage(Storage[str]):
    async def load(self, path: Path | str, encoding: str = "utf-8") -> str:
        async with aiofiles.open(self._path(path), "r", encoding=encoding) as f:
            return await f.read()
    
    async def load_line_stream(self, path: Path | str, encoding: str = "utf-8") -> AsyncGenerator[str, None]:
        async with aiofiles.open(self._path(path), "r", encoding=encoding) as f:
            async for line in f:
                yield line
    
    async def load_stream(self, path: Path | str, encoding: str = "utf-8", chunk_size: int = 1024) -> AsyncGenerator[str, None]:
        async with aiofiles.open(self._path(path), "r", encoding=encoding) as f:
            while True:
                chunk = await f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    async def save(self, path: Path | str, data: str, encoding: str = "utf-8", append: bool = False) -> None:
        async with aiofiles.open(self._path(path), "w" if not append else "a", encoding=encoding) as f:
            await f.write(data)
    
    async def save_stream(self, path: Path | str, data: Iterable[str], encoding: str = "utf-8", append: bool = False) -> None:
        async with aiofiles.open(self._path(path), "w" if not append else "a", encoding=encoding) as f:
            for line in data:
                await f.write(line)
    
    async def save_astream(self, path: Path | str, data: AsyncIterable[str], encoding: str = "utf-8", append: bool = False) -> None:
        async with aiofiles.open(self._path(path), "w" if not append else "a", encoding=encoding) as f:
            async for line in data:
                await f.write(line)
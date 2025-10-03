import aiofiles
from pathlib import Path
from typing import AsyncGenerator, AsyncIterable, Iterable
from ._storage import Storage

class BinaryStorage(Storage[bytes]):
    async def load(self, path: Path | str) -> bytes:
        async with aiofiles.open(self._path(path), "rb") as f:
            return await f.read()
    
    async def load_line_stream(self, path: Path | str) -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(self._path(path), "rb") as f:
            async for line in f:
                yield line
    
    async def load_stream(self, path: Path | str, chunk_size: int = 1024) -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(self._path(path), "rb") as f:
            while True:
                chunk = await f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    async def save(self, path: Path | str, data: bytes, append: bool = False) -> None:
        async with aiofiles.open(self._path(path), "wb" if not append else "ab") as f:
            await f.write(data)
    
    async def save_stream(self, path: Path | str, stream: Iterable[bytes], append: bool = False) -> None:
        async with aiofiles.open(self._path(path), "wb" if not append else "ab") as f:
            for line in stream:
                await f.write(line)
    
    async def save_astream(self, path: Path | str, stream: AsyncIterable[bytes], append: bool = False) -> None:
        async with aiofiles.open(self._path(path), "wb" if not append else "ab") as f:
            async for line in stream:
                await f.write(line)
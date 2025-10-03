from ._base_storage import Storage
from pathlib import Path
from typing import Any, AsyncGenerator, AsyncIterable, Iterable, TypeVar
import orjson

T = TypeVar("T")

class OrjsonStorage(Storage):
    """
    orjson存储

    存储json数据
    """
    async def load_json(self, path: Path | str, default: T = None) -> Any | T:
        try:
            return orjson.loads(
                self.load_binary(path)
            )
        except Exception as e:
            if default is None:
                raise
            else:
                return default
    
    async def save_json(self, path: Path | str, data: Any):
        self.save_binary(
            path,
            orjson.dumps(data)
        )
    
    async def load_jsonl(self, path: Path | str, default: T = None) -> AsyncGenerator[Any | T, None]:
        async for line in self.load_line_stream_binary(path):
            try:
                yield orjson.loads(line)
            except Exception as e:
                if default is None:
                    raise
                else:
                    yield default
    
    async def save_jsonl(self, path: Path | str, data: Iterable[Any], append: bool = False):
        def json_dumps(obj: Iterable[Any]):
            for line in obj:
                yield orjson.dumps(line)
                yield b"\n"
        
        await self.save_stream_binary(
            path,
            json_dumps(data),
            append = append
        )
    
    async def save_jsonl_a(self, path: Path | str, data: AsyncIterable[Any], append: bool = False):
        async def json_dumps(obj: AsyncIterable[Any]):
            async for line in obj:
                yield orjson.dumps(line)
                yield b"\n"
        
        await self.save_astream_binary(
            path,
            json_dumps(data),
            append = append
        )
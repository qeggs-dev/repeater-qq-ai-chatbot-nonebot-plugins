from pathlib import Path
from typing import Generator, Iterable
from ._storage import Storage
from nonebot import logger

class BinaryStorage(Storage[bytes]):
    def load(self, path: Path | str) -> bytes:
        try:
            path = self._path(path)
            logger.info(f"Loading binary from {path}")
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            with open(path, "rb") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading binary from {path}: {e}")
            raise
    
    def load_line_stream(self, path: Path | str) -> Generator[bytes, None]:
        try:
            path = self._path(path)
            logger.info(f"Use line-by-line chunk streaming to load the file \"{path}\"")
            with open(path, "rb") as f:
                for line in f:
                    yield line
        except Exception as e:
            logger.error(f"Error loading binary line stream from {path}: {e}")
            raise
    
    def load_stream(self, path: Path | str, chunk_size: int = 1024) -> Generator[bytes, None]:
        try:
            path = self._path(path)
            logger.info(f"Stream load the file \"{path}\" in {chunk_size}-byte chunks")
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            logger.error(f"Error loading binary stream from {path}: {e}")
            raise
    
    def save(self, path: Path | str, data: bytes, append: bool = False) -> None:
        try:
            path = self._path(path)
            logger.info(f"Saving binary to {path}")
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            with open(path, "wb" if not append else "ab") as f:
                f.write(data)
        except Exception as e:
            logger.error(f"Error saving binary to {path}: {e}")
            raise
    
    def save_stream(self, path: Path | str, stream: Iterable[bytes], append: bool = False) -> None:
        try:
            path = self._path(path)
            logger.info(f"Saving binary stream to {path}")
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            with open(self._path(path), "wb" if not append else "ab") as f:
                for line in stream:
                    f.write(line)
        except Exception as e:
            logger.error(f"Error saving binary stream to {path}: {e}")
            raise
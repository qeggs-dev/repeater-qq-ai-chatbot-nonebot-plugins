from ._base_storage import TextStorage
from pathlib import Path
from typing import Any
import yaml

class YamlStorage(TextStorage):
    """
    YAML Storage

    存储文件格式为 YAML
    """
    async def load_json(self, path: Path | str, encoding: str = "utf-8") -> Any:
        return self.load(
            path,
            encoding = encoding
        )
    
    async def save_json(self, path: Path | str, data: Any, encoding: str = "utf-8"):
        self.save(
            path,
            yaml.safe_dump(data),
            encoding = encoding
        )

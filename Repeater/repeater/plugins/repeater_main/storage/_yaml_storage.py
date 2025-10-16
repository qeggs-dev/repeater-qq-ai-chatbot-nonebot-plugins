from ._sync_base_storage import TextStorage
from pathlib import Path
from typing import Any
import yaml
from nonebot import logger

class YamlStorage(TextStorage):
    """
    YAML Storage

    存储文件格式为 YAML
    """
    def load_yaml(self, path: Path | str, encoding: str = "utf-8") -> Any:
        try:
            logger.info(f"Loading yaml from {path}")
            return self.load(
                path,
                encoding = encoding
            )
        except Exception as e:
            logger.error(f"load yaml error: {e}")
            return None
    
    def save_yaml(self, path: Path | str, data: Any, encoding: str = "utf-8"):
        try:
            logger.info(f"Saving yaml to {path}")
            self.save(
                path,
                yaml.safe_dump(data),
                encoding = encoding
            )
        except Exception as e:
            logger.error(f"save yaml error: {e}")

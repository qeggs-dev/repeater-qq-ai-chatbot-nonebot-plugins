from nonebot import get_plugin_config
from pydantic import BaseModel, Field
from pathlib import Path

class StoragePath(BaseModel):
    storage_base_path: str = Field(default_factory=lambda: str((Path.cwd() / "storage").absolute()))

storage_path = get_plugin_config(StoragePath)
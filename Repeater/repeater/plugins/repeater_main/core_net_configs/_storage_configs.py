from pydantic import BaseModel
from ..storage import json_storage
from nonebot import logger

class StorageConfigs(BaseModel):
    max_text_length: int = 400
    max_single_line_length: int = 64
    max_text_lines: int = 10

try:
    storage_config = StorageConfigs(**json_storage.load_json("configs/main_api.json"))
except Exception:
    logger.warning("main_api.json not found, using default configs")
    storage_config = StorageConfigs()
    try:
        json_storage.save_json("configs/main_api.json", storage_config.model_dump())
    except Exception as e:
        logger.error(f"Error saving main_api.json({e})")
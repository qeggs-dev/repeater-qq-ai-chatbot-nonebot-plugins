import json
import httpx
from nonebot import logger
from typing import (
    Optional,
    Union
)

from ..core_config import *

class ChatCore:
    def __init__(self, session_id: str):
        self.url = f"{CHAT_API}:{CHAT_PORT}"
        self.session_id = session_id
    # region get_utl
    async def get_user_data_file_url(self):
        return f'{self.url}/{DOWNLOAD_USER_DATA_FILE_ROUTE}/{self.session_id}.zip'
    # endregion